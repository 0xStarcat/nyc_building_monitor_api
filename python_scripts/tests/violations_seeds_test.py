import json
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
    insertion_of_record_ecb(c)
    conn.close()

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
  except Exception as error:
    conn.close()
    print(error)
    raise error


def insertion_of_record_hpd(c):
  violation_json = [ 
    {"source": "HPD","apartment":"1234","approveddate":"2013-10-10T00:00:00.000","bbl":"1234","bin":"1234","block":"5628","boro":"NOT BRONX","boroid":"5","buildingid":"1234","censustract":"63","class":"B","communityboard":"4","councildistrict":"8","currentstatus":"VIOLATION CLOSED","currentstatusdate":"2014-10-17T00:00:00.000","currentstatusid":"19","highhousenumber":"1234","housenumber":"123","inspectiondate":"2013-10-08T00:00:00.000","latitude":"40","longitude":"-73.926605","lot":"24","lowhousenumber":"1234","novdescription":"SECTION 27-2005.1 some words go here!","novid":"4706454","novissueddate":"2013-10-11T00:00:00.000","novtype":"Original","nta":"West Concourse","ordernumber":"501","originalcertifybydate":"2013-11-29T00:00:00.000","originalcorrectbydate":"2013-11-15T00:00:00.000","registrationid":"0k","story":"3","streetcode":"35020","streetname":"somewhere","violationid":"a good id","violationstatus":"Close","zip":"10451"}
  ]

  test_context.context.violations_seeds.seed(c, violation_json)

  try: 
    c.execute('SELECT id FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entries = c.fetchall()
    assert len(entries) == 1
    
    c.execute('SELECT building_id FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 1

    c.execute('SELECT unique_id FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'a good id'

    c.execute('SELECT date FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == '20131008'

    c.execute('SELECT penalty_imposed FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == ''

    c.execute('SELECT source FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'HPD'

    c.execute('SELECT violation_code FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'SECTION 27-2005.1'

    c.execute('SELECT status FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'closed'

    c.execute('SELECT status_description FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'VIOLATION CLOSED'
  except AssertionError as error:
    raise error


def insertion_of_record_ecb(c):
  violation_json = [
    {"source": "ECB", "aggravated_level":"NO","amount_paid":".00","balance_due":"2400.00","bin":"4618517","block":"5628","boro":"5","certification_status":"CERTIFICATE ACCEPTED","dob_violation_number":"060711CSSCWJM08","ecb_violation_number":"unique id","ecb_violation_status":"RESOLVE","hearing_date":"20120221","hearing_status":"IN VIOLATION","hearing_time":"830","infraction_code1":"109","isn_dob_bis_extract":"946264","issue_date":"20110607","lot":"24","penality_imposed":"2400.00","respondent_city":"HUNTINGTON STAT","respondent_house_number":"34","respondent_name":"HEMPTON PARK CORPORATION","respondent_street":"W 18 ST","respondent_zip":"11746","section_law_description1":"BC 3301.2,27-1009(A)                                                        FAIL TO SAFEGUARD PERS/PROPERTY AFFECTED BY CONSTRUCTION OP","served_date":"20110715","severity":"Unknown","violation_description":"FAILURE TO SAFEGUARD ALL PERSONS & PROPERTY AFFECTED BY CONSTRUCTION OPERATIONS. FLATBED TRUCK BLOCKING ENTIRE SIDEWALK (SITE ENTRANCE) WHILE BEING UNLOADED BY UNLICENSED OPERATOR ON CRANE CD 3876. ABOVE IS","violation_type":"Construction"}
  ]

  test_context.context.violations_seeds.seed(c, violation_json)

  try: 
    c.execute('SELECT id FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entries = c.fetchall()
    assert len(entries) == 1
    
    c.execute('SELECT building_id FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 1

    c.execute('SELECT unique_id FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'unique id'

    c.execute('SELECT date FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == '20110607'

    c.execute('SELECT penalty_imposed FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == '2400.00'

    c.execute('SELECT source FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'ECB'

    c.execute('SELECT violation_code FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == '109'

    c.execute('SELECT status FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'closed'

    c.execute('SELECT status_description FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'CERTIFICATE ACCEPTED'
  except AssertionError as error:
    raise error


def insertion_of_record_dob(c):
  violation_json = [
    { "source": "DOB", "penality_imposed": "10000", "bin":"3116172","block":"5628","lot":"24","boro":"5","description":"A really good violation.","disposition_comments":"Wow you should have seen that.","ecb_number":"1234","house_number":"2","isn_dob_bis_viol":"3","issue_date":"19991014","number":"a unique id violation","street":"fake st","violation_category":"VW*-VIOLATION - WORK W/O PERMIT DISMISSED","violation_number":"22?","violation_type":"C-CONSTRUCTION","violation_type_code":"C"}
  ]

  test_context.context.violations_seeds.seed(c, violation_json)
  
  try: 
    c.execute('SELECT id FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entries = c.fetchall()
    assert len(entries) == 1
    
    c.execute('SELECT building_id FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 1

    c.execute('SELECT unique_id FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'a unique id violation'

    c.execute('SELECT date FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == '19991014'

    c.execute('SELECT penalty_imposed FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == '10000'

    c.execute('SELECT source FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'DOB'

    c.execute('SELECT violation_code FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'C'

    c.execute('SELECT status FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'closed'

    c.execute('SELECT status_description FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'VW*-VIOLATION - WORK W/O PERMIT DISMISSED - Wow you should have seen that.'

    c.execute('SELECT ecb_number FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == '1234'
  except AssertionError as error:
    raise error

# get_violation_id
def test_get_violation_id_with_violationid():
  violation = {"violationid": 1}
  assert test_context.context.violations_seeds.get_violation_id(violation) == 1

def test_get_violation_id_with_ecb_violation_number():
  violation = {"ecb_violation_number": 1}
  assert test_context.context.violations_seeds.get_violation_id(violation) == 1

def test_get_violation_id_with_number():
  violation = {"number": 1}
  assert test_context.context.violations_seeds.get_violation_id(violation) == 1

def test_get_violation_id_with_non_field():
  violation = {"not_unique_id": 1}
  assert test_context.context.violations_seeds.get_violation_id(violation) == None
  
# get_description

def test_get_description_1():
  violation = {"violation_description": "hello"}
  assert test_context.context.violations_seeds.get_description(violation) == "hello"

def test_get_description_2():
  violation = {"description": "hello"}
  assert test_context.context.violations_seeds.get_description(violation) == "hello"

def test_get_description_3():
  violation = {"novdescription": "hello"}
  assert test_context.context.violations_seeds.get_description(violation) == "hello"

def test_get_description_4():
  violation = {"not_description": "hello"}
  assert test_context.context.violations_seeds.get_description(violation) == ""

# get_code

def test_get_code_1():
  violation = {"violation_type_code": "hello"}
  assert test_context.context.violations_seeds.get_code(violation) == "hello"

def test_get_code_2():
  violation = {"infraction_code1": "hello"}
  assert test_context.context.violations_seeds.get_code(violation) == "hello"

def test_get_code_3():
  violation = {"novdescription": "SECTION 2000 WITH TEXT"}
  assert test_context.context.violations_seeds.get_code(violation) == "SECTION 2000"

def test_get_code_4():
  violation = {"not_description": "hello"}
  assert test_context.context.violations_seeds.get_code(violation) == ""

# get_status

def test_get_status_1():
  violation = {"violationstatus": "Close"}
  assert test_context.context.violations_seeds.get_status(violation) == "closed"

def test_get_status_2():
  violation = {"ecb_violation_status": "RESOLVE"}
  assert test_context.context.violations_seeds.get_status(violation) == "closed"

def test_get_status_3():
  violation = {"violation_category": "DISMISSED"}
  assert test_context.context.violations_seeds.get_status(violation) == "closed"

def test_get_status_4():
  violation = {"violationstatus": "Open"}
  assert test_context.context.violations_seeds.get_status(violation) == "open"

def test_get_status_5():
  violation = {"ecb_violation_status": "ACTIVE"}
  assert test_context.context.violations_seeds.get_status(violation) == "open"

def test_get_status_6():
  violation = {"violation_category": "VIOLATION ACTIVE"}
  assert test_context.context.violations_seeds.get_status(violation) == "open"

# get bbl

def test_get_bbl_1():
  boro_id = "3"
  violation = {"block": "01111", "lot": "0222"}
  assert test_context.context.violations_seeds.get_bbl(boro_id, violation) == 3011110222

def test_get_bbl_2():
  boro_id = "3"
  violation = {"block": "01111", "lot": "00222"}
  assert test_context.context.violations_seeds.get_bbl(boro_id, violation) == 3011110222

def test_get_bbl_3():
  boro_id = "3"
  violation = {"block": "1111", "lot": "222"}
  assert test_context.context.violations_seeds.get_bbl(boro_id, violation) == 3011110222

def test_extract_section_code_1():
  description = "SECTION 27-2013 HERE IS SOME UPPER CASE TEXT"
  assert test_context.context.violations_seeds.extract_section_code(description) == "SECTION 27-2013"

def test_extract_section_code_2():
  description = "asfnjsadf 27-2013 HERE IS SOME UPPER CASE TEXT"
  assert test_context.context.violations_seeds.extract_section_code(description) == None