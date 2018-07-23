import os
import sqlite3
import config
import test_context
test_db = config.TEST_DB_URL

def new_cursor():
  conn = sqlite3.connect(test_db, timeout=10)
  c = conn.cursor()
  c.execute('pragma foreign_keys=on;')
  c.execute('pragma recursive_triggers=on')
  return c

def setup_db():
  print("  ****** Setting up test DB ******")

  c = new_cursor()

  try:
    test_context.context.boroughs_seeds.create_table(c)
    test_context.context.neighborhoods_seeds.create_table(c)
    test_context.context.census_tracts_seeds.create_table(c)
    test_context.context.buildings_seeds.create_table(c)
    test_context.context.building_events_seeds.create_table(c)
    test_context.context.violations_seeds.create_table(c)
    test_context.context.service_calls_seeds.create_table(c)
  except Exception as error:
    print("Failure to create test tables ")
    print(error)
    drop_dB()
    return

def drop_db():
  print('  * dropping test db')
  open(test_db, 'w').close()