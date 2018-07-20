import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..')) 

import json
from seeds import boroughs_seeds
from helpers import boundary_helpers

table = 'community_districts'
col1 = 'borough_id'
col2 = 'name'
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
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table}(id), {col2} TEXT, {col3} TEXT, {col4} INT, {col5} INT, {col6} INT, {col7} INT, {col8} INT, {col9} INT, {col10} INT, {col11} INT, {col12} INT, {col13} TEXT, {col14} INTEGER, {col15} INTEGER, {col16} INTEGER, {col17} INTEGER, {col18} INTEGER, UNIQUE({col2}))'\
    .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6, col7=col7, col8=col8, col9=col9, col10=col10, col11=col11, col12=col12, col13=col13, col14=col14, col15=col15, col16=col16, col17=col17, col18=col18, ref_table=boroughs_seeds.table))
  
  c.execute('CREATE INDEX idx_cd_borough_id ON {tn}({col1})'.format(tn=table, col1=col1))

def seed_community_districts(c, community_district_json):
  print("** Seeding community districts...")

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
      .format(tn=table, col1=col1, col2=col2, col3=col3, col13=col13), (boro_id, name, geo, representative_point))

