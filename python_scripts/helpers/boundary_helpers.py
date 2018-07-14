import json
from shapely.geometry import shape, Point

def get_record_from_coordinates(geometry, records, geo_index):
  match = next((record for record in records if shape(json.loads(record[geo_index])).contains(Point(shape(geometry).representative_point()))), False) 
  if match:
    return match
  else:
    return None

