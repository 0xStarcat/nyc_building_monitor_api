import json
from seeds import boroughs_seeds
from seeds import community_districts_seeds
from seeds import neighborhoods_seeds
from seeds import census_tracts_seeds

from shapely.geometry import shape, Point

buildings_table = 'buildings'
bldg_col1 = 'borough_id'
bldg_col2 = 'community_district_id'
bldg_col3 = 'neighborhood_id'
bldg_col4 = 'census_tract_id'
bldg_col5 = 'boro_code'
bldg_col6 = 'CT2010'
bldg_col7 = 'block'
bldg_col8 = 'lot'
bldg_col9 = 'address'
bldg_col10 = 'geometry'
bldg_col11 = 'year_built'
bldg_col12 = 'residential_units'
bldg_col13 = 'total_violations'
bldg_col14 = 'total_sales'
bldg_col15 = 'total_service_calls'
bldg_col16 = 'total_service_calls_with_violation_result'
bldg_col17 = 'total_service_calls_with_no_action_result'
bldg_col18 = 'total_service_calls_unable_to_investigate_result'
bldg_col19 = 'total_service_calls_open_over_month'

def convert_building_polygon_to_point(geometry):
  polygon = shape(geometry)
  return polygon.representative_point()

def find_foreign_keys(c, building):
  # TODO - see if geo matching or data matching produces better results.
  if building["properties"]["CT2010"]: 
    c.execute('SELECT * FROM census_tracts WHERE {cn1}={boro_code} and {cn2}={ct_name}'.format(cn1="boro_code", boro_code=building["properties"]["BoroCode"], cn2="CTLabel", ct_name=building["properties"]["CT2010"].zfill(6)))
    ct = c.fetchone()
  else:
    return None

  # match = next((tract for tract in census_tracts_data if shape(json.loads(tract[7])).contains(convert_building_polygon_to_point(building["geometry"]))), False) 
  if ct:
    return {
      "borough_id": ct[1],
      "community_district_id": ct[2],
      "neighborhood_id": ct[3],
      "census_tract_id": ct[0]
    }
  else:
    return None

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table1}(id), {col2} INTEGER NOT NULL REFERENCES {ref_table2}(id), {col3} INTEGER NOT NULL REFERENCES {ref_table3}(id), {col4} INTEGER NOT NULL REFERENCES {ref_table4}(id), {col5} INT, {col6} TEXT, {col7} TEXT, {col8} TEXT, {col9} TEXT, {col10} TEXT, {col11} INTEGER, {col12} INTEGER, {col13} INTEGER, {col14} INTEGER, {col15} INTEGER, {col16} INTEGER, {col17} INTEGER, {col18} INTEGER, {col19} INTEGER)'\
    .format(tn=buildings_table, col1=bldg_col1, col2=bldg_col2, col3=bldg_col3, col4=bldg_col4, col5=bldg_col5, col6=bldg_col6, col7=bldg_col7, col8=bldg_col8, col9=bldg_col9, col10=bldg_col10, col11=bldg_col11, col12=bldg_col12, col13=bldg_col13, col14=bldg_col14, col15=bldg_col15, col16=bldg_col16, col17=bldg_col17, col18=bldg_col18, col19=bldg_col19, ref_table1=boroughs_seeds.boroughs_table, ref_table2=community_districts_seeds.community_districts_table, ref_table3=neighborhoods_seeds.neighborhoods_table, ref_table4=census_tracts_seeds.census_tracts_table))

  c.execute('CREATE INDEX idx_bldg_block_and_lot ON {tn}({col7}, {col8})'.format(tn=buildings_table, col7=bldg_col7, col8=bldg_col8))
  c.execute('CREATE INDEX idx_bldg_address ON {tn}({col9})'.format(tn=buildings_table, col9=bldg_col9))
  c.execute('CREATE INDEX idx_bldg_census_tract_id ON {tn}({col4})'.format(tn=buildings_table, col4=bldg_col4))
  c.execute('CREATE INDEX idx_bldg_neighborhood_id ON {tn}({col3})'.format(tn=buildings_table, col3=bldg_col3))
  c.execute('CREATE INDEX idx_bldg_community_district_id ON {tn}({col2})'.format(tn=buildings_table, col2=bldg_col2))
  c.execute('CREATE INDEX idx_bldg_borough_id ON {tn}({col1})'.format(tn=buildings_table, col1=bldg_col1))

