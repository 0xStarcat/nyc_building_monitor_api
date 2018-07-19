import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '../../python_scripts'))

import json
from seeds import buildings_seeds
from seeds import building_events_seeds
import datetime
from helpers import csv_helpers
import config

violations_table = 'violations'
vio_col1 = 'building_id'
vio_col2 = 'date'
vio_col3 = 'description'
vio_col4 = 'penalty_imposed'
vio_col5 = 'source'
vio_col6 = 'violation_id'

def get_violation_id(violation):
  if "violationid" in violation:
    return violation["violationid"]
  elif "ecb_violation_number" in violation:
    return violation["ecb_violation_number"]
  elif "number" in violation:
    return violation["number"]
  else:
    print("No unique id found")
    return None

def get_description(violation):
  description = ""
  if "violation_description" in violation:
    description = violation["violation_description"]
  elif "description" in violation:
    description = violation["description"]
  else:
    pass
  return description

def get_penalty(violation):
  penalty_imposed = ""
  if "penality_imposed" in violation:
    if violation["penality_imposed"] == ".00":
      pass
    else:
      penalty_imposed = violation["penality_imposed"]

  return penalty_imposed

def get_date(violation):
  if "issue_date" in violation:
    return violation["issue_date"]
  elif "inspectiondate" in violation:
    return datetime.datetime.strptime(violation['inspectiondate'][:10], "%Y-%m-%d").strftime("%Y%m%d")
  else:
    return False

def get_bbl(boro_id, violation):
  return int(str(boro_id) + str(violation["block"].lstrip("0").zfill(5) + str(violation["lot"].lstrip("0").zfill(4))))

def get_building_match(c, violation):
  if "boroid" in violation:
    boro_id = violation["boroid"]
  elif "boro" in violation:
    boro_id = violation["boro"]
  else:
    return None

  if "block" not in violation or "lot" not in violation:
    return None

  if boro_id and violation["block"] and violation["lot"]:
    bbl = get_bbl(boro_id, violation)
    c.execute('SELECT * FROM buildings WHERE bbl=\'{bbl}\''.format(bbl=bbl))
    return c.fetchone()
  else:
    return None

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {bldg_table}(id), {col2} TEXT, {col3} TEXT, {col4} TEXT, {col5} TEXT, {col6} TEXT)'\
    .format(tn=violations_table, col1=vio_col1, col2=vio_col2, col3=vio_col3, col4=vio_col4,col5=vio_col5, col6=vio_col6, bldg_table=buildings_seeds.buildings_table))

  c.execute('CREATE INDEX idx_violation_building_id ON {tn}({col1})'.format(tn=violations_table, col1=vio_col1))
  c.execute('CREATE INDEX idx_violation_source ON {tn}({col5})'.format(tn=violations_table, col5=vio_col5))

def seed_violations(c, violation_json, write_to_csv=False):
  print("Seeding Violations...")

  for index, violation in enumerate(violation_json):
    if index % 1000 == 0:
      print("Violation: " + str(index) + "/" + str(len(violation_json)))
    
    building_match = get_building_match(c, violation)

    if not building_match:
      print("  * no building match found", "call: " + str(index) + "/" + str(len(violation_json)))
      continue

    building_id = building_match[0]
    
    date = get_date(violation)

    if date == False:
      print("  * no issue_date or inspectiondate found", "call: " + str(index) + "/" + str(len(violation_json)))
      continue

    description = get_description(violation)

    penalty_imposed = get_penalty(violation)
    source = violation['source']
    unique_id = get_violation_id(violation)
    # Create Violation
    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}) VALUES ({building_id}, \'{date}\', \"{description}\", \'{penalty_imposed}\', \'{source}\', \'{unique_id}\')'\
      .format(tn=violations_table, col1=vio_col1, col2=vio_col2, col3=vio_col3, col4=vio_col4, col5=vio_col5, col6=vio_col6, building_id=building_id, date=date, description=description, penalty_imposed=penalty_imposed, source=source, unique_id=unique_id))

    insertion_id = c.lastrowid

    c.execute('SELECT * FROM {tn} WHERE {cn}={b_id}'\
      .format(tn=buildings_seeds.buildings_table, cn='id', b_id=building_id))

    building = c.fetchone()

    # Create Building Event
    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'\
      .format(tn=building_events_seeds.building_events_table, col1="borough_id", col2="community_district_id", col3="neighborhood_id", col4="census_tract_id", col5="building_id", col6="eventable", col7="eventable_id", col8="event_date"), (building[1], building[2], building[3], building[4], building[0], 'violation', insertion_id, date))

    # write csv row
    if write_to_csv:
      csv_helpers.write_csv(c, violation, config.VIOLATIONS_CSV_URL, index == 0)
