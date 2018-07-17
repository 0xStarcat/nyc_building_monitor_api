import json
from seeds import boroughs_seeds
from seeds import buildings_seeds
from seeds import building_events_seeds
from helpers import csv_helpers


from shapely.geometry import Point, mapping
import datetime

permit_clusters_table = 'permit_clusters'
permit_cluster_col1 = 'geometry'
permit_cluster_col2 = 'borough_id'
permit_cluster_col3 = 'house_number'
permit_cluster_col4 = 'street_name'

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} TEXT, {col2} INTEGER REFERENCES {borough_table}(id), {col3} TEXT, {col4} TEXT)'\
    .format(tn=permit_clusters_table, col1=permit_cluster_col1, col2=permit_cluster_col2, col3=permit_cluster_col3, col4=permit_cluster_col4, borough_table=boroughs_seeds.boroughs_table))

  c.execute('CREATE INDEX idx_permit_cluster_borough_id ON {tn}({col2})'.format(tn=permit_clusters_table, col2=permit_cluster_col2))
  c.execute('CREATE INDEX idx_permit_cluster_street_name_and_house_number ON {tn}({col4}, {col3})'.format(tn=permit_clusters_table, col3=permit_cluster_col3, col4=permit_cluster_col4))

def seed_cluster_from_permit(c, permit, geometry, borough_id):
  print("Seeding a permit cluster...")
  house_number = permit["house__"]
  street_name = permit["street_name"]

  c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}) VALUES (?, ?, ?, ?)'\
      .format(tn=permit_clusters_table, col1=permit_cluster_col1, col2=permit_cluster_col2, col3=permit_cluster_col3, col4=permit_cluster_col4), (geometry, borough_id, str(house_number), str(street_name)))