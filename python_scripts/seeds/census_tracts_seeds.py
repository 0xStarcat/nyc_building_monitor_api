import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..')) 

from helpers import boundary_helpers
import json
from seeds import neighborhoods_seeds
from seeds import community_districts_seeds
from seeds import boroughs_seeds

census_tracts_table = 'census_tracts'
ct_col1 = 'borough_id'
ct_col2 = 'community_district_id'
ct_col3 = 'neighborhood_id'
ct_col4 = 'name'
ct_col5 = 'CTLabel'
ct_col6 = 'boro_code'
ct_col7 = 'geometry'
ct_col8 = 'total_buildings'
ct_col9 = 'total_violations'
ct_col10 = 'total_sales'
ct_col11 = 'total_permits'
ct_col12 = 'total_service_calls'
ct_col13 = 'total_service_calls_with_violation_result'
ct_col14 = 'total_service_calls_with_no_action_result'
ct_col15 = 'total_service_calls_unable_to_investigate_result'
ct_col16 = 'total_service_calls_open_over_month'
ct_col17 = 'representative_point'
ct_col18 = 'service_calls_average_days_to_resolve'

def create_census_tracts_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table1}(id), {col2} INTEGER NOT NULL REFERENCES {ref_table2}(id), {col3} INTEGER NOT NULL REFERENCES {ref_table3}(id), {col4} TEXT, {col5} TEXT, {col6} INT, {col7} TEXT, {col8} INT, {col9} INT, {col10} INT, {col11} INT, {col12} INT, {col13} INT, {col14} INT, {col15} INT, {col16} INT, {col17} TEXT, {col18}, INT)'\
    .format(tn=census_tracts_table, ref_table1=boroughs_seeds.boroughs_table, ref_table2=community_districts_seeds.community_districts_table, ref_table3=neighborhoods_seeds.neighborhoods_table, col1=ct_col1, col2=ct_col2, col3=ct_col3, col4=ct_col4, col5=ct_col5, col6=ct_col6, col7=ct_col7, col8=ct_col8, col9=ct_col9, col10=ct_col10, col11=ct_col11, col12=ct_col12, col13=ct_col13, col14=ct_col14, col15=ct_col15, col16=ct_col16, col17=ct_col17, col18=ct_col18))

def seed_census_tracts(c, census_tract_json):
  print("** Seeding Census Tracts...")
  

  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table1}(id), {col2} INTEGER NOT NULL REFERENCES {ref_table2}(id), {col3} INTEGER NOT NULL REFERENCES {ref_table3}(id), {col4} TEXT, {col5} TEXT, {col6} INT, {col7} TEXT, {col8} INT, {col9} INT, {col10} INT, {col11} INT, {col12} INT, {col13} INT, {col14} INT, {col15} INT, {col16} INT, {col17} TEXT, {col18}, INT)'\
    .format(tn=census_tracts_table, ref_table1=boroughs_seeds.boroughs_table, ref_table2=community_districts_seeds.community_districts_table, ref_table3=neighborhoods_seeds.neighborhoods_table, col1=ct_col1, col2=ct_col2, col3=ct_col3, col4=ct_col4, col5=ct_col5, col6=ct_col6, col7=ct_col7, col8=ct_col8, col9=ct_col9, col10=ct_col10, col11=ct_col11, col12=ct_col12, col13=ct_col13, col14=ct_col14, col15=ct_col15, col16=ct_col16, col17=ct_col17, col18=ct_col18))

  c.execute('CREATE INDEX idx_ct_neighborhood_id ON {tn}({col3})'.format(tn=census_tracts_table, col3=ct_col3))
  c.execute('CREATE INDEX idx_ct_community_district_id ON {tn}({col2})'.format(tn=census_tracts_table, col2=ct_col2))
  c.execute('CREATE INDEX idx_ct_borough_id ON {tn}({col1})'.format(tn=census_tracts_table, col1=ct_col1))
  c.execute('CREATE INDEX idx_ct_boro_code ON {tn}({col6})'.format(tn=census_tracts_table, col6=ct_col6))

  c.execute('SELECT * FROM {tn}'.format(tn=neighborhoods_seeds.neighborhoods_table))
  neighborhoods = c.fetchall()

  for index, ct in enumerate(census_tract_json["features"]):
    print("CT: " + str(index) + "/" + str(len(census_tract_json["features"])))
    
    name = ct["properties"]["CT2010"]
    boro_code = int(ct["properties"]["BoroCode"])

    if "manual_neighborhood" in ct["properties"]:
      c.execute('SELECT * FROM neighborhoods WHERE name=\'{name}\''.format(name=ct["properties"]["manual_neighborhood"]))
      neighborhood = c.fetchone()
    else:
      neighborhood = boundary_helpers.get_record_from_coordinates(ct["geometry"], neighborhoods, 4)
    
    if not neighborhood:
      print("  * -- no neighborhood found", boro_code, name)
      continue

    boro_id = neighborhood[1]
    cd_id = neighborhood[2]
    n_id = neighborhood[0]
    ct_label = ct["properties"]["CTLabel"]
    geometry = json.dumps(ct["geometry"], separators=(',', ':'))
    representative_point = json.dumps(boundary_helpers.get_representative_point_geojson(ct["geometry"]))

    c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col17}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'\
      .format(tn=census_tracts_table, col1=ct_col1, col2=ct_col2, col3=ct_col3, col4=ct_col4, col5=ct_col5, col6=ct_col6, col7=ct_col7, col17=ct_col17), (boro_id, cd_id, n_id, name, ct_label, boro_code, geometry, representative_point))

  c.execute('SELECT * FROM {tn}'.format(tn=census_tracts_table))
  all_rows = c.fetchall()
  # for row in all_rows:
  #   print(row[1])
  print(len(all_rows), " seeded")
