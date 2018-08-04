import sqlite3
import config
import context

sqlite_file = config.DATABASE_URL

def migrate():
  conn = sqlite3.connect(sqlite_file, timeout=10)
  c = conn.cursor()
  c.execute('pragma foreign_keys=on;')
  c.execute('pragma recursive_triggers=on')

  create_updates_table(c)


def create_updates_table(c):
  print("creating updates table")
  try:
    context.updates_seeds.create_table(c)
  except Exception as error:
    print(error)
    raise error