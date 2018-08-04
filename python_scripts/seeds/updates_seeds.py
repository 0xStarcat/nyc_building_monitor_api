import datetime

table = "updates"
col1 = "date"
col2 = "new_violations"
col3 = "new_service_calls"
col4 = "resolved_violations"
col5 = "resolved_service_calls"

def create_table(c):
  c.execute('CREATE TABLE IF NOT EXISTS {tn} (id INTEGER PRIMARY KEY AUTOINCREMENT)'.format(tn=table))

  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} TEXT".format(tn=table, cn=col1))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col2))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col3))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col4))
  c.execute("ALTER TABLE {tn} ADD COLUMN {cn} INT".format(tn=table, cn=col5))
  
def new_empty_entry(c, date):
  parsed_date = datetime.datetime.strptime(date, '%Y%m%d%H%M%S').strftime("%Y%m%d%H%M%S")

  c.execute('INSERT INTO {tn} ({col}) VALUES(?)'.format(tn=table, col=col1), str(parsed_date))

def new_entry(c, entry_data):
  parsed_date = datetime.datetime.strptime(entry_data["date"], '%Y%m%d%H%M%S').strftime("%Y%m%d%H%M%S")
  new_violations = int(entry_data["new_violations"])
  new_service_calls = int(entry_data["new_service_calls"])
  resolved_violations = int(entry_data["resolved_violations"])
  resolved_service_calls = int(entry_data["resolved_service_calls"])

  c.execute('INSERT INTO {tn} ({col1}, {col2}, {col3}, {col4}, {col5}) VALUES(?, ?, ?, ?, ?)'.format(tn=table, col1=col1, col2=col2, col3=col3, col4=col4, col5=col5), (str(parsed_date), new_violations, new_service_calls, resolved_violations, resolved_service_calls))
