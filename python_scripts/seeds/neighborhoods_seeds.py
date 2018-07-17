import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..')) 

import json
from seeds import boroughs_seeds
from seeds import community_districts_seeds
from helpers import boundary_helpers

neighborhoods_table = 'neighborhoods'

def seed_neighborhoods(c, neighborhood_json):
  print("** Seeding Neighborhoods...")
  neigh_col1 = 'borough_id'
  neigh_col2 = 'community_district_id'
  neigh_col3 = 'name'
  neigh_col4 = 'geometry'
  neigh_col5 = 'total_buildings'
  neigh_col6 = 'total_violations'
  neigh_col7 = 'total_sales'
  neigh_col8 = 'total_permits'
  neigh_col9 = 'total_service_calls'
  neigh_col10 = 'total_service_calls_with_violation_result'
  neigh_col11 = 'total_service_calls_with_no_action_result'
  neigh_col12 = 'total_service_calls_unable_to_investigate_result'
  neigh_col13 = 'total_service_calls_open_over_month'
  neigh_col14 = 'representative_point'


  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table}(id), {col2} INTEGER NOT NULL REFERENCES {ref_table2}(id), {col3} TEXT, {col4} TEXT, {col5} INT, {col6} INT, {col7} INT, {col8} INT, {col9} INT, {col10} INT, {col11} INT, {col12} INT, {col13} INT, {col14} TEXT, UNIQUE({col3}))'\
    .format(tn=neighborhoods_table, ref_table=boroughs_seeds.boroughs_table, ref_table2=community_districts_seeds.community_districts_table, col1=neigh_col1, col2=neigh_col2, col3=neigh_col3, col4=neigh_col4, col5=neigh_col5, col6=neigh_col6, col7=neigh_col7, col8=neigh_col8, col9=neigh_col9, col10=neigh_col10, col11=neigh_col11, col12=neigh_col12, col13=neigh_col13, col14=neigh_col14))

  c.execute('CREATE INDEX idx_n_community_district_id ON {tn}({col2})'.format(tn=neighborhoods_table, col2=neigh_col2))
  c.execute('CREATE INDEX idx_n_borough_id ON {tn}({col1})'.format(tn=neighborhoods_table, col1=neigh_col1))

  c.execute('SELECT * FROM {tn}'.format(tn=community_districts_seeds.community_districts_table))
  community_districts = c.fetchall()

  for index, neighborhood in enumerate(neighborhood_json["features"]):
    print("Neighborhood: " + str(index) + "/" + str(len(neighborhood_json["features"])))
    
    name = neighborhood["properties"]["neighborhood"]
    c_district = boundary_helpers.get_record_from_coordinates(neighborhood["geometry"], community_districts, 3)
    if not c_district:
      print("  * -- no community district found", name)
      continue

    cd_id = c_district[0]
    boro_id = c_district[1]

    geo = json.dumps(neighborhood["geometry"], separators=(',',':'))
    representative_point = json.dumps(boundary_helpers.get_representative_point_geojson(neighborhood["geometry"]))

    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col14}) VALUES (?, ?, ?, ?, ?)'
      .format(tn=neighborhoods_table, col1=neigh_col1, col2=neigh_col2, col3=neigh_col3, col4=neigh_col4, col14=neigh_col14), (boro_id, cd_id, name, geo, representative_point))

