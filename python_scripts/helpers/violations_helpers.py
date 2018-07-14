import datetime
now = datetime.datetime.now()

def calculate_average_for_year(violations, year):
  if int(now.year) == int(year):
    return round((len(violations) / percent_year_complete) / 12, 2)
  else:
    return round(len(violations) / 12, 2)

def calculate_violations_per_building(violationNum, buildingNum, year):
  if violationNum and buildingNum and year:
    if int(now.year) == int(year):
      return round((violationNum / percent_year_complete) / float(buildingNum), 2)
    else:
      return round(float(violationNum) / float(buildingNum), 2)
  else:
    print("Missing value: " + str(violationNum) + " - " + str(buildingNum) + " - " + str(year))

def match_boundary_to_building_num(boundary, boundary_key, buildings_data):
  match = next((neighborhood for neighborhood in buildings_data if neighborhood[0] == boundary[boundary_key]), [])

  if len(match) > 0:
    return match[1]
  else: 
    print("  * couldn't match neighborhood to building data. please check! : " + boundary[boundary_key])

def calculate_average_violations_total(violations_per_building, year_data):
  average = 0
  for number in violations_per_building:
    average += float(number)

  average = round(average / len(year_data), 2)
  return average