import os, json

def traverse(path):
  result = []
  try:
    for dir in next(os.walk(path + "."))[1]:
      test_data_file_path = path + dir + "/test.json"
      if os.path.isfile(test_data_file_path):
        with open(test_data_file_path, 'r') as test_data_file:
          test_data = json.load(test_data_file)
          test_data["directory"] = str(path+dir)
          if (test_data["active"]):
            result.append(test_data)
      result.extend(traverse(path+dir+"/"))
    return result
  except StopIteration:
    return result

tests = traverse("eo-tests/")
matrix = {}
matrix["include"] = tests

print("::set-output name=matrix::" + json.dumps(matrix))