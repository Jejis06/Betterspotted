import os
from sys import platform
import subprocess

installnode= False

print("[Checking node]")
result = subprocess.run(['node', '-v'], stdout=subprocess.PIPE)
if (str(result.stdout.decode('utf-8')) != str(result.stdout.decode('utf-8')).replace('v',"")):
    installnode= True

if installnode:
   if (platform.system()== "Linux"):
        print("[Installing node]")
        os.system("sudo apt install curl")
        os.system("curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -")
        os.system("sudo apt-get install -y nodejs")
   else:
       print("[Install node from here : https://nodejs.org/en/download/]")
print("[installing modules]")
os.system("npm install tough-cookie-filestore2")
os.system("npm install instagram-web-api")
os.system("npm install dotenv --save")
print("[installing python modules]")
os.system("pip install subprocess PIL numpy textwrap flask colorsys json colorama datetime atexit apscheduler")






