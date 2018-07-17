import json
from seeds import boroughs_seeds
from seeds import community_districts_seeds
from seeds import neighborhoods_seeds
from seeds import census_tracts_seeds

from seeds import building_events_seeds
from helpers import csv_helpers


from shapely.geometry import Point, mapping
import datetime

permit_clusters_table = 'permit_clusters'
permit_cluster_col1 = 'borough_id'
permit_cluster_col2 = 'community_district_id'
permit_cluster_col3 = 'neighborhood_id'
permit_cluster_col4 = 'census_tract_id'
permit_cluster_col5 = 'geometry'
permit_cluster_col6 = 'house_number'
permit_cluster_col7 = 'street_name'

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER REFERENCES {ref_table1}(id), {col2} INTEGER REFERENCES {ref_table2}(id), {col3} INTEGER REFERENCES {ref_table3}(id), {col4} INTEGER REFERENCES {ref_table4}(id), {col5} TEXT, {col6} TEXT, {col7} TEXT)'\
    .format(tn=permit_clusters_table, col1=permit_cluster_col1, col2=permit_cluster_col2, col3=permit_cluster_col3, col4=permit_cluster_col4, col5=permit_cluster_col5, col6=permit_cluster_col6, col7=permit_cluster_col7,  ref_table1=boroughs_seeds.boroughs_table, ref_table2=community_districts_seeds.community_districts_table, ref_table3=neighborhoods_seeds.neighborhoods_table, ref_table4=census_tracts_seeds.census_tracts_table))

  c.execute('CREATE INDEX idx_permit_cluster_borough_id ON {tn}({col1})'.format(tn=permit_clusters_table, col2=permit_cluster_col1))
  c.execute('CREATE INDEX idx_permit_cluster_community_distrct_id ON {tn}({col2})'.format(tn=permit_clusters_table, col2=permit_cluster_col2))
  c.execute('CREATE INDEX idx_permit_cluster_neighborhood_id ON {tn}({col3})'.format(tn=permit_clusters_table, col2=permit_cluster_col3))
  c.execute('CREATE INDEX idx_permit_cluster_census_tract_id ON {tn}({col4})'.format(tn=permit_clusters_table, col2=permit_cluster_col4))

  c.execute('CREATE INDEX idx_permit_cluster_street_name_and_house_number ON {tn}({col4}, {col3})'.format(tn=permit_clusters_table, col3=permit_cluster_col3, col4=permit_cluster_col4))

def seed_cluster_from_permit(c, permit, geometry, borough_id):
  print("Seeding a permit cluster...")
  house_number = permit["house__"]
  street_name = permit["street_name"]

  c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7},) VALUES (?, ?, ?, ?, ?, ?, ?)'\
      .format(tn=permit_clusters_table, col1=permit_cluster_col1, col2=permit_cluster_col2, col3=permit_cluster_col3, col4=permit_cluster_col4, col5=permit_cluster_col5, col6=permit_cluster_col6, col7=permit_cluster_col7), (permit[1], permit[2], permit[3], permit[4], str(geometry), str(house_number), str(street_name)))