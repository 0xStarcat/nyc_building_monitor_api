import datetime
import context

table = context.service_calls_seeds.table

# Script
# 1) Grab all api calls with a closed date set to last X days
# 2) Loop through our open database calls to find a match on unique_id in the api open calls
# 3) If a match is found and the database call is still open, update the database with new status

def update_row(c, api_row):
  c.execute('SELECT * FROM service_calls WHERE unique_id={key}'.format(key=api_row["unique_key"]))
  call = c.fetchone()
  if (call and call[4].lower() == "open" and api_row["status"].lower() != "open"):
    print(call[4], api_row["status"].lower())
    print(" * updating a call...")
    pass
  else:
    return False


  date = str(datetime.datetime.strptime(api_row["created_date"][:10], "%Y-%m-%d").strftime("%Y%m%d"))
  status = str(api_row["status"]).lower() if "status" in api_row else "missing"
  resolution_description = api_row["resolution_description"] if "resolution_description" in api_row else "missing"
  resolution_violation = context.service_calls_seeds.resulted_in_violation(resolution_description)
  resolution_no_action = context.service_calls_seeds.took_no_action(resolution_description)
  unable_to_investigate = context.service_calls_seeds.unable_to_investigate_call(resolution_description)
  closed_date = str(datetime.datetime.strptime(api_row["closed_date"][:10], "%Y-%m-%d").strftime("%Y%m%d")) if "status" in api_row and "closed_date" in api_row and api_row["status"].lower() != "open" and api_row["status"].lower() != "pending" else None
  
  days_to_close = int(context.service_calls_seeds.calculate_days_to_close(date, closed_date)) if closed_date else None
  if status.lower() == "open":
    open_over_month = context.service_calls_seeds.is_open_over_month(status, date)
  else:
    open_over_month = context.service_calls_seeds.was_open_over_month(closed_date, date)

  c.execute('UPDATE {tn} SET status=?, resolution_description=?, resolution_violation=?, resolution_no_action=?, unable_to_investigate=?, open_over_month=?, closed_date=?, days_to_close=? WHERE {cn}=\"{value}\"'\
    .format(tn=table, cn="unique_id", value=str(api_row["unique_key"])), (status, resolution_description, resolution_violation, resolution_no_action, unable_to_investigate, open_over_month, closed_date, days_to_close))

  return True

def api_request(table, source):
  url = 'https://data.cityofnewyork.us/resource/fhrw-4uyv.json?$where=(agency=\'DOB\' OR agency=\'HPD\') AND closed_date > "'+ context.api_helpers.get_previous_days(table, source, 30) + '"&'

  api_response = context.api_helpers.request_from_api_no_seed(url)
  return api_response

def check_statuses(c, conn):
  table = context.service_calls_seeds.table
  source = None

  api_json = api_request(table, source)
  print("Found " + str(len(api_json)) + " open calls in the API")

  calls_updated = 0
  for api_row in api_json:
    if update_row(c, api_row):
      calls_updated += 1
    else:
      print("  X Call not updated", api_row["unique_key"])
      continue

  print(str(calls_updated) + " calls were updated")
  return calls_updated
  