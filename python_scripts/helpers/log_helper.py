import os
import config


def log_is_empty():
  return os.stat(config.LOG_URL).st_size == 0

def write_to_log(string):
  with open(config.LOG_URL, 'a') as log_file:
    log_file.write(string)