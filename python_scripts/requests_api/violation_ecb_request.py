import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from helpers import api_helpers
from seeds import violations_seeds

table = violations_seeds.violations_table
source = "ECB"
# violation_type is not "Site Safety"
ecb_url = 'https://data.cityofnewyork.us/resource/gq3f-5jm8.json?$where=issue_date between "'+ api_helpers.get_next_day_to_request(table, source) + '" and "' + api_helpers.get_today(table, source) + '" AND violation_type not in("Site Safety")&'


def make_request():
  return api_helpers.request_from_api(ecb_url, source, violations_seeds.seed_violations)