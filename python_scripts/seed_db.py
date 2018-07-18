import sqlite3
import json

from seeds import boroughs_seeds
from seeds import community_districts_seeds
from seeds import neighborhoods_seeds
from seeds import census_tracts_seeds
from seeds import buildings_seeds
from seeds import incomes_seeds
from seeds import rents_seeds
from seeds import racial_makeup_seeds
from seeds import violations_seeds
from seeds import sales_seeds
from seeds import permits_seeds
from seeds import permit_clusters_seeds

from seeds import service_calls_seeds
from seeds import building_events_seeds

from helpers import csv_helpers
import config
sqlite_file = config.DATABASE_URL

def drop_buildings_data_tables(c):
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=building_events_seeds.building_events_table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=service_calls_seeds.service_calls_table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=permits_seeds.permits_table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=permit_clusters_seeds.permit_clusters_table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=sales_seeds.sales_table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=violations_seeds.violations_table))

def drop_buildings_table(c):
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=buildings_seeds.buildings_table))

def drop_boundary_tables(c):
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=racial_makeup_seeds.racial_makeup_table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=rents_seeds.rents_table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=incomes_seeds.incomes_table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=census_tracts_seeds.census_tracts_table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=neighborhoods_seeds.neighborhoods_table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=community_districts_seeds.community_districts_table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=boroughs_seeds.boroughs_table))

def clear_csvs():
  csv_helpers.clear_csv(config.VIOLATIONS_CSV_URL)
  csv_helpers.clear_csv(config.PERMITS_CSV_URL)
  csv_helpers.clear_csv(config.SERVICE_CALLS_CSV_URL)

def create_buildings_data_tables(c):
  sales_seeds.create_table(c)
  permit_clusters_seeds.create_table(c)
  permits_seeds.create_table(c)
  service_calls_seeds.create_table(c)
  violations_seeds.create_table(c)
  building_events_seeds.create_table(c)

def seed_buildings_data(c):
  sales_csv = list(csv.reader(open("data/sales_data/csv/nyc_sales_2010-2017.csv")))[1:]
  sales_seeds.seed_sales(c, sales_csv)

def seed_buildings(c, conn):
  buildings_seeds.create_table(c)

  mn_building_json = json.load(open('data/buildings_data/mn_mappluto.geojson'))
  buildings_seeds.seed_buildings(c, mn_building_json)
  conn.commit()

  bx_building_json = json.load(open('data/buildings_data/bx_mappluto.geojson'))
  buildings_seeds.seed_buildings(c, bx_building_json)
  conn.commit()

  bk_building_json = json.load(open('data/buildings_data/bk_mappluto.geojson'))
  buildings_seeds.seed_buildings(c, bk_building_json)
  conn.commit()

  qn_building_json = json.load(open('data/buildings_data/qn_mappluto.geojson'))
  buildings_seeds.seed_buildings(c, qn_building_json)
  conn.commit()

  si_building_json = json.load(open('data/buildings_data/si_mappluto.geojson'))
  buildings_seeds.seed_buildings(c, si_building_json)
  conn.commit()

  # adds total_buildings number to boundary data tables
  buildings_seeds.add_counts_to_boundary_data(c)
  conn.commit()

def seed_boundary_tables(c, conn):
  borough_json = json.load(open('data/boundary_data/boroughs.geojson'))
  community_district_json = json.load(open('data/boundary_data/community_districts.geojson'))
  neighborhood_json = json.load(open('data/boundary_data/neighborhoods.geojson'))
  census_tract_json = json.load(open('data/boundary_data/census_tracts_2010.geojson'))
  incomes_csv = list(csv.reader(open("data/income_data/censustract-medianhouseholdincome2017.csv")))[1:]
  rents_csv = list(csv.reader(open("data/rent_data/censustract-medianrentall2017.csv")))[1:]
  racial_makeup_csv = list(csv.reader(open("data/race_data/nyc_race_2010_by_census_tract.csv")))[1:]
  
  boroughs_seeds.seed_boroughs(c, borough_json)
  conn.commit()
  community_districts_seeds.seed_community_districts(c, community_district_json)
  conn.commit()
  neighborhoods_seeds.seed_neighborhoods(c, neighborhood_json)
  conn.commit()
  census_tracts_seeds.seed_census_tracts(c, census_tract_json)
  conn.commit()
  incomes_seeds.seed_incomes(c, incomes_csv)
  conn.commit()
  rents_seeds.seed_rents(c, rents_csv)
  conn.commit()
  racial_makeup_seeds.seed_racial_makeups(c, racial_makeup_csv)
  conn.commit()

def drop():

  conn = sqlite3.connect(sqlite_file, timeout=10)
  c = conn.cursor()
  c.execute('pragma foreign_keys=on;')

  clear_csvs()
  drop_buildings_data_tables(c)
  drop_buildings_table(c)
  drop_boundary_tables(c)
  conn.commit()
  conn.close()

def seed():
  conn = sqlite3.connect(sqlite_file, timeout=10)
  c = conn.cursor()
  c.execute('pragma foreign_keys=on;')
  c.execute('pragma recursive_triggers=on')

  seed_boundary_tables(c, conn)
  seed_buildings(c, conn)
  create_buildings_data_tables(c)
  seed_buildings_data(c)  
  conn.commit()
  conn.close()

def test():
  conn = sqlite3.connect(sqlite_file, timeout=10)
  c = conn.cursor()
  
  c.execute('pragma foreign_keys=on;')
  c.execute('SELECT * FROM {tn} WHERE {cn1}=\'{source}\' order by date desc'.format(tn='violations', cn1="source", source='HPD'))
  # c.execute('SELECT * FROM permits')
  all_rows = c.fetchall()
  print(all_rows[0])

  # c.execute('SELECT * FROM violations')
  # all_rows = c.fetchall()
  # print(len(all_rows))

  # c.execute('SELECT * FROM permits')
  # all_rows = c.fetchall()
  # print(len(all_rows))

  # c.execute('SELECT * FROM service_calls')
  # all_rows = c.fetchall()
  # print(len(all_rows))

  # c.execute('SELECT * FROM sales')
  # all_rows = c.fetchall()
  # print(len(all_rows))
  # print(all_rows[len(all_rows) - 1])
  # for row in all_rows:
    # print(row[1])
  conn.commit()
  conn.close()