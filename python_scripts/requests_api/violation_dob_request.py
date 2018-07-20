import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from helpers import api_helpers
from seeds import violations_seeds

def make_request(conn, write_to_csv=False):
  table = violations_seeds.table
  source = "DOB"
  dob_url = 'https://data.cityofnewyork.us/resource/dvnq-fhaa.json?$where=issue_date between "'+ api_helpers.get_next_day_to_request(conn, table, source) + '" and "' + api_helpers.get_today(table, source) + '" AND violation_type_code not in("LL5", "LL5/73", "ES")&'
  return api_helpers.request_from_api(conn, dob_url, source, violations_seeds.seed_violations, write_to_csv)