import json
from shapely.geometry import shape
import context

table = 'buildings'
virtual_table = 'building_search'

col1 = 'borough_id'
col2 = 'neighborhood_id'
col3 = 'census_tract_id'
col4 = 'boro_code'
col5 = 'CT2010'
col6 = 'bbl'
col7 = 'block'
col8 = 'lot'
col9 = 'address'
col10 = 'geometry'
col11 = 'representative_point'
col12 = 'year_built'
col13 = 'residential_units'
col14 = 'bldg_class'
col15 = 'residential'
col16 = 'total_violations'
col17 = 'total_sales'
col18 = 'total_service_calls'
col19 = 'total_service_calls_open_over_month'
col20 = 'service_calls_average_days_to_resolve'


def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table1}(id), {col2} INTEGER NOT NULL REFERENCES {ref_table2}(id), {col3} INTEGER NOT NULL REFERENCES {ref_table3}(id))'
            .format(tn=table, col1=col1, col2=col2, col3=col3, ref_table1=context.boroughs_seeds.table, ref_table2=context.neighborhoods_seeds.table, ref_table3=context.census_tracts_seeds.table))

  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col4))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col5))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col6))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col7))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col8))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col9))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col10))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col11))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col12))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col13))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col14))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} BOOLEAN".format(tn=table, cn=col15))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col16))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col17))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col18))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col19))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col20))

  c.execute('CREATE INDEX idx_bldg_block_and_lot ON {tn}({col1}, {col2})'.format(tn=table, col1=col7, col2=col8))
  c.execute('CREATE INDEX idx_bldg_census_tract_id ON {tn}({col})'.format(tn=table, col=col3))
  c.execute('CREATE INDEX idx_bldg_neighborhood_id ON {tn}({col})'.format(tn=table, col=col2))
  c.execute('CREATE INDEX idx_bldg_borough_id ON {tn}({col})'.format(tn=table, col=col1))
  c.execute('CREATE INDEX idx_bldg_class ON {tn}({col})'.format(tn=table, col=col14))

  c.execute('CREATE INDEX idx_bldg_borough_and_residential ON {tn}({col1}, {col2})'.format(
      tn=table, col1=col1, col2=col15))
  c.execute('CREATE INDEX idx_bldg_neighborhood_and_residential ON {tn}({col1}, {col2})'.format(
      tn=table, col1=col2, col2=col15))
  c.execute('CREATE INDEX idx_bldg_census_tract_and_residential ON {tn}({col1}, {col2})'.format(
      tn=table, col1=col3, col2=col15))

  c.execute('CREATE UNIQUE INDEX idx_bldg_boroid_and_address ON {tn}({col1}, {col2})'.format(
      tn=table, col1=col4, col2=col9))
  c.execute('CREATE UNIQUE INDEX idx_bldg_bbl ON {tn}({col})'.format(tn=table, col=col6))


def seed_virtual_table(c):
  c.execute("SELECT * FROM {tn}".format(tn=table))
  buildings = c.fetchall()

  for (index, building) in enumerate(buildings):
    if index % 1000 == 0:
      print("seeding building: " + str(index) + '/' + str(len(buildings)))

    c.execute('SELECT * FROM boroughs WHERE id={b_id}'.format(b_id=building[1]))
    b_name = c.fetchone()[1]
    split = building[9].strip().split(" ")
    house_number = split[0]

    # If no numbers are found in the house number, don't insert
    if any(char.isdigit() for char in house_number) == False:
      continue
    del split[0]
    street = " ".join(split)
    c.execute('INSERT INTO building_search (id, house_number, address, borough_name) VALUES (?, ?, ?, ?)',
              (building[0], str(house_number), str(street), b_name))


def convert_building_polygon_to_point(geometry):
  return shape(geometry).representative_point()


def find_foreign_keys(c, building):
  # TODO - see if geo matching or data matching produces better results.
  if building["properties"]["CT2010"]:
    c.execute('SELECT * FROM census_tracts WHERE {cn1}={boro_code} and {cn2}={ct_name}'.format(
        cn1="boro_code", boro_code=building["properties"]["BoroCode"], cn2="CTLabel", ct_name=building["properties"]["CT2010"]))
    ct = c.fetchone()
  else:
    c.execute('SELECT id, borough_id, neighborhood_id, geometry FROM census_tracts')
    census_tracts_data = c.fetchall()
    ct = next((tract for tract in census_tracts_data if shape(json.loads(tract[3])).contains(
        convert_building_polygon_to_point(building["geometry"]))), None)

  if not ct:
    return None
  else:
    return {
        "borough_id": ct[1],
        "neighborhood_id": ct[2],
        "census_tract_id": ct[0]
    }


