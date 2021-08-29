import sys
import json
from run_compilation_test import run_compilation_test
from run_runtime_test import run_runtime_test

test_dir = sys.argv[1]
environment = sys.argv[2]
with open(test_dir + "/test.json", 'r') as test_data_file:
  test_data = json.load(test_data_file)
  test_data["directory"] = test_dir

type = test_data["type"]
if type == "compilation":
  run_compilation_test(test_data, environment)
elif type == "runtime":
  run_runtime_test(test_data, environment)
elif type == "compilation-speed-test":
  run_compilation_test(test_data, environment, True)
else:
  raise TypeError(f"Uknown Test Type:\"{type}\"!")