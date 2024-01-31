import os, sys
import time
import requests
import json
import logging
from PIL import Image

#from common.PTest_common import cCommonDataConfig
#from common.PTest_log import cPTest_log

LIMIT_RETRY = 2
retry_counter = 0

class cPTest_database:
    # cCommonDataConfig.ptest_model_name = "m8prime"
    # cCommonDataConfig.ptest_server_path = 'http://ptest.quanergy.com/'
    # cCommonDataConfig.qpnum = "QP5ADB"
    # cCommonDataConfig.ptest_process_json_path = 'http://ptest.quanergy.com/m8prime/automate/getfile/'
    # ptest_process_json_path = 'http://ptest.quanergy.com/m8prime/automate/getfile/QP5ADB'
    def __init__(self, serial_num, username, password, ptest_server_path, ptest_model_name):

        self.serial_num = serial_num
        self.qpnum = serial_num
        self.username = username
        self.password = password
        self.ptest_server_path = ptest_server_path
        self.reconnect = True
        self.ptest_model_name = ptest_model_name

        self ._connection = None

    def mPTest_database_check_connection(self, retry_counter=0):

        # Connection Path
        ptest_connect_path_user = self.ptest_server_path
        message = "In mPTest_database_check_connection(): Server path:{}".format(ptest_connect_path_user)
        # print(message)
        logging.info(message)

        # Check Connection to PTest
        if not self._connection:

            conn_status = {}

            try:

                # Request Database Connection
                headers = {'Content-Type': 'application/json'}
                self._connection = requests.get(ptest_connect_path_user, headers=headers)
                conn_status = self._connection.status_code

                # Raises Exception on Http Error
                self._connection.raise_for_status()

                # Return Connection to Database
                self._connection.autocommit = False

            except requests.exceptions.RequestException as error:
                if not self.reconnect or retry_counter >= LIMIT_RETRY:
                    raise SystemExit(error)
                else:
                    retry_counter += 1
                    message = "In mPTest_database_check_connection() : Got error: {}.reconnect:{}".format(error, retry_counter)
                    print(message)
                    logging.info(message)
                    time.sleep(3)
                    self.mPTest_database_check_connection(retry_counter)

            finally:

                if conn_status == 200:
                    message = "In mPTest_database_check_connection() : connection Status Successful :{}".format(conn_status)
                    logging.info(message)
                    print(message)
                elif conn_status == 404:
                    message = "In mPTest_database_check_connection() : Connection Failed. HTTP request Error:{}".format(conn_status.status_code)
                    logging.info(message)
                    print(message)
                else:
                    message = 'In mPTest_database_check_connection(): Connection Failed. Status Code:{}'.format(conn_status.status_code)
                    logging.info(message)
                    print(message)

        else:
            conn_status = self._connection.status_code

        return conn_status

    def mPTest_database_User_Authentication(self):

        logging.info("=====================================================================")
        logging.info("In mPTest_database_User_Authentication() : Authenticate User on PTest")
        logging.info("=====================================================================")

        getJsonFile = {}

        # URL Path
        ptest_verify_user_path = self.mPTest_database_verify_user_path()
        message = "In mPTest_database_User_Authentication(): path:{}".format(ptest_verify_user_path)
        print(message)
        logging.info(message)

        # Format Json data
        user_data = {"user": self.username, "pwd": self.password, "qpnum": self.serial_num}
        message = "In mPTest_database_User_Authentication(): Username:{}".format(self.username)
        print(message)
        logging.info(message)

        message = "In mPTest_database_User_Authentication(): Serial Number:{}".format(self.serial_num)
        print(message)
        logging.info(message)

        # Validate User on PTest
        if self.mPTest_database_check_connection() == 200:

            try:
                headers = {'Content-Type': 'application/json'}
                authentication_post_status = requests.post(ptest_verify_user_path , headers=headers, data=json.dumps(user_data))
                message = "In mPTest_database_User_Authentication(): connection Status:{}".format(authentication_post_status.status_code)
                print(message)
                logging.info(message)

                getJsonFile = authentication_post_status.json()

            except Exception as error:

                if authentication_post_status.status_code == 404:
                    message = "In mPTest_database_User_Authentication(): HTTP request Error:{}".format(authentication_post_status.status_code)
                    logging.error(message)
                else:
                    message = 'In mPTest_database_User_Authentication(): Connection Failed:{} Status Code:{}'.format(error,getJsonFile.status_code)
                    logging.error(message)

                raise SystemExit(error)

            finally:

                if 'err' in getJsonFile.keys():
                    if getJsonFile['err'] == "":
                        message = "In mPTest_database_User_Authentication(): Authentication Successful"
                        print(message)
                        logging.info(message)
                    else:
                        message = "In mPTest_database_User_Authentication(): Authentication Failed: {}".format(getJsonFile['err'])
                        logging.error(message)
                        print(message)
                        #QMessageBox.information(QMessageBox(), " Validation Error :{}".format(getJsonFile['err']))
                        #raise

            return getJsonFile

    def mPTest_database_get_json_process_file(self):

        logging.info("=============================================================================")
        logging.info(" In mPTest_database_get_json_process_file() :Get Master JSON File from PTest ")
        logging.info("=============================================================================")

        fullpath = self.mPTest_database_json_process_path()
        getJsonFile = {}

        message = "In mPTest_database_get_json_process_file(): Check Connection:{}".format(self.mPTest_database_check_connection())
        print(message)
        logging.info(message)

        if self.mPTest_database_check_connection() == 200:
            message = "0. In mPTest_database_get_json_process_file(): Master_json_process_path:{}".format(fullpath)
            logging.info(message)

            try:
                headers = {'Content-Type': 'application/json'}
                print(fullpath)
                getFileStatus = requests.get(fullpath, headers=headers)
                connectionStatus =  getFileStatus.status_code
                message = "1. In mPTest_database_get_json_process_file() : connection Status:{}".format(connectionStatus)
                logging.info(message)

                # Get JSON Process File
                getJsonFile = getFileStatus.json()
                print(getJsonFile)

                if 'err' in getJsonFile.keys() or len(getJsonFile) == 0:
                    message = "2. In mPTest_database_get_json_process_file(): Unknown Json file: {}".format(getJsonFile['err'])
                    logging.error(message)
                    # QMessageBox.information(QMessageBox(), "Error", "Unknown Json file:{}".format(getJsonFile['err']))
                    #return getJsonFile['err']
                else:
                    logging.info("In mPTest_database_get_json_process_file() : connection Successful")


            except requests.exceptions.RequestException as error:
                message = "In mPTest_database_get_json_process_file(): got error: {}".format(error)
                logging.error(message)
                #raise SystemExit(error)

            except Exception as error:
                if getJsonFile.status_code == 404:
                    message = "In mPTest_database_get_json_process_file(): HTTP request Error:{}".format(getJsonFile.status_code)
                    #print(message)
                    logging.error(message)
                else:
                    message ='In mPTest_database_get_json_process_file(): Connection Failed:{} Status Code:{}'.format(error, getJsonFile.status_code)
                    #print(message)
                    logging.error(message)

                #raise SystemExit(error)
                raise

        return getJsonFile, getJsonFile.keys()

    def mPTest_database_get_json_model_list(self, retry_counter=0):

        # Logging will not work here
        message = "In mPTest_database_get_json_model_list() : Get Model List File from PTest"
        print(message)

        fullpath = self.mPTest_database_json_model_path()
        print("In mPTest_database_get_json_model_list() : Model path: ", fullpath)

        get_model_list = {}
        conn_status_code = 404
        conn_status = False

        if self._connection.status_code == 200:

            if not conn_status:

                conn_status = {}

                try:
                    # Connect to PTest
                    headers = {'Content-Type': 'application/json'}
                    conn_status = requests.get(fullpath, headers=headers)
                    conn_status_code = conn_status.status_code

                    # Raises Exception on Http Error
                    conn_status.raise_for_status()

                    # Check Connection Status
                    if conn_status_code == 200:
                        message = "In mPTest_database_get_json_model_list() : connection Status Successful :{}".format(conn_status_code)
                        print(message)

                    # Fetch Model List from PTest
                    get_model_list = conn_status.json()
                    self.ptest_model_list = get_model_list
                    #return cCommonDataConfig.ptest_model_list

                except requests.exceptions.RequestException as error:
                    if not self.reconnect or retry_counter >= LIMIT_RETRY:
                        raise SystemExit(error)
                    else:
                        retry_counter += 1
                        print("In mPTest_database_get_json_model_list() : got error: {}.reconnect:{}".format(error, retry_counter))
                        time.sleep(3)
                        self.mPTest_database_get_json_model_list(retry_counter)

                finally:
                    if conn_status_code == 200:
                        message = "In mPTest_database_get_json_model_list() : connection Status Successful :{}".format(conn_status_code)
                        logging.info(message)
                        print(message)
                    elif conn_status_code == 404:
                        message = "In mPTest_database_get_json_model_list() : Connection Failed. HTTP request Error:{}".format(conn_status.status_code)
                        logging.info(message)
                        print(message)
                    else:
                        message = 'In mPTest_database_get_json_model_list(): Connection Failed Status Code:{}'.format(conn_status.status_code)
                        logging.info(message)
                        print(message)

                '''   except Exception as error:
                    if conn_status_code == 404:
                        print("In mPTest_database_get_json_model_list() : Connection Failed:{} .HTTP request Error :{}".format(error, conn_status_code))
                    else:
                        print('In mPTest_database_get_json_model_list(): Connection Failed:{} Status Code:{}'.format(error, conn_status_code))

                    raise SystemExit(error)'''

        return self.ptest_model_list

    def mPTest_database_post_json(self, process_name, subprocess_name, inputDataFrame):

        message = "In mPTest_database_post_json() : Push JSON File to PTest"
        print(message)
        logging.info(message)

        ptest_push_path = self.mPTest_database_post_path()
        message = "In mPTest_database_post_json(): path:{}".format(ptest_push_path)
        logging.info(message)

        # Format Json data
        json_data = {
            "user": self.username, "pwd": self.password,
            "process_data": {
                process_name: {
                    subprocess_name: inputDataFrame
                }
            }
        }

        json_dict = {'data': json.dumps(json_data)}
        files = {'file1': ""}

        # Push Json Data to PTest
        if self.mPTest_database_check_connection() == 200:
                try:
                    headers = {'Content-Type': 'application/json'}
                    connection_status = requests.get(ptest_push_path, headers=headers)
                    post_status = requests.post(ptest_push_path, data=json_dict, files=files)
                    message = "In mPTest_database_post_json(): connection Status:{}".format(connection_status.status_code)
                    logging.info(message)

                except requests.exceptions.RequestException as error:
                    message = "In mPTest_database_post_json() : got error: {}".format(error)
                    logging.info(message)
                    raise SystemExit(error)

        return post_status.json()

    def mPTest_database_post_file(self, process_name, subprocess_name, inputdataFiles, model):

        # logger = cPtest_log.logger()

        message = "In mPTest_database_post_data_file() : Push JSON File to PTest"
        print(message)
        logging.info(message)

        ptest_push_path = self.mPTest_database_post_path()
        # ptest_push_path = 'http://ptest-stage.corp.quanergy.com/m1/automate/updateprocessdata/' + "QP4A8B" + '/'
        message = "In mPTest_database_post_data_file(): path:{}".format(ptest_push_path)
        print(message)
        one_file_json = {
                "user": self.username, "pwd": self.password,
                "process_data": {
                    process_name: {
                        subprocess_name: {"value": "file1", "spec_bool": 1},
                    }
                }
            }

        if "Power_Calibration_Over_Temperature" in subprocess_name:
            # 1. Format Json data
            if model == "m8prime":
                json_data = {
                    "user": self.username, "pwd": self.password,
                    "process_data": {
                        process_name: {
                            "Generate_Ini": {"value": "file4", "spec_bool": 1},
                            subprocess_name:
                                {"Plots": {"Raw0": {"value": "file1", "spec_bool": 1},
                                           "Raw1": {"value": "file2", "spec_bool": 1},
                                           "Raw2": {"value": "file3", "spec_bool": 1}}
                                 }
                        }
                    }
                }
            elif model == "m1edge":
                json_data = {
                    "user": self.username, "pwd": self.password,
                    "process_data": {
                        process_name: {
                            "Generate_Ini": {"Beam7": "file4"},
                            subprocess_name:
                                {"Plots": {"Raw0": {"value": "file1", "spec_bool": 1},
                                           "Raw1": {"value": "file2", "spec_bool": 1},
                                           "Raw2": {"value": "file3", "spec_bool": 1}}
                                 }
                        }
                    }
                }
            elif model == "mq":
                json_data = {
                    "user": self.username, "pwd": self.password,
                    "process_data": {
                        process_name: {
                            "Generate_Ini": {"value": "file4", "spec_bool": 1},
                            subprocess_name:
                                {"Plots": {"Raw0": {"value": "file1", "spec_bool": 1},
                                           "Raw1": {"value": "file2", "spec_bool": 1},
                                           "Raw2": {"value": "file3", "spec_bool": 1}}
                                 }
                        }
                    }
                }
            # 2. Create Json data dict
            json_dict = {'data': json.dumps(json_data)}

            # 3. Create File Handlers
            with open(inputdataFiles[0], 'rb') as image:
                fileobj1 = image.read()
            with open(inputdataFiles[1], 'rb') as image:
                fileobj2 = image.read()
            with open(inputdataFiles[2], 'rb') as image:
                fileobj3 = image.read()
            fileobj4 = open(inputdataFiles[3], 'rb')

            # 4. Dict of files
            files = {'file1': ""}
            files = {
                'file1': (inputdataFiles[0], fileobj1),
                'file2': (inputdataFiles[1], fileobj2),
                'file3': (inputdataFiles[2], fileobj3),
                'file4': (inputdataFiles[3], fileobj4),
            }
        elif "Receiver_Peak_Test" in subprocess_name:
            json_data = one_file_json
            json_dict = {'data': json.dumps(json_data)}
            fileobj1 = open(inputdataFiles[0], 'rb')
            files = {
                'file1': (inputdataFiles[0], fileobj1)
            }
        elif "APD_Alignment" in subprocess_name:
            # 1. Format Json data
            if model == "mq":
                json_data = {
                    "user": self.username, "pwd": self.password,
                    "process_data": {
                        process_name: {
                            subprocess_name: {"beam1": "file1",
                                              "beam8": "file2"}
                        }
                    }
                }
            # 2. Create Json data dict
            json_dict = {'data': json.dumps(json_data)}

            # 3. Create File Handlers
            with open(inputdataFiles[0], 'rb') as image:
                fileobj1 = image.read()
            with open(inputdataFiles[1], 'rb') as image:
                fileobj2 = image.read()

            # 4. Dict of files
            files = {'file1': ""}
            files = {
                'file1': (inputdataFiles[0], fileobj1),
                'file2': (inputdataFiles[1], fileobj2)
            }

        # 5.Push Json Data to PTest
        if self.mPTest_database_check_connection() == 200:
            try:
                headers = {'Content-Type': 'multipart/form-data; boundary=c7cbfdd911b4e720f1dd8f479c50bc7f'}
                connection_status = requests.get(ptest_push_path, headers=headers)
                post_status = requests.post(ptest_push_path, data=json_dict, files=files)

                message = "In mPTest_database_post_data_file(): Post Status in text:{}".format(post_status.text)
                logging.info(message)

                message = "In mPTest_database_post_data_file(): Post Status in Json:{}".format(post_status.json())
                logging.info(message)
                print(message)

                message = "In mPTest_database_post_data_file(): connection Status:{}".format(connection_status.status_code)
                logging.info(message)

            except requests.exceptions.RequestException as error:
                message = "In mPTest_database_post_data_file() : got error: {}".format(error)
                logging.info(message)
                raise SystemExit(error)

        return post_status.json()

    def mPTest_database_json_model_path(self):

        json_model_full_path = os.path.join(self.ptest_server_path, 'helper/model_list/')
        logging.info("In mPTest_database_json_model_path : Model Path:", json_model_full_path)
        self.ptest_model_json_path = json_model_full_path
        return json_model_full_path

    def mPTest_database_verify_user_path(self):

        verify_user_full_path = os.path.join(self.ptest_server_path, 'helper/verifyuser_qpnum/')
        #logging.info("In mPTest_database_json_model_path : Model Path:", verify_user_full_path)
        self.ptest_verify_user_path = verify_user_full_path
        return verify_user_full_path

    def mPTest_database_json_process_path(self):

        print('In mPTest_database_json_process_path(): PTest Server Path:', self.ptest_server_path)
        print('In mPTest_database_json_process_path(): PTest Model Name :', self.ptest_model_name)
        print('In mPTest_database_json_process_path(): PTest QPNUMB     :', self.qpnum)

        self.ptest_process_json_path = self.ptest_server_path + self.ptest_model_name + '/' + 'automate/getfile/'
        json_process_full_path = os.path.join(self.ptest_process_json_path, self.qpnum + '/')

        print("In mPTest_database_json_process_path(): PTest JSON Process Path ", json_process_full_path)

        return json_process_full_path

    def mPTest_database_post_path(self):

        self.ptest_post_path = self.ptest_server_path + self.ptest_model_name + '/' + 'automate/updateprocessdata/'
        self.ptest_post_path = os.path.join(self.ptest_post_path, self.qpnum + '/')
        json_post_full_path = self.ptest_post_path
        return json_post_full_path
