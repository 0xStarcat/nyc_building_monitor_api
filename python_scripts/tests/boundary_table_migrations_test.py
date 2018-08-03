import json
import test_context
import setup_tests
import factories
  
def seed_db():
  setup_tests.setup_db()
  factories.seed_test_db_with_buildings_violations_calls()

def test_insertions():

  try:
    seed_db()
    conn = setup_tests.new_conn()
    c = conn.cursor()
    table = "census_tracts"
    update_data_census_tracts(c, table)
    conn.close()

  except Exception as error:
    conn.close()
    print(error)
    raise error


def update_data_census_tracts(c, table):
  
  test_context.context.boundary_table_migrations.update_data(c, table)

  try: 
    c.execute('SELECT total_violations FROM {tn}'.format(tn=table))
    entry = c.fetchone()
    assert entry[0] == 3

    c.execute('SELECT total_service_calls FROM {tn}'.format(tn=table))
    entry = c.fetchone()
    assert entry[0] == 3

    c.execute('SELECT total_service_calls_open_over_month FROM {tn}'.format(tn=table))
    entry = c.fetchone()
    assert entry[0] == 1

    c.execute('SELECT service_calls_average_days_to_resolve FROM {tn}'.format(tn=table))
    entry = c.fetchone()
    assert entry[0] == 35.5

    c.execute('SELECT total_sales FROM {tn}'.format(tn=table))
    entry = c.fetchone()
    assert entry[0] == None

    c.execute('SELECT total_permits FROM {tn}'.format(tn=table))
    entry = c.fetchone()
    assert entry[0] == None

  except AssertionError as error:
    raise error


