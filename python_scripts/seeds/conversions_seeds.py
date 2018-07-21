import json
from seeds import buildings_seeds
from seeds import building_events_seeds
from seeds import sales_seeds

table = 'conversions'

col1 = 'building_id'
col2 = 'sale_id'
col3 = 'date'
col4 = 'source'
col5 = 'converted_from'
col6 = 'converted_to'
col7 = 'converted_residential'
col8 = 'converted_non_residential'

def get_residential_r_class(bldg_class):
  if bldg_class[0].lower() != "r":
    return False

  try:
    return bldg_class.lower() == "rr" or int(bldg_class[1]) >= 0
  except: 
    return False

def class_is_residential(bldg_class):
  cl = bldg_class[:1].lower()
  return cl == "a" or cl == "b" or cl == "c" or cl == "d" or cl == "l" or get_residential_r_class(bldg_class) or cl == "s"

def class_is_non_residential(bldg_class):
  return class_is_residential(bldg_class) != True

def create_table(c):
	c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table1}(id), {col2} INTEGER NOT NULL REFERENCES {ref_table2}(id), {col3} TEXT, {col4} TEXT, {col5} TEXT, {col6} TEXT, {col7} BOOLEAN, {col8} BOOLEAN)'\
    .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6, col7=col7, col8=col8, ref_table1=buildings_seeds.table, ref_table2=sales_seeds.table))

def create_row_from_sale(c, sale_id, date, class_from, class_to, building):
  # Create Conversion
  building_id = building[0]

  date = date
  source = "sale"
  converted_from = class_from
  converted_to = class_to

  converted_residential = class_is_non_residential(converted_from) and class_is_residential(converted_to)
  converted_non_residential = class_is_residential(converted_from) and class_is_non_residential(converted_to)

  try:
    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}) VALUES ({building_id}, {sale_id}, \'{date}\', \"{source}\", \'{converted_from}\', \'{converted_to}\', \'{converted_residential}\', \'{converted_non_residential}\')'\
      .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6, col7=col7, col8=col8, building_id=building_id, sale_id=sale_id, date=date, source=source, converted_from=converted_from, converted_to=converted_to, converted_residential=converted_residential, converted_non_residential=converted_non_residential))
  except:
    print("  +X unable to insert")

  insertion_id = c.lastrowid

  # Create Building Event
  c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'\
    .format(tn=building_events_seeds.table, col1="borough_id", col2="community_district_id", col3="neighborhood_id", col4="census_tract_id", col5="building_id", col6="eventable", col7="eventable_id", col8="event_date"), (building[1], building[2], building[3], building[4], building[0], 'conversion', insertion_id, date))