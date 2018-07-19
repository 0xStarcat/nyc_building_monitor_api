import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '../../python_scripts'))

from helpers import api_helpers
from seeds import permits_seeds
import sqlite3

def make_request(conn, write_to_csv=False):
  table = permits_seeds.permits_table
  source = "DOB"
  permit_url = 'https://data.cityofnewyork.us/resource/83x8-shf7.json?job_type=NB&residential=YES&$where=issuance_date between \''+ api_helpers.get_next_day_to_request(conn, table, source) + '\' and \'' + api_helpers.get_today(table, source) + '\'&'

  return api_helpers.request_from_api(conn, permit_url, source, permits_seeds.seed_permits_from_json, write_to_csv)
