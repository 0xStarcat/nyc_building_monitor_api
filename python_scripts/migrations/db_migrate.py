import sqlite3

import neighborhoods_migration
import census_tracts_migration
import buildings_migration

sqlite_file = 'bk_building_violation_project.sqlite'

conn = sqlite3.connect(sqlite_file, timeout=10)
c = conn.cursor()
c.execute('pragma foreign_keys=on;')

# neighborhoods_migration.migrate_neighborhoods_data(c)
# census_tracts_migration.migrate_census_tracts_data(c)
# buildings_migration.migrate_buildings_data(c)


conn.commit() 

c.execute('SELECT * FROM census_tracts')

results = c.fetchall()
print(results[0])