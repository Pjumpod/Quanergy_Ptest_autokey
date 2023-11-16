import os
import glob
import re
import logging
import pandas as pd
from io import StringIO
import platform
import json
from tkinter import messagebox


class cPTest_results:

    def mResults_get_input_files(self, subprocess_name, results_dir_path, model_type):

        logging.info("==============================================================")
        logging.info("In mResults_get_input_files() : Get Results Files from Server ")
        logging.info("==============================================================")
        # print("AP0")
        get_files_results_static_process_file_str = self.mResults_list_static_xml_process(subprocess_name)
        # print(get_files_results_static_process_file_str)
        results_qpnum_path = results_dir_path # os.path.join(results_dir_path, qpnum + '/')
        print("In mResults_get_input_files() :'Results Server Path {}".format(results_qpnum_path))
        print("In mResults_get_input_files() :'Results static dictionary {}".format(get_files_results_static_process_file_str))
        results_dataframe = {}
        results_list_of_dataframe_dictionary = {}
        get_files_results_static_process_file_list = str(get_files_results_static_process_file_str).split(",")

        try:

            if get_files_results_static_process_file_list:

                # 1. Get List of csv files of a Process(Eg: Vertical Angle) from Static Dictionary
                print("In mResults_get_input_files() :'Results process name {} static dictionary files {}".format(subprocess_name, get_files_results_static_process_file_list))

                # 2. Get each file from list of files of a Process from Static Dictionary
                for result_file in get_files_results_static_process_file_list:

                    # 3. Check QP dir path exists in the Server Path
                    if os.path.isdir(results_qpnum_path):
                        print("In mResults_get_input_files() :'Directory {} Exist.".format(results_qpnum_path))
                        print("Find files for " + result_file)
                        # 4. Get all files from Results Server(results_qpnum_path) that matches subprocess result filename
                        get_files_results_qpnum_dir_path = glob.glob("".join([results_qpnum_path, "\\*{}".format(result_file)]))
                        latest_file = max(get_files_results_qpnum_dir_path, key=os.path.getctime)
                        get_files_results_qpnum_dir_path = {latest_file}
                        print("In mResults_get_input_files() :'List Files in Directory {}".format(get_files_results_qpnum_dir_path))
                        # logging.info("In mResults_get_input_files() :'List Files in Directory {}".format(get_files_results_qpnum_dir_path))

                        # Check get file list from Server Path is not empty
                        if bool(get_files_results_qpnum_dir_path):

                            # 2. Get file list form results_qpnum_dir
                            for result_file_ in get_files_results_qpnum_dir_path:
                                print("In mResults_get_input_files() :'Get Each result_File in List {}".format(result_file_))
                                # Each raw file converted to ptest json process DataFrame
                                results_dataframe = self.mResults_map_results_to_ptest(result_file_, subprocess_name, model_type)
                                results_list_of_dataframe_dictionary[result_file_] = results_dataframe
                        else:
                            logging.error("In mResults_get_input_files() :'Result file do not exist in the Server Path .")
                            # returns empty list to gui
                    else:
                        logging.error("In mResults_get_input_files() :'Results Server Path do not exist.")
            else:

                logging.error("In mResults_get_input_files() :'process_name: {} not in Results static Dictionary.".format(subprocess_name))
                # QMessageBox.information(QMessageBox(), "Info", "Results file not in Results static Dictionary")

        except Exception as error:
            logging.info("In mResults_get_input_files() : Message ", error)
            raise SystemExit(error)

        return results_list_of_dataframe_dictionary

    def mResults_list_static_xml_process(self, subprocess_name):
        # Read static data from XML object . Returns output files in XML as a List for specific subprocess (XML Model)
        # dict_static_result_files_subprocess = xmlFileReader.getXmlParamDictionary(ptest_dict_static_xml_subprocess, subprocess_name)
        # print(dict_static_result_files_subprocess)

        # Read static data from as List
        # setup.ptest_tests_xml_parser(dict_static_result_files_subprocess)
        #if not setup.sSetListOfFiles:
        #    logging.info("In mResults_list_static_xml_process() :'process_name: {} not in Results static Dictionary.".format(subprocess_name))
        # QMessageBox.information(QMessageBox(), "Info", "Results file not in Results static Dictionary")
        #    raise FileNotFoundError
        with open("setting.json", "r") as read_file:
            setting = json.load(read_file)

        return setting[subprocess_name]

    def mResults_map_results_to_ptest(self, results_file_fullpath, subprocess_name, model_type):

        # Convert each csv file to dataframe
        dict_input_raw_data = ""
        if subprocess_name == "Power_Calibration_Over_Temperature":
            return results_file_fullpath
        if "min_range" in subprocess_name.lower():
            f = open(results_file_fullpath, 'r')
            lines = f.readlines()[1:]
            f.close()
            tmpstr = lines[0]
            tmpstr = tmpstr.replace("\"[", "").replace("]\"", "_")
            tmpstr = tmpstr.replace("_,", "\n\r")
            tmpstr = tmpstr.replace("_", "\n\r").replace("\'", "")
            strIO = StringIO(tmpstr)
            dict_input_raw_data = pd.read_csv(strIO, header=None)
        elif "noise_test" in subprocess_name.lower():
            if model_type == "m8prime":
                f = open(results_file_fullpath, 'r')
                lines = f.readlines()[1:]
                f.close()
                if (len(lines) > 1) and (len(lines[0]) > 1):
                    messagebox.showerror("ERROR", "Noise Test ไม่ถูก key ข้อมูล => ติดต่อ จุมภฏ \n\r\n\r"
                                                  "Noise Test is not key yet, Contract Jumpod \n\r\n\r"
                                                  "Tel : 083-768-7507")
                    return results_file_fullpath
                strIO = StringIO("""0,0
                1,0
                2,0
                3,0
                4,0
                5,0
                6,0
                7,0""")
                dict_input_raw_data = pd.read_csv(strIO, header=None)
                # print("Data :", lines)
                # print("Len : ", len(lines))
                # print("LEN0 :", len(lines[0]))
            if model_type == "m1edge":
                f = open(results_file_fullpath, 'r')
                lines = f.readlines()[1:]
                f.close()
                print("LEN0 :", len(lines[0].strip()))
                if len(lines[0].strip()) == 0:
                    lines[0] = "0"
                else:
                    lines[0] = lines[0].strip()
                strIO = StringIO("0," + lines[0])
                dict_input_raw_data = pd.read_csv(strIO, header=None)
        elif ".csv" in results_file_fullpath.lower():
            dict_input_raw_data = pd.read_csv(results_file_fullpath, header=None)
        elif ".png" in results_file_fullpath.lower():
            return results_file_fullpath
        elif ".txt" in results_file_fullpath.lower():
            dict_input_raw_data = pd.read_csv(results_file_fullpath, header=None, delimiter=":")
        result_file_name = os.path.basename(results_file_fullpath)
        results_dataframe = {}

        logging.info("In mResults_map_results_to_ptest():  Result_file_name :{}".format(result_file_name))
        print("In mResults_map_results_to_ptest():  Result_file raw dataframe : \n {}".format(dict_input_raw_data))

        if bool(re.search("vertical_angle", result_file_name, re.IGNORECASE)):
            if model_type == "m8prime":
                results_dataframe = dict_input_raw_data.iloc[1:9, [2, 3]].values
                results_dataframe = results_dataframe.astype(float)
                results_dataframe = pd.DataFrame(results_dataframe,
                                                   columns=['True_Angle', 'Error'],
                                                   index=['beam1', 'beam2', 'beam3', 'beam4', 'beam5', 'beam6', 'beam7', 'beam8'],
                                                   dtype=object)

        elif bool(re.search("range_calibration", subprocess_name, re.IGNORECASE)):
            if model_type == "m8prime":
                results_dataframe = dict_input_raw_data.iloc[[0, 1, 2, 3, 4, 5, 6, 7], 1].values
                results_dataframe = results_dataframe.astype(float)
                results_dataframe = pd.DataFrame(results_dataframe,
                                                   columns=['offset'],
                                                   index=['beam1', 'beam2', 'beam3', 'beam4', 'beam5', 'beam6', 'beam7', 'beam8'],
                                                   dtype=object)
            if model_type == "m1edge":
                results_dataframe = dict_input_raw_data.iloc[6, 1]
                results_dataframe = results_dataframe.astype(float)

        elif bool(re.search("encoder_calibration", subprocess_name, re.IGNORECASE)):
            results_dataframe = dict_input_raw_data.iloc[[1]].values
            results_dataframe = results_dataframe.astype(float)
            if model_type == "m8prime":
                results_dataframe = pd.DataFrame(results_dataframe,
                                                columns=['amplitude', 'phase'],
                                                index=['Results'],
                                                dtype=object)
            if model_type == "m1edge":
                results_dataframe = pd.DataFrame(results_dataframe,
                                                columns=['Amplitude', 'Phase'],
                                                index=['Results'],
                                                dtype=object)
        elif bool(re.search("min_range", subprocess_name, re.IGNORECASE)):
            if model_type == "m8prime":
                results_dataframe = dict_input_raw_data.iloc[[0, 1, 2, 3, 4, 5, 6, 7], 1].values
                results_dataframe = results_dataframe.astype(float)
                results_dataframe = pd.DataFrame(results_dataframe,
                                                   columns=['min_distance'],
                                                   index=['beam1', 'beam2', 'beam3', 'beam4', 'beam5', 'beam6', 'beam7', 'beam8'],
                                                   dtype=object)
            if model_type == "m1edge":
                results_dataframe = dict_input_raw_data.iloc[0, 1]
                results_dataframe = results_dataframe.astype(float)

        elif bool(re.search("noise_test", subprocess_name, re.IGNORECASE)):
            if model_type == "m8prime":
                results_dataframe = dict_input_raw_data.iloc[[0, 1, 2, 3, 4, 5, 6, 7], 1].values
                results_dataframe = results_dataframe.astype(float)
                results_dataframe = pd.DataFrame(results_dataframe,
                                                   columns=['points'],
                                                   index=['beam1', 'beam2', 'beam3', 'beam4', 'beam5', 'beam6', 'beam7', 'beam8'],
                                                   dtype=object)
            if model_type == "m1edge":
                results_dataframe = dict_input_raw_data.iloc[0, 1]
                results_dataframe = results_dataframe.astype(float)

        elif bool(re.search("tnom", subprocess_name, re.IGNORECASE)):
            results_dataframe = dict_input_raw_data.iloc[8, 1]
            results_dataframe = results_dataframe.astype(float)
        else:
            logging.error("In mResults_map_results_to_ptest,  Result_file raw dataframe :{} is failed to Parse".format(results_dataframe))
            # raise SystemExit()

        print("In mResults_map_results_to_ptest():  Result_file raw dataframe : \n {}".format(dict_input_raw_data))
        return results_dataframe

    def validate_Performance_Data(self, data_file_path, min_limit, max_limit):

        df_performance_test = pd.read_csv(data_file_path)
        data_cnt = len(df_performance_test)
        print("Total records in DataFrame : ", data_cnt)

        # Get column List . Ignore Index
        # columns_list = ['Beam1', 'Beam2', 'Beam3', 'Beam4', 'Beam5', 'Beam6', 'Beam7', 'Beam8']
        my_list = df_performance_test.columns.values.tolist()
        columns_list = df_performance_test.iloc[:, 1:].columns.values.tolist()  # Skip col0
        print("col list", my_list)
        print("col list", columns_list)

        if not columns_list:
            print("columns_list is Empty")
            return

        # 1. Check for NUll values
        check_for_nan = df_performance_test.isnull().values.any()
        print("Check for null Values in DataFrame:", check_for_nan)

        if not check_for_nan:

            # 2.Check for correlation
            series_performance_test = df_performance_test.corrwith(df_performance_test['nJ'])
            print("Print correlation values", series_performance_test)

            # check correlation condition
            if (series_performance_test <= 1).all() & (series_performance_test > 0.1).all():

                print("Check correlation condition Successful : Ready to push")

                # 3. Check tail data , check max value of all Beams don't exceed Limits
                # columns_list = ['Beam1', 'Beam2', 'Beam3', 'Beam4', 'Beam5', 'Beam6', 'Beam7', 'Beam8']
                df_tail_data = pd.DataFrame(df_performance_test, columns=columns_list, index=None)
                last_row = df_tail_data.iloc[-1]
                print("Dataframe Tail Data \n", last_row)

                # min_limit = 400
                # max_limit = 800
                print("Dataframe Tail Data Limits MaxLimit:{} LowLimit:{}".format(max_limit, min_limit))
                print("\n")
                if (last_row <= max_limit).all() & (last_row > min_limit).all():
                    print("Limit check on last value of all Beams is Successful: Ready to push")
                else:
                    print("Limit check on last value of all Beams is Failed:  Dont push data")

                # 4. Plot Data
                # columns_list = ['Beam1', 'Beam2', 'Beam3', 'Beam4', 'Beam5', 'Beam6', 'Beam7', 'Beam8']
                # df_plot = pd.DataFrame(df_performance_test, index=df_performance_test['nJ'], columns=columns_list)
                # df_plot.plot.line()

                return df_performance_test, columns_list

            else:
                print("Check correlation condition Failed : Don't push data")

        else:
            print(" Data incomplete. Data failed to push ")


    def mResults_dir_path(self, qpnum: str):
        with open("setting.json", "r") as read_file:
            setting = json.load(read_file)
        if setting is not None:
            if platform.system().upper() == "WINDOWS":
                ptest_results_dir_path = setting['windows_path']
            else:
                ptest_results_dir_path = setting['linux_path']
            full_results_path = os.path.join(ptest_results_dir_path, qpnum + "/")
            ptest_results_dir_path = full_results_path
            if os.path.exists(ptest_results_dir_path):
                return ptest_results_dir_path
            else:
                print(ptest_results_dir_path, " path not exist")
                return ""
        else:
            return ""