import numpy as np
import json

data = None
# Prepare data for csv convertion
with open("results_pso.json") as json_file:
  print("Reading data")
  data = json.load(json_file)
  for result in data:
    # Make all fields to the same level, no nesting. Remove simulation results as this is not needed for table
    result["best_fit"] = result["best_result"]["best_fit"]
    result["rounds_to_best"] = result["best_result"]["rounds_to_best"]
    result.pop("simulation_results", None)
    result.pop("best_result", None)
  print("Data read")
with open("results_pso_to_csv.json", "w") as outfile:
  print("Writing data")
  json_string = json.dumps(data, indent=4)
  outfile.write(json_string)
  print("Json data written")