def seed(c, building_json):
  print("Seeding Buildings...")

  for index, building in enumerate(building_json["features"]):
    if index % 1000 == 0:
      print("Building: " + str(index) + "/" + str(len(building_json["features"])))

    try:
      representative_point = json.dumps(context.boundary_helpers.get_representative_point_geojson(building["geometry"]))
    except:
      print("  X No Geo")
      continue

    if "BBL" not in building["properties"] or "Block" not in building["properties"] or "Lot" not in building["properties"] or "Address" not in building["properties"]:
      print("  * Missing geo information", str(index) + "/" + str(len(building_json["features"])))
      continue

    foreign_keys = find_foreign_keys(c, building)
    if foreign_keys == None:
      print("  * no CT", building["properties"]["Address"], str(index) + "/" + str(len(building_json["features"])))
      continue

    borough_id = int(foreign_keys["borough_id"])
    neighborhood_id = int(foreign_keys["neighborhood_id"])
    census_tract_id = int(foreign_keys["census_tract_id"])
    boro_code = int(building["properties"]["BoroCode"])
    ct_2010 = str(building["properties"]["CT2010"])
    bbl = int(building["properties"]["BBL"])
    block = str(building["properties"]["Block"])
    lot = str(building["properties"]["Lot"])
    address = str(building["properties"]["Address"])
    geometry = json.dumps(building["geometry"], separators=(',', ':'))
    year_built = int(building["properties"]["YearBuilt"])
    bldg_class = str(building["properties"]["BldgClass"])
    residential_units = int(building["properties"]["UnitsRes"])

    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}, {col9}, {col10}, {col11}, {col12}, {col13}, {col14}, {col15}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
              .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6, col7=col7, col8=col8, col9=col9, col10=col10, col11=col11, col12=col12, col13=col13, col14=col14, col15=col15), (borough_id, neighborhood_id, census_tract_id, boro_code, ct_2010, bbl, block, lot, address, geometry, representative_point, year_built, residential_units, bldg_class, residential_units > 0))


def add_counts_to_boundary_data(c):
  # Census Tracts
  c.execute('SELECT id FROM census_tracts')
  data = c.fetchall()
  print("Counting buildings for census tracts")

  for row in data:
    c.execute('SELECT COUNT(*) FROM buildings WHERE census_tract_id={id}'
              .format(id=row[0]))

    buildings_count = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM buildings WHERE census_tract_id={id} AND residential = 1'
              .format(id=row[0]))

    residential_buildings_count = c.fetchone()[0]

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'
              .format(tn=context.census_tracts_seeds.table, cn="total_residential_buildings", value=residential_buildings_count, id=row[0]))

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'
              .format(tn=context.census_tracts_seeds.table, cn="total_buildings", value=buildings_count, id=row[0]))

  # Neighborhoods
  c.execute('SELECT id FROM neighborhoods')
  data = c.fetchall()
  print("Counting buildings for neighborhoods")

  for row in data:
    c.execute('SELECT COUNT(*) FROM buildings WHERE neighborhood_id={id}'
              .format(id=row[0]))

    buildings_count = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM buildings WHERE neighborhood_id={id} AND residential = 1'
              .format(id=row[0]))

    residential_buildings_count = c.fetchone()[0]

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'
              .format(tn=context.neighborhoods_seeds.table, cn="total_residential_buildings", value=residential_buildings_count, id=row[0]))

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'
              .format(tn=context.neighborhoods_seeds.table, cn="total_buildings", value=buildings_count, id=row[0]))

  # Boroughs
  c.execute('SELECT id FROM boroughs')
  data = c.fetchall()
  print("Counting buildings for boroughs")

  for row in data:
    c.execute('SELECT COUNT(*) FROM buildings WHERE borough_id={id}'
              .format(id=row[0]))

    buildings_count = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM buildings WHERE borough_id={id} AND residential = 1'
              .format(id=row[0]))

    residential_buildings_count = c.fetchone()[0]

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'
              .format(tn=context.boroughs_seeds.table, cn="total_residential_buildings", value=residential_buildings_count, id=row[0]))

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'
              .format(tn=context.boroughs_seeds.table, cn="total_buildings", value=buildings_count, id=row[0]))
