import math
from seeds import boroughs_seeds
from seeds import community_districts_seeds
from seeds import census_tracts_seeds
from seeds import neighborhoods_seeds

rents_table = 'rents'

def find_foreign_keys(c, rent):
  
  if rent[2][:5] == "36061":
    # Manhattan
    borough_code = 1
  elif rent[2][:5] == "36005":
    # Bronx
    borough_code = 2
  elif rent[2][:5] == "36047":
    # Brooklyn
    borough_code = 3
  elif rent[2][:5] == "36081":
    # Queens
    borough_code = 4
  elif rent[2][:5] == "36085":
    # Staten Island
    borough_code = 5

  c.execute('SELECT * FROM {tn} WHERE {cn1}={boro_code} and {cn2}=\'{ct_number}\''\
      .format(tn=census_tracts_seeds.census_tracts_table, cn1="boro_code", cn2="name", boro_code=borough_code, ct_number=str(rent[2][5:])))
  
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

def seed_rents(c, rent_csv):
  print("Seeding rents")
  rent_col1 = 'borough_id'
  rent_col2 = 'community_district_id'
  rent_col3 = 'neighborhood_id'
  rent_col4 = 'census_tract_id'
  rent_col5 = 'median_rent_2011'
  rent_col6 = 'median_rent_2017'
  rent_col7 = 'median_rent_change_2011_2017'

  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table1}(id), {col2} INTEGER NOT NULL REFERENCES {ref_table2}(id), {col3} INTEGER NOT NULL REFERENCES {ref_table3}(id), {col4} INTEGER NOT NULL REFERENCES {ref_table4}(id), {col5} REAL, {col6} REAL, {col7} REAL)'\
    .format(tn=rents_table, col1=rent_col1, col2=rent_col2, col3=rent_col3, col4=rent_col4, col5=rent_col5, col6=rent_col6, col7=rent_col7,ref_table1=boroughs_seeds.boroughs_table, ref_table2=community_districts_seeds.community_districts_table, ref_table3=neighborhoods_seeds.neighborhoods_table, ref_table4=census_tracts_seeds.census_tracts_table))

  for index, row in enumerate(rent_csv):
    print("rent: " + str(index) + "/" + str(len(rent_csv)))
    
    foreign_keys = find_foreign_keys(c, row)
    if foreign_keys == None:
      print("  - No tract match found")
      continue

    boro_id = foreign_keys["boro_id"]
    cd_id = foreign_keys["cd_id"]
    ct_id = foreign_keys["census_tract_id"]
    n_id = foreign_keys["neighborhood_id"]

    if not row[3] and not row[4]:
      print("  - no rent data")
      continue

    if not row[3]:
      mr_2011 = 0
    else:
      mr_2011 = round(float(row[3]), 2)\

    if not row[4]:
      mr_2017 = 0
    else:
      mr_2017 = round(float(row[4]), 2)

    if not row[3] or not row[4]:
      change_2011_2017 = 0
    else:
     change_2011_2017 = round(mr_2017 - mr_2011, 2)

    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}) VALUES (?, ?, ?, ?, ?, ?, ?)'\
      .format(tn=rents_table, col1=rent_col1, col2=rent_col2, col3=rent_col3, col4=rent_col4, col5=rent_col5, col6=rent_col6, col7=rent_col7), (boro_id, cd_id, n_id, ct_id, mr_2011, mr_2017, change_2011_2017))


