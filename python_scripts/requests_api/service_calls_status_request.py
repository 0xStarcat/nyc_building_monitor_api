import sqlite3
import datetime
import context

table = context.service_calls_seeds.table
import config

def update_service_call_row(c, api_json):
  date = str(datetime.datetime.strptime(api_json["created_date"][:10], "%Y-%m-%d").strftime("%Y%m%d"))
  print(date)
  status = str(api_json["status"]).lower() if "status" in api_json else "missing"
  resolution_description = api_json["resolution_description"] if "resolution_description" in api_json else "missing"
  resolution_violation = context.service_calls_seeds.resulted_in_violation(resolution_description)
  resolution_no_action = context.service_calls_seeds.took_no_action(resolution_description)
  unable_to_investigate = context.service_calls_seeds.unable_to_investigate_call(resolution_description)
  closed_date = str(datetime.datetime.strptime(api_json["closed_date"][:10], "%Y-%m-%d").strftime("%Y%m%d")) if "status" in api_json and "closed_date" in api_json and api_json["status"].lower() != "open" and api_json["status"].lower() != "pending" else None
  
  days_to_close = int(context.service_calls_seeds.calculate_days_to_close(date, closed_date)) if closed_date else None
  if status.lower() == "open":
    open_over_month = context.service_calls_seeds.is_open_over_month(status, date)
  else:
    open_over_month = context.service_calls_seeds.was_open_over_month(closed_date, date)

  c.execute('UPDATE {tn} SET status=\"{status}\", resolution_description=\"{resolution_description}\", resolution_violation=\"{resolution_violation}\", resolution_no_action=\"{resolution_no_action}\", unable_to_investigate=\"{unable_to_investigate}\", open_over_month=\"{open_over_month}\", closed_date=\"{closed_date}\", days_to_close=\"{days_to_close}\" WHERE {cn}=\"{value}\"'\
    .format(tn=table, cn="unique_id", value=str(api_json["unique_key"]), status=status, resolution_description=resolution_description, resolution_violation=resolution_violation, resolution_no_action=resolution_no_action, unable_to_investigate=unable_to_investigate, open_over_month=open_over_month, closed_date=closed_date, days_to_close=days_to_close)) 


def api_request():
  url = 'https://data.cityofnewyork.us/resource/fhrw-4uyv.json?$where= created_date between "'+ context.api_helpers.get_next_day_to_request(conn, table, source) + '" and "' + context.api_helpers.get_today(table, source) + '"& agency \'DOB\' OR agency \'HPD\' AND status \'Open\'&'
  api_response = context.api_helpers.request_from_api_no_seed(url)
  print(api_response)
  print(str(len(api_response)))
  return api_response

def check_statuses(c, conn, api_json):
  table = context.service_calls_seeds.table
  source = None

  c.execute('SELECT * FROM {tn} WHERE {cn}=\'{value}\''.format(tn=table, cn='status', value='open'))
  open_calls = c.fetchall()
  print("Found " + str(len(open_calls)) + " open calls to check")
  
  api_json = api_request()

  for index, call in enumerate(open_calls):
    still_open = next((api_row for api_row in api_response if call[9] == api_row["unique_id"]), False) 
    if still_open:
      print("  * No status change", index + "/" + str(len(open_calls)))
      del open_calls[index]
  
  print("** Calls remaining with assumed status change: ", str(len(open_calls)))
  
  for index, call in enumerate(open_calls):
    url = 'https://data.cityofnewyork.us/resource/fhrw-4uyv.json?unique_key=' + call[9]
    api_call = context.api_helpers.request_single_row_from_api(url)[0]
    if not api_call:
      print("  * Call not retrieved from api.", index + "/" + str(len(open_calls)))
      continue
    if api_call["status"].lower() != "open":
      print(" ++ Updating status of ", call[9], index + "/" + str(len(open_calls)))
      
      c.execute('DELETE FROM {tn} WHERE {cn}={value}'.format(tn=table, cn="id", value=call[0]))
      context.service_calls_seeds.seed(c, api_call)
      conn.commit()



  # for index, call in enumerate(open_calls):
  #   print("checking call status: " + str(index) + '/' + str(len(open_calls)))
  #   url = 'https://data.cityofnewyork.us/resource/fhrw-4uyv.json?unique_key=' + call[9]
  #   dob_url = 'https://data.cityofnewyork.us/resource/fhrw-4uyv.json?$where= created_date between "'+ context.api_helpers.get_next_day_to_request(conn, table, source) + '" and "' + context.api_helpers.get_today(table, source) + '"& (agency DOB OR agency HPD) AND status Open'

  #   source = call[11]
  