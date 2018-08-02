import smtplib
import datetime
import config
import shutil
import os

import api_requests
from helpers import log_helper

username = os.environ(["BUILDING_MONITOR_EMAIL"])
password = os.environ(["BUILDING_MONITIR_EMAIL_PASSWORD"])

print(username)

shutil.copy(config.DATABASE_URL, config.DATABASE_BACKUP_URL)

log_helper.write_to_log(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + '\n')
api_requests.request(False)
# api_requests.check_call_statuses()
api_requests.update_data()


shutil.move(config.DATABASE_URL, config.DATABASE_TEMP_URL)
shutil.move(config.DATABASE_BACKUP_URL, config.DATABASE_URL)
os.remove(config.DATABASE_TEMP_URL)

log_helper.write_to_log("Database replaced\n")
log_helper.write_to_log("***\n")



fromaddr = "NYC Building Monitor"
toaddrs  = "jadeahking@gmail.com"

log = open("python_scripts/log/log.txt", "r").read().split("***")
print(log)
msg = log[len(log) - 2]

print(msg)
print("Message length is", len(msg))


server = smtplib.SMTP('smpt.gmail.com:587')
server.set_debuglevel(1)
server.starttls()
server.login(username, password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()