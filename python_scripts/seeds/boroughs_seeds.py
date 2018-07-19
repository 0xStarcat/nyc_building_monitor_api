import json
from helpers import boundary_helpers

boroughs_table = 'boroughs'

def seed_boroughs(c, borough_json):
  print("** Seeding Boroughs...")
  boro_col1 = 'name'
  boro_col2 = 'code' 
  boro_col3 = 'geometry'
  boro_col4 = 'total_buildings'
  boro_col5 = 'total_violations'
  boro_col6 = 'total_sales'
  boro_col7 = 'total_permits'
  boro_col8 = 'total_service_calls'
  boro_col9 = 'total_service_calls_with_violation_result'
  boro_col10 = 'total_service_calls_with_no_action_result'
  boro_col11 = 'total_service_calls_unable_to_investigate_result'
  boro_col12 = 'total_service_calls_open_over_month'
  boro_col13 = 'representative_point'
  boro_col14 = 'service_calls_average_days_to_resolve'

  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} TEXT, {col2} INTEGER, {col3} TEXT, {col4} INT, {col5} INT, {col6} INT, {col7} INT, {col8} INT, {col9} INT, {col10} INT, {col11} INT, {col12} INT, {col13} TEXT, {col14} INTEGER, UNIQUE({col1}), UNIQUE({col2}))'\
    .format(tn=boroughs_table, col1=boro_col1, col2=boro_col2, col3=boro_col3, col4=boro_col4, col5=boro_col5, col6=boro_col6, col7=boro_col7, col8=boro_col8, col9=boro_col9, col10=boro_col10, col11=boro_col11, col12=boro_col12, col13=boro_col13, col14=boro_col14))

  for index, borough in enumerate(borough_json["features"]):
    print("Borough: " + str(index) + "/" + str(len(borough_json["features"])))
    name = borough["properties"]["BoroName"]
    code = borough["properties"]["BoroCode"]
    geo = json.dumps(borough["geometry"], separators=(',',':'))
    representative_point = json.dumps(boundary_helpers.get_representative_point_geojson(borough["geometry"]))

    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col13}) VALUES (?, ?, ?, ?)'\
      .format(tn=boroughs_table, col1=boro_col1, col2=boro_col2, col3=boro_col3, col13=boro_col13), (name, code, geo, representative_point))
