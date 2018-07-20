import json
from .. import context

table = 'census_tracts'
col1 = 'borough_id'
col2 = 'neighborhood_id'
col3 = 'name'
col4 = 'CTLabel'
col5 = 'boro_code'
col6 = 'geometry'
col7 = 'representative_point'
col8 = 'total_buildings'
col9 = 'total_residential_buildings'
col10 = 'total_violations'
col11 = 'total_sales'
col12 = 'total_permits'
col13 = 'total_service_calls'
col14 = 'total_service_calls_open_over_month'
col15 = 'service_calls_average_days_to_resolve'

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT)'.format(tn=table))

  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INTEGER NOT NULL REFERENCES {ref_table}(id)".format(cn=col1, ref_table=context.boroughs_seeds.table))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INTEGER NOT NULL REFERENCES {ref_table}(id)".format(cn=col2, ref_table=context.neighborhoods_seeds.table))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(cn=col3))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(cn=col4))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(cn=col5))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(cn=col6))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(cn=col7))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(cn=col8))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(cn=co9))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(cn=col10))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(cn=col11))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(cn=col12))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(cn=col13))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(cn=col14))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(cn=col15))

  c.execute('CREATE INDEX idx_ct_neighborhood_id ON {tn}({col})'.format(tn=table, col=col3))
  c.execute('CREATE INDEX idx_ct_borough_id ON {tn}({col})'.format(tn=table, col=col1))
  c.execute('CREATE INDEX idx_ct_boro_code ON {tn}({col})'.format(tn=table, col=col6))
  c.execute('CREATE UNIQUE INDEX idx_ct_boro_code_and_name ON {tn}({col1}, {col2})'.format(tn=table, col1=col5, col2=col3))
  c.execute('CREATE UNIQUE INDEX idx_ct_boro_code_and_ctlabel ON {tn}({col1}, {col2})'.format(tn=table, col1=col5, col2=col4))

def seed_census_tracts(c, census_tract_json):
  print("** Seeding Census Tracts...")

  c.execute('SELECT * FROM {tn}'.format(tn=context.neighborhoods_seeds.table))
  neighborhoods = c.fetchall()

  for index, ct in enumerate(census_tract_json["features"]):
    print("CT: " + str(index) + "/" + str(len(census_tract_json["features"])))
    
    if "manual_neighborhood" in ct["properties"]:
      c.execute('SELECT * FROM neighborhoods WHERE name=\'{name}\''.format(name=ct["properties"]["manual_neighborhood"]))
      neighborhood = c.fetchone()
    else:
      neighborhood = context.boundary_helpers.get_record_from_coordinates(ct["geometry"], neighborhoods, 3)
    
    if not neighborhood:
      print("  X -- no neighborhood found", boro_code, name)
      continue

    name = ct["properties"]["CT2010"]
    boro_code = int(ct["properties"]["BoroCode"])
    boro_id = neighborhood[1]
    n_id = neighborhood[0]
    ct_label = ct["properties"]["CTLabel"]
    geometry = json.dumps(ct["geometry"], separators=(',', ':'))
    representative_point = json.dumps(context.boundary_helpers.get_representative_point_geojson(ct["geometry"]))

    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}) VALUES (?, ?, ?, ?, ?, ?, ?)'\
      .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6, col7=col7), (boro_id, n_id, name, ct_label, boro_code, geometry, representative_point))