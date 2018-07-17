import json
from seeds import buildings_seeds
from seeds import building_events_seeds
from seeds import permit_clusters_seeds
from seeds import census_tracts_seeds
from seeds import neighborhoods_seeds
from seeds import community_districts_seeds
from seeds import boroughs_seeds
from helpers import boundary_helpers
from helpers import csv_helpers
import config

from shapely.geometry import Point, mapping
import datetime

permits_table = 'permits'
permit_col1 = 'borough_id'
permit_col2 = 'community_district_id'
permit_col3 = 'neighborhood_id'
permit_col4 = 'census_tract_id'
permit_col5 = 'permit_cluster_id'
permit_col6 = 'date'
permit_col7 = 'geometry'
permit_col8 = 'source'
permit_col9 = 'permit_type'
permit_col10 = 'owner_business_name'
permit_col11 = 'owner_first_name'
permit_col12 = 'owner_last_name'
permit_col13 = 'job_start_date'
permit_col14 = 'house_number'
permit_col15 = 'street_name'

def find_foreign_keys(c, permit, census_tracts):

  if permit["geometry"]: 
    ct = boundary_helpers.get_record_from_coordinates(permit["geometry"], census_tracts, 7)
    ct = c.fetchone()
  else:
    return None

  if ct:
    return {
      "borough_id": ct[1],
      "community_district_id": ct[2],
      "neighborhood_id": ct[3],
      "census_tract_id": ct[0]
    }
  else:
    return None

def get_geometry(lon, lat):
  if lon and lat:
    return mapping(Point(float(lon), float(lat)))
  else:
    return None

def get_building_match(c, block, lot):
  c.execute('SELECT * FROM buildings WHERE block={v_block} AND lot={v_lot}'.format(v_block=str(block), v_lot=str(lot)))
  return c.fetchone()

def get_borough_match(c, name):
  c.execute('SELECT * FROM boroughs WHERE name=\'{name}\' COLLATE NOCASE'.format(name=str(name)))
  return c.fetchone()

def get_permit_cluster_match(c, geo):
  c.execute('SELECT * FROM permit_clusters WHERE geometry=\'{geo}\''.format(geo=geo))
  return c.fetchone()

def convert_date_format(date):
  return datetime.datetime.strptime(date[:10], "%Y-%m-%d").strftime("%Y%m%d")

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER REFERENCES {ref_table1}(id), {col2} INTEGER REFERENCES {ref_table2}(id), {col3} INTEGER REFERENCES {ref_table3}(id), {col4} INTEGER REFERENCES {ref_table4}(id), {col5} INTEGER REFERENCES {ref_table5}(id), {col6} TEXT, {col7} TEXT, {col8} TEXT, {col9} TEXT, {col10} TEXT, {col11} TEXT, {col12} TEXT, {col13} TEXT, {col14} TEXT, {col15} TEXT)'\
    .format(tn=permits_table, col1=permit_col1, col2=permit_col2, col3=permit_col3, col4=permit_col4, col5=permit_col5, col6=permit_col6, col7=permit_col7, col8=permit_col8, col9=permit_col9, col10=permit_col10, col11=permit_col11, col12=permit_col12, col13=permit_col13, col14=permit_col14, col15=permit_col15, ref_table1=boroughs_seeds.boroughs_table, ref_table2=community_districts_seeds.community_districts_table, ref_table3=neighborhoods_seeds.neighborhoods_table, ref_table4=census_tracts_seeds.census_tracts_table, ref_table5=permit_clusters_seeds.permit_clusters_table))

  c.execute('CREATE INDEX idx_permit_census_tract_id ON {tn}({col1})'.format(tn=permits_table, col1=permit_col1))
  c.execute('CREATE INDEX idx_permit_neighborhood_id ON {tn}({col2})'.format(tn=permits_table, col2=permit_col1))
  c.execute('CREATE INDEX idx_permit_community_district_id ON {tn}({col3})'.format(tn=permits_table, col3=permit_col1))
  c.execute('CREATE INDEX idx_permit_borough_id ON {tn}({col4})'.format(tn=permits_table, col4=permit_col1))
  c.execute('CREATE INDEX idx_permit_permit_cluster_id ON {tn}({col5})'.format(tn=permits_table, col5=permit_col1))
  c.execute('CREATE INDEX idx_permit_type ON {tn}({col9})'.format(tn=permits_table, col9=permit_col5))
  c.execute('CREATE INDEX idx_permit_owner_business_name ON {tn}({col10})'.format(tn=permits_table, col10=permit_col6))
  c.execute('CREATE INDEX idx_permit_street_name_and_house_number ON {tn}({col15}, {col14})'.format(tn=permits_table, col14=permit_col10, col15=permit_col11))


def seed_permits_from_json(c, permit_json):
  print("Seeding permits...")

  c.execute('SELECT * FROM census_tracts')
  census_tracts = c.fetchall()
  for index, permit in enumerate(permit_json):
    print("permit: " + str(index) + "/" + str(len(permit_json)))
    
    # building_match = get_building_match(c, permit["block"], permit["lot"])

    # if not building_match:
    #   print("  - no building match found")

    # building_id = None # building_match[0] if building_match else None
    
    fkeys = find_foreign_keys(c, permit, census_tracts)

    if not fkeys:
      print("  X no boundary match found")
      continue

    date = convert_date_format(permit["issuance_date"])

    if "gis_longitude" not in permit and "gis_latitude" not in permit:
      print("  * no geo information")
      continue

    geometry = json.dumps(get_geometry(permit["gis_longitude"], permit["gis_latitude"]), separators=(',', ':'))
    source = permit["source"]
    permit_type = permit["permit_type"]
    owner_business_name = permit["owner_s_business_name"] if "owner_s_business_name" in permit else ""
    owner_first_name = permit["owner_s_first_name"] if "owner_s_first_name" in permit else ""
    owner_last_name = permit["owner_s_last_name"] if "owner_s_last_name" in permit else ""
    house_number = permit["house__"]
    street_name = permit["street_name"]
    job_start_date = convert_date_format(permit["job_start_date"]) if "job_start_date" in permit else ""

    permit_cluster = get_permit_cluster_match(c, geometry)

    if permit_cluster:
      permit_cluster_id = permit_cluster[0]
      print (" ^^ joining to permit cluster")
    else:
      permit_clusters_seeds.seed_cluster_from_permit(c, permit, geometry, fkeys[0])
      permit_cluster_id = c.lastrowid
      print(" ++ seeding a cluster", permit_cluster_id)

    # create permit
    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}, {col9}, {col10}, {col11}, {col12}, {col13}, {col14} ,{col15}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'\
      .format(tn=permits_table, col1=permit_col1, col2=permit_col2, col3=permit_col3, col4=permit_col4, col5=permit_col5, col6=permit_col6, col7=permit_col7, col8=permit_col8, col9=permit_col9, col10=permit_col10, col11=permit_col11, col12=permit_col12, col13=permit_col13, col14=permit_col14, col15=permit_col15), (fkeys[0], fkeys[1], fkeys[2], fkeys[3], permit_cluster_id, str(date), str(geometry), str(source), str(permit_type), str(owner_business_name), str(owner_first_name), str(owner_last_name), str(job_start_date), str(house_number), str(street_name)))

    csv_helpers.write_csv(c, permit, config.PERMITS_CSV_URL, index == 0)

