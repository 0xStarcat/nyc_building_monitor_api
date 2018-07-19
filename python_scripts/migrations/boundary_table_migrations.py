tables = ['census_tracts', 'neighborhoods', 'community_districts', 'boroughs']

col1 = 'total_violations'
col2 = 'total_sales'
col3 = 'total_permits' # new building permit (permit_type NB) only
col4 = 'total_service_calls'
col5 = 'total_service_calls_with_violation_result'
col6 = 'total_service_calls_with_no_action_result'
col7 = 'total_service_calls_unable_to_investigate_result'
col8 = 'total_service_calls_open_over_month'
col9 = 'service_calls_average_days_to_resolve'

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
    column_name = 'community_district_id'
  if table == tables[3]:
    column_name = 'borough_id'

  c.execute('SELECT * FROM {tn}'\
    .format(tn=table))
  
  results = c.fetchall()
  
  for index, row in enumerate(results):
    print(table + " - updating row " + str(index) + '/' + str(len(results)))

    # Violations
    c.execute('SELECT * FROM building_events WHERE eventable=\'{event}\' AND {cn}={id}'\
      .format(event='violation', cn=column_name, id=row[0]))

    violations_count = len(c.fetchall())

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
      .format(tn=table, cn=col1, value=violations_count, id=row[0]))

    # sales

    c.execute('SELECT * FROM building_events WHERE eventable=\'{event}\' AND {cn}={id}'\
      .format(event='sale', cn=column_name, id=row[0]))

    sales_count = len(c.fetchall())

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
      .format(tn=table, cn=col2, value=sales_count, id=row[0]))

    # permits

    c.execute('SELECT * FROM permits WHERE {cn}={id} AND {cn2}=\'{type}\''\
      .format(event='permit', cn=column_name, cn2='permit_type', id=row[0], type='NB'))

    permits_count = len(c.fetchall())

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
      .format(tn=table, cn=col3, value=permits_count, id=row[0]))

    # service calls

    c.execute('SELECT * FROM building_events WHERE eventable=\'{event}\' AND {cn}={id}'\
      .format(event='service_call', cn=column_name, id=row[0]))

    service_calls = c.fetchall()
    service_calls_count = len(service_calls)

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
      .format(tn=table, cn=col4, value=service_calls_count, id=row[0]))

    # service calls with result
    
    service_calls_violation_result_count = 0
    service_calls_no_action_result_count = 0
    service_calls_unable_to_investigate_result_count = 0
    service_calls_open_over_month = 0

    for event in service_calls:
      c.execute('SELECT * FROM service_calls WHERE id={id}'.format(id=event[7])) # find service call by eventable_id of building_event
      entry = c.fetchone()
      if entry[5] == True:
        service_calls_violation_result_count += 1
      elif entry[6] == True:
        service_calls_no_action_result_count += 1
      elif entry[7] == True:
        service_calls_unable_to_investigate_result_count += 1
      elif entry[10] == True:
        service_calls_open_over_month += 1

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
      .format(tn=table, cn=col5, value=service_calls_violation_result_count, id=row[0]))
    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
      .format(tn=table, cn=col6, value=service_calls_no_action_result_count, id=row[0]))
    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
      .format(tn=table, cn=col7, value=service_calls_unable_to_investigate_result_count, id=row[0]))
    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
      .format(tn=table, cn=col8, value=service_calls_open_over_month, id=row[0]))

    # Average days to resolve service call

    c.execute('SELECT AVG(days_to_close) from service_calls WHERE {cn} = {id} AND days_to_close IS NOT NULL'\
      .format(cn=column_name, id=row[0]))

    average = c.fetchone()

    c.execute('UPDATE {tn} SET {cn} = {value} WHERE id={id}'\
      .format(tn=table, cn=col9, value=average, id=row[0]))

