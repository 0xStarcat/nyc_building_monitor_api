import os

ROOT_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, '..'))) # This is your Project Root
DATABASE_URL = os.path.abspath(os.path.join(ROOT_DIR, 'nyc_data_map.sqlite'))
