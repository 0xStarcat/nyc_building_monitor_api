import json
import context

table = 'neighborhoods'
col1 = 'borough_id'
col2 = 'name'
col3 = 'geometry'
col4 = 'representative_point'
col5 = 'total_buildings'
col6 = 'total_residential_buildings'
col7 = 'total_violations'
col8 = 'total_sales'
col9 = 'total_permits'
col10 = 'total_service_calls'
col11 = 'total_service_calls_open_over_month'
col12 = 'service_calls_average_days_to_resolve'

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table}(id))'.format(tn=table, col1=col1, ref_table=context.boroughs_seeds.table))

  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col2))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col3))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col4))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col5))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col6))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col7))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col8))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col9))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col10))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col11))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col12))

  c.execute('CREATE INDEX idx_n_borough_id ON {tn}({col1})'.format(tn=table, col1=col1))
  c.execute('CREATE UNIQUE INDEX idx_n_name ON {tn}({col2})'.format(tn=table, col2=col2))

def seed_neighborhoods(c, neighborhood_json):
  print("** Seeding Neighborhoods...")

  c.execute('SELECT id, geometry FROM {tn}'.format(tn=context.boroughs_seeds.table))
  boroughs = c.fetchall()

  for index, neighborhood in enumerate(neighborhood_json["features"]):
    print("Neighborhood: " + str(index) + "/" + str(len(neighborhood_json["features"])))
    
    borough = context.boundary_helpers.get_record_from_coordinates(neighborhood["geometry"], boroughs, 1)
    if not borough:
      print("  X -- no borough found", name)
      continue

    boro_id = borough[0]
    name = neighborhood["properties"]["neighborhood"]
    geo = json.dumps(neighborhood["geometry"], separators=(',',':'))
    representative_point = json.dumps(context.boundary_helpers.get_representative_point_geojson(neighborhood["geometry"]))

    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}) VALUES (?, ?, ?, ?)'
      .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4), (boro_id, name, geo, representative_point))

