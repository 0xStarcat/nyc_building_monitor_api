import math
import context

table = 'incomes'
col1 = 'borough_id'
col2 = 'neighborhood_id'
col3 = 'census_tract_id'
col4 = 'median_income_2011'
col5 = 'median_income_2017'
col6 = 'median_income_change_2011_2017'

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table1}(id), {col2} INTEGER NOT NULL REFERENCES {ref_table2}(id), {col3} INTEGER NOT NULL REFERENCES {ref_table3}(id))'\
    .format(tn=table, col1=col1, col2=col2, col3=col3, ref_table1=context.boroughs_seeds.table, ref_table2=context.neighborhoods_seeds.table, ref_table3=context.census_tracts_seeds.table))
  
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} REAL".format(tn=table, cn=col4))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} REAL".format(tn=table, cn=col5))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} REAL".format(tn=table, cn=col6))

  c.execute('CREATE UNIQUE INDEX idx_income_ct ON {tn}({col})'.format(tn=table, col=col3))

def find_tract_and_neighborhood_match(c, income):
  if income[2][:5] == "36061":
    # Manhattan
    borough_code = 1
  elif income[2][:5] == "36005":
    # Bronx
    borough_code = 2
  elif income[2][:5] == "36047":
    # Brooklyn
    borough_code = 3
  elif income[2][:5] == "36081":
    # Queens
    borough_code = 4
  elif income[2][:5] == "36085":
    # Staten Island
    borough_code = 5
  else:
    print(income[2])
    borough_code = ""

  c.execute('SELECT * FROM {tn} WHERE {cn1}={boro_code} and {cn2}=\'{ct_number}\''\
    .format(tn=context.census_tracts_seeds.table, cn1="boro_code", cn2="name", boro_code=borough_code, ct_number=str(income[2][5:])))
  
  result = c.fetchone()
  if result:
    return {
      "census_tract_id": result[0],
      "neighborhood_id": result[2],
      "boro_id": result[1]
    }
  else:
    return None

def seed(c, income_csv):
  print("Seeding incomes")

  for index, row in enumerate(income_csv):
    print("income: " + str(index) + "/" + str(len(income_csv)))
    foreign_keys = find_tract_and_neighborhood_match(c, row)
    if foreign_keys == None:
      print("  - No tract match found")
      continue

    boro_id = foreign_keys["boro_id"]
    ct_id = foreign_keys["census_tract_id"]
    n_id = foreign_keys["neighborhood_id"]

    if not row[3] and not row[4]:
      print("  - no income data")
      continue

    if not row[3]:
      mi_2011 = 0
    else:
      mi_2011 = round(float(row[3]), 2)\

    if not row[4]:
      mi_2017 = 0
    else:
      mi_2017 = round(float(row[4]), 2)

    if not row[3] or not row[4]:
      change_2011_2017 = 0
    else:
     change_2011_2017 = round(mi_2017 - mi_2011, 2)

    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}) VALUES (?, ?, ?, ?, ?, ?)'\
      .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6), (boro_id, n_id, ct_id, mi_2011, mi_2017, change_2011_2017))
