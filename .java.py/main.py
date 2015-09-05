#!/usr/bin/python3
from sys        import argv, dont_write_bytecode
from os         import listdir, system, getcwd, path
from re         import findall
from json       import loads, dumps
dont_write_bytecode = True

def runProject():
  if not path.isdir(getcwd()+"/.jpy"):
    print("Project not found!")
    return False 
  openData = open(getcwd()+"/.jpy/data.json")
  data = loads(openData.read())
  openData.close()

  translateCode(getcwd()+"/"+data["name"]+".jpy", data["name"])
  for name in data["classes"]:
    translateCode(getcwd()+"/"+name+".jpy")

  system("python3 -B "+getcwd()+"/"+data["name"]+".py")

def translateCode(filePath, main=False):
  openFile = open(filePath)
  code = openFile.read()
  openFile.close()

  for arr in findall(r"class (.*):", code):
    code = code.replace("def %s("%arr, "def __init__(")

  if main != False:
    code = autoImportClasses()+code
    code = "from sys import argv\n"+code+"\nif __name__ == \"__main__\": %s().main(argv)" % main

  createPythonFile(filePath, code)

def autoImportClasses():
  openData = open(getcwd()+"/.jpy/data.json")
  data = loads(openData.read())
  openData.close()

  imports = "\n"

  for cls in data["classes"]:
    fcls = filterPathToClass(cls)
    imports+="from %s import %s\n"%(fcls[1],fcls[0])
  imports+="\n"

  return imports

def filterPathToClass(path):
  fullPath = path
  path = path.split("/")
  result = ".".join(path)
  if len(path) == 1:
    fullPath = path[0]
  elif len(path) > 1:
    fullPath = path[-1]

  return [fullPath, result]

def createPythonFile(filePath, code):
  createFile = open(filePath[0:-3]+"py", "w")
  createFile.write(code)
  createFile.close()

def createProject(name):
  if len(name) < 2:
    print("Bad project name!")
    return False
  if path.isdir(getcwd()+"/.jpy"):
    print("Project is created!")
    return False

  system("cd %s && mkdir .jpy && cd .jpy && echo '{\"name\": \"%s\",\"classes\":[]}' > data.json" % (getcwd(), name))
  if not path.isfile(getcwd()+"/"+name+".jpy"):
    system("cd %s && echo 'class %s:\n\tdef main(self,args):\n\t\tprint(\"Hello world!\")' > %s.jpy" % (getcwd(), name, name))

  print("Project '%s' created!" % name)

def removeProject():
  if not path.isdir(getcwd()+"/.jpy"):
    print("Project not found!")
    return False 

  system("cd %s && rm .jpy/* && rmdir .jpy && rm *.py" % getcwd())

  if path.isdir(getcwd()+"/__pycache__"):
    system("cd %s && rm __pycache__/* && rmdir __pycache__" % getcwd())

  print("Project removed!")

def createClass(name):
  if len(name) < 2:
    print("Bad project name!")
    return False

  if not path.isdir(getcwd()+"/.jpy"):
    print("Project not defined!")
    return False

  fullName = name
  name = name.split("/")
  if len(name) == 1:
    name = name[0]
  elif len(name) > 1:
    name = name[-1]

  if not path.isfile(getcwd()+"/"+name+".jpy"):
    createClass = open(getcwd()+"/"+fullName+".jpy","w")
    createClass.write('class %s:\n\tdef %s(self):\n\t\tprint(\"Hello module!\")'%(name,name))
    createClass.close()

  openData = open(getcwd()+"/.jpy/data.json")
  data = loads(openData.read())
  openData.close()

  data["classes"].append(fullName)

  updateData = open(getcwd()+"/.jpy/data.json","w")
  updateData.write(dumps(data, indent=4))
  updateData.close()
  print("Class created!")

def removeClass(name):
  if len(name) < 2:
    print("Bad class name!")
    return False
  if not path.isdir(getcwd()+"/.jpy"):
    print("Project not found!")
    return False
  if not path.isfile(getcwd()+"/"+name+".jpy"):
    print("Class not found!")
    return False

  openData = open(getcwd()+"/.jpy/data.json")
  data = loads(openData.read())
  openData.close()

  del(data[data.index(name)])

  updateData = open(getcwd()+"/.jpy/data.json", "w")
  updateData.write(dumps(data, indent=4))
  updateData.close()

def createPackage(name):
  if not path.isdir(getcwd()+"/.jpy"):
    print("Project not found!")
    return False

  if path.isdir(getcwd()+"/"+name):
    print("Package is created!")
    return False

  system("cd %s && mkdir %s && cd %s && echo '#init file'> __init__.py" % (getcwd(), name, name))
  print("Project created!")

def removePackage(name):
  if not path.isdir(getcwd()+"/.jpy"):
    print("Project not found!")
    return False

  if not path.isdir(getcwd()+"/"+name):
    print("Package is created!")
    return False

  try:
    system("cd %s && rmdir %s" % (getcwd(), name))
  except:
    system("cd %s && rm -i %s/* && rmdir %s" % (getcwd(), name, name))
  print("Project removed!")

homeCmd = """Java.py v0.0.1(Apha) linux version.
--help - to get help information
Author: Roman Naumenko-Vahnitsky"""
helpCmd = """--init <name> - create project, <name> - name project
--run - run you project
--create class <class_name> - create new class/file
--create package <package_name> - create new package folder
--remove class <class_name> - remove class/file
--remove package <package_name> - remove package folder
--remove project <project_name> - remove project (.jpy files won't delete)"""

if len(argv) >= 2:
  if argv[1] == "--init":
    try:
      createProject(argv[2])
    except Exception as e:
      print("--init ERROR!\n",e)

  elif argv[1] == "--run":
    try:
      runProject()
    except Exception as e:
      print("--run ERROR!\n",e)

  elif argv[1] == "--create":
    try:
      if argv[2] == "class":
        createClass(argv[3])
      if argv[2] == "package":
        createPackage(argv[3])
    except Exception as e:
      print("--create ERROR!\n",e)

  elif argv[1] == "--remove":
    try:
      if argv[2] == "project":
        removeProject()
      elif argv[2] == "class":
        removeClass(argv[3])
      elif argv[2] == "package":
        removePackage(argv[3])
    except Exception as e:
      print("--remove ERROR!\n",e)

  elif argv[1] == "--help":
    print(helpCmd)

  else:
    print("This unknown me command")
else:
  print(homeCmd)