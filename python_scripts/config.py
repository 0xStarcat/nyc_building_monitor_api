import os

ROOT_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))  # This is your Project Root
DATABASE_URL = os.path.abspath(os.path.join(ROOT_DIR, 'nyc_data_map.sqlite'))
DATABASE_BACKUP_URL = os.path.abspath(os.path.join(ROOT_DIR, 'nyc_data_map.backup.sqlite'))
DATABASE_TEMP_URL = os.path.abspath(os.path.join(ROOT_DIR, 'nyc_data_map.temp.sqlite'))
TEST_DB_URL = os.path.abspath(os.path.join(ROOT_DIR, 'test_db.sqlite'))

LOG_URL = os.path.abspath(os.path.join(ROOT_DIR, 'python_scripts/log/log.txt'))
VIOLATIONS_CSV_URL = os.path.abspath(os.path.join(ROOT_DIR, 'data/violations_data/csv/nyc_violations_data.csv'))
PERMITS_CSV_URL = os.path.abspath(os.path.join(ROOT_DIR, 'data/permit_data/csv/nyc_permits_data.csv'))
SERVICE_CALLS_CSV_URL = os.path.abspath(os.path.join(
    ROOT_DIR, 'data/service_calls_data/csv/nyc_service_calls_data.csv'))
EVICTIONS_CSV_URL = os.path.abspath(os.path.join(ROOT_DIR, 'data/evictions_data/csv/nyc_evictions_data.csv'))

# Data

BOROUGHS_DATA = os.path.abspath(os.path.join(ROOT_DIR, 'data/boundary_data/boroughs.geojson'))
NEIGHBORHOODS_DATA = os.path.abspath(os.path.join(ROOT_DIR, 'data/boundary_data/neighborhoods.geojson'))
CENSUS_TRACTS_DATA = os.path.abspath(os.path.join(ROOT_DIR, 'data/boundary_data/census_tracts_2010.geojson'))

INCOME_DATA = os.path.abspath(os.path.join(ROOT_DIR, 'data/income_data/censustract-medianhouseholdincome2017.csv'))
RENT_DATA = os.path.abspath(os.path.join(ROOT_DIR, 'data/rent_data/censustract-medianrentall2017.csv'))
RACE_DATA = os.path.abspath(os.path.join(ROOT_DIR, 'data/race_data/pop_race2010_ct.csv'))

MN_BUILDINGS_DATA = os.path.abspath(os.path.join(ROOT_DIR, 'data/buildings_data/mn_mappluto.geojson'))
BK_BUILDINGS_DATA = os.path.abspath(os.path.join(ROOT_DIR, 'data/buildings_data/bk_mappluto.geojson'))
BX_BUILDINGS_DATA = os.path.abspath(os.path.join(ROOT_DIR, 'data/buildings_data/bx_mappluto.geojson'))
SI_BUILDINGS_DATA = os.path.abspath(os.path.join(ROOT_DIR, 'data/buildings_data/si_mappluto.geojson'))
QN_BUILDINGS_DATA = os.path.abspath(os.path.join(ROOT_DIR, 'data/buildings_data/qn_mappluto.geojson'))
