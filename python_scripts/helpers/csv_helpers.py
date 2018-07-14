import json
import csv
import os

def clear_csv(out_file):
  f = open(out_file, "w+")
  f.close()

def write_csv(c, json_data, out_file, write_header):
  writer = csv.writer(open(out_file, "a"))

  # is CSV empty?
  if write_header and os.stat(out_file).st_size == 0:
    headers = ["borough", "community district", "neighborhood", "census tract"]
    for attr in json_data:
      headers.append(attr)
    writer.writerow(headers)

  row_attributes = []
  for attr in json_data:
    row_attributes.append(json_data[attr])

  writer.writerow(row_attributes)
