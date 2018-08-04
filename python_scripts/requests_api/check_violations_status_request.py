import sqlite3
import datetime
import config
from seeds import violations_seeds

from helpers import api_helpers

table = violations_seeds.table

# Script
# 1) Grab all api violaton,s with a closed date set to last X days
# 2) Loop through our open database violaton,s to find a match on unique_id in the api open violaton,s
# 3) If a match is found and the database violaton, is still open, update the database with new status

def update_row(c, api_row):
  unique_id = violations_seeds.get_violation_id(api_row)
  c.execute('SELECT * FROM violations WHERE unique_id=\"{key}\"'.format(key=unique_id))
  violaton = c.fetchone()
  if (violaton and violaton[8] == "open" and violations_seeds.get_status(api_row) != "open"):
    print(" * updating a violaton,...")
    pass
  else:
    return False

  status = violations_seeds.get_status(api_row)
  status_description = violations_seeds.get_status_description(api_row)

  c.execute('UPDATE {tn} SET status=?, status_description=? WHERE {cn}=\"{value}\"'\
    .format(tn=table, cn="unique_id", value=str(unique_id)), (status, status_description))

  return True

def api_request(table, source):
  if source == 'DOB':
    url = 'https://data.cityofnewyork.us/resource/dvnq-fhaa.json?$where=disposition_date > "'+ api_helpers.get_previous_days(table, source, 365) + '"&'
  elif source == "ECB":
    url = 'https://data.cityofnewyork.us/resource/gq3f-5jm8.json?$where=issue_date > "'+ api_helpers.get_previous_days(table, source, 365) + '" AND hearing_date is not PENDING&'
  elif source == "HPD":
    url = 'https://data.cityofnewyork.us/resource/b2iz-pps8.json?$where=currentstatusdate > "'+ api_helpers.get_previous_days(table, source, 365) + '" AND violationstatus is not Open&'

  api_response = api_helpers.request_from_api_no_seed(url)
  return api_response

def check_statuses(c, conn):
  table = violations_seeds.table
  sources = ['DOB', 'ECB', 'HPD']

  violations_updated = 0
  for source in sources:
    api_json = api_request(table, source)
    print("Found " + str(len(api_json)) + " open violations in the API")

    
    for index in range(0, len(api_json)):
      if update_row(c, api_json[index]):
        violations_updated += 1
      else:
        print("  X Call not updated", str(index) + '/' + str(len(api_json)))
        continue

  print(str(violations_updated) + " violations were updated")
  return violations_updated
  