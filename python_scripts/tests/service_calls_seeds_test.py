import context
import datetime

def test_calculate_days_to_close():
	day_open = '20000101'
	day_closed = '20000131'
	assert context.seed_db.service_calls_seeds.calculate_days_to_close(day_open, day_closed) == 30

def test_is_open_over_month_open_past():
	status = "Open"
	day_open = '20180501'
	assert context.seed_db.service_calls_seeds.is_open_over_month(status, day_open) == True

def test_is_open_over_month_open_today():
  status = "Open"
  day_open = datetime.datetime.today().strftime("%Y%m%d")
  assert context.seed_db.service_calls_seeds.is_open_over_month(status, day_open) == False

def test_is_open_over_month_pending_past():
  status = "Pending"
  day_open = '20180501'
  assert context.seed_db.service_calls_seeds.is_open_over_month(status, day_open) == True

def test_is_open_over_month_pending_today():
  status = "Pending"
  day_open = datetime.datetime.today().strftime("%Y%m%d")
  assert context.seed_db.service_calls_seeds.is_open_over_month(status, day_open) == False