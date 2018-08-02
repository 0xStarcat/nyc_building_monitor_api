def migrate():
  conn = sqlite3.connect(sqlite_file, timeout=10)
  c = conn.cursor()
  c.execute('pragma foreign_keys=on;')
  c.execute('pragma recursive_triggers=on')

  create_updates_table(c)


def create_updates_table(c):
	try:
		context.updates_seeds.create_table(c)
	except:
		print("Table already exists. Skipping.")