import sqlite3

import requests_api 
import migrations
import seeds

from helpers import log_helper
import config

def update_data():
  conn = sqlite3.connect(config.DATABASE_BACKUP_URL, timeout=10)
  c = conn.cursor()
  c.execute('pragma foreign_keys=on;')
  
  migrations.boundary_table_migrations.update_all(c, conn)
  log_helper.write_to_log(" ++ boundary counts updated" + "\n")
  migrations.buildings_migration.update_data(c)
  log_helper.write_to_log(" ++ building counts updated" + "\n")
  conn.commit()
  conn.close()

def check_call_statuses():
  conn = sqlite3.connect(config.DATABASE_BACKUP_URL, timeout=10)
  c = conn.cursor()
  c.execute('pragma foreign_keys=on;')

  total_closed_service_calls = requests_api.check_service_calls_status_request.check_statuses(c, conn)
  conn.commit()
  return { "total_closed_service_calls" : total_closed_service_calls }

def request(write_to_csv=False):
  conn = sqlite3.connect(config.DATABASE_BACKUP_URL, timeout=10)

  dob_service_call_count = requests_api.service_calls_dob_request.make_request(conn, write_to_csv)
  log_helper.write_to_log(" ++ dob service calls added: " + str(dob_service_call_count) + "\n")
  
  hpd_service_call_count = requests_api.service_calls_hpd_request.make_request(conn, write_to_csv)
  log_helper.write_to_log(" ++ hpd service calls added: " + str(hpd_service_call_count) + "\n")
  
  dob_violation_count = requests_api.violation_dob_request.make_request(conn, write_to_csv)
  log_helper.write_to_log(" ++ dob violations added: " + str(dob_violation_count) + "\n")
  
  ecb_violation_count = requests_api.violation_ecb_request.make_request(conn, write_to_csv)
  log_helper.write_to_log(" ++ ecb violations added: " + str(ecb_violation_count) + "\n")
  
  hpd_violation_count = requests_api.violation_hpd_request.make_request(conn, write_to_csv)
  log_helper.write_to_log(" ++ hpd violations added: " + str(hpd_violation_count) + "\n")
  
  # r = seeds.evictions_request.make_request(conn, write_to_csv)
  # log_helper.write_to_log(" ++ evictions added: " + str(r) + "\n")
  # r = seeds.permit_request.make_request(conn, write_to_csv)
  # log_helper.write_to_log(" ++ permits added: " + str(r) + "\n")
  
  conn.commit()
  conn.close()
  
  total_new_service_calls = dob_service_call_count + hpd_service_call_count
  total_new_violations = dob_violation_count + ecb_violation_count + hpd_violation_count
  
  return { "total_new_service_calls": total_new_service_calls, "total_new_violations": total_new_violations }


