import os, shutil, subprocess
import glob

def run_runtime_test(test, environment):
  if environment == "hse":
    dest_dir = "environments/hse-environments/runtime-tests-environment"
  elif environment == "cqfn":
    dest_dir = "environments/cqfn-environments/runtime-tests-environment"
  else:
    raise TypeError(f"Uknown Environment for Runtime Tests \"{environment}\"!")

  for filename in glob.glob(os.path.join(test["directory"], '*.*')):
    if os.path.isfile(filename):
      shutil.copy(filename, dest_dir + "/eo")

  subprocess.run(["ls", "-la", f"{dest_dir}/eo"])

  expected_result = test["result"]
  completed_compilation_process = subprocess.run(["mvn", "clean", "compile", "--file", dest_dir + '/pom.xml'])

  if not completed_compilation_process.returncode == 0:
    if expected_result == "_fail":
      print("OK!")
      return
    else:
      raise AssertionError("This is a runtime test. Although the compilation of the test's sources failed!")

  completed_runtime_process = subprocess.run([dest_dir + "/run.sh"], text=True, capture_output=True, encoding="utf-8")
  if completed_runtime_process.returncode == 0 and expected_result == "_fail":
    raise AssertionError("This runtime test must have failed, although it run with no exceptions.")
  elif completed_runtime_process.returncode != 0 and expected_result != "_fail":
    print(completed_runtime_process.stderr)
    raise AssertionError("This runtime test must have run with no exceptions, however it failed.")
  elif completed_runtime_process.returncode == 0 and expected_result == "_ok":
    print("OK!")
    return
  else:
    real_result = completed_runtime_process.stdout
    if expected_result != real_result:
      raise AssertionError("Expected runtime result: \"" + str(expected_result) + "\", but got: \"" + str(real_result) + "\".")
    else:
      print("OK!")
      return