import context


# Script
# 1) Grab all api violation,s with a closed date set to last X days
# 2) Loop through our open database violation,s to find a match on unique_id in the api open violation,s
# 3) If a match is found and the database violation, is still open, update the database with new status

def update_row(c, api_row):
  table = context.violations_seeds.table

  unique_id = context.violations_seeds.get_violation_id(api_row)
  c.execute('SELECT * FROM violations WHERE unique_id=\"{key}\"'.format(key=unique_id))
  violation = c.fetchone()
  if (violation and violation[8] == "open" and context.violations_seeds.get_status(api_row) != "open"):
    print(" * updating a violation,...")
  else:
    return False

  status = context.violations_seeds.get_status(api_row)
  status_description = context.violations_seeds.get_status_description(api_row)

  c.execute('UPDATE {tn} SET status=?, status_description=? WHERE {cn}=\"{value}\"'\
    .format(tn=table, cn="unique_id", value=str(unique_id)), (status, status_description))

  return True

def api_request(table, source):
  if source == 'DOB':
    url = 'https://data.cityofnewyork.us/resource/dvnq-fhaa.json?$where=disposition_date > "'+ context.api_helpers.get_previous_days(table, source, 365) + '"&'
  elif source == "ECB":
    url = 'https://data.cityofnewyork.us/resource/gq3f-5jm8.json?$where=issue_date > "'+ context.api_helpers.get_previous_days(table, source, 365) + '" AND hearing_status!="PENDING"&'
  elif source == "HPD":
    url = 'https://data.cityofnewyork.us/resource/b2iz-pps8.json?$where=currentstatusdate > "'+ context.api_helpers.get_previous_days(table, source, 180) + '" AND violationstatus!="Open"&'

  api_response = context.api_helpers.request_from_api_no_seed(url)
  return api_response

def check_statuses(c):
  table = context.violations_seeds.table
  sources = ['DOB', 'ECB', 'HPD']

  violations_updated = 0
  for source in sources:
    api_json = api_request(table, source)
    print("Found " + str(len(api_json)) + " open violations in the API")

    
    for index in range(0, len(api_json)):
      if update_row(c, api_json[index]):
        violations_updated += 1
      else:
        print("  X Violation not updated", str(index) + '/' + str(len(api_json)))
        continue

  print(str(violations_updated) + " violations were updated")
  return violations_updated
  