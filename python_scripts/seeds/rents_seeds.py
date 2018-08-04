import context

table = 'rents'
col1 = 'borough_id'
col2 = 'neighborhood_id'
col3 = 'census_tract_id'
col4 = 'median_rent_2011'
col5 = 'median_rent_2017'
col6 = 'median_rent_change_2011_2017'

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table1}(id), {col2} INTEGER NOT NULL REFERENCES {ref_table2}(id), {col3} INTEGER NOT NULL REFERENCES {ref_table3}(id))'\
    .format(tn=table, col1=col1, col2=col2, col3=col3, ref_table1=context.boroughs_seeds.table, ref_table2=context.neighborhoods_seeds.table, ref_table3=context.census_tracts_seeds.table))
  
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} REAL".format(tn=table, cn=col4))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} REAL".format(tn=table, cn=col5))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} REAL".format(tn=table, cn=col6))

  c.execute('CREATE UNIQUE INDEX idx_rent_ct ON {tn}({col})'.format(tn=table, col=col3))

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
    .format(tn=context.census_tracts_seeds.table, cn1="boro_code", cn2="name", boro_code=borough_code, ct_number=str(rent[2][5:])))
  
  result = c.fetchone()
  if result:
    return {
      "census_tract_id": result[0],
      "neighborhood_id": result[2],
      "boro_id": result[1]
      }
  else:
    return None

def seed(c, rent_csv):
  print("Seeding rents")

  for index, row in enumerate(rent_csv):
    print("rent: " + str(index) + "/" + str(len(rent_csv)))
    
    foreign_keys = find_foreign_keys(c, row)
    if foreign_keys == None:
      print("  - No tract match found")
      continue

    boro_id = foreign_keys["boro_id"]
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

    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}) VALUES (?, ?, ?, ?, ?, ?)'\
      .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6), (boro_id, n_id, ct_id, mr_2011, mr_2017, change_2011_2017))


