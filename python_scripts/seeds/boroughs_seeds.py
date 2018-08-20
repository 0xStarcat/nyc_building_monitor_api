import json
import context

table = 'boroughs'
col1 = 'name'
col2 = 'code'
col3 = 'geometry'
col4 = 'representative_point'
col5 = 'total_buildings'
col6 = 'total_violations'
col7 = 'total_residential_buildings'
col8 = 'total_sales'
col9 = 'total_permits'
col10 = 'total_service_calls'
col11 = 'total_service_calls_open_over_month'
col12 = 'service_calls_average_days_to_resolve'


def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT)'.format(tn=table))

  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col1))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col2))
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

  c.execute('CREATE UNIQUE INDEX idx_boro_name ON {tn}({col})'.format(tn=table, col=col1))
  c.execute('CREATE UNIQUE INDEX idx_boro_code ON {tn}({col})'.format(tn=table, col=col2))


def seed(c, borough_json):
  print("** Seeding Boroughs...")

  for index, borough in enumerate(borough_json["features"]):
    print("Borough: " + str(index) + "/" + str(len(borough_json["features"])))
    name = borough["properties"]["BoroName"]
    code = borough["properties"]["BoroCode"]
    geo = json.dumps(borough["geometry"], separators=(',', ':'))
    representative_point = json.dumps(context.boundary_helpers.get_representative_point_geojson(
        borough["geometry"]), separators=(',', ':'))

    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}) VALUES (?, ?, ?, ?)'
              .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4), (name, code, geo, representative_point))
