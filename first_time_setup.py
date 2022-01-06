import os 

existing_python_path = os.environ.get("PYTHONPATH")

if not existing_python_path:
  os.environ['PYTHONPATH'] = os.getcwd()
  
else:
  os.environ['PYTHONPATH'] = existing_python_path + ";" + os.getcwd()
