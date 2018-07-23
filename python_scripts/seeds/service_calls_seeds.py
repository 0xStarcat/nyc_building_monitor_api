import json
import datetime
import config 
import context 

table = 'service_calls'
col1 = 'building_id'
col2 = 'unique_id'
col3 = 'date'
col4 = 'status'
col5 = 'source'
col6 = 'description'
col7 = 'resolution_description'
col8 = 'resolution_violation'
col9 = 'resolution_no_action'
col10 = 'unable_to_investigate'
col11 = 'open_over_month'
col12 = 'closed_date'
col13 = 'days_to_close'

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table}(id))'\
    .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6, col7=col7, col8=col8, col9=col9, col10=col10, col11=col11, col12=col12, col13=col13, ref_table=context.buildings_seeds.table))

  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col2))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col3))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col4))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col5))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col6))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col7))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} BOOLEAN".format(tn=table, cn=col8))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} BOOLEAN".format(tn=table, cn=col9))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} BOOLEAN".format(tn=table, cn=col10))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} BOOLEAN".format(tn=table, cn=col11))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col12))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col13))

  c.execute('CREATE INDEX idx_call_building_id ON {tn}({col})'.format(tn=table, col=col1))
  c.execute('CREATE INDEX idx_call_date ON {tn}({col})'.format(tn=table, col=col3))
  c.execute('CREATE INDEX idx_call_source ON {tn}({col})'.format(tn=table, col=col5))
  c.execute('CREATE INDEX idx_call_res_vio ON {tn}({col})'.format(tn=table, col=col8))
  c.execute('CREATE INDEX idx_call_res_na ON {tn}({col})'.format(tn=table, col=col9))
  c.execute('CREATE INDEX idx_call_res_unable ON {tn}({col})'.format(tn=table, col=col10))
  c.execute('CREATE INDEX idx_call_open_over_month ON {tn}({col})'.format(tn=table, col=col11))
  c.execute('CREATE UNIQUE INDEX idx_call_unique_id ON {tn}({col})'.format(tn=table, col=col2))

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
  elif "The Department of Buildings investigated this complaint and closed it. If" in description:
    return True
  else:
    return False

def calculate_days_to_close(date_open, date_closed):
  date_difference = datetime.datetime.strptime(date_closed, "%Y%m%d") - datetime.datetime.strptime(date_open, "%Y%m%d")
  return int(date_difference.days)

def is_open_over_month(status, processed_date):
  return (status.lower() == "open" or status.lower() == "pending") and (datetime.date.today() - datetime.datetime.strptime(processed_date, "%Y%m%d").date()).days > 30

def get_building_match(c, bbl):
  c.execute('SELECT id FROM buildings WHERE bbl=\"{bbl}\"'.format(bbl=bbl))
  return c.fetchone()

def seed(c, service_calls_json, write_to_csv=False):
  print("Seeding calls...")

  for index, call in enumerate(service_calls_json):
    if index % 1000 == 0:
      print("call: " + str(index) + "/" + str(len(service_calls_json)))
    
    building_match = get_building_match(c, call["bbl"]) if "bbl" in call else None
    
    if not building_match: 
      print("  * no building match found", "call: " + str(index) + "/" + str(len(service_calls_json)))
      continue

    building_id = int(building_match[0])
    
    resolution_description = call["resolution_description"] if "resolution_description" in call else "unknown"
    if call_is_duplicate(resolution_description):
      # print("  * duplicate complaint found", "call: " + str(index) + "/" + str(len(service_calls_json)))
      continue

    resolution_violation = resulted_in_violation(resolution_description)
    resolution_no_action = took_no_action(resolution_description)
    unable_to_investigate = unable_to_investigate_call(resolution_description)

    date = str(datetime.datetime.strptime(call["created_date"][:10], "%Y-%m-%d").strftime("%Y%m%d"))
    closed_date = str(datetime.datetime.strptime(call["closed_date"][:10], "%Y-%m-%d").strftime("%Y%m%d")) if "status" in call and "closed_date" in call and call["status"].lower() != "open" and call["status"].lower() != "pending" else None
    days_to_close = int(calculate_days_to_close(date, closed_date)) if closed_date else None
    source = str(call["agency"]) if "agency" in call else "unknown"
    status = str(call["status"]) if "status" in call else "unknown"
    unique_id = str(call["unique_key"]) if "unique_key" in call else ""
    open_over_month = is_open_over_month(status, date)
    description = str(call["descriptor"])
    address = str(call["incident_address"]) if "incident_address" in call else ""
    
    
    # Create call
    try: 
      c.execute('INSERT INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}, {col9}, {col10}, {col11}, {col12}, {col13}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'\
        .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6, col7=col7, col8=col8, col9=col9, col10=col10, col11=col11, col12=col12, col13=col13), (building_id, unique_id, date, status, source, description, resolution_description, resolution_violation, resolution_no_action, unable_to_investigate, open_over_month, closed_date, days_to_close))
    except Exception as error:
      print("ERROR", error)
      continue

    # Create Building Event
    insertion_id = int(c.lastrowid)

    c.execute('SELECT * FROM {tn} WHERE {cn}={b_id}'\
      .format(tn=context.buildings_seeds.table, cn='id', b_id=building_id))

    building = c.fetchone()

    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}) VALUES (?, ?, ?, ?, ?, ?, ?)'\
      .format(tn=context.building_events_seeds.table, col1="borough_id", col2="neighborhood_id", col3="census_tract_id", col4="building_id", col5="eventable", col6="eventable_id", col7="event_date"), (building[1], building[2], building[3], building[0], 'service_call', insertion_id, date))

    # write csv row
    if write_to_csv:
      context.csv_helpers.write_csv(c, call, config.SERVICE_CALLS_CSV_URL, index == 0)
