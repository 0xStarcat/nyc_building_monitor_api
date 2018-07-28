import test_context
import setup_tests
import factories

def seed_db():
  setup_tests.setup_db()
  factories.seed_test_db_with_open_service_calls()

def test_service_calls_status_request_on_open_records():
  seed_db()
  conn = setup_tests.new_conn()
  c = conn.cursor()
  c.execute('pragma foreign_keys=on;')
  c.execute('pragma recursive_triggers=on')

  try:
    with_closed_api_record(c)
    with_open_api_record(c)
  except Exception as error:
    print(error)
    setup_tests.drop_db()
    raise error

def with_closed_api_record(c):
  api_json = {"address_type":"ADDRESS","agency":"DOB","agency_name":"Department of Buildings","bbl":"5056280024","borough":"BROOKLYN","city":"BROOKLYN","closed_date":"2018-07-18T08:53:55.000","community_board":"05 BROOKLYN","complaint_type":"Building/Use","created_date":"2018-05-18T08:53:55.000","descriptor":"Illegal Conversion Of Residential Building/Space","facility_type":"N/A","incident_address":"fake","incident_zip":"11207","latitude":"40","location":{"type":"Point","coordinates":[-73.890480139432,40]},"longitude":"-73.89048013943226","open_data_channel_type":"UNKNOWN","park_borough":"BROOKLYN","park_facility_name":"Unspecified","resolution_action_updated_date":"2018-07-18T00:00:00.000","resolution_description":"The Department of Buildings investigated this complaint and closed it. If the problem still exists, please call 311 and file a new complaint. If you are outside of New York City, please call (212) NEW-YORK (212-639-9675).","status":"Closed","street_name":"fake","unique_key":"1234","x_coordinate_state_plane":"1014629","y_coordinate_state_plane":"1"}
  unique_id = api_json["unique_key"]

  try:
    test_context.context.service_calls_status_request.update_service_call_row(c, api_json)

    c.execute('SELECT unique_id FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.service_calls_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == '1234'

    c.execute('SELECT status FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.service_calls_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'closed'

    c.execute('SELECT resolution_description FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.service_calls_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'The Department of Buildings investigated this complaint and closed it. If the problem still exists, please call 311 and file a new complaint. If you are outside of New York City, please call (212) NEW-YORK (212-639-9675).'

    c.execute('SELECT resolution_violation FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.service_calls_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'False'

    c.execute('SELECT resolution_no_action FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.service_calls_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'True'

    c.execute('SELECT unable_to_investigate FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.service_calls_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'False'

    c.execute('SELECT open_over_month FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.service_calls_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'True'

    c.execute('SELECT closed_date FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.service_calls_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == '20180718'

    c.execute('SELECT days_to_close FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.service_calls_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 61
  except AssertionError as error:
    raise error

def with_open_api_record(c):
  api_json = {"address_type":"ADDRESS","agency":"DOB","agency_name":"Department of Buildings","bbl":"5056280024","borough":"BROOKLYN","city":"BROOKLYN","closed_date":"2018-07-18T08:53:55.000","community_board":"05 BROOKLYN","complaint_type":"Building/Use","created_date":"2018-05-18T08:53:55.000","descriptor":"Illegal Conversion Of Residential Building/Space","facility_type":"N/A","incident_address":"fake","incident_zip":"11207","latitude":"40","location":{"type":"Point","coordinates":[-73.890480139432,40]},"longitude":"-73.89048013943226","open_data_channel_type":"UNKNOWN","park_borough":"BROOKLYN","park_facility_name":"Unspecified","resolution_action_updated_date":"2018-07-18T00:00:00.000","resolution_description":"Still open...","status":"Open","street_name":"fake","unique_key":"1234","x_coordinate_state_plane":"1014629","y_coordinate_state_plane":"1"}
  unique_id = api_json["unique_key"]

  try:
    test_context.context.service_calls_status_request.update_service_call_row(c, api_json)

    c.execute('SELECT unique_id FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.service_calls_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == '1234'

    c.execute('SELECT status FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.service_calls_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'open'

    c.execute('SELECT resolution_description FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.service_calls_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'Still open...'

    c.execute('SELECT resolution_violation FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.service_calls_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'False'

    c.execute('SELECT resolution_no_action FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.service_calls_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'False'

    c.execute('SELECT unable_to_investigate FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.service_calls_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'False'

    c.execute('SELECT open_over_month FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.service_calls_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'True'

    c.execute('SELECT closed_date FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.service_calls_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'None'

    c.execute('SELECT days_to_close FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.service_calls_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'None'
  except AssertionError as error:
    raise error

