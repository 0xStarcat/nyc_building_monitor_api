import test_context
import setup_tests
import factories

def seed_db():
  setup_tests.setup_db()
  factories.seed_test_db_with_open_violations()

def test_check_violations_status_request_on_open_records():
  

  try:
    conn = setup_tests.new_conn()
    c = conn.cursor()
    seed_db()
    with_closed_dob_record(c)
    conn.close()

    conn = setup_tests.new_conn()
    c = conn.cursor()
    seed_db()
    with_closed_ecb_record(c)
    conn.close()

    conn = setup_tests.new_conn()
    c = conn.cursor()
    seed_db()
    with_closed_hpd_record(c)
    conn.close()

    seed_db()
    conn = setup_tests.new_conn()
    c = conn.cursor()
    # with_open_api_record(c)
    conn.close()
  except Exception as error:
    conn.close()
    print(error)
    raise error

def with_closed_dob_record(c):
  api_json = { "source": "DOB", "penality_imposed": "10000", "bin":"3116172","block":"5628","lot":"24","boro":"5","description":"A really good violation.","disposition_comments":"Wow you should have seen that.","ecb_number":"1234","house_number":"2","isn_dob_bis_viol":"3","issue_date":"19991014","number":"a unique id violation","street":"fake st","violation_category":"VW*-VIOLATION - WORK W/O PERMIT DISMISSED","violation_number":"22?","violation_type":"C-CONSTRUCTION","violation_type_code":"C"}

  unique_id = api_json["number"]

  try:
    test_context.context.check_violations_status_request.update_row(c, api_json)

    c.execute('SELECT unique_id FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.violations_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'a unique id violation'

    c.execute('SELECT status FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.violations_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'closed'

    c.execute('SELECT status_description FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.violations_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'VW*-VIOLATION - WORK W/O PERMIT DISMISSED - Wow you should have seen that.'
  except AssertionError as error:
    raise error

def with_closed_ecb_record(c):
  api_json = {"source": "ECB", "aggravated_level":"NO","amount_paid":".00","balance_due":"2400.00","bin":"4618517","block":"5628","boro":"5","certification_status":"CERTIFICATE ACCEPTED","dob_violation_number":"060711CSSCWJM08","ecb_violation_number":"unique for ecb id","ecb_violation_status":"RESOLVE","hearing_date":"20120221","hearing_status":"","hearing_time":"830","infraction_code1":"109","isn_dob_bis_extract":"946264","issue_date":"20110607","lot":"24","penality_imposed":"2400.00","respondent_city":"HUNTINGTON STAT","respondent_house_number":"34","respondent_name":"HEMPTON PARK CORPORATION","respondent_street":"W 18 ST","respondent_zip":"11746","section_law_description1":"BC 3301.2,27-1009(A)                                                        FAIL TO SAFEGUARD PERS/PROPERTY AFFECTED BY CONSTRUCTION OP","served_date":"20110715","severity":"Unknown","violation_description":"FAILURE TO SAFEGUARD ALL PERSONS & PROPERTY AFFECTED BY CONSTRUCTION OPERATIONS. FLATBED TRUCK BLOCKING ENTIRE SIDEWALK (SITE ENTRANCE) WHILE BEING UNLOADED BY UNLICENSED OPERATOR ON CRANE CD 3876. ABOVE IS","violation_type":"Construction"}


  unique_id = api_json["ecb_violation_number"]

  try:
    test_context.context.check_violations_status_request.update_row(c, api_json)

    c.execute('SELECT unique_id FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.violations_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'unique for ecb id'

    c.execute('SELECT status FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.violations_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'closed'

    c.execute('SELECT status_description FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.violations_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'CERTIFICATE ACCEPTED'
  except AssertionError as error:
    raise error

def with_closed_hpd_record(c):
  api_json = {"source": "HPD","apartment":"1234","approveddate":"2013-10-10T00:00:00.000","bbl":"1234","bin":"1234","block":"5628","boro":"NOT BRONX","boroid":"5","buildingid":"1234","censustract":"63","class":"B","communityboard":"4","councildistrict":"8","currentstatus":"CLOSE","currentstatusdate":"2014-10-17T00:00:00.000","currentstatusid":"19","highhousenumber":"1234","housenumber":"123","inspectiondate":"2013-10-08T00:00:00.000","latitude":"40","longitude":"-73.926605","lot":"24","lowhousenumber":"1234","novdescription":"SECTION 27-2005 some words go here!","novid":"4706454","novissueddate":"2013-10-11T00:00:00.000","novtype":"Original","nta":"West Concourse","ordernumber":"501","originalcertifybydate":"2013-11-29T00:00:00.000","originalcorrectbydate":"2013-11-15T00:00:00.000","registrationid":"0k","story":"3","streetcode":"35020","streetname":"somewhere","violationid":"a good id","violationstatus":"Close","zip":"10451"}



  unique_id = api_json["violationid"]

  try:
    test_context.context.check_violations_status_request.update_row(c, api_json)

    c.execute('SELECT unique_id FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.violations_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'a good id'

    c.execute('SELECT status FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.violations_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'closed'

    c.execute('SELECT status_description FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.violations_seeds.table, unique_id=unique_id))
    entry = c.fetchone()
    assert entry[0] == 'CLOSE'
  except AssertionError as error:
    raise error

# def with_open_api_record(c):
#   api_json = {"address_type":"ADDRESS","agency":"DOB","agency_name":"Department of Buildings","bbl":"5056280024","borough":"BROOKLYN","city":"BROOKLYN","closed_date":"2018-07-18T08:53:55.000","community_board":"05 BROOKLYN","complaint_type":"Building/Use","created_date":"2018-05-18T08:53:55.000","descriptor":"Illegal Conversion Of Residential Building/Space","facility_type":"N/A","incident_address":"fake","incident_zip":"11207","latitude":"40","location":{"type":"Point","coordinates":[-73.890480139432,40]},"longitude":"-73.89048013943226","open_data_channel_type":"UNKNOWN","park_borough":"BROOKLYN","park_facility_name":"Unspecified","resolution_action_updated_date":"2018-07-18T00:00:00.000","resolution_description":"Still open...","status":"Open","street_name":"fake","unique_key":"1234","x_coordinate_state_plane":"1014629","y_coordinate_state_plane":"1"}
#   unique_id = api_json["unique_key"]

#   try:
#     test_context.context.check_violations_status_request.update_row(c, api_json)

#     c.execute('SELECT unique_id FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.violations_seeds.table, unique_id=unique_id))
#     entry = c.fetchone()
#     assert entry[0] == '1234'

#     c.execute('SELECT status FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.violations_seeds.table, unique_id=unique_id))
#     entry = c.fetchone()
#     assert entry[0] == 'open'

#     c.execute('SELECT status_description FROM {tn} WHERE unique_id=\"{unique_id}\"'.format(tn=test_context.context.violations_seeds.table, unique_id=unique_id))
#     entry = c.fetchone()
#     assert entry[0] == 'closed'
#   except AssertionError as error:
#     raise error

