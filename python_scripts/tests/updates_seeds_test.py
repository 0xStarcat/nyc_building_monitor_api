import datetime
import test_context
import setup_tests

def seed_db():
  setup_tests.setup_db()

def test_insertions():

  try:
    seed_db()
    conn = setup_tests.new_conn()
    c = conn.cursor()
    insert_record_test(c)
    conn.close()
  except Exception as error:
    print(error)
    conn.close()
    raise error

def insert_record_test(c):
  new_entry_counts = { "new_service_calls": 100, "new_violations": 200 }
  status_update_counts = { "resolved_service_calls" : 300, "resolved_violations": 400 }
  date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
  update_data = { "date": date,**new_entry_counts, **status_update_counts}
  test_context.context.updates_seeds.new_entry(c, update_data)

  try: 
    c.execute('SELECT date FROM {tn}'.format(tn=test_context.context.updates_seeds.table))
    entry = c.fetchone()
    assert entry[0] == date
    
    c.execute('SELECT new_service_calls FROM {tn}'.format(tn=test_context.context.updates_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 100

    c.execute('SELECT new_violations FROM {tn}'.format(tn=test_context.context.updates_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 200

    c.execute('SELECT resolved_service_calls FROM {tn}'.format(tn=test_context.context.updates_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 300

    c.execute('SELECT resolved_violations FROM {tn}'.format(tn=test_context.context.updates_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 400

  except AssertionError as error:
    raise error