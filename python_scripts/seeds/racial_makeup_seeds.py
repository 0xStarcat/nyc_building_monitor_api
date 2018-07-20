from seeds import boroughs_seeds
from seeds import community_districts_seeds
from seeds import census_tracts_seeds
from seeds import neighborhoods_seeds

table = 'racial_makeups'

def find_foreign_keys(c, race):

  c.execute('SELECT * FROM {tn} WHERE {cn1}={boro_code} and {cn2}=\'{ct_number}\''\
      .format(tn=census_tracts_seeds.table, cn1="boro_code", cn2="name", boro_code=int(race[2]), ct_number=str(race[3]).zfill(6)))

  result = c.fetchone()
  if result:
    return {
      "census_tract_id": result[0],
      "neighborhood_id": result[3],
      "cd_id": result[2],
      "boro_id": result[1]
      }
  else:
    print(str(str(race[2]) + str(race[3]).zfill(6)))
    return None

def seed_racial_makeups(c, racial_makeup_csv):
  print("Seeding racial_makeups...")
  race_col1 = 'borough_id'
  race_col2 = 'community_district_id'
  race_col3 = 'neighborhood_id'
  race_col4 = 'census_tract_id'
  race_col5 = 'percent_white_2010'


  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table1}(id), {col2} INTEGER NOT NULL REFERENCES {ref_table2}(id), {col3} INTEGER NOT NULL REFERENCES {ref_table3}(id), {col4} INTEGER NOT NULL REFERENCES {ref_table4}(id), {col5} REAL)'\
    .format(tn=table, col1=race_col1, col2=race_col2, col3=race_col3, col4=race_col4, col5=race_col5,ref_table1=boroughs_seeds.table, ref_table2=community_districts_seeds.table, ref_table3=neighborhoods_seeds.table, ref_table4=census_tracts_seeds.table))

  for index, row in enumerate(racial_makeup_csv):
    print("racial_makeup: " + str(index) + "/" + str(len(racial_makeup_csv)))

    foreign_keys = find_foreign_keys(c, row)
    if foreign_keys == None:
      print("  - No tract match found")
      continue

    boro_id = foreign_keys["boro_id"]
    cd_id = foreign_keys["cd_id"]
    ct_id = foreign_keys["census_tract_id"]
    n_id = foreign_keys["neighborhood_id"]

    if not float(row[4]) and not float(row[5]):
      print("  - no race data")
      continue

    percent_white_2010 = round((float(row[5]) / float(row[4])) * 100, 2)


    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}) VALUES (?, ?, ?, ?, ?)'\
      .format(tn=table, col1=race_col1, col2=race_col2, col3=race_col3, col4=race_col4, col5=race_col5), (boro_id, cd_id, n_id, ct_id,percent_white_2010))


