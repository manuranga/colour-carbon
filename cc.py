import sys
import subprocess
import signal
import re
from os import path
import json

process = None  # global var to hold carbon server process
colourMap = {"unknownLine": 6,
             "infoLog": 113,
             "warnLog": 184,
             "errorLog": 197,
             "debugLog": 183,
             "wireIn": 70,
             "wireOut": 58,
             "msg": 15,
             "exception": 168,
             "exceptionClass": 167,
             "exceptionLine": 161,
             "exceptionFile": 162,
             "time": 237}


def processLine(line):
    if line.startswith("["):
        processLogLine(line)
    elif line.startswith("\t") or re.match("[a-zA-Z][\w\.]*: ", line):
        processException(line)
    else:
        cPrint('unknownLine', line)


def processException(line):
    if line.startswith('\tat'):
        cPrint('exception', '\tat ')
        groups = re.search('at (.*)\(([^:]*)(:?.*)\)', line).groups()
        cPrint('exceptionClass', groups[0])
        cPrint('exception', '(')
        cPrint('exceptionFile', groups[1])
        if groups[2].startswith(':'):
            cPrint('exception', ':')
            cPrint('exceptionLine', groups[2][1:])
        cPrint('exception', ')')
        ePrint('\n')
    elif line.startswith('\t...'):
        cPrint('exception', line)
    else:
        pos = line.find(':')
        cPrint('exceptionClass', line[0:pos])
        cPrint('exception', line[pos:])


def processLogLine(line):
    time = line[1:24]
    level = line[26:32].strip()
    msgStart = line.find(" ", 34)
    topic = line[33:msgStart].strip()
    if topic.endswith("}"):
        topic = topic[:-1]
    msg = line[msgStart:]

    processTime(time)
    processTopic(level, topic)
    processMsg(topic, msg)


def processTime(time):
    cPrint("time", time[11:])
    ePrint(" ")


def processTopic(level, topic):
    if not topic == "wire":
        cPrint(level.lower() + "Log", topic)
        ePrint(" ")


def processMsg(topic, msg):
    if topic == "wire":
        direction = "In" if msg[2] == ">" else "Out"
        cPrint("wire" + direction, msg[2:])
    else:
        cPrint("msg", msg)


def ePrint(text):
    sys.stdout.write(text)


def cPrint(n, line):
    sys.stdout.write("[38;5;" + str(colourMap[n]) + "m" + line + "[0m")


def handler(signum=None, frame=None):
    print('Signal handler called with signal', signum)
    for line in iter(process.stdout.readline, ''):
        processLine(line)
    sys.exit(0)

########## Signal hooks ###########

for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
    signal.signal(sig, handler)

########## Load Config ############

configPath = path.join(path.expanduser("~"), ".ccrc", "config.json")
configPath = configPath if path.isfile(configPath) else path.join(path.dirname(path.realpath(__file__)), "config.json")

if path.isfile(configPath):
    config = json.load(open(configPath))
    colourMap = config['colourMap']

############## Main ###############

args = ["./bin/wso2server.sh"] + sys.argv[1:]
process = subprocess.Popen(args, stdout=subprocess.PIPE)
for line in iter(process.stdout.readline, ''):
    processLine(line)
