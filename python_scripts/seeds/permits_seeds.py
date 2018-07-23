import json
import context
import config

from shapely.geometry import Point, mapping
import datetime

table = 'permits'
col1 = 'borough_id'
col2 = 'neighborhood_id'
col3 = 'census_tract_id'
col4 = 'permit_cluster_id'
col5 = 'building_id'
col6 = 'geometry'
col7 = 'house_number'
col8 = 'street_name'
col9 = 'date'
col10 = 'source'
col11 = 'permit_type'
col12 = 'owner_business_name'
col13 = 'owner_first_name'
col14 = 'owner_last_name'
col15 = 'job_start_date'

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER REFERENCES {ref_table1}(id), {col2} INTEGER REFERENCES {ref_table2}(id), {col3} INTEGER REFERENCES {ref_table3}(id), {col4} INTEGER REFERENCES {ref_table4}(id), {col5} INTEGER REFERENCES {ref_table5}(id))'\
    .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, ref_table1=context.boroughs_seeds.table, ref_table2=context.neighborhoods_seeds.table, ref_table3=context.census_tracts_seeds.table, ref_table4=context.permit_clusters_seeds.table, ref_table5=context.buildings_seeds.table))

  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col6))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col7))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col8))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col9))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col10))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col11))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col12))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col13))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col14))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col15))

  c.execute('CREATE INDEX idx_permit_borough_id ON {tn}({col})'.format(tn=table, col=col1))
  c.execute('CREATE INDEX idx_permit_neighborhood_id ON {tn}({col})'.format(tn=table, col=col2))
  c.execute('CREATE INDEX idx_permit_census_tract_id ON {tn}({col})'.format(tn=table, col=col3))
  c.execute('CREATE INDEX idx_permit_permit_cluster_id ON {tn}({col})'.format(tn=table, col=col4))
  c.execute('CREATE INDEX idx_permit_building_id ON {tn}({col})'.format(tn=table, col=col5))
  c.execute('CREATE INDEX idx_permit_date ON {tn}({col})'.format(tn=table, col=col9))
  c.execute('CREATE INDEX idx_permit_type ON {tn}({col})'.format(tn=table, col=col11))
  c.execute('CREATE INDEX idx_permit_owner_business_name ON {tn}({col})'.format(tn=table, col=col12))
  c.execute('CREATE INDEX idx_permit_owner_first_and_last_name ON {tn}({col1}, {col2})'.format(tn=table, col1=col13, col2=col14))
  c.execute('CREATE INDEX idx_permit_house_and_street ON {tn}({col1}, {col2})'.format(tn=table, col1=col7, col2=col8))

def find_foreign_keys(c, permit):
  if permit["borough"]:
    c.execute('SELECT code FROM {tn} WHERE {cn1}=\'{borough_name}\' COLLATE NOCASE'.format(tn=context.boroughs_seeds.table, cn1='name', borough_name=permit['borough']))
    borough_code = c.fetchone()[2] 
  else:
    print("  X no borough")
    return None

  if permit["gis_census_tract"]: 
    c.execute('SELECT id, borough_id, neighborhood_id FROM {tn} WHERE {cn1}={boro_code} and {cn2}={ct_name}'.format(tn=context.census_tracts_seeds.table, cn1="boro_code", boro_code=borough_code, cn2="CTLabel", ct_name=permit["gis_census_tract"]))
    ct = c.fetchone()
  else:
    print("  X no CT")
    return None
 
  if ct:
    return {
      "borough_id": ct[1],
      "neighborhood_id": ct[2],
      "census_tract_id": ct[0]
    }
  else:
    return None

def get_geometry(lon, lat):
  if lon and lat:
    return Point(float(lon), float(lat))
  else:
    return None

def get_building_match(c, block, lot):
  c.execute('SELECT * FROM buildings WHERE block={v_block} AND lot={v_lot}'.format(v_block=str(block), v_lot=str(lot)))
  return c.fetchone()

def get_borough_match(c, name):
  c.execute('SELECT * FROM boroughs WHERE name=\'{name}\' COLLATE NOCASE'.format(name=str(name)))
  return c.fetchone()

def get_permit_cluster_match(c, geo):
  c.execute('SELECT id FROM permit_clusters WHERE geometry=\'{geo}\''.format(geo=geo))
  return c.fetchone()

def convert_date_format(date):
  return datetime.datetime.strptime(date[:10], "%Y-%m-%d").strftime("%Y%m%d")

def seed_permits_from_json(c, permit_json, write_to_csv=False):
  print("Seeding permits...")

  for index, permit in enumerate(permit_json):
    if index % 1000 == 0:
      print("permit: " + str(index) + "/" + str(len(permit_json)))
    


    if "gis_longitude" not in permit and "gis_latitude" not in permit:
      print("  * no geo information", "call: " + str(index) + "/" + str(len(permit_json)))
      continue

    geometry = get_geometry(permit["gis_longitude"], permit["gis_latitude"])
    geometry_json = str(json.dumps(mapping(geometry), separators=(',', ':')))
    fkeys = find_foreign_keys(c, permit)

    if not fkeys:
      print("  X no boundary match found", "call: " + str(index) + "/" + str(len(permit_json)))
      continue

    # building_match = get_building_match(c, permit["block"], permit["lot"])

    # if not building_match:
    #   print("  - no building match found")
    building_id = None # building_match[0] if building_match else None
    street_name = str(permit["street_name"])
    house_number = str(permit["house__"])
    date = str(convert_date_format(permit["issuance_date"]))
    source = str(permit["source"]) # From api call
    permit_type = str(permit["permit_type"])
    owner_business_name = str(permit["owner_s_business_name"]) if "owner_s_business_name" in permit else ""
    owner_first_name = str(permit["owner_s_first_name"]) if "owner_s_first_name" in permit else ""
    owner_last_name = str(permit["owner_s_last_name"]) if "owner_s_last_name" in permit else ""
    job_start_date = str(convert_date_format(permit["job_start_date"])) if "job_start_date" in permit else ""

    permit_cluster = get_permit_cluster_match(c, geometry_json)

    if permit_cluster:
      permit_cluster_id = int(permit_cluster[0])
      # print (" ^^ joining to permit cluster")
    else:
      permit_cluster_id = int(context.permit_clusters_seeds.seed_cluster_from_permit(c, permit, geometry_json, fkeys))
      print(" ++ seeding a cluster", permit_cluster_id)

    # create permit
    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}, {col9}, {col10}, {col11}, {col12}, {col13}, {col14} ,{col15}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'\
      .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6, col7=col7, col8=col8, col9=col9, col10=col10, col11=col11, col12=col12, col13=col13, col14=col14, col15=col15), (fkeys["borough_id"], fkeys["neighborhood_id"], fkeys["census_tract_id"], permit_cluster_id, building_id, geometry_json, house_number, street_name, date, source, permit_type, owner_business_name, owner_first_name, owner_last_name, job_start_date))

    if write_to_csv:
      context.csv_helpers.write_csv(c, permit, config.PERMITS_CSV_URL, index == 0)

