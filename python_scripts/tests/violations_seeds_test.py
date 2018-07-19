import context

# get_violation_id
def test_get_violation_id_with_violationid():
  violation = {"violationid": 1}
  assert context.seed_db.violations_seeds.get_violation_id(violation) == 1

def test_get_violation_id_with_ecb_violation_number():
  violation = {"ecb_violation_number": 1}
  assert context.seed_db.violations_seeds.get_violation_id(violation) == 1

def test_get_violation_id_with_number():
  violation = {"number": 1}
  assert context.seed_db.violations_seeds.get_violation_id(violation) == 1

def test_get_violation_id_with_non_field():
  violation = {"not_unique_id": 1}
  assert context.seed_db.violations_seeds.get_violation_id(violation) == None
  
# get_description

def test_get_description_with_violation_description():
  violation = {"violation_description": "hello"}
  assert context.seed_db.violations_seeds.get_description(violation) == "hello"

def test_get_description_with_description():
  violation = {"description": "hello"}
  assert context.seed_db.violations_seeds.get_description(violation) == "hello"

def test_get_description_with_non_field():
  violation = {"not_description": "hello"}
  assert context.seed_db.violations_seeds.get_description(violation) == ""

# get bbl

def test_get_bbl_1():
  boro_id = "3"
  violation = {"block": "01111", "lot": "0222"}
  assert context.seed_db.violations_seeds.get_bbl(boro_id, violation) == 3011110222

def test_get_bbl_2():
  boro_id = "3"
  violation = {"block": "01111", "lot": "00222"}
  assert context.seed_db.violations_seeds.get_bbl(boro_id, violation) == 3011110222

def test_get_bbl_3():
  boro_id = "3"
  violation = {"block": "1111", "lot": "222"}
  assert context.seed_db.violations_seeds.get_bbl(boro_id, violation) == 3011110222