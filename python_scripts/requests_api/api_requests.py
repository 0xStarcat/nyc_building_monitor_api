import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '../../python_scripts'))

import sqlite3


from requests_api import violation_dob_request
from requests_api import violation_ecb_request
from requests_api import violation_hpd_request
from requests_api import service_calls_dob_request
from requests_api import service_calls_hpd_request
from requests_api import service_calls_dohmh_request
from requests_api import permit_request

from migrations import buildings_migration
from migrations import boundary_table_migrations

from helpers import log_helper

def update_data():
  conn = sqlite3.connect('nyc_data_map.sqlite', timeout=10)
  c = conn.cursor()
  c.execute('pragma foreign_keys=on;')
  
  boundary_table_migrations.update_all(c, conn)
  log_helper.write_to_log(" ++ boundary counts updated")
  buildings_migration.update_data(c)
  log_helper.write_to_log(" ++ building counts updated")
  conn.commit()
  conn.close()



def request():
  r = service_calls_dob_request.make_request()
  log_helper.write_to_log(" ++ dob service calls added: " + str(r) + "\n")
  r = service_calls_hpd_request.make_request()
  log_helper.write_to_log(" ++ hpd service calls added: " + str(r) + "\n")
  r = violation_dob_request.make_request()
  log_helper.write_to_log(" ++ dob violations added: " + str(r) + "\n")
  r = violation_ecb_request.make_request()
  log_helper.write_to_log(" ++ ecb violations added: " + str(r) + "\n")
  r = violation_hpd_request.make_request()
  log_helper.write_to_log(" ++ hpd violations added: " + str(r) + "\n")
  r = permit_request.make_request()
  log_helper.write_to_log(" ++ permits added: " + str(r) + "\n")


