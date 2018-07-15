import json
from seeds import buildings_seeds
from seeds import building_events_seeds
from helpers import csv_helpers


from shapely.geometry import Point, mapping
import datetime

permits_table = 'permits'
permit_col1 = 'building_id'
permit_col2 = 'date'
permit_col3 = 'geometry'
permit_col4 = 'source'

def get_geometry(lon, lat):
  if lon and lat:
    return mapping(Point(float(lon), float(lat)))
  else:
    return None

def get_building_match(c, block, lot):
  c.execute('SELECT * FROM buildings WHERE block={v_block} AND lot={v_lot}'.format(v_block=str(block), v_lot=str(lot)))
  return c.fetchone()

def convert_date_format(issuance_date):
  return datetime.datetime.strptime(issuance_date[:10], "%Y-%m-%d").strftime("%Y%m%d")

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER REFERENCES {bldg_table}(id), {col2} TEXT, {col3} INT, {col4} TEXT)'\
    .format(tn=permits_table, col1=permit_col1, col2=permit_col2, col3=permit_col3, col4=permit_col4, bldg_table=buildings_seeds.buildings_table))

  c.execute('CREATE INDEX idx_permit_building_id ON {tn}({col1})'.format(tn=permits_table, col1=permit_col1))


def seed_permits_from_json(c, permit_json):
  print("Seeding permits...")

  for index, permit in enumerate(permit_json):
    print("permit: " + str(index) + "/" + str(len(permit_json)))
    
    building_match = get_building_match(c, permit["block"], permit["lot"])

    if not building_match:
      print("  - no building match found")

    building_id = building_match[0] if building_match else None
    date = convert_date_format(permit["issuance_date"])

    if "gis_longitude" not in permit and "gis_latitude" not in permit:
      print("  * no geo information")
      continue

    geometry = get_geometry(permit["gis_longitude"], permit["gis_latitude"])
    source = permit["source"]

    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}) VALUES (?, ?, ?, ?)'\
      .format(tn=permits_table, col1=permit_col1, col2=permit_col2, col3=permit_col3, col4=permit_col4), (building_id, str(date), str(geometry), str(source)))


    if building_id:
      insertion_id = c.lastrowid
      
      c.execute('SELECT * FROM {tn} WHERE {cn}={b_id}'\
        .format(tn=buildings_seeds.buildings_table, cn='id', b_id=building_id))

      building = c.fetchone()

      # Create Building Event
      c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'\
        .format(tn=building_events_seeds.building_events_table, col1="borough_id", col2="community_district_id", col3="neighborhood_id", col4="census_tract_id", col5="building_id", col6="eventable", col7="eventable_id", col8="event_date"), (building[1], building[2], building[3], building[4], building[0], 'permit', insertion_id, date))

    csv_helpers.write_csv(c, permit, 'data/permit_data/csv/nyc_permits_data.csv', index == 0)

