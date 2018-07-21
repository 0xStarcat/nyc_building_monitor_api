import sqlite3
import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from helpers import api_helpers
from seeds import service_calls_seeds

table = service_calls_seeds.table
import config

def check_statuses():
  conn = sqlite3.connect(config.DATABASE_BACKUP_URL, timeout=10)
  c = conn.cursor()
  c.execute('pragma foreign_keys=on;')
  table = service_calls_seeds.table
  source = None

  c.execute('SELECT * FROM {tn} WHERE {cn}=\'{value}\''.format(tn=table, cn='status', value='Open'))
  open_calls = c.fetchall()
  print("Found " + str(len(open_calls)) + " open calls to check")
  
  url = 'https://data.cityofnewyork.us/resource/fhrw-4uyv.json?$where= created_date between "'+ api_helpers.get_next_day_to_request(conn, table, source) + '" and "' + api_helpers.get_today(table, source) + '"& agency \'DOB\' OR agency \'HPD\' AND status \'Open\'&'
  api_response = api_helpers.request_from_api_no_seed(url)
  print(api_response)
  print(str(len(api_response)))

  for index, call in enumerate(open_calls):
    still_open = next((api_row for api_row in api_response if call[9] == api_row["unique_id"]), False) 
    if still_open:
      print("  * No status change", index + "/" + str(len(open_calls)))
      del open_calls[index]
  
  print("** Calls remaining with assumed status change: ", str(len(open_calls)))
  
  for index, call in enumerate(open_calls):
    url = 'https://data.cityofnewyork.us/resource/fhrw-4uyv.json?unique_key=' + call[9]
    api_call = api_helpers.request_single_row_from_api(url)[0]
    if not api_call:
      print("  * Call not retrieved from api.", index + "/" + str(len(open_calls)))
      continue
    if api_call["status"].lower() != "open":
      print(" ++ Updating status of ", call[9], index + "/" + str(len(open_calls)))
      
      c.execute('DELETE FROM {tn} WHERE {cn}={value}'.format(tn=table, cn="id", value=call[0]))
      service_calls_seeds.seed(c, api_call)
      conn.commit()



  # for index, call in enumerate(open_calls):
  #   print("checking call status: " + str(index) + '/' + str(len(open_calls)))
  #   url = 'https://data.cityofnewyork.us/resource/fhrw-4uyv.json?unique_key=' + call[9]
  #   dob_url = 'https://data.cityofnewyork.us/resource/fhrw-4uyv.json?$where= created_date between "'+ api_helpers.get_next_day_to_request(conn, table, source) + '" and "' + api_helpers.get_today(table, source) + '"& (agency DOB OR agency HPD) AND status Open'

  #   source = call[11]
  