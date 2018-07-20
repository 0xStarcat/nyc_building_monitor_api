import json
import datetime
import config 
from helpers import csv_helpers
from seeds import buildings_seeds
from seeds import building_events_seeds

table = 'evictions'

col1 = 'building_id'
col2 = 'court_index_number'
col3 = 'address'
col4 = 'apt_number'
col5 = 'date'
col6 = 'status'
col7 = 'source'

def get_borough_code(eviction):
  if eviction["borough"].lower() == "manhattan":
    return 1
  if eviction["borough"].lower() == "bronx":
    return 2
  if eviction["borough"].lower() == "brooklyn":
    return 3
  if eviction["borough"].lower() == "queens":
    return 4
  if eviction["borough"].lower() == "staten island":
    return 5 

def find_building(c, eviction):
  boro_code = get_borough_code(eviction)
  print("B", boro_code, eviction["eviction_address"])
  c.execute('SELECT * FROM buildings WHERE boro_code={boro_code} AND address=\"{address}\"'.format(boro_code=boro_code, address=eviction["eviction_address"]))
  return c.fetchone()

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table1}(id), {col2} TEXT, {col3} TEXT, {col4} TEXT, {col5} TEXT, {col6} TEXT, {col7} TEXT)'\
    .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6, col7=col7, ref_table1=buildings_seeds.buildings_table))

  c.execute('CREATE INDEX idx_eviction_bldg_id ON {tn}({col1})'.format(tn=table, col1=col1))

def seed_table(c, json, write_to_csv=False):
  print("Seeding evictions")

  for index, eviction in enumerate(json):
    if index % 1000 == 0:
      print("Eviction: " + str(index) + "/" + str(len(json)))
    building = find_building(c, eviction)

    if not building:
      print("  X no building", str(index) + "/" + str(len(json)))
      continue

    building_id = building[0]
    court_index_number = eviction["court_index_number"]
    address = eviction["eviction_address"] 
    apt_number = eviction["eviction_apt_num"] if "eviction_apt_num" in eviction else ""
    date = datetime.datetime.strptime(eviction['executed_date'][:10], "%Y-%m-%d").strftime("%Y%m%d")
    status = eviction["schedule_status"]

    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}) VALUES ({building_id}, \"{court_index_number}\", \"{address}\", \"{apt_number}\", \'{date}\', \'{status}\', \'{source}\')'\
      .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6, col7=col7, building_id=building_id, court_index_number=court_index_number, address=address, apt_number=apt_number, date=date, status=status, source="NYC"))

    insertion_id = c.lastrowid

    # Create Building Event
    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'\
      .format(tn=building_events_seeds.building_events_table, col1="borough_id", col2="community_district_id", col3="neighborhood_id", col4="census_tract_id", col5="building_id", col6="eventable", col7="eventable_id", col8="event_date"), (building[1], building[2], building[3], building[4], building[0], 'eviction', insertion_id, date))

    # write csv row
    if write_to_csv:
      csv_helpers.write_csv(c, eviction, config.EVICTIONS_CSV_URL, index == 0)

