import re,sys
#from common.PTest_common import cCommonDataConfig

class cXmlReaderMainDataObject(object):

    def __init__(self):
        self.messages = []
        self.sfunModuleName = ""
        self.sAliasModuleName = ""
        self.bTestEnable = False
        self.iTestID = 0

    def add_params(self, key, val):
        self.messages.append((key, val))

    def message_count(self):
        return len(self.messages)

class cXmlReaderParamList(object):

    def __init__(self):
        self.my_objects = []


def getXmlMainObject(xmlRootNode, objXmlObjectList):

    print('In PTest_xml_reader . getXmlMainObject(): %s ' % xmlRootNode.tag)
    iTestID = 0
    for child in xmlRootNode.getchildren():
        if child.tag == 'Module':
            iTestID = iTestID + 1
            objXmlDataObject = cXmlReaderMainDataObject()
            objXmlDataObject.sfunModuleName = child.attrib['Name']
            objXmlDataObject.sAliasModuleName = (child.attrib['AliasName'])
            objXmlDataObject.bTestEnable = (child.attrib['IsTestEnable'])
            objXmlDataObject.iTestID = iTestID
            for Params in child.getchildren():
                for Param in Params.getchildren():
                    objXmlDataObject.add_params(Param.attrib['name'], Param.text)

            objXmlObjectList.my_objects.append(objXmlDataObject)

        else:
            raise cCommonDataConfig.CustomException(1)

def getXmlParamDictionary(objXmlObjectList, testModuleName):
    try:
        print("objXmlObjectList : ", objXmlObjectList)
        print("testModuleName : ", testModuleName)
        for obj in objXmlObjectList.my_objects:
            if bool(re.search(testModuleName, str(obj.sfunModuleName), re.IGNORECASE)):

                # Create List Of Parameters of an Object sfunModuleName
                listOfTuplesToDict = dict(obj.messages)
                return listOfTuplesToDict

    except Exception as instance:
        raise MemoryError
