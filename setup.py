from getpass    import getuser
from os         import system, getcwd, path
from sys        import exit, platform


def installLinux(user):
  print("Install...")
  try:
    system("cd %s && cp -R .java.py /home/%s && echo 'alias jpy=\"python3 /home/%s/.java.py/main.py\"' > /home/%s/.bash_aliases" % (getcwd(), user, user,user))
    print("Copy files complete...")
  except:
    print("Copy files error!")

  print("Install complete...\nwrite jpy --help to help")

def installWindows(user):
  print("Установка для вашей системы временно не возможна")
  exit()

if "linux" in platform:
  cmd = input("Do you want to install 'Pys'? (Д,н) ")
  if cmd == "Y" or cmd == "y" or cmd == "Д" or cmd == "д":
    installLinux(getuser())
  else:
    print("Install exit")
    exit()
