import os

def log_is_empty():
  return os.stat("../log/log.txt").st_size == 0

def write_to_log(string):
  with open("python_scripts/log/log.txt", "a") as log_file:
    log_file.write(string)