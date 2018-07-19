import json
from seeds import buildings_seeds
from seeds import building_events_seeds
import datetime
from helpers import csv_helpers
import config 

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
call_col12 = 'closed_date'
call_col13 = 'days_to_close'

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

def calculate_days_to_close(date_open, date_closed):
  date_difference = datetime.datetime.strptime(date_closed, "%Y%m%d") - datetime.datetime.strptime(date_open, "%Y%m%d")
  return int(date_difference.days)

def is_open_over_month(status, processed_date):
  return (status.lower() == "open" or status.lower() == "pending") and (datetime.date.today() - datetime.datetime.strptime(processed_date, "%Y%m%d").date()).days > 30

def get_building_match(c, bbl):
  c.execute('SELECT * FROM buildings WHERE bbl=\"{bbl}\"'.format(bbl=bbl))
  return c.fetchone()

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {bldg_table}(id), {col2} TEXT, {col3} TEXT, {col4} TEXT, {col5} BOOLEAN, {col6} BOOLEAN, {col7} BOOLEAN, {col8} TEXT, {col9} TEXT, {col10} BOOLEAN, {col11} TEXT, {col12} TEXT, {col13} INT)'\
    .format(tn=service_calls_table, col1=call_col1, col2=call_col2, col3=call_col3, col4=call_col4, col5=call_col5, col6=call_col6, col7=call_col7, col8=call_col8, col9=call_col9, col10=call_col10, col11=call_col11, col12=call_col12, col13=call_col13, bldg_table=buildings_seeds.buildings_table))

  c.execute('CREATE INDEX idx_call_building_id ON {tn}({col1})'.format(tn=service_calls_table, col1=call_col1))
  c.execute('CREATE INDEX idx_call_source ON {tn}({col6})'.format(tn=service_calls_table, col6=call_col6))

def seed_service_calls_from_json(c, service_calls_json, write_to_csv=False):
  print("Seeding calls...")

  for index, call in enumerate(service_calls_json):
    if index % 1000 == 0:
      print("call: " + str(index) + "/" + str(len(service_calls_json)))
    
    
    resolution_description = call["resolution_description"] if "resolution_description" in call else "unknown"
    if call_is_duplicate(resolution_description):
      print("  * duplicate complaint found", "call: " + str(index) + "/" + str(len(service_calls_json)))
      continue

    resolution_violation = resulted_in_violation(resolution_description)
    resolution_no_action = took_no_action(resolution_description)
    unable_to_investigate = unable_to_investigate_call(resolution_description)

    date = datetime.datetime.strptime(call["created_date"][:10], "%Y-%m-%d").strftime("%Y%m%d")
    closed_date = datetime.datetime.strptime(call["closed_date"][:10], "%Y-%m-%d").strftime("%Y%m%d") if "status" in call and "closed_date" in call and call["status"].lower() != "open" and call["status"].lower() != "pending" else None
    days_to_close = calculate_days_to_close(date, closed_date) if closed_date else None
    source = call["agency"] if "agency" in call else "unknown"
    status = call["status"] if "status" in call else "unknown"
    unique_key = call["unique_key"]
    open_over_month = is_open_over_month(status, date)
    description = call["descriptor"]
    address = call["incident_address"] if "incident_address" in call else ""
    building_match = get_building_match(c, call["bbl"])
    
    if not building_match: 
      print("  * no building match found", "call: " + str(index) + "/" + str(len(service_calls_json)))
      continue

    building_id = building_match[0]
    
    # Create call
    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}, {col9}, {col10}, {col11}, {col12}, {col13}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'\
      .format(tn=service_calls_table, col1=call_col1, col2=call_col2, col3=call_col3, col4=call_col4, col5=call_col5, col6=call_col6, col7=call_col7, col8=call_col8, col9=call_col9, col10=call_col10, col11=call_col11, col12=call_col12, col13=call_col13), (building_id, date, description, resolution_description, resolution_violation, resolution_no_action, unable_to_investigate, status, unique_key, open_over_month, source, closed_date, days_to_close))

    insertion_id = c.lastrowid

    c.execute('SELECT * FROM {tn} WHERE {cn}={b_id}'\
      .format(tn=buildings_seeds.buildings_table, cn='id', b_id=building_id))

    building = c.fetchone()

    # Create Building Event
    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'\
      .format(tn=building_events_seeds.building_events_table, col1="borough_id", col2="community_district_id", col3="neighborhood_id", col4="census_tract_id", col5="building_id", col6="eventable", col7="eventable_id", col8="event_date"), (building[1], building[2], building[3], building[4], building[0], 'service_call', insertion_id, date))

    # write csv row
    if write_to_csv:
      csv_helpers.write_csv(c, call, config.SERVICE_CALLS_CSV_URL, index == 0)
