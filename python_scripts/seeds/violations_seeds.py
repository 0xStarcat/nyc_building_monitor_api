import datetime
import config
import context

table = 'violations'
col1 = 'building_id'
col2 = 'unique_id'
col3 = 'date'
col4 = 'description'
col5 = 'penalty_imposed'
col6 = 'source'
col7 = 'violation_code'
col8 = 'status'
col9 = 'status_description'
col10 ='ecb_number'

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table}(id))'\
    .format(tn=table, col1=col1, ref_table=context.buildings_seeds.table))

  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col2))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col3))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col4))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col5))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col6))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col7))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col8))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col9))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col10))

  c.execute('CREATE INDEX idx_violation_building_id ON {tn}({col})'.format(tn=table, col=col1))
  c.execute('CREATE INDEX idx_violation_source ON {tn}({col})'.format(tn=table, col=col6))
  c.execute('CREATE INDEX idx_violation_code ON {tn}({col})'.format(tn=table, col=col7))
  c.execute('CREATE INDEX idx_violation_date ON {tn}({col})'.format(tn=table, col=col3))
  c.execute('CREATE INDEX idx_violation_status ON {tn}({col})'.format(tn=table, col=col8))

  c.execute('CREATE UNIQUE INDEX idx_violation_unique_id ON {tn}({col})'.format(tn=table, col=col2))

def get_violation_id(violation):
  if "violationid" in violation: #HPD
    return violation["violationid"]
  elif "ecb_violation_number" in violation: #ECB
    return violation["ecb_violation_number"]
  elif "number" in violation: #DoB
    return violation["number"]
  else:
    print("  * No unique id found")
    return None

def get_status(violation):
  status = ""
  if "violationstatus" in violation: #HPD
    status = "closed" if "close" in violation["violationstatus"].lower() else "open"
  elif "ecb_violation_status" in violation: #ecb
    status = "closed" if "resolve" in violation["ecb_violation_status"].lower() else "open"
  elif "violation_category" in violation: #DOB
    status = "open" if "active" in violation["violation_category"].lower() else "closed"
  else:
    print("  * no status found")
    return None
  return status

def get_status_description(violation):
  status_description = ""
  if "currentstatus" in violation: #hpd
    status_description = violation["currentstatus"]
  elif "certification_status" in violation: #ecb
    status_description = violation["certification_status"] #dob
  elif "violation_category" in violation and "disposition_comments" in violation:
    status_description = violation["violation_category"] + " - " + violation["disposition_comments"]
  elif "violation_category" in violation:
    status_description = violation["violation_category"]
  else:
    # print("  * no violation status description")
    return None
  return status_description

def get_description(violation):
  description = ""
  if "violation_description" in violation:
    description = violation["violation_description"] #ECB
  elif "description" in violation:
    description = violation["description"] #DOB
  elif "novdescription" in violation: #HPD
    description = violation["novdescription"]
  return description

def extract_section_code(description):
  if "SECTION" in description:
    split =  description.split(" ")
    return split[0] + " " + split[1]
  return

def get_code(violation):
  code = ""
  if "violation_type_code" in violation: # ECB
    code = violation["violation_type_code"]
  elif "infraction_code1" in violation: #DOB
    code = violation["infraction_code1"]
  elif "novdescription" in violation: #HPD - need to parse section law from this
    code = extract_section_code(violation["novdescription"])
  return code

def get_penalty(violation):
  penalty_imposed = ""
  if "penality_imposed" in violation:
    if violation["penality_imposed"] == ".00":
      pass
    else:
      penalty_imposed = violation["penality_imposed"]

  return penalty_imposed

def get_date(violation):
  if "issue_date" in violation: # DOB and ECB
    return violation["issue_date"]
  elif "inspectiondate" in violation: # HPD
    return datetime.datetime.strptime(violation['inspectiondate'][:10], "%Y-%m-%d").strftime("%Y%m%d")
  else:
    return False

def get_bbl(boro_id, violation):
  try: 
    bbl = int(str(boro_id) + str(violation["block"].lstrip("0").zfill(5) + str(violation["lot"].lstrip("0").zfill(4))))
  except:
    print("  * unable to get BBL")
    return None
  return bbl

def get_building_match(c, violation):
  if "boroid" in violation:
    boro_id = violation["boroid"]
  elif "boro" in violation:
    boro_id = violation["boro"]
  else:
    print("  X no BORO")
    return None

  if "block" not in violation or "lot" not in violation:
    print("  X no block or lot")
    return None

  if boro_id and violation["block"] and violation["lot"]:
    bbl = get_bbl(boro_id, violation)
    c.execute('SELECT id FROM buildings WHERE bbl=\"{bbl}\"'.format(bbl=bbl))
    return c.fetchone()
  else:
    return None

def seed(c, violation_json, write_to_csv=False):
  print("Seeding Violations...")

  for index, violation in enumerate(violation_json):
    if index % 1000 == 0:
      print("Violation: " + str(index) + "/" + str(len(violation_json)))
    
    date = str(get_date(violation))
    if date == False:
      print("  * no issue_date or inspectiondate found", str(index) + "/" + str(len(violation_json)))
      continue
      
    building_match = get_building_match(c, violation)

    if not building_match:
      # print("  * no building match found", str(index) + "/" + str(len(violation_json)))
      continue

    building_id = int(building_match[0])
    unique_id = str(get_violation_id(violation))

    

    description = str(get_description(violation))
    penalty_imposed = str(get_penalty(violation))
    source = violation['source'] # field added from from API call
    violation_code = str(get_code(violation))
    status = get_status(violation)
    status_description = get_status_description(violation)
    ecb_number = violation["ecb_number"] if "ecb_number" in violation else None
    # Create Violation
    try:
      c.execute('INSERT INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}, {col9}, {col10}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'\
        .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6, col7=col7, col8=col8, col9=col9, col10=col10), (building_id, unique_id, date, description, penalty_imposed, source, violation_code, status, status_description, ecb_number))
    except Exception as error:
      print("ERROR", error)
      continue

    # Create Building Event
    insertion_id = c.lastrowid

    c.execute('SELECT id, borough_id, neighborhood_id, census_tract_id FROM {tn} WHERE {cn}={building_id}'\
      .format(tn=context.buildings_seeds.table, cn='id', building_id=building_id))

    building = c.fetchone()

    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}) VALUES (?, ?, ?, ?, ?, ?, ?)'\
      .format(tn=context.building_events_seeds.table, col1="borough_id", col2="neighborhood_id", col3="census_tract_id", col4="building_id", col5="eventable", col6="eventable_id", col7="event_date"), (building[1], building[2], building[3], building[0], 'violation', insertion_id, date))

    # write csv row
    if write_to_csv:
      context.csv_helpers.write_csv(c, violation, config.VIOLATIONS_CSV_URL, index == 0)
