import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from helpers import api_helpers
from seeds import violations_seeds

# Boro = 3 (brooklyn)
# Issued between dates
# violation_type_code is not
  # "c" (construction), 
  # "LL5" or "LL5/83" (fire safety in office buildings), 
  # "ES" (electric sign, probably business)

table = violations_seeds.violations_table
source = "DOB"
dob_url = 'https://data.cityofnewyork.us/resource/dvnq-fhaa.json?$where=issue_date between "'+ api_helpers.get_next_day_to_request(table, source) + '" and "' + api_helpers.get_today(table, source) + '" AND violation_type_code not in("LL5", "LL5/73", "ES")&'

def make_request():
  return api_helpers.request_from_api(dob_url, source, violations_seeds.seed_violations)