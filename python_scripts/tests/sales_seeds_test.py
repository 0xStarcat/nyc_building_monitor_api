import context

# get_residential_r_class
def test_get_residential_r_class_1():
  bldg_class = "R0"
  assert context.seed_db.sales_seeds.get_residential_r_class(bldg_class) == True

def test_get_residential_r_class_2():
  bldg_class = "RA"
  assert context.seed_db.sales_seeds.get_residential_r_class(bldg_class) == False

def test_get_residential_r_class_3():
  bldg_class = "RR"
  assert context.seed_db.sales_seeds.get_residential_r_class(bldg_class) == True

# class_is_residential
def test_class_is_residential_1():
  bldg_class = "A0"
  assert context.seed_db.sales_seeds.class_is_residential(bldg_class) == True

# class_is_residential
def test_class_is_residential_2():
  bldg_class = "G1"
  assert context.seed_db.sales_seeds.class_is_residential(bldg_class) == False

# class_is_residential
def test_class_is_residential_3():
  bldg_class = "R4"
  assert context.seed_db.sales_seeds.class_is_residential(bldg_class) == True

# class_is_residential
def test_class_is_residential_4():
  bldg_class = "V0"
  assert context.seed_db.sales_seeds.class_is_residential(bldg_class) == True

# class_is_non_residential

def test_class_is_non_residential_1():
  bldg_class = "V0"
  assert context.seed_db.sales_seeds.class_is_non_residential(bldg_class) == False

def test_class_is_non_residential_2():
  bldg_class = "R4"
  assert context.seed_db.sales_seeds.class_is_non_residential(bldg_class) == False

def test_class_is_non_residential_3():
  bldg_class = "F1"
  assert context.seed_db.sales_seeds.class_is_non_residential(bldg_class) == True