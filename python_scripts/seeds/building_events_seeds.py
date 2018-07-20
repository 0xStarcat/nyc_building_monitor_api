from seeds import buildings_seeds
from seeds import census_tracts_seeds
from seeds import neighborhoods_seeds
from seeds import community_districts_seeds
from seeds import boroughs_seeds

table = 'building_events'
event_col1 = 'borough_id'
event_col2 = 'community_district_id'
event_col3 = 'neighborhood_id'
event_col4 = 'census_tract_id'
event_col5 = 'building_id'
event_col6 = 'eventable'
event_col7 = 'eventable_id'
event_col8 = 'event_date'

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table1}(id), {col2} INTEGER NOT NULL REFERENCES {ref_table2}(id), {col3} INTEGER NOT NULL REFERENCES {ref_table3}(id), {col4} INTEGER NOT NULL REFERENCES {ref_table4}(id), {col5} INTEGER NOT NULL REFERENCES {ref_table5}(id), {col6} TEXT NOT NULL, {col7} INTEGER NOT NULL, {col8} TEXT, UNIQUE({col6}, {col7}))'\
    .format(tn=table, col1=event_col1, col2=event_col2, col3=event_col3, col4=event_col4, col5=event_col5, col6=event_col6, col7=event_col7, col8=event_col8, ref_table1=boroughs_seeds.table,  ref_table2=community_districts_seeds.table, ref_table3=neighborhoods_seeds.table, ref_table4=census_tracts_seeds.table, ref_table5=buildings_seeds.table))

  c.execute('CREATE INDEX idx_borough_building_events ON {tn}({col1})'.format(tn=table, col1=event_col1))
  c.execute('CREATE INDEX idx_community_district_building_events ON {tn}({col2})'.format(tn=table, col2=event_col2))
  c.execute('CREATE INDEX idx_neighborhood_building_events ON {tn}({col3})'.format(tn=table, col3=event_col3))
  c.execute('CREATE INDEX idx_census_tract_building_events ON {tn}({col4})'.format(tn=table, col4=event_col4))
  c.execute('CREATE INDEX idx_building_building_events ON {tn}({col5})'.format(tn=table, col5=event_col5))

  
  c.execute('CREATE INDEX idx_building_eventables ON building_events(eventable)')
  c.execute('CREATE INDEX idx_building_ct_eventables ON building_events(census_tract_id, eventable)')
  c.execute('CREATE INDEX idx_building_n_eventables ON building_events(neighborhood_id, eventable)')
  c.execute('CREATE INDEX idx_building_b_eventables ON building_events(borough_id, eventable)')
