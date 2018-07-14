import json
from seeds import buildings_seeds
from seeds import building_events_seeds
import datetime
from helpers import csv_helpers

service_calls_table = 'service_calls'
call_col1 = 'building_id'
call_col2 = 'date'
call_col3 = 'description'
call_col4 = 'resolution_description'
call_col5 = 'resolution_violation'
call_col6 = 'resolution_no_action'
call_col7 = 'unable_to_investigate'
call_col8 = 'status'
call_col9 = 'unique_key'
call_col10 = 'open_over_month'
call_col11 = 'source'

def call_is_duplicate(description):
  if "another service request number" in description:
    return True
  elif "More than one complaint was received" in description:
    return True
  elif "already reported by" in description:
    return True
  else:
    return False

def resulted_in_violation(description):
  if "violation" in description and "No violations were issued" not in description:
    return True
  elif "Violations" in description and "No violations were issued" not in description:
    return True
  else:
    return False

def unable_to_investigate_call(description):
  if "gain access" in description:
    return True
  if "attempted to investigate" in description:
    return True
  elif "Please check back later for status" in description:
    return True
  else:
    return False

def took_no_action(description):
  if "No violations were issued" in description:
    return True
  elif "no further action" in description:
    return True
  elif "had been restored" in description:
    return True
  else:
    return False

def is_open_over_month(status, processed_date):
  return status.lower() == "open" and (datetime.date.today() - datetime.datetime.strptime(processed_date, "%Y%m%d").date()).days > 30

def get_building_match(c, address):
  c.execute('SELECT * FROM buildings WHERE address=\"{address}\"'.format(address=address))
  return c.fetchone()

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {bldg_table}(id), {col2} TEXT, {col3} TEXT, {col4} TEXT, {col5} BOOLEAN, {col6} BOOLEAN, {col7} BOOLEAN, {col8} TEXT, {col9} TEXT, {col10} BOOLEAN, {col11})'\
    .format(tn=service_calls_table, col1=call_col1, col2=call_col2, col3=call_col3, col4=call_col4, col5=call_col5, col6=call_col6, col7=call_col7, col8=call_col8, col9=call_col9, col10=call_col10, col11=call_col11, bldg_table=buildings_seeds.buildings_table))

  c.execute('CREATE INDEX idx_call_building_id ON {tn}({col1})'.format(tn=service_calls_table, col1=call_col1))
  c.execute('CREATE INDEX idx_call_source ON {tn}({col6})'.format(tn=service_calls_table, col6=call_col6))

def seed_service_calls_from_csv(c, service_calls_csv):
  print("Seeding calls...")

  for index, call in enumerate(service_calls_csv):
    print("call: " + str(index) + "/" + str(len(service_calls_csv)))
    
    date = datetime.datetime.strptime(call[1][:10], "%Y-%m-%d").strftime("%Y%m%d")

    resolution_description = call[21]
    if call_is_duplicate(resolution_description):
      print("  * duplicate complaint found")
      continue

    resolution_violation = resulted_in_violation(call[21])
    resolution_no_action = took_no_action(call[21])
    unable_to_investigate = unable_to_investigate_call(call[21])

    source = call[3]
    status = call[19]
    unique_key = call[0]
    open_over_month = is_open_over_month(status, date)
    description = call[6]
    building_match = get_building_match(c, call[9])
    if building_match:
      pass
    else: 
      print("  * no building match found")
      continue

    building_id = building_match[0]
    
    # Create call
    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}, {col9}, {col10}, {col11}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'\
      .format(tn=service_calls_table, col1=call_col1, col2=call_col2, col3=call_col3, col4=call_col4, col5=call_col5, col6=call_col6, col7=call_col7, col8=call_col8, col9=call_col9, col10=call_col10, col11=call_col11), (building_id, date, description, resolution_description, resolution_violation, resolution_no_action, unable_to_investigate, status, unique_key, open_over_month, source))

    insertion_id = c.lastrowid

    c.execute('SELECT * FROM {tn} WHERE {cn}={b_id}'\
      .format(tn=buildings_seeds.buildings_table, cn='id', b_id=building_id))

    building = c.fetchone()

    # Create Building Event
    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}) VALUES ({ct_id}, {n_id}, {building_id}, \'{eventable}\', \"{event_id}\", \"{event_date}\")'\
      .format(tn=building_events_seeds.building_events_table, col1="census_tract_id", col2="neighborhood_id", col3="building_id", col4="eventable", col5="eventable_id", col6="event_date", event_date=date, ct_id=building[6], n_id=building[7], building_id=building_id, eventable='service_call', event_id=insertion_id))

def seed_service_calls_from_json(c, service_calls_json):
  print("Seeding calls...")

  for index, call in enumerate(service_calls_json):
    print("call: " + str(index) + "/" + str(len(service_calls_json)))
    
    date = datetime.datetime.strptime(call["created_date"][:10], "%Y-%m-%d").strftime("%Y%m%d")

    resolution_description = call["resolution_description"] if "resolution_description" in call else "unknown"
    if call_is_duplicate(resolution_description):
      print("  * duplicate complaint found")
      continue

    resolution_violation = resulted_in_violation(resolution_description)
    resolution_no_action = took_no_action(resolution_description)
    unable_to_investigate = unable_to_investigate_call(resolution_description)

    source = call["agency"] if "agency" in call else "unknown"
    status = call["status"] if "status" in call else "unknown"
    unique_key = call["unique_key"]
    open_over_month = is_open_over_month(status, date)
    description = call["descriptor"]
    address = call["incident_address"] if "incident_address" in call else ""
    building_match = get_building_match(c, address)
    if building_match:
      pass
    else: 
      print("  * no building match found")
      continue

    building_id = building_match[0]
    
    # Create call
    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}, {col9}, {col10}, {col11}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'\
      .format(tn=service_calls_table, col1=call_col1, col2=call_col2, col3=call_col3, col4=call_col4, col5=call_col5, col6=call_col6, col7=call_col7, col8=call_col8, col9=call_col9, col10=call_col10, col11=call_col11), (building_id, date, description, resolution_description, resolution_violation, resolution_no_action, unable_to_investigate, status, unique_key, open_over_month, source))

    insertion_id = c.lastrowid

    c.execute('SELECT * FROM {tn} WHERE {cn}={b_id}'\
      .format(tn=buildings_seeds.buildings_table, cn='id', b_id=building_id))

    building = c.fetchone()

    # Create Building Event
    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'\
      .format(tn=building_events_seeds.building_events_table, col1="borough_id", col2="community_district_id", col3="neighborhood_id", col4="census_tract_id", col5="building_id", col6="eventable", col7="eventable_id", col8="event_date"), (building[1], building[2], building[3], building[4], building[0], 'service_call', insertion_id, date))

    # write csv row
    csv_helpers.write_csv(c, call, 'data/service_calls_data/csv/nyc_service_calls_data.csv', index == 0)
