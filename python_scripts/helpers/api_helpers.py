import sqlite3
import datetime
import requests
import json 
import csv

def get_next_day_to_request(conn, table_name, source):
  c = conn.cursor()
  c.execute('pragma foreign_keys=on;')
  c.execute('SELECT date FROM {tn} WHERE {cn1}=\'{source}\' order by date desc'.format(tn=table_name, cn1="source", source=source))
  entry = c.fetchone() 
  print("Latest entry: ", entry)
  if entry:
    if table_name == 'violations' and source != "HPD":
      return (datetime.datetime.strptime(str(entry[0]), '%Y%m%d') + datetime.timedelta(days=1)).strftime("%Y%m%d")
    else:
      return (datetime.datetime.strptime(str(entry[0]), '%Y%m%d') + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
  else:
    return get_start_date(table_name, source)

def get_today(table_name, source):
  if table_name == 'violations' and source != "HPD":
    return datetime.date.today().strftime("%Y%m%d")
  else:
    return datetime.date.today().strftime("%Y-%m-%d")

def get_start_date(table_name, source):
  if table_name == 'violations' and source != "HPD":
    return "20100101"
  else:
    return "2010-01-01"

def request_single_row_from_api(url):
  print("requesting from: ", url)
  return json.loads(requests.get(url).text)

def request_from_api_no_seed(url):
  print("requesting from: ", url)
  offset = 0
  limit = 50000  
  request_data = []
  count = 0

  def request(off):
    r = requests.get(url+'&$limit='+str(limit)+'&$offset=' + str(off))

    data = json.loads(r.text)
    print(data)
    for d in data:
      request_data.append(d)
    return data

  while len(request(offset)) > 0:
    offset = offset + limit
    print("records retrieved: ", len(request_data))

  return request_data

def request_from_api(conn, url, source, seed_method=None, write_to_csv=False):
  c = conn.cursor()
  c.execute('pragma foreign_keys=on;')
  print("requesting from: ", url)
  offset = 0
  limit = 50000  
  request_data = []
  count = 0

  def request(off):
    r = requests.get(url+'&$limit='+str(limit)+'&$offset=' + str(off))
    
    data = json.loads(r.text)
    for d in data:
      request_data.append(d)
    return data

  while len(request(offset)) > 0:
    offset = offset + limit
    print("records retrieved: ", len(request_data))

    if source:
      for data in request_data:
        data["source"] = source

    if seed_method:
      seed_method(c, request_data, write_to_csv)
      conn.commit()
    count += len(request_data)
    print("  * " + str(count) + " records seeded.")
    request_data = []

  conn.commit()

  return count

