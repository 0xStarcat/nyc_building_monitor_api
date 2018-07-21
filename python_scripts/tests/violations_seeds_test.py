import os
import sqlite3
import json
import test_context
import config 
import setup_tests
import factories

test_db = config.TEST_DB_URL

def seed_db():
  setup_tests.setup_db()
  factories.seed_test_db_with_building()

  

def drop_table(c):
  os.remove(test_db)

def test_insertion_of_record():
  seed_db()
  conn = sqlite3.connect(test_db, timeout=10)
  c = conn.cursor()
  c.execute('pragma foreign_keys=on;')
  violation_json = [
    { "source": "ECB", "penality_imposed": "10000", "bin":"3116172","block":"5628","boro":"5","description":"A really good violation.","disposition_comments":"Wow you should have seen that.","ecb_number":"1234","house_number":"2","isn_dob_bis_viol":"3","issue_date":"19991014","lot":"24","number":"a unique id violation","street":"fake st","violation_category":"VW*-VIOLATION - WORK W/O PERMIT DISMISSED","violation_number":"22?","violation_type":"C-CONSTRUCTION","violation_type_code":"C"}
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

    c.execute('SELECT violation_code FROM {tn}'.format(tn=test_context.context.violations_seeds.table))
    entry = c.fetchone()
    assert entry[0] == 'C'
  except AssertionError as error:
    raise error
    drop_table(c)

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