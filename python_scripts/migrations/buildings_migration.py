table = 'buildings'

col1 = 'total_violations'
col2 = 'total_service_calls'
col3 = 'total_service_calls_open_over_month'
col4 = 'service_calls_average_days_to_resolve'
col5 = 'total_sales'

def update_data(c):
  print("Updating buildings")
  c.execute('SELECT * FROM {tn}'\
    .format(tn=table))

  results = c.fetchall()

  for index, row in enumerate(results):
    print("updating row " + str(index) + '/' + str(len(results)))

    # Violations
    c.execute('SELECT * FROM building_events WHERE eventable=\'{event}\' AND building_id={id}'\
      .format(event='violation', id=row[0]))

    violations_count = len(c.fetchall())

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
      .format(tn=table, cn=col1, value=violations_count, id=row[0]))

    # service calls

    c.execute('SELECT * FROM building_events WHERE eventable=\'{event}\' AND building_id={id}'\
      .format(event='service_call', id=row[0]))

    service_calls_events = c.fetchall()
    service_calls_events_count = len(service_calls_events)

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
      .format(tn=table, cn=col2, value=service_calls_events_count, id=row[0]))

    # service calls with result
    
    service_calls_open_over_month = 0

    for event in service_calls_events:
      c.execute('SELECT * FROM service_calls WHERE id={id}'.format(id=event[6]))
      entry = c.fetchone()

      if entry[11] == True:
        service_calls_open_over_month += 1
    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
      .format(tn=table, cn=col3, value=service_calls_open_over_month, id=row[0]))

    # Average days to resolve service call

    c.execute('SELECT AVG(days_to_close) FROM building_events JOIN service_calls ON building_events.eventable_id = service_calls.id WHERE {cn} = {id} AND eventable="service_call" AND days_to_close NOT NULL'\
      .format(cn='building_events.building_id', id=row[0]))

    average = c.fetchone()[0] or None

    c.execute('UPDATE {tn} SET {cn} = ? WHERE id=?'\
      .format(tn=table, cn=col4), (average, row[0]))


     # # sales

    # c.execute('SELECT * FROM building_events WHERE eventable=\'{event}\' AND building_id={id}'\
    #   .format(event='sale', id=row[0]))

    # sales_count = len(c.fetchall())

    # c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
    #   .format(tn=table, cn=col2, value=sales_count, id=row[0]))

