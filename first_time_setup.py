import os 

existing_python_path = os.environ.get("PYTHONPATH")


#if the path does not exist, create the python path and add the framework
if not existing_python_path:
  os.environ['PYTHONPATH'] = os.getcwd()

#if the path exists, append the framework to the end.  If the framework is already there, return
else:
  if os.getcwd() in existing_python_path:
    return
  os.environ['PYTHONPATH'] = existing_python_path + ";" + os.getcwd()