def seed_buildings(c, building_json):
  print("Seeding Buildings...")
  
  for index, building in enumerate(building_json["features"]):
    print("Building: " + str(index) + "/" + str(len(building_json["features"])))
    
    residential_units = building["properties"]["UnitsRes"]

    if (int(residential_units) == 0):
      print("  * no residential units")
      continue
    if "Block" not in building["properties"] or "Lot" not in building["properties"] or "Address" not in building["properties"]:
      print("  * Missing Block, Lot, or Address")
      continue

    foreign_keys = find_foreign_keys(c, building)
    if foreign_keys == None:
      print("  * no CT matches found")
      continue

    borough_id = foreign_keys["borough_id"]
    community_district_id = foreign_keys["community_district_id"]
    neighborhood_id = foreign_keys["neighborhood_id"]
    census_tract_id = foreign_keys["census_tract_id"]

    boro_code = int(building["properties"]["BoroCode"])
    ct_2010 = building["properties"]["CT2010"]
    block = building["properties"]["Block"]
    lot = building["properties"]["Lot"]
    address = building["properties"]["Address"]
    geometry = json.dumps(building["geometry"], separators=(',',':'))
    year_built = building["properties"]["YearBuilt"]
    
    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}, {col9}, {col10}, {col11}, {col12}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'\
      .format(tn=buildings_table, col1=bldg_col1, col2=bldg_col2, col3=bldg_col3, col4=bldg_col4, col5=bldg_col5, col6=bldg_col6, col7=bldg_col7, col8=bldg_col8, col9=bldg_col9, col10=bldg_col10, col11=bldg_col11, col12=bldg_col12), (borough_id, community_district_id, neighborhood_id, census_tract_id, boro_code, ct_2010, block, lot, address, geometry, year_built, residential_units))

def add_counts_to_boundary_data(c):
  # Census Tracts
  c.execute('SELECT * FROM census_tracts')
  data = c.fetchall()
  print("Counting buildings for census tracts")

  for row in data:
    c.execute('SELECT * FROM buildings WHERE census_tract_id={id}'\
      .format(id=row[0]))

    buildings_count = len(c.fetchall())

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
      .format(tn=census_tracts_seeds.census_tracts_table, cn="total_buildings", value=buildings_count, id=row[0]))

  # Neighborhoods
  c.execute('SELECT * FROM neighborhoods')
  data = c.fetchall()
  print("Counting buildings for neighborhoods")

  for row in data:
    c.execute('SELECT * FROM buildings WHERE neighborhood_id={id}'\
      .format(id=row[0]))

    buildings_count = len(c.fetchall())

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
      .format(tn=neighborhoods_seeds.neighborhoods_table, cn="total_buildings", value=buildings_count, id=row[0]))

  # Community Districts
  c.execute('SELECT * FROM community_districts')
  data = c.fetchall()
  print("Counting buildings for community districts")

  for row in data:
    c.execute('SELECT * FROM buildings WHERE community_district_id={id}'\
      .format(id=row[0]))

    buildings_count = len(c.fetchall())

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
      .format(tn=community_districts_seeds.community_districts_table, cn="total_buildings", value=buildings_count, id=row[0]))

  # Boroughs
  c.execute('SELECT * FROM boroughs')
  data = c.fetchall()
  print("Counting buildings for boroughs")

  for row in data:
    c.execute('SELECT * FROM buildings WHERE borough_id={id}'\
      .format(id=row[0]))

    buildings_count = len(c.fetchall())

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
      .format(tn=boroughs_seeds.boroughs_table, cn="total_buildings", value=buildings_count, id=row[0]))

  c.execute('SELECT * FROM buildings')
  all_rows = c.fetchall()
  print(all_rows[len(all_rows) - 1])
