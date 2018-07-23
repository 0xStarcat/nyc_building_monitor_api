import json
from shapely.geometry import Point, mapping
import datetime

import context

table = 'permit_clusters'
col1 = 'borough_id'
col2 = 'neighborhood_id'
col3 = 'census_tract_id'
col4 = 'geometry'
col5 = 'house_number'
col6 = 'street_name'

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER REFERENCES {ref_table1}(id), {col2} INTEGER REFERENCES {ref_table2}(id), {col3} INTEGER REFERENCES {ref_table3}(id))'\
    .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6,  ref_table1=context.boroughs_seeds.table, ref_table2=context.neighborhoods_seeds.table, ref_table3=context.census_tracts_seeds.table))

  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col4))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col5))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col6))

  c.execute('CREATE INDEX idx_permit_cluster_borough_id ON {tn}({col})'.format(tn=table, col=col1))
  c.execute('CREATE INDEX idx_permit_cluster_neighborhood_id ON {tn}({col})'.format(tn=table, col=col2))
  c.execute('CREATE INDEX idx_permit_cluster_census_tract_id ON {tn}({col})'.format(tn=table, col=col3))
  c.execute('CREATE INDEX idx_permit_cluster_house_and_street ON {tn}({col1}, {col2})'.format(tn=table, col1=col5, col2=col6))

def seed_cluster_from_permit(c, permit, geometry, fkeys):
  print("Seeding a permit cluster...")
  house_number = str(permit["house__"])
  street_name = str(permit["street_name"])

  c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}) VALUES (?, ?, ?, ?, ?, ?)'\
    .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, col6=col6), (fkeys["borough_id"], fkeys["neighborhood_id"], fkeys["census_tract_id"], geometry, house_number, street_name))

  return c.lastrowid