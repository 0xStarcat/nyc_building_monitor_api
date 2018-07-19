import json
from seeds import buildings_seeds
from seeds import building_events_seeds

table = 'conversions'

col1 = 'building_id'
col2 = 'date'
col3 = 'source'
col4 = 'converted_from'
col5 = 'converted_to'


def create_table(c):
	c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col1} INTEGER NOT NULL REFERENCES {ref_table1}(id), {col2} TEXT, {col3} TEXT, {col4} TEXT, {col5} TEXT)'\
    .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, ref_table1=buildings_seeds.buildings_table))

def create_row_from_sale(c, sale, building):
  # Create Conversion
  building_id = building[0]
  date = sale

  c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}) VALUES ({building_id}, \'{date}\', \"{source}\", \'{converted_from}\', \'{converted_to}\')'\
    .format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5, building_id=building_id, date=date, source=source, converted_from=converted_from, converted_to=converted_to))

  insertion_id = c.lastrowid

  # Create Building Event
  c.execute('INSERT OR IGNORE INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7}, {col8}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'\
    .format(tn=building_events_seeds.building_events_table, col1="borough_id", col2="community_district_id", col3="neighborhood_id", col4="census_tract_id", col5="building_id", col6="eventable", col7="eventable_id", col8="event_date"), (building[1], building[2], building[3], building[4], building[0], 'conversion', insertion_id, date))