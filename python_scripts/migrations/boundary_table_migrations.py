tables = ['census_tracts', 'neighborhoods', 'boroughs']

col1 = 'total_violations'
col2 = 'total_service_calls'
col3 = 'total_service_calls_open_over_month'
col4 = 'service_calls_average_days_to_resolve'
col5 = 'total_sales'
col6 = 'total_permits' # new building permit (permit_type NB) only
col7 = 'total_evictions'

def update_all(c, conn):
  for table in tables:
    print("Updating " + table + "...")
    update_data(c, table)
    conn.commit()

def update_data(c, table):
  if table == tables[0]:
    column_name = 'census_tract_id'
  if table == tables[1]:
    column_name = 'neighborhood_id'
  if table == tables[2]:
    column_name = 'borough_id'

  c.execute('SELECT * FROM {tn}'\
    .format(tn=table))
  
  results = c.fetchall()
  
  for index, row in enumerate(results):
    print(table + " - updating row " + str(index) + '/' + str(len(results)))

    # Violations
    c.execute('SELECT id, COUNT(id) FROM building_events WHERE {cn}={id} AND eventable=\'{event}\''\
      .format(event='violation', cn=column_name, id=row[0]))

    violations_count = c.fetchone()[1]

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
      .format(tn=table, cn=col1, value=violations_count, id=row[0]))

    # service calls

    c.execute('SELECT * FROM building_events WHERE {cn}={id} AND eventable=\'{event}\''\
      .format(event='service_call', cn=column_name, id=row[0]))

    service_call_events = c.fetchall()
    service_call_events_count = len(service_call_events)
    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
      .format(tn=table, cn=col2, value=service_call_events_count, id=row[0]))

    # service calls with result
    
    service_calls_open_over_month = 0

    for event in service_call_events:
      c.execute('SELECT * FROM service_calls WHERE id={id}'.format(id=event[6])) # find service call by eventable_id of building_event
      service_call = c.fetchone()

      if not service_call:
        print("Entry not found", event)
        continue

      if service_call[11] == True:
        service_calls_open_over_month += 1

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
      .format(tn=table, cn=col3, value=service_calls_open_over_month, id=row[0]))

    # Average days to resolve service call

    c.execute('SELECT AVG(days_to_close) FROM building_events JOIN service_calls ON building_events.eventable_id = service_calls.id WHERE {cn} = {id} AND eventable="service_call" AND days_to_close NOT NULL'\
      .format(cn=column_name, id=row[0]))

    average = c.fetchone()[0] or None

    c.execute('UPDATE {tn} SET {cn} = ? WHERE id=?'\
      .format(tn=table, cn=col4), (average, row[0]))

    # sales

    # c.execute('SELECT id, COUNT(id) FROM building_events WHERE {cn}={id} AND eventable=\'{event}\''\
    #   .format(event='sale', cn=column_name, id=row[0]))

    # sales_count = c.fetchone()[1]

    # c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
    #   .format(tn=table, cn=col5, value=sales_count, id=row[0]))


    # permits

    # c.execute('SELECT id, COUNT(id) FROM permits WHERE {cn}={id} AND {cn2}=\'{type}\''\
    #   .format(event='permit', cn=column_name, cn2='permit_type', id=row[0], type='NB'))

    # permits_count = c.fetchone()[1]

    # c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
    #   .format(tn=table, cn=col6, value=permits_count, id=row[0]))


    # evictions

    # c.execute('SELECT * FROM building_events WHERE {cn}={id} AND eventable=\'{event}\''\
    #   .format(event='eviction', cn=column_name, id=row[0]))

    # evictions_count = len(c.fetchall())

    # c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
    #   .format(tn=table, cn=col10, value=evictions_count, id=row[0]))

