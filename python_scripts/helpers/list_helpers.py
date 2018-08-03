def find_matches_and_remove(list1, list2, match_key1, match_key2):
  original_count = len(list1)
  list2a = list(filter(lambda x: x["agency"].lower() == "dob", list2))
  list2b = list(filter(lambda x: x["agency"].lower() == "hpd", list2))

  for index in range(len(list1) - 1, 0, -1):
    if index % 250 == 0:
      print("Remaining: " + str(index) + ' starting:' + str(original_count))
    else:
      pass
    # make smaller lists for speed
    
    if list1[index][5].lower() == "dob":
      match = next((row for row in list2a if list1[index][match_key1] == row[match_key2]), False) 
    elif list1[index][5].lower() == "hpd":
      match = next((row for row in list2b if list1[index][match_key1] == row[match_key2]), False) 
    else:
      print("couldn't find source")
      match = next((row for row in list2 if list1[index][match_key1] == row[match_key2]), False) 

    if match:
      print("  * Match found, removing: ", str(index) + "/" + str(original_count))
      list1.remove(list1[index])
    # list2.remove(match)
    else:
      continue