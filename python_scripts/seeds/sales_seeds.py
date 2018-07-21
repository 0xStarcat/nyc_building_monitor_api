import context
import datetime

sales_table = 'sales'
col1 = 'building_id'
col2 = 'address'
col3 = 'apartment_number'
col4 = 'date'
col5 = 'price'
col6 = 'building_class_at_sale'
col7 = 'building_class_after_sale'

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {bldg_table}(id), {col2} TEXT, {col3} INT, {col4} TEXT, {col5} TEXT, {col6} TEXT, {col7} TEXT, UNIQUE({col1}, {col2}) ON CONFLICT REPLACE)'\
    .format(tn=sales_table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6, col7=col7, bldg_table=context.buildings_seeds.table))

  c.execute('CREATE INDEX idx_sale_building_id ON {tn}({col1})'.format(tn=sales_table, col1=col1))
  c.execute('CREATE TRIGGER insert_sale_with_price BEFORE INSERT ON {tn} FOR EACH ROW WHEN (SELECT price FROM {tn} WHERE date = NEW.date AND building_id = NEW.building_id) > NEW.price BEGIN SELECT RAISE(IGNORE); END;'.format(tn=sales_table))

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
      .format(tn=sales_table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6, col7=col7, building_id=building_id, date=date, price=price, bldg_class_at_sale=bldg_class_at_sale, bldg_class_after_sale=bldg_class_after_sale, address=address, apartment_number=apartment_number))


    insertion_id = c.lastrowid

    c.execute('SELECT * FROM {tn} WHERE {cn}={b_id}'\
      .format(tn=context.buildings_seeds.table, cn='id', b_id=building_id))

    building = c.fetchone()

    # Create Building Event
    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'\
      .format(tn=context.building_events_seeds.table, col1="borough_id", col2="community_district_id", col3="neighborhood_id", col4="census_tract_id", col5="building_id", col6="eventable", col7="eventable_id", col8="event_date"), (building[1], building[2], building[3], building[4], building[0], 'sale', insertion_id, date))

    # Create Conversion if needed
    if bldg_class_at_sale and bldg_class_after_sale and bldg_class_at_sale != bldg_class_after_sale:
      print("  + Creating conversion", str(index) + "/" + str(len(sale_csv)))
      context.conversions_seeds.create_row_from_sale(c, insertion_id, date, bldg_class_at_sale, bldg_class_after_sale, building)

def evaluate_building_conversions(c):
  c.execute('SELECT * FROM conversions')