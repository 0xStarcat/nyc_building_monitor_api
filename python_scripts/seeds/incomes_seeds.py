import math
from seeds import boroughs_seeds
from seeds import community_districts_seeds
from seeds import census_tracts_seeds
from seeds import neighborhoods_seeds

table = 'incomes'

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
      .format(tn=census_tracts_seeds.table, cn1="boro_code", cn2="name", boro_code=borough_code, ct_number=str(income[2][5:])))
  result = c.fetchone()
  if result:
    return {
      "census_tract_id": result[0],
      "neighborhood_id": result[3],
      "cd_id": result[2],
      "boro_id": result[1]
    }
  else:
    return None

def seed_incomes(c, income_csv):
  print("Seeding incomes")
  income_col1 = 'borough_id'
  income_col2 = 'community_district_id'
  income_col3 = 'neighborhood_id'
  income_col4 = 'census_tract_id'
  income_col5 = 'median_income_2011'
  income_col6 = 'median_income_2017'
  income_col7 = 'median_income_change_2011_2017'

  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table1}(id), {col2} INTEGER NOT NULL REFERENCES {ref_table2}(id), {col3} INTEGER NOT NULL REFERENCES {ref_table3}(id), {col4} INTEGER NOT NULL REFERENCES {ref_table4}(id), {col5} REAL, {col6} REAL, {col7} REAL)'\
    .format(tn=table, col1=income_col1, col2=income_col2, col3=income_col3, col4=income_col4, col5=income_col5, col6=income_col6, col7=income_col7,ref_table1=boroughs_seeds.table, ref_table2=community_districts_seeds.table, ref_table3=neighborhoods_seeds.table, ref_table4=census_tracts_seeds.table))

  for index, row in enumerate(income_csv):
    print("income: " + str(index) + "/" + str(len(income_csv)))
    foreign_keys = find_tract_and_neighborhood_match(c, row)
    if foreign_keys == None:
      print("  - No tract match found")
      continue

    boro_id = foreign_keys["boro_id"]
    cd_id = foreign_keys["cd_id"]
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

    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}) VALUES (?, ?, ?, ?, ?, ?, ?)'\
      .format(tn=table, col1=income_col1, col2=income_col2, col3=income_col3, col4=income_col4, col5=income_col5, col6=income_col6, col7=income_col7), (boro_id, cd_id, n_id, ct_id, mi_2011, mi_2017, change_2011_2017))
