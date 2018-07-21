import sqlite3
import config
import test_context

test_db = config.TEST_DB_URL

def setup_db():
  open(test_db, 'a').close()
  conn = sqlite3.connect(test_db, timeout=10)
  c = conn.cursor()
  c.execute('pragma foreign_keys=on;')

  try:
    test_context.context.boroughs_seeds.create_table(c)
    test_context.context.neighborhoods_seeds.create_table(c)
    test_context.context.census_tracts_seeds.create_table(c)
    test_context.context.buildings_seeds.create_table(c)
    test_context.context.building_events_seeds.create_table(c)
    test_context.context.violations_seeds.create_table(c)
  except:
    conn.commit()
    return