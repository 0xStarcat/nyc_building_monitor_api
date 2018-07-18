import seed_db

print("running...")
seed_db.drop()
seed_db.seed()
print("complete.")