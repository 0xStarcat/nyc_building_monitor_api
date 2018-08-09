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

  for index in range(len(results)):
    if index % 1000:
      print("updating building " + str(index) + '/' + str(len(results)))

    # Violations
    c.execute('SELECT COUNT(ALL) FROM violations WHERE building_id={id}'\
      .format(id=results[index][0]))

    violations_count = c.fetchone()[0]

    c.execute('UPDATE {tn} SET {cn}={value} WHERE id={id}'\
      .format(tn=table, cn=col1, value=violations_count, id=results[index][0]))

    # service calls

    c.execute('SELECT open_over_month FROM service_calls WHERE building_id={id}'\
      .format(id=results[index][0]))

    service_calls = c.fetchall()
    service_calls_events_count = len(service_calls)

    c.execute('UPDATE {tn} SET {cn}=\"{value}\" WHERE id={id}'\
      .format(tn=table, cn=col2, value=service_calls_events_count, id=results[index][0]))

    # service calls open over month
    
    service_calls_open_over_month = 0

    for sc_index in range(len(service_calls)):
      if service_calls[sc_index][0] == True:
        service_calls_open_over_month += 1

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
      .format(tn=table, cn=col3, value=service_calls_open_over_month, id=results[index][0]))

    # Average days to resolve service call

    c.execute('SELECT AVG(days_to_close) FROM service_calls WHERE building_id={id} AND days_to_close NOT NULL'\
      .format(id=results[index][0]))

    average = c.fetchone()[0] or None

    c.execute('UPDATE {tn} SET {cn} = ? WHERE id=?'\
      .format(tn=table, cn=col4), (average, results[index][0]))


