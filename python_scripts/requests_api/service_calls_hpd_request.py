import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from helpers import api_helpers
from seeds import service_calls_seeds
import sqlite3
conn = sqlite3.connect('nyc_data_map.sqlite', timeout=10)

table = service_calls_seeds.service_calls_table
source = "HPD"
dob_url = 'https://data.cityofnewyork.us/resource/fhrw-4uyv.json?agency=HPD&$where=created_date between "'+ api_helpers.get_next_day_to_request(conn, table, source) + '" and "' + api_helpers.get_today(table, source) + '"&'

def make_request():
  return api_helpers.request_from_api(conn, dob_url, source, service_calls_seeds.seed_service_calls_from_json)