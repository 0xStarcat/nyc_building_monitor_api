import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..')) 

import json
from seeds import boroughs_seeds
from helpers import boundary_helpers

community_districts_table = 'community_districts'

def seed_community_districts(c, community_district_json):
  print("** Seeding community districts...")
  cd_col1 = 'borough_id'
  cd_col2 = 'name'
  cd_col3 = 'geometry'
  cd_col4 = 'total_buildings'
  cd_col5 = 'total_violations'
  cd_col6 = 'total_sales'
  cd_col7 = 'total_permits'
  cd_col8 = 'total_service_calls'
  cd_col9 = 'total_service_calls_with_violation_result'
  cd_col10 = 'total_service_calls_with_no_action_result'
  cd_col11 = 'total_service_calls_unable_to_investigate_result'
  cd_col12 = 'total_service_calls_open_over_month'
  cd_col13 = 'representative_point'
  cd_col14 = 'service_calls_average_days_to_resolve'

  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table}(id), {col2} TEXT, {col3} TEXT, {col4} INT, {col5} INT, {col6} INT, {col7} INT, {col8} INT, {col9} INT, {col10} INT, {col11} INT, {col12} INT, {col13} TEXT, {col14} INTEGER, UNIQUE({col2}))'\
    .format(tn=community_districts_table, col1=cd_col1, col2=cd_col2, col3=cd_col3, col4=cd_col4, col5=cd_col5, col6=cd_col6, col7=cd_col7, col8=cd_col8, col9=cd_col9, col10=cd_col10, col11=cd_col11, col12=cd_col12, col13=cd_col13, col14=cd_col14, ref_table=boroughs_seeds.boroughs_table))

  for index, community_district in enumerate(community_district_json["features"]):
    print("Sub-Borough: " + str(index) + "/" + str(len(community_district_json["features"])))
    
    name = community_district["properties"]["BoroCD"]
    
    c.execute('SELECT * FROM boroughs WHERE code={code}'.format(code=int(str(name)[:1])))
    boro_id = c.fetchone()[0]
    if not boro_id:
      print("  * -- no borough found", name)
      continue

    geo = json.dumps(community_district["geometry"], separators=(',',':'))
    representative_point = json.dumps(boundary_helpers.get_representative_point_geojson(community_district["geometry"]))

    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col13}) VALUES (?, ?, ?, ?)'\
      .format(tn=community_districts_table, col1=cd_col1, col2=cd_col2, col3=cd_col3, col13=cd_col13), (boro_id, name, geo, representative_point))

