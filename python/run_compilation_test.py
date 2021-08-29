import os, shutil, subprocess
import glob

def run_compilation_test(test, environment, speed_test=False):
  if environment == "hse":
    dest_dir = "environments/hse-environments/compilation-tests-environment"
  elif environment == "cqfn":
    dest_dir = "environments/cqfn-environments/compilation-tests-environment"
  else:
    raise TypeError(f"Uknown Compilation Environment \"{environment}\"!")

  for filename in glob.glob(os.path.join(test["directory"], '*.*')):
    if os.path.isfile(filename):
      shutil.copy(filename, dest_dir + "/eo")

  subprocess.run(["ls", "-la", f"{dest_dir}/eo"])

  command = ["mvn", "clean", "compile", "--file", dest_dir + '/pom.xml']
  if speed_test:
    command.insert(0, "time")
    
  completed_compilation_process = subprocess.run(command, text=True, capture_output=True, encoding="utf-8")

  if completed_compilation_process.returncode == 0:
    actual_compilation_result = "ok"
  else:
    actual_compilation_result = "fail"
  
  if speed_test:
    expected_compilation_result = "ok"
  else:
    expected_compilation_result = test["result"]

  if expected_compilation_result != actual_compilation_result:
    raise AssertionError("Expected compilation result: \"" + str(expected_compilation_result) + "\", but got: \"" + str(actual_compilation_result) + "\".")
  else:
    if speed_test:
      print(actual_compilation_result.stdout)
    else:
      print("OK!")
