import json
from helpers import boundary_helpers

table = 'boroughs'
col1 = 'name'
col2 = 'code' 
col3 = 'geometry'
col4 = 'total_buildings'
col5 = 'total_violations'
col6 = 'total_sales'
col7 = 'total_permits'
col8 = 'total_service_calls'
col9 = 'total_service_calls_with_violation_result'
col10 = 'total_service_calls_with_no_action_result'
col11 = 'total_service_calls_unable_to_investigate_result'
col12 = 'total_service_calls_open_over_month'
col13 = 'representative_point'
col14 = 'service_calls_average_days_to_resolve'
col15 = 'total_residential_buildings'
col16 = 'total_conversions'
col17 = 'total_conversions_to_non_residential'
col18 = 'total_evictions'

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} TEXT, {col2} INTEGER, {col3} TEXT, {col4} INT, {col5} INT, {col6} INT, {col7} INT, {col8} INT, {col9} INT, {col10} INT, {col11} INT, {col12} INT, {col13} TEXT, {col14} INTEGER, {col15} INTEGER, {col16} INTEGER, {col17} INTEGER, {col18} INTEGER, UNIQUE({col1}), UNIQUE({col2}))'\
    .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6, col7=col7, col8=col8, col9=col9, col10=col10, col11=col11, col12=col12, col13=col13, col14=col14, col15=col15, col16=col16, col17=col17, col18=col18))

def seed_boroughs(c, borough_json):
  print("** Seeding Boroughs...")

  for index, borough in enumerate(borough_json["features"]):
    print("Borough: " + str(index) + "/" + str(len(borough_json["features"])))
    name = borough["properties"]["BoroName"]
    code = borough["properties"]["BoroCode"]
    geo = json.dumps(borough["geometry"], separators=(',',':'))
    representative_point = json.dumps(boundary_helpers.get_representative_point_geojson(borough["geometry"]))

    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col13}) VALUES (?, ?, ?, ?)'\
      .format(tn=table, col1=col1, col2=col2, col3=col3, col13=col13), (name, code, geo, representative_point))
