import context

table = 'racial_makeups'
col1 = 'borough_id'
col2 = 'neighborhood_id'
col3 = 'census_tract_id'
col4 = 'percent_white_2010'

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table1}(id), {col2} INTEGER NOT NULL REFERENCES {ref_table2}(id), {col3} INTEGER NOT NULL REFERENCES {ref_table3}(id))'\
    .format(tn=table, col1=col1, col2=col2, col3=col3, ref_table1=context.boroughs_seeds.table, ref_table2=context.neighborhoods_seeds.table, ref_table3=context.census_tracts_seeds.table))
  
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} REAL".format(tn=table, cn=col4))

  c.execute('CREATE UNIQUE INDEX idx_racial_makeup_ct ON {tn}({col})'.format(tn=table, col=col3))

def find_foreign_keys(c, race):

  c.execute('SELECT * FROM {tn} WHERE {cn1}={boro_code} and {cn2}=\'{ct_number}\''\
    .format(tn=context.census_tracts_seeds.table, cn1="boro_code", cn2="name", boro_code=int(race[2]), ct_number=str(race[3]).zfill(6)))

  result = c.fetchone()
  if result:
    return {
      "census_tract_id": result[0],
      "neighborhood_id": result[2],
      "boro_id": result[1]
      }
  else:
    print(str(str(race[2]) + str(race[3]).zfill(6)))
    return None

def seed(c, racial_makeup_csv):
  print("Seeding racial_makeups...")
  

  for index, row in enumerate(racial_makeup_csv):
    print("racial_makeup: " + str(index) + "/" + str(len(racial_makeup_csv)))

    foreign_keys = find_foreign_keys(c, row)
    if foreign_keys == None:
      print("  - No tract match found")
      continue

    boro_id = foreign_keys["boro_id"]
    ct_id = foreign_keys["census_tract_id"]
    n_id = foreign_keys["neighborhood_id"]

    if not float(row[4]) and not float(row[5]):
      print("  - no race data")
      continue

    percent_white_2010 = round((float(row[5]) / float(row[4])) * 100, 2)

    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}) VALUES (?, ?, ?, ?)'\
      .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4), (boro_id, n_id, ct_id, percent_white_2010))


