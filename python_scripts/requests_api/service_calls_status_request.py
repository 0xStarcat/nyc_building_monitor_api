import sqlite3
import datetime
import config
from seeds import service_calls_seeds

from helpers import api_helpers
from helpers.list_helpers import find_matches_and_remove

table = service_calls_seeds.table

# Script
# 1) Grab the open calls in our database
# 2) Grab *ALL* the open calls in the api
# 3) Loop through our open database calls to find a match on unique_id in the api open calls
# 4) If a match is found, then the call is still open. Delete it from list.
# 5) With the leftover calls in the list, do an individual API query of its status and update it.

def update_service_call_row(c, api_json):
  date = str(datetime.datetime.strptime(api_json["created_date"][:10], "%Y-%m-%d").strftime("%Y%m%d"))
  status = str(api_json["status"]).lower() if "status" in api_json else "missing"
  resolution_description = api_json["resolution_description"] if "resolution_description" in api_json else "missing"
  resolution_violation = service_calls_seeds.resulted_in_violation(resolution_description)
  resolution_no_action = service_calls_seeds.took_no_action(resolution_description)
  unable_to_investigate = service_calls_seeds.unable_to_investigate_call(resolution_description)
  closed_date = str(datetime.datetime.strptime(api_json["closed_date"][:10], "%Y-%m-%d").strftime("%Y%m%d")) if "status" in api_json and "closed_date" in api_json and api_json["status"].lower() != "open" and api_json["status"].lower() != "pending" else None
  
  days_to_close = int(service_calls_seeds.calculate_days_to_close(date, closed_date)) if closed_date else None
  if status.lower() == "open":
    open_over_month = service_calls_seeds.is_open_over_month(status, date)
  else:
    open_over_month = service_calls_seeds.was_open_over_month(closed_date, date)

  c.execute('UPDATE {tn} SET status=\"{status}\", resolution_description=\"{resolution_description}\", resolution_violation=\"{resolution_violation}\", resolution_no_action=\"{resolution_no_action}\", unable_to_investigate=\"{unable_to_investigate}\", open_over_month=\"{open_over_month}\", closed_date=\"{closed_date}\", days_to_close=\"{days_to_close}\" WHERE {cn}=\"{value}\"'\
    .format(tn=table, cn="unique_id", value=str(api_json["unique_key"]), status=status, resolution_description=resolution_description, resolution_violation=resolution_violation, resolution_no_action=resolution_no_action, unable_to_investigate=unable_to_investigate, open_over_month=open_over_month, closed_date=closed_date, days_to_close=days_to_close)) 


def api_request(table, source):
  url = 'https://data.cityofnewyork.us/resource/fhrw-4uyv.json?$where=(agency=\'DOB\' OR agency=\'HPD\') AND closed_date > "'+ api_helpers.get_previous_days(table, source, 14) + '"&'

  # url = 'https://data.cityofnewyork.us/resource/fhrw-4uyv.json?$where=status=\'Open\' AND (agency=\'DOB\' OR agency=\'HPD\') AND created_date between "'+ api_helpers.get_start_date(table, source) + '" and "' + api_helpers.get_today(table, source) + '"&'
  api_response = api_helpers.request_from_api_no_seed(url)
  return api_response

def check_statuses(c, conn):
  table = service_calls_seeds.table
  source = None

  # Get all open database calls
  c.execute('SELECT * FROM {tn} WHERE {cn}=\'{value}\''.format(tn=table, cn='status', value='open'))
  open_calls = c.fetchall()
  print("Found " + str(len(open_calls)) + " open calls in the DB")
  
  # Get all open API calls
  api_json = api_request(table, source)
  print("Found " + str(len(api_json)) + " open calls in the API")

  # Compare the two lists (use a copy to iterate over so you can delete from original list)
  
  find_matches_and_remove(open_calls, api_json, 2, "unique_key")

  print("** Calls remaining with assumed status change: ", str(len(open_calls)))
  
  # Check each individual call's status and update the database row.
  calls_updated = 0
  for index, call in enumerate(open_calls):
    url = 'https://data.cityofnewyork.us/resource/fhrw-4uyv.json?unique_key=' + call[2]
    api_call = api_helpers.request_single_row_from_api(url)[0]
    if not api_call:
      print("  * Call not retrieved from api.", str(index) + "/" + str(len(open_calls)))
      continue
    if api_call["status"].lower() != "open":
      print(" ++ Updating status of ", call[2], str(index) + "/" + str(len(open_calls)))
      update_service_call_row(c, api_call)
      calls_updated += 1
    else:
      print("  * No Updates.")

  print(str(calls_updated) + " calls were updated")
  return calls_updated
  