import re

bEnableMainLog = True
bEnableConsoleLog = False

#Setup
sSetServerPath = None
sSetResultFilesPath = None
sSetLogFilesPath = None

# Tests
sSetListOfFiles = []

def ptest_setup_xml_parser(xmldatalist):

    global bEnableMainLog
    global bEnableConsoleLog
    global sSetServerPath
    global sSetResultFilesPath
    global sSetLogFilesPath

    bEnableMainLog = bool(re.match(str(xmldatalist.get('enableMainLog')), 'true', re.IGNORECASE))
    bEnableConsoleLog = bool(re.match(str(xmldatalist.get('enableConsoleLog')), 'true', re.IGNORECASE))

    sSetServerPath = xmldatalist.get('setServerPath')
    sSetResultFilesPath = xmldatalist.get('setResultFilePath')
    sSetLogFilesPath = xmldatalist.get('setLogFilePath')

def ptest_tests_xml_parser(xmldatalist):

    global sSetListOfFiles
    sSetListOfFiles = list((xmldatalist.get('output files')).split(','))