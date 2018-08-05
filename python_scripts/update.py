import smtplib
import datetime
import sqlite3
import config
import shutil
import os
import context
import api_requests


print("Starting data update...")
shutil.copy(config.DATABASE_URL, config.DATABASE_BACKUP_URL)

context.log_helper.write_to_log(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + '\n')
new_entry_counts = api_requests.request(False)
status_update_counts = api_requests.check_call_statuses()
api_requests.update_data()

update_counts_data = { "date": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),**new_entry_counts, **status_update_counts}

conn = sqlite3.connect(config.DATABASE_BACKUP_URL, timeout=10)
c = conn.cursor()
context.updates_seeds.new_entry(c, update_counts_data)
conn.commit()

shutil.move(config.DATABASE_URL, config.DATABASE_TEMP_URL)
shutil.move(config.DATABASE_BACKUP_URL, config.DATABASE_URL)
os.remove(config.DATABASE_TEMP_URL)

context.log_helper.write_to_log("Database replaced\n")
context.log_helper.write_to_log("***\n")



username = os.environ["BUILDING_MONITOR_EMAIL"]
password = os.environ["BUILDING_MONITOR_EMAIL_PASSWORD"]
fromaddr = "NYC Building Monitor"
toaddrs  = "jadeahking@gmail.com"

log = open(config.LOG_URL, "r").read().split("***")
print(log)
msg = log[len(log) - 2]

print(msg)
print("Message length is", len(msg))


server = smtplib.SMTP('smtp.gmail.com:587')
server.set_debuglevel(1)
server.starttls()
server.login(username, password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()