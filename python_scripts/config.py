import os

ROOT_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, '..'))) # This is your Project Root
DATABASE_URL = os.path.abspath(os.path.join(ROOT_DIR, 'nyc_data_map.sqlite'))
DATABASE_BACKUP_URL = os.path.abspath(os.path.join(ROOT_DIR, 'nyc_data_map.backup.sqlite'))
DATABASE_TEMP_URL = os.path.abspath(os.path.join(ROOT_DIR, 'nyc_data_map.temp.sqlite'))
TEST_DB_URL = os.path.abspath(os.path.join(ROOT_DIR, 'test_db.sqlite'))

LOG_URL = os.path.abspath(os.path.join(ROOT_DIR, 'python_scripts/log/log.txt'))
VIOLATIONS_CSV_URL = os.path.abspath(os.path.join(ROOT_DIR, 'data/violations_data/csv/nyc_violations_data.csv'))
PERMITS_CSV_URL = os.path.abspath(os.path.join(ROOT_DIR, 'data/permit_data/csv/nyc_permits_data.csv'))
SERVICE_CALLS_CSV_URL = os.path.abspath(os.path.join(ROOT_DIR, 'data/service_calls_data/csv/nyc_service_calls_data.csv'))
EVICTIONS_CSV_URL = os.path.abspath(os.path.join(ROOT_DIR, 'data/evictions_data/csv/nyc_evictions_data.csv'))
