import datetime

import seed_db
import api_requests
from helpers import log_helper

def test():
  seed_db.test()

def prepare():
  deed_db.drop()
  seed_db.seed()

def update():
  log_helper.write_to_log(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + '\n')
  api_requests.request()
  api_requests.update_data()
  # api_requests.check_call_statuses()

