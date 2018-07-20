import json
import csv
import xlrd

from seeds import buildings_seeds
from seeds import building_events_seeds
from seeds import conversions_seeds

import datetime
sales_table = 'sales'
sale_col1 = 'building_id'
sale_col2 = 'date'
sale_col3 = 'price'
sale_col4 = 'building_class_at_sale'
sale_col5 = 'building_class_after_sale'
sale_col6 = 'address'
sale_col7 = 'apartment_number'

def fix_brooklyn_csv():
  filename = "data/sales_data/csv/brooklyn_sales_2010-2017-backup.csv"
  writer = csv.writer(open("data/sales_data/csv/brooklyn_sales_2010-2017.csv", "a"))
  
  rows = list(csv.reader(open(filename)))
  writer.writerow(rows[0])
  
  for row in rows[1:]:
    try:
      row[20] = datetime.datetime.strptime(row[20], "%m/%d/%y").strftime("%m/%d/%Y")
    except ValueError as e:
      row[20] = datetime.datetime.strptime(row[20], "%m/%d/%Y").strftime("%m/%d/%Y")
    
    writer.writerow(row)

def merge_csv():
  years = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017"]
  boroughs = ["manhattan", "bronx", "queens", "statenisland"]

  for borough in boroughs:
    filename = "data/sales_data/csv/"+borough+"_sales_2010-2017.csv"
    writer = csv.writer(open(filename, "a"))

    for year in years:
      print("Writing ", borough, year, filename)
      xls_book = xlrd.open_workbook("data/sales_data/"+year+"_"+borough+".xls")
      sheet = xls_book.sheets()[0]

      row_start = 3 if year == "2010" else 5
      for index, row in enumerate(range(sheet.nrows)[row_start:]):
        parsed_row = sheet.row_values(row)
        
        if year == "2010" and index == 0:
          writer.writerow(parsed_row)
        else:
          year, month, day, hour, minute, second = xlrd.xldate_as_tuple(parsed_row[len(parsed_row) - 1], xls_book.datemode)
          py_date = datetime.datetime(year, month, day, hour, minute, second).strftime("%m/%d/%Y")
          parsed_row = parsed_row[:-1] + [py_date]
          writer.writerow(parsed_row)

def create_master_csv():
  filename = "data/sales_data/csv/nyc_sales_2010-2017.csv"
  writer = csv.writer(open(filename, "a"))
  for row in list(csv.reader(open("data/sales_data/csv/bronx_sales_2010-2017.csv"))):
    writer.writerow(row)
  for row in list(csv.reader(open("data/sales_data/csv/brooklyn_sales_2010-2017.csv")))[1:]:
    writer.writerow(row)
  for row in list(csv.reader(open("data/sales_data/csv/manhattan_sales_2010-2017.csv")))[1:]:
    writer.writerow(row)
  for row in list(csv.reader(open("data/sales_data/csv/queens_sales_2010-2017.csv")))[1:]:
    writer.writerow(row)
  for row in list(csv.reader(open("data/sales_data/csv/statenisland_sales_2010-2017.csv")))[1:]:
    writer.writerow(row)

def get_price(sale):
  price = 0
  if sale[19]:
    price = sale[19].replace(",", "").replace(".", "").replace(" ", "").replace("-", "").lstrip("$")
  else:
    # print("  * No price found")
    pass
  return price

def get_bbl(boro_id, sale):
  try: 
    bbl = int(str(boro_id) + str(int(float(sale[4]))).lstrip("0").zfill(5) + str(int(float(sale[5]))).lstrip("0").zfill(4))
  except:
    print("  * unable to get BBL")
    return None
  return bbl

