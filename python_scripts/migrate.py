from migrations import db_migrate

print ("migrating...")
db_migrate.migrate()