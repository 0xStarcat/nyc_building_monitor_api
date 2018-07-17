import sqlite3

from requests_api import violation_dob_request
from requests_api import violation_ecb_request
from requests_api import violation_hpd_request
from requests_api import service_calls_dob_request
from requests_api import service_calls_hpd_request
from requests_api import service_calls_status_request
from requests_api import permit_request

from migrations import buildings_migration
from migrations import boundary_table_migrations

from helpers import log_helper
import config

def update_data():
  conn = sqlite3.connect(config.DATABASE_URL, timeout=10)
  c = conn.cursor()
  c.execute('pragma foreign_keys=on;')
  
  boundary_table_migrations.update_all(c, conn)
  log_helper.write_to_log(" ++ boundary counts updated" + "\n")
  # buildings_migration.update_data(c)
  # log_helper.write_to_log(" ++ building counts updated" + "\n")
  conn.commit()
  conn.close()

def check_call_statuses():
  service_calls_status_request.check_statuses()


def request():
  conn = sqlite3.connect(config.DATABASE_URL, timeout=10)

  r = service_calls_dob_request.make_request(conn)
  log_helper.write_to_log(" ++ dob service calls added: " + str(r) + "\n")
  r = service_calls_hpd_request.make_request(conn)
  log_helper.write_to_log(" ++ hpd service calls added: " + str(r) + "\n")
  r = violation_dob_request.make_request(conn)
  log_helper.write_to_log(" ++ dob violations added: " + str(r) + "\n")
  r = violation_ecb_request.make_request(conn)
  log_helper.write_to_log(" ++ ecb violations added: " + str(r) + "\n")
  r = violation_hpd_request.make_request(conn)
  log_helper.write_to_log(" ++ hpd violations added: " + str(r) + "\n")
  r = permit_request.make_request(conn)
  log_helper.write_to_log(" ++ permits added: " + str(r) + "\n")
  conn.commit()
  conn.close()


