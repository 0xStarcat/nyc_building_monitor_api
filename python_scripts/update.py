import smtplib

import db_scripts
from helpers import log_helper

db_scripts.update()
log_helper.write_to_log("***\n")

fromaddr = "NYC Building Watcher"
toaddrs  = "jadeahking@gmail.com"

log = open("python_scripts/log/log.txt", "r").read().split("***")
print(log)
msg = log[len(log) - 2]

print(msg)
print("Message length is", len(msg))

server = smtplib.SMTP('localhost')
server.set_debuglevel(1)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()