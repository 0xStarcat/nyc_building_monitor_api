import csv
import xlrd

def fix_brooklyn_csv():
  filename = "data/sales_data/csv/brooklyn_sales_2010-2017-backup.csv"
  writer = csv.writer(open("data/sales_data/csv/brooklyn_sales_2010-2017.csv", "a"))
  
  rows = list(csv.reader(open(filename)))
  writer.writerow(rows[0])
  
  for row in rows[1:]:
    try:
      row[20] = datetime.datetime.strptime(row[20], "%m/%d/%y").strftime("%m/%d/%Y")
    except ValueError as e:
      row[20] = datetime.datetime.strptime(row[20], "%m/%d/%Y").strftime("%m/%d/%Y")
    
    writer.writerow(row)

def merge_csv():
  years = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017"]
  boroughs = ["manhattan", "bronx", "queens", "statenisland"]

  for borough in boroughs:
    filename = "data/sales_data/csv/"+borough+"_sales_2010-2017.csv"
    writer = csv.writer(open(filename, "a"))

    for year in years:
      print("Writing ", borough, year, filename)
      xls_book = xlrd.open_workbook("data/sales_data/"+year+"_"+borough+".xls")
      sheet = xls_book.sheets()[0]

      row_start = 3 if year == "2010" else 5
      for index, row in enumerate(range(sheet.nrows)[row_start:]):
        parsed_row = sheet.row_values(row)
        
        if year == "2010" and index == 0:
          writer.writerow(parsed_row)
        else:
          year, month, day, hour, minute, second = xlrd.xldate_as_tuple(parsed_row[len(parsed_row) - 1], xls_book.datemode)
          py_date = datetime.datetime(year, month, day, hour, minute, second).strftime("%m/%d/%Y")
          parsed_row = parsed_row[:-1] + [py_date]
          writer.writerow(parsed_row)

def create_master_csv():
  filename = "data/sales_data/csv/nyc_sales_2010-2017.csv"
  writer = csv.writer(open(filename, "a"))
  for row in list(csv.reader(open("data/sales_data/csv/bronx_sales_2010-2017.csv"))):
    writer.writerow(row)
  for row in list(csv.reader(open("data/sales_data/csv/brooklyn_sales_2010-2017.csv")))[1:]:
    writer.writerow(row)
  for row in list(csv.reader(open("data/sales_data/csv/manhattan_sales_2010-2017.csv")))[1:]:
    writer.writerow(row)
  for row in list(csv.reader(open("data/sales_data/csv/queens_sales_2010-2017.csv")))[1:]:
    writer.writerow(row)
  for row in list(csv.reader(open("data/sales_data/csv/statenisland_sales_2010-2017.csv")))[1:]:
    writer.writerow(row)
