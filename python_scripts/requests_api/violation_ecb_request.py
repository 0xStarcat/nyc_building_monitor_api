import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from helpers import api_helpers
from seeds import violations_seeds
import sqlite3




def make_request(conn, write_to_csv=False):
  table = violations_seeds.table
  source = "ECB"
  ecb_url = 'https://data.cityofnewyork.us/resource/gq3f-5jm8.json?$where=issue_date between "'+ api_helpers.get_next_day_to_request(conn, table, source) + '" and "' + api_helpers.get_today(table, source) + '"&'
  return api_helpers.request_from_api(conn, ecb_url, source, violations_seeds.seed, write_to_csv)