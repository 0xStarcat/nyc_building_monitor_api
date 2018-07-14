import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from helpers import api_helpers
from seeds import violations_seeds

table = violations_seeds.violations_table
source = "hpd"
hpd_url = 'https://data.cityofnewyork.us/resource/b2iz-pps8.json?$where=inspectiondate between "'+ api_helpers.get_next_day_to_request(table, source) + '" and "' + api_helpers.get_today(table, source) + '"&'

def make_request():
  return api_helpers.request_from_api(hpd_url, source, violations_seeds.seed_violations)