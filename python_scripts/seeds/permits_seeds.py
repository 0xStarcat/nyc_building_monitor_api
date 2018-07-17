import json
from seeds import buildings_seeds
from seeds import building_events_seeds
from seeds import permit_clusters_seeds

from helpers import csv_helpers
import config

from shapely.geometry import Point, mapping
import datetime

permits_table = 'permits'
permit_col1 = 'building_id'
permit_col2 = 'date'
permit_col3 = 'geometry'
permit_col4 = 'source'
permit_col5 = 'permit_type'
permit_col6 = 'owner_business_name'
permit_col7 = 'owner_first_name'
permit_col8 = 'owner_last_name'
permit_col9 = 'job_start_date'
permit_col10 = 'house_number'
permit_col11 = 'street_name'
permit_col12 = 'permit_cluster_id'

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
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER REFERENCES {bldg_table}(id), {col2} TEXT, {col3} INT, {col4} TEXT, {col5} TEXT, {col6} TEXT, {col7} TEXT, {col8} TEXT, {col9} TEXT, {col10} TEXT, {col11} TEXT, {col12} INTEGER REFERENCES {permit_clusters_table})'\
    .format(tn=permits_table, col1=permit_col1, col2=permit_col2, col3=permit_col3, col4=permit_col4, col5=permit_col5, col6=permit_col6, col7=permit_col7, col8=permit_col8, col9=permit_col9, col10=permit_col10, col11=permit_col11, col12=permit_col12, bldg_table=buildings_seeds.buildings_table, permit_clusters_table=permit_clusters_seeds.permit_clusters_table))

  c.execute('CREATE INDEX idx_permit_building_id ON {tn}({col1})'.format(tn=permits_table, col1=permit_col1))
  c.execute('CREATE INDEX idx_permit_type ON {tn}({col5})'.format(tn=permits_table, col5=permit_col5))
  c.execute('CREATE INDEX idx_permit_owner_business_name ON {tn}({col6})'.format(tn=permits_table, col6=permit_col6))
  c.execute('CREATE INDEX idx_permit_street_name_and_house_number ON {tn}({col11}, {col10})'.format(tn=permits_table, col10=permit_col10, col11=permit_col11))


def seed_permits_from_json(c, permit_json):
  print("Seeding permits...")

  for index, permit in enumerate(permit_json):
    print("permit: " + str(index) + "/" + str(len(permit_json)))
    
    building_match = get_building_match(c, permit["block"], permit["lot"])

    if not building_match:
      print("  - no building match found")

    building_id = None # building_match[0] if building_match else None
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

    borough = get_borough_match(c, permit["borough"])
    if not borough:
      print("  X no borough found")
      continue

    borough_id = borough[0]

    permit_cluster = get_permit_cluster_match(c, geometry)

    if permit_cluster:
      permit_cluster_id = permit_cluster[0]
      print (" ^^ joining to permit cluster")
    else:
      permit_clusters_seeds.seed_cluster_from_permit(c, permit, geometry, borough_id)
      permit_cluster_id = c.lastrowid
      print(" ++ seeding a cluster", permit_cluster_id)

    # create permit
    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}, {col9}, {col10}, {col11}, {col12}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'\
      .format(tn=permits_table, col1=permit_col1, col2=permit_col2, col3=permit_col3, col4=permit_col4, col5=permit_col5, col6=permit_col6, col7=permit_col7, col8=permit_col8, col9=permit_col9, col10=permit_col10, col11=permit_col11, col12=permit_col12), (building_id, str(date), str(geometry), str(source), str(permit_type), str(owner_business_name), str(owner_first_name), str(owner_last_name), str(job_start_date), str(house_number), str(street_name), permit_cluster_id))
    
    # Create Building Event
    if building_id:
      insertion_id = c.lastrowid
      
      c.execute('SELECT * FROM {tn} WHERE {cn}={b_id}'\
        .format(tn=buildings_seeds.buildings_table, cn='id', b_id=building_id))

      building = c.fetchone()
      
      c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'\
        .format(tn=building_events_seeds.building_events_table, col1="borough_id", col2="community_district_id", col3="neighborhood_id", col4="census_tract_id", col5="building_id", col6="eventable", col7="eventable_id", col8="event_date"), (building[1], building[2], building[3], building[4], building[0], 'permit', insertion_id, date))

    csv_helpers.write_csv(c, permit, config.PERMITS_CSV_URL, index == 0)