def get_building_match(c, sale):
  boro_id = int(float(sale[0]))
  bbl = get_bbl(boro_id, sale)
  if not bbl:
    return None

  c.execute('SELECT * FROM buildings WHERE bbl={bbl}'.format(bbl=bbl))
  match = c.fetchone()
  # try BBL, then address
  if match:
    return match
  else:
    c.execute('SELECT * FROM buildings WHERE boro_code={boro_id} AND address=\"{address}\"'.format(boro_id=boro_id, address=sale[8].strip()))
    return c.fetchone()

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {bldg_table}(id), {col2} TEXT, {col3} INT, {col4} TEXT, {col5} TEXT, {col6} TEXT, {col7} TEXT, UNIQUE({col1}, {col2}) ON CONFLICT REPLACE)'\
    .format(tn=sales_table, col1=sale_col1, col2=sale_col2, col3=sale_col3, col4=sale_col4, col5=sale_col5, col6=sale_col6, col7=sale_col7, bldg_table=buildings_seeds.buildings_table))

  c.execute('CREATE INDEX idx_sale_building_id ON {tn}({col1})'.format(tn=sales_table, col1=sale_col1))
  c.execute('CREATE TRIGGER insert_sale_with_price BEFORE INSERT ON {tn} FOR EACH ROW WHEN (SELECT price FROM {tn} WHERE date = NEW.date AND building_id = NEW.building_id) > NEW.price BEGIN SELECT RAISE(IGNORE); END;'.format(tn=sales_table))

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
  return not class_is_residential(bldg_class)

def seed_sales(c, sale_csv):
  print("Seeding sales...")

  for index, sale in enumerate(sale_csv):
    if index % 1000 == 0:
      print("sale: " + str(index) + "/" + str(len(sale_csv)))
    if len(sale) < 21:
      print("  X malformed sale record", "sale: " + str(index) + "/" + str(len(sale_csv)))
      continue

    
    building_match = get_building_match(c, sale)

    if not building_match: 
      print("  X no building match found", "sale: " + str(index) + "/" + str(len(sale_csv)))
      continue

    building_id = building_match[0]
    date = datetime.datetime.strptime(sale[20], "%m/%d/%Y").strftime("%Y%m%d")
    price = get_price(sale)
    bldg_class_at_sale = str(sale[18]).strip()
    bldg_class_after_sale = str(sale[7]).strip()
    bldg_class_now = building_match[22]
    address = sale[8]
    apartment_number = sale[9]
    # Create Sale
    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}) VALUES ({building_id}, \'{date}\', \"{price}\", \'{bldg_class_at_sale}\',  \'{bldg_class_after_sale}\', \"{address}\", \'{apartment_number}\')'\
      .format(tn=sales_table, col1=sale_col1, col2=sale_col2, col3=sale_col3, col4=sale_col4, col5=sale_col5, col6=sale_col6, col7=sale_col7, building_id=building_id, date=date, price=price, bldg_class_at_sale=bldg_class_at_sale, bldg_class_after_sale=bldg_class_after_sale, address=address, apartment_number=apartment_number))


    insertion_id = c.lastrowid

    c.execute('SELECT * FROM {tn} WHERE {cn}={b_id}'\
      .format(tn=buildings_seeds.buildings_table, cn='id', b_id=building_id))

    building = c.fetchone()

    # Create Building Event
    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'\
      .format(tn=building_events_seeds.building_events_table, col1="borough_id", col2="community_district_id", col3="neighborhood_id", col4="census_tract_id", col5="building_id", col6="eventable", col7="eventable_id", col8="event_date"), (building[1], building[2], building[3], building[4], building[0], 'sale', insertion_id, date))

    # Create Conversion if needed
    if bldg_class_at_sale and bldg_class_after_sale and bldg_class_at_sale != bldg_class_after_sale:
      print("  + Creating conversion", str(index) + "/" + str(len(sale_csv)))
      conversions_seeds.create_row_from_sale(c, insertion_id, date, bldg_class_at_sale, bldg_class_after_sale, building)

def evaluate_building_conversions(c):
  c.execute('SELECT * FROM conversions')