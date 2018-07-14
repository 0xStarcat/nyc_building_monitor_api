import datetime
from helpers import log_helper
from seeds import seed_db
from requests_api import api_requests

def test():
  seed_db.test()

def prepare():
  # deed_db.drop()
  seed_db.seed()

def update():
  log_helper.write_to_log(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + '\n')
  api_requests.request()
  api_requests.update_data()

