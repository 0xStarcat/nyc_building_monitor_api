import datetime
import test_context
import setup_tests
import factories

def seed_db():
  setup_tests.setup_db()
  factories.seed_test_db_with_building()

def test_insertions():

  try:
    seed_db()
    conn = setup_tests.new_conn()
    c = conn.cursor()
    insertion_of_record_dob(c)
    conn.close()

    seed_db()
    conn = setup_tests.new_conn()
    c = conn.cursor()
    insertion_of_record_hpd(c)
    conn.close()

    seed_db()
    conn = setup_tests.new_conn()
    c = conn.cursor()
    insertion_of_record_open(c)
    conn.close()
  except Exception as error:
    print(error)
    raise error

def insertion_of_record_dob(c):
  # A no action call that was closed

  service_call_json = [
    {"address_type":"ADDRESS","agency":"DOB","agency_name":"Department of Buildings","bbl":"5056280024","borough":"BROOKLYN","city":"BROOKLYN","closed_date":"2018-07-18T08:53:55.000","community_board":"05 BROOKLYN","complaint_type":"Building/Use","created_date":"2018-07-18T08:53:55.000","descriptor":"Illegal Conversion Of Residential Building/Space","facility_type":"N/A","incident_address":"fake","incident_zip":"11207","latitude":"40","location":{"type":"Point","coordinates":[-73.890480139432,40]},"longitude":"-73.89048013943226","open_data_channel_type":"UNKNOWN","park_borough":"BROOKLYN","park_facility_name":"Unspecified","resolution_action_updated_date":"2018-07-18T00:00:00.000","resolution_description":"The Department of Buildings investigated this complaint and closed it. If the problem still exists, please call 311 and file a new complaint. If you are outside of New York City, please call (212) NEW-YORK (212-639-9675).","status":"Closed","street_name":"fake","unique_key":"1234","x_coordinate_state_plane":"1014629","y_coordinate_state_plane":"1"}
  ]

  test_context.context.service_calls_seeds.seed(c, service_call_json)
  
  try: 
    c.execute('SELECT id FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entries = c.fetchall()
    assert len(entries) == 1
    
    c.execute('SELECT building_id FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 1

    c.execute('SELECT unique_id FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == '1234'

    c.execute('SELECT date FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == '20180718'

    c.execute('SELECT status FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'closed'

    c.execute('SELECT source FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'DOB'

    c.execute('SELECT description FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'Illegal Conversion Of Residential Building/Space'

    c.execute('SELECT resolution_description FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'The Department of Buildings investigated this complaint and closed it. If the problem still exists, please call 311 and file a new complaint. If you are outside of New York City, please call (212) NEW-YORK (212-639-9675).'

    c.execute('SELECT resolution_violation FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 0

    c.execute('SELECT resolution_no_action FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 1

    c.execute('SELECT unable_to_investigate FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 0

    c.execute('SELECT open_over_month FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 0

    c.execute('SELECT closed_date FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == '20180718'

    c.execute('SELECT days_to_close FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 0

    c.execute('SELECT complaint_type FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == "Building/Use"
  except AssertionError as error:
    raise error

def insertion_of_record_hpd(c):
  # An unable to investigate call has been closed.

  service_call_json = [
    {"address_type":"ADDRESS","agency":"HPD","agency_name":"Department of Housing Preservation and Development","bbl":"5056280024","borough":"BROOKLYN","city":"BROOKLYN","closed_date":"2015-08-20T10:20:40.000","community_board":"01 BROOKLYN","complaint_type":"GENERAL","created_date":"2015-06-10T18:39:08.000","descriptor":"BELL/BUZZER/INTERCOM","facility_type":"N/A","incident_address":"fake","incident_zip":"11206","latitude":"40","location":{"type":"Point","coordinates":[-73.94003123834,40]},"location_type":"RESIDENTIAL BUILDING","longitude":"-73.94003123833956","open_data_channel_type":"PHONE","park_borough":"BROOKLYN","park_facility_name":"Unspecified","resolution_action_updated_date":"2015-08-20T10:20:40.000","resolution_description":"The Department of Housing Preservation and Development was not able to gain access to inspect the following conditions. The complaint has been closed. If the condition still exists, please file a new complaint.","status":"Closed","street_name":"fake","unique_key":"1234","x_coordinate_state_plane":"1000876","y_coordinate_state_plane":"1"}
  ]

  test_context.context.service_calls_seeds.seed(c, service_call_json)
  
  try: 
    c.execute('SELECT id FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entries = c.fetchall()
    assert len(entries) == 1
    
    c.execute('SELECT building_id FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 1

    c.execute('SELECT unique_id FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == '1234'

    c.execute('SELECT date FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == '20150610'

    c.execute('SELECT status FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'closed'

    c.execute('SELECT source FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'HPD'

    c.execute('SELECT description FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'BELL/BUZZER/INTERCOM'

    c.execute('SELECT resolution_description FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'The Department of Housing Preservation and Development was not able to gain access to inspect the following conditions. The complaint has been closed. If the condition still exists, please file a new complaint.'

    c.execute('SELECT resolution_violation FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 0

    c.execute('SELECT resolution_no_action FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 0

    c.execute('SELECT unable_to_investigate FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 1

    c.execute('SELECT open_over_month FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 0

    c.execute('SELECT closed_date FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == '20150820'

    c.execute('SELECT days_to_close FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 71

    c.execute('SELECT complaint_type FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == "GENERAL"
  except AssertionError as error:
    raise error

def insertion_of_record_open(c):
# An open call

  service_call_json = [
    {"address_type":"ADDRESS","agency":"HPD","agency_name":"Department of Housing Preservation and Development","bbl":"5056280024","borough":"BROOKLYN","city":"BROOKLYN","closed_date":"2015-08-20T10:20:40.000","community_board":"01 BROOKLYN","complaint_type":"GENERAL","created_date":"2015-06-10T18:39:08.000","descriptor":"BELL/BUZZER/INTERCOM","facility_type":"N/A","incident_address":"fake","incident_zip":"11206","latitude":"40","location":{"type":"Point","coordinates":[-73.94003123834,40]},"location_type":"RESIDENTIAL BUILDING","longitude":"-73.94003123833956","open_data_channel_type":"PHONE","park_borough":"BROOKLYN","park_facility_name":"Unspecified","resolution_action_updated_date":"2015-08-20T10:20:40.000","resolution_description":"The Department of Housing Preservation and Development was not able to gain access to inspect the following conditions. The complaint has been closed. If the condition still exists, please file a new complaint.","status":"Open","street_name":"fake","unique_key":"1234","x_coordinate_state_plane":"1000876","y_coordinate_state_plane":"1"}
  ]

  test_context.context.service_calls_seeds.seed(c, service_call_json)
  
  try: 
    c.execute('SELECT id FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entries = c.fetchall()
    assert len(entries) == 1
    
    c.execute('SELECT building_id FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 1

    c.execute('SELECT unique_id FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == '1234'

    c.execute('SELECT date FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == '20150610'

    c.execute('SELECT status FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'open'

    c.execute('SELECT source FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'HPD'

    c.execute('SELECT description FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'BELL/BUZZER/INTERCOM'

    c.execute('SELECT resolution_description FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'The Department of Housing Preservation and Development was not able to gain access to inspect the following conditions. The complaint has been closed. If the condition still exists, please file a new complaint.'

    c.execute('SELECT resolution_violation FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 0

    c.execute('SELECT resolution_no_action FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 0

    c.execute('SELECT unable_to_investigate FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 1

    c.execute('SELECT open_over_month FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 1

    c.execute('SELECT closed_date FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == None

    c.execute('SELECT days_to_close FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == None

    c.execute('SELECT complaint_type FROM {tn}'.format(tn=test_context.context.service_calls_seeds.table))
    entry = c.fetchone()
    assert entry[0] == "GENERAL"
  except AssertionError as error:
    raise error

def test_calculate_days_to_close():
	day_open = '20000101'
	day_closed = '20000131'
	assert test_context.context.service_calls_seeds.calculate_days_to_close(day_open, day_closed) == 30

def test_is_open_over_month_open_past():
	status = "Open"
	day_open = '20180501'
	assert test_context.context.service_calls_seeds.is_open_over_month(status, day_open) == True

def test_is_open_over_month_open_today():
  status = "Open"
  day_open = datetime.datetime.today().strftime("%Y%m%d")
  assert test_context.context.service_calls_seeds.is_open_over_month(status, day_open) == False

def test_is_open_over_month_pending_past():
  status = "Pending"
  day_open = '20180501'
  assert test_context.context.service_calls_seeds.is_open_over_month(status, day_open) == True

def test_is_open_over_month_pending_today():
  status = "Pending"
  day_open = datetime.datetime.today().strftime("%Y%m%d")
  assert test_context.context.service_calls_seeds.is_open_over_month(status, day_open) == False