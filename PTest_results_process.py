import os
import glob
import re
import logging

import pandas as pd
from io import StringIO
import platform
import json
from tkinter import messagebox
from datetime import datetime


class cPTest_results:

    def __init__(self):
        self.range_acc = 50.07

    def mResults_get_input_files(self, subprocess_name, results_dir_path, model_type):

        logging.info("==============================================================")
        logging.info("In mResults_get_input_files() : Get Results Files from Server ")
        logging.info("==============================================================")
        # print("AP0")
        get_files_results_static_process_file_str = self.mResults_list_static_xml_process(subprocess_name)
        # print(get_files_results_static_process_file_str)
        results_qpnum_path_2 = os.path.join(results_dir_path, 'range_test_data/')
        if ("accuracy_test" in subprocess_name.lower()) or ("range_test" in subprocess_name.lower()):
            results_dir_path = os.path.join(results_dir_path, 'accuracy_test_data/')
        # elif "range_test" in subprocess_name.lower():
        #    results_dir_path = os.path.join(results_dir_path, 'range_test_data/')
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
                        if ("accuracy_test" in subprocess_name.lower()) or ("range_test" in subprocess_name.lower()):
                            get_files_results_qpnum_dir_path += glob.glob(
                                "".join([results_qpnum_path_2, "\\*{}".format(result_file)]))
                            latest_file = max(get_files_results_qpnum_dir_path, key=os.path.getmtime)
                            get_files_results_qpnum_dir_path = [
                                file for file in get_files_results_qpnum_dir_path # glob.glob(results_qpnum_path + '\\*.csv')
                                if (datetime.fromtimestamp(os.path.getmtime(latest_file)) - datetime.fromtimestamp(os.path.getmtime(file))).total_seconds() < 86400
                            ]
                        else:
                            latest_file = max(get_files_results_qpnum_dir_path, key=os.path.getmtime)
                            get_files_results_qpnum_dir_path = {latest_file}
                        print("In mResults_get_input_files() :'List Files in Directory {}".format(get_files_results_qpnum_dir_path))
                        # logging.info("In mResults_get_input_files() :'List Files in Directory {}".format(get_files_results_qpnum_dir_path))

                        # Check get file list from Server Path is not empty
                        if bool(get_files_results_qpnum_dir_path):
                            if "accuracy_test" in subprocess_name.lower():
                                print("In mResults_get_input_files() :'Start with {}".format(get_files_results_qpnum_dir_path[0]))
                                csv_content = pd.read_csv(get_files_results_qpnum_dir_path[0])
                                for result_file_ in get_files_results_qpnum_dir_path:
                                    if result_file_ == get_files_results_qpnum_dir_path[0]:
                                        pass
                                    else:
                                        print("In mResults_get_input_files() :'Concat the file in List {}".format(result_file_))
                                        csv_content = pd.concat([csv_content, pd.read_csv(result_file_)], ignore_index=True)
                                print("Merge data before process is \n\r{}".format(csv_content))
                                results_dataframe = self.mResult_accuracy_process(model_type, csv_content)
                                results_list_of_dataframe_dictionary["ACC_Test"] = results_dataframe
                            elif "range_test" in subprocess_name.lower():
                                print("In mResults_get_input_files() :'Start with {}".format(
                                    get_files_results_qpnum_dir_path[0]))
                                csv_content = pd.read_csv(get_files_results_qpnum_dir_path[0])
                                for result_file_ in get_files_results_qpnum_dir_path:
                                    if result_file_ == get_files_results_qpnum_dir_path[0]:
                                        pass
                                    else:
                                        print("In mResults_get_input_files() :'Concat the file in List {}".format(
                                            result_file_))
                                        csv_content = pd.concat([csv_content, pd.read_csv(result_file_)],
                                                                ignore_index=True)
                                print("Merge data before process is \n\r{}".format(csv_content))
                                results_dataframe = self.mResult_range_process(model_type, csv_content)
                                results_list_of_dataframe_dictionary["RANGE_Test"] = results_dataframe
                            else:
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

            if model_type == "mq":
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
            if model_type == "mq":
                results_dataframe = dict_input_raw_data.iloc[1:9, [2, 3]].values
                print(results_dataframe)
                results_dataframe = results_dataframe.astype(float)
                results_dataframe = pd.DataFrame(results_dataframe,
                                                   columns=['True_Angle', 'Error'],
                                                   index=['beam1', 'beam2', 'beam3', 'beam4', 'beam5', 'beam6', 'beam7', 'beam8'],
                                                   dtype=object).abs()

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
            if model_type == "mq":
                results_dataframe = dict_input_raw_data.iloc[[0, 1, 2, 3, 4, 5, 6, 7], 1].values
                results_dataframe = results_dataframe.astype(float)
                results_dataframe = pd.DataFrame(results_dataframe,
                                                   columns=['offset'],
                                                   index=['beam1', 'beam2', 'beam3', 'beam4', 'beam5', 'beam6', 'beam7', 'beam8'],
                                                   dtype=object)

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
            if model_type == "mq":
                results_dataframe = pd.DataFrame(results_dataframe,
                                                columns=['amplitude', 'phase'],
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
            if model_type == "mq":
                results_dataframe = dict_input_raw_data.iloc[[0, 1, 2, 3, 4, 5, 6, 7], 1].values
                results_dataframe = results_dataframe.astype(float)
                results_dataframe = pd.DataFrame(results_dataframe,
                                                   columns=['min_distance'],
                                                   index=['beam1', 'beam2', 'beam3', 'beam4', 'beam5', 'beam6', 'beam7', 'beam8'],
                                                   dtype=object)

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
            if model_type == "mq":
                results_dataframe = dict_input_raw_data.iloc[[0, 1, 2, 3, 4, 5, 6, 7], 1].values
                results_dataframe = results_dataframe.astype(float)
                results_dataframe = pd.DataFrame(results_dataframe,
                                                   columns=['points'],
                                                   index=['beam1', 'beam2', 'beam3', 'beam4', 'beam5', 'beam6', 'beam7', 'beam8'],
                                                   dtype=object)
        elif bool(re.search("encoder_offset", subprocess_name, re.IGNORECASE)):
            if model_type == "mq":
                results_dataframe = dict_input_raw_data.iloc[8, 1]
                results_dataframe = results_dataframe.astype(float)
        elif bool(re.search("tnom", subprocess_name, re.IGNORECASE)):
            if model_type == "mq":
                results_dataframe = dict_input_raw_data.iloc[9, 1]
                results_dataframe = results_dataframe.astype(float)
            if model_type == "m1edge" or model_type == "m8prime":
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

    def mResult_accuracy_process(self, model_type, df):
        start_beam = 6 if model_type == "m1edge" else 0
        df2 = df[(df.Beam == start_beam) &
                (df.Selected_Range == self.range_acc) &
                (df.Points > 3)
                ]
        print(df2)
        df2 = df2.reindex(df2['Adj_Accuracy(cm)'].abs().sort_values().index) # df2.nsmallest(1, 'Adj_Accuracy(cm)', key=lambda x: abs(x))
        df2 = df2.iloc[[0]]
        results_dataframe = df2
        if model_type.lower() == "m8prime":
            beam_list = [1, 2, 3, 4, 5, 6, 7]
            for i in beam_list:
                df3 = df[(df.Beam == i) &
                        (df.Selected_Range == self.range_acc) &
                        (df.Points > 3)
                        ]
                print(df3)
                df3 = df3.reindex(df3['Adj_Accuracy(cm)'].abs().sort_values().index)
                df3 = df3.iloc[[0]]
                if len(df3) == 0:
                    df4 = df[(df.Beam == i)]
                    self.errorPrompt(i, df4)
                df2 = pd.concat([df2, df3], ignore_index=True)
                df2['Adj_Accuracy(cm)'] = df2['Adj_Accuracy(cm)'].abs()
            print('The best result is : \n\r {}'.format(df2))
            results_dataframe = df2.iloc[[0, 1, 2, 3, 4, 5, 6, 7], [3, 2, 7, 8]].values
            results_dataframe = results_dataframe.astype(float)
            results_dataframe = pd.DataFrame(results_dataframe,
                                         columns=['offset', 'true_distance', 'STD', 'Yaw'],
                                         index=['beam1', 'beam2', 'beam3', 'beam4', 'beam5', 'beam6', 'beam7', 'beam8'],
                                         dtype=object)
        if model_type.lower() == "m1edge":
            # df2 = df[(df.Beam == 6) &
            #         (df.Selected_Range == self.range_acc) &
            #         (df.Points > 3)
            #         ]
            # df2 = df2.reindex(df2['Adj_Accuracy(cm)'].abs().sort_values().index)
            df2['Adj_Accuracy(cm)'] = df2['Adj_Accuracy(cm)'].abs()
            # df2 = df2.iloc[[0]]
            results_dataframe = df2.iloc[[0], [3, 2, 7, 8]].values
            results_dataframe = results_dataframe.astype(float)
            results_dataframe = pd.DataFrame(results_dataframe,
                                             columns=['offset', 'True_Distance', 'STD', 'Yaw'],
                                             index=['Beam7'],
                                             dtype=object)
        print('The summary data to key to ptest is : \n\r {}'.format(results_dataframe))
        return results_dataframe

    def mResult_range_process(self, model_type, df):
        df = df[df['Selected_Range'] != self.range_acc]
        start_beam = 6 if model_type == "m1edge" else 0
        df2 = df[(df.Beam == start_beam) &
                (df.Points > 3)
                ]
        print(df2)
        df2 = df2.nlargest(1, 'Selected_Range', keep='all')
        df2 = df2.nlargest(1, 'Points')
        results_dataframe = df2
        if model_type.lower() == "m8prime":
            beam_list = [1, 2, 3, 4, 5, 6, 7]
            for i in beam_list:
                df3 = df[(df.Beam == i) &
                         (df.Points > 3)
                         ]
                print(df3)
                df3 = df3.nlargest(1, 'Selected_Range', keep='all')
                df3 = df3.nlargest(1, 'Points')
                if len(df3) == 0:
                    df4 = df[(df.Beam == i)]
                    self.errorPrompt(i, df4)
                df2 = pd.concat([df2, df3], ignore_index=True)
            print('The best result is : \n\r {}'.format(df2))
            results_dataframe = df2.iloc[[0, 1, 2, 3, 4, 5, 6, 7], [2, 5]].values
            results_dataframe = results_dataframe.astype(float)
            results_dataframe = pd.DataFrame(results_dataframe,
                                         columns=['range', 'points'],
                                         index=['beam1', 'beam2', 'beam3', 'beam4', 'beam5', 'beam6', 'beam7', 'beam8'],
                                         dtype=object)
        if model_type.lower() == "m1edge":
            # df2 = df[(df.Beam == 6) &
            #         (df.Points > 3)
            #         ]
            print(df2)
            # df2 = df2.nlargest(1, 'Selected_Range', keep='all')
            # df2 = df2.nlargest(1, 'Points')
            results_dataframe = df2.iloc[[0], [2, 5]].values
            results_dataframe = results_dataframe.astype(float)
            results_dataframe = pd.DataFrame(results_dataframe,
                                             columns=['Range', 'Points'],
                                             index=['Results'],
                                             dtype=object)
        print('The summary data to key to ptest is : \n\r {}'.format(results_dataframe))
        return results_dataframe

    def errorPrompt(self, beamnumber, df):
        messagebox.showerror("Beam missing", "Beam {} all data are FAILED \n\r {}". format(beamnumber, df))
        input("HIT ENTER TO CLOSE")
        quit(1)
