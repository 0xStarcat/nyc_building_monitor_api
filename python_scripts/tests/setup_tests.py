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

def new_conn():
  conn = sqlite3.connect(test_db, timeout=10)
  return conn

def setup_db():
  drop_db()
  print("  ****** Setting up test DB ******")
  conn = new_conn()
  c = conn.cursor()
  c.execute('pragma foreign_keys=on;')
  c.execute('pragma recursive_triggers=on')

  try:
    test_context.context.boroughs_seeds.create_table(c)
    test_context.context.neighborhoods_seeds.create_table(c)
    test_context.context.census_tracts_seeds.create_table(c)
    test_context.context.buildings_seeds.create_table(c)
    test_context.context.building_events_seeds.create_table(c)
    test_context.context.violations_seeds.create_table(c)
    test_context.context.service_calls_seeds.create_table(c)
    test_context.context.updates_seeds.create_table(c)
    conn.commit()
    conn.close()
  except Exception as error:
    print("Failure to create test tables ")
    print(error)
    conn.close()
    return

def drop_db():
  print('  * dropping test db')
  conn = new_conn()
  c = conn.cursor()
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=test_context.context.building_events_seeds.table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=test_context.context.service_calls_seeds.table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=test_context.context.violations_seeds.table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=test_context.context.buildings_seeds.table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=test_context.context.buildings_seeds.virtual_table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=test_context.context.racial_makeup_seeds.table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=test_context.context.rents_seeds.table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=test_context.context.incomes_seeds.table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=test_context.context.census_tracts_seeds.table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=test_context.context.neighborhoods_seeds.table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=test_context.context.boroughs_seeds.table))
  c.execute('DROP TABLE IF EXISTS {tn}'.format(tn=test_context.context.updates_seeds.table))

  conn.commit()
  conn.close()


