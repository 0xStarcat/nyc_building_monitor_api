import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '../../python_scripts'))

from helpers import api_helpers
from seeds import evictions_seeds
import sqlite3

def make_request(conn, write_to_csv=False):
  table = evictions_seeds.table
  source = "NYC"
  url = 'https://data.cityofnewyork.us/resource/fxkt-ewig.json?residential_commercial_ind=Residential&$where=executed_date between \''+ api_helpers.get_next_day_to_request(conn, table, source) + '\' and \'' + api_helpers.get_today(table, source) + '\'&'

  return api_helpers.request_from_api(conn, url, source, evictions_seeds.seed_table, write_to_csv)
