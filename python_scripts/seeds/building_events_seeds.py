import context

table = 'building_events'
col1 = 'borough_id'
col2 = 'neighborhood_id'
col3 = 'census_tract_id'
col4 = 'building_id'
col5 = 'eventable'
col6 = 'eventable_id'
col7 = 'event_date'

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table1}(id), {col2} INTEGER NOT NULL REFERENCES {ref_table2}(id), {col3} INTEGER NOT NULL REFERENCES {ref_table3}(id), {col4} INTEGER NOT NULL REFERENCES {ref_table4}(id))'\
    .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, ref_table1=context.boroughs_seeds.table, ref_table2=context.neighborhoods_seeds.table, ref_table3=context.census_tracts_seeds.table, ref_table4=context.buildings_seeds.table))

  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col5))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col6))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col7))

  c.execute('CREATE INDEX idx_borough_building_events ON {tn}({col})'.format(tn=table, col=col1))
  c.execute('CREATE INDEX idx_neighborhood_building_events ON {tn}({col})'.format(tn=table, col=col2))
  c.execute('CREATE INDEX idx_census_tract_building_events ON {tn}({col})'.format(tn=table, col=col3))
  c.execute('CREATE INDEX idx_building_building_events ON {tn}({col})'.format(tn=table, col=col4))

  
  c.execute('CREATE INDEX idx_building_eventables ON {tn}({col})'.format(tn=table, col=col5))
  c.execute('CREATE INDEX idx_building_ct_eventables ON {tn}({col1}, {col2})'.format(tn=table, col1=col3, col2=col5))
  c.execute('CREATE INDEX idx_building_n_eventables ON {tn}({col1}, {col2})'.format(tn=table, col1=col2, col2=col5))
  c.execute('CREATE INDEX idx_building_b_eventables ON {tn}({col1}, {col2})'.format(tn=table, col1=col1, col2=col5))
