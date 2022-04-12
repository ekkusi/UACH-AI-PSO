import numpy as np
import json

data = None
# Correct rounds_to_best_average values
with open("results_ea.json") as json_file:
  print("Reading data")
  data = json.load(json_file)
  for result in data["results"]:
    rounds_to_best_list = list(map(lambda r: r["rounds_to_best"], result["simulation_results"]))
    result["rounds_to_best_average"] = round(np.average(rounds_to_best_list))
  print("Data read")
  data = data["results"]
with open("results_ea_fixed.json", "w") as outfile:
  print("Writing data")
  json_string = json.dumps(data, indent=4)
  outfile.write(json_string)
  print("Json data written")