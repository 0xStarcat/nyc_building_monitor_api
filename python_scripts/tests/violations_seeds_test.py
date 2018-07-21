import test_context

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