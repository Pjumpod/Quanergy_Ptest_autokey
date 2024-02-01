import logging


class cPTest_parser_json:

    def __init__(self, process_name, subprocess_name, model):
        self. process_name = process_name
        self.subprocess_name = subprocess_name
        self.model = model
    # Parser process
    def mPtest_parser_get_process(self, dict_master_process):

        logging.info("=====================================================================")
        logging.info("In mPtest_parser_get_process(): Parse Process ")
        logging.info("=====================================================================")

        dict_process = dict_master_process[self.process_name]

        #if not dict_process:
            #raise PTest_common.CustomException(1, "In mPtest_parser_get_process(): Process not Found in Json file ")

        logging.info("In mPtest_parser_get_process(): Process:{}".format((dict_process.keys())))
        return dict_process, dict_process.keys()

    # Parser sub-process
    def mPTest_parser_get_subprocess(self, dict_process):
        logging.info("In mPTest_parser_get_subprocess(): Parse SubProcess ")
        dict_subprocess = dict_process[self.subprocess_name]

        #if not dict_subprocess:
            #raise PTest_common.CustomException(1, "In mPtest_parser_get_subprocess(): SubProcess not Found in Json file ")

        logging.info("In mPTest_parser_get_subprocess(): Sub Process:{}".format(dict_subprocess))
        return dict_subprocess

    # Parser both process and sub-process . Creates final process packet dictionary
    def mPTest_parser_json(self, dict_master_process):

        logging.info("=====================================================================")
        logging.info("In mPTest_parser_json():  Parse Json ")
        logging.info("=====================================================================")

        if not dict_master_process:

            logging.error("In mPTest_parser_json(): Master Process Json file is Empty.Failed to Parse Master Process:{}".format(dict_master_process))
            # QMessageBox.information(QMessageBox(), "Info", "Master Json File is Empty")
            #raise PTest_common.CustomException(1, "In mPTest_parser_json(): Master Process not Found in Json file ")

        try:

            # GET PROCESS
            dict_process, dict_process_keys = self.mPtest_parser_get_process(dict_master_process)

            # GET SUB_PROCESS
            dict_subprocess = self.mPTest_parser_get_subprocess(dict_process)

            # CREATE DATA PACKET
            dict_final_process = {}

            # FIND THE PACKET TYPE
            subprocess_type = dict_subprocess[0]

            # 1. If type is ASSY, INSP, QA
            if subprocess_type == 'ASSY' or subprocess_type == 'INSP' or subprocess_type == 'QA':
                subprocess_datatype = dict_subprocess[1]
                dict_final_process = {
                    'subprocess_type': subprocess_type,
                    'subprocess_data_type': subprocess_datatype
                }

            # 2.If type is SN or SN_ignore
            elif subprocess_type == 'SN_ignore' or subprocess_type == 'SN':
                dict_final_process = {
                    'subprocess_type': subprocess_type,
                }
                return dict_final_process

            # 3.If type is ALIGN
            elif subprocess_type == 'ALIGN':
                dict_final_process = {
                    'subprocess_type': subprocess_type,
                }

            # 4. If type is TEST1x1
            elif subprocess_type == 'TEST_1x1':
                dict_final_process = {
                    'subprocess_type': subprocess_type
                }
                for keys in dict_subprocess[1]:
                    if keys == 'type':
                        subprocess_datatype = dict_subprocess[1][keys]
                        dict_final_process['subprocess_data_type'] = subprocess_datatype
                    if keys == 'spec' or keys == 'spec_bool':
                        spec_type = keys
                        dict_final_process['subprocess_spec_type'] = spec_type

            # 5. If type is TESTmxn
            elif subprocess_type == 'TEST_mxn':
                # Inialize
                dict_final_process = {}

                # Parse Rows and Cols
                rows = dict_subprocess[1]['rows']
                cols = dict_subprocess[1]['cols']

                # Initialize
                dict_final_process['subprocess_type'] = subprocess_type
                dict_final_process['rows'] = rows
                dict_final_process['cols'] = cols

            else:
                logging.error("In mPTest_parser_json(): Parser failed to parse Master File")
                # QMessageBox.information(QMessageBox(), "Info", "Parser failed to parse Master File")
                #raise PTest_common.CustomException(1, "In mPTest_parser_json_file(): Json file failed processed")

        except Exception as error:
            raise error

        #logging.error("In mPTest_parser_json(): Master Process:{}".format(dict_master_process))
        return dict_final_process

    # Parser both process and sub-process . Creates final process packet dictionary . Fills Data
    def mPTest_parser_create_data_packet(self, dict_master_process, dict_input_raw_data):

        logging.info("=====================================================================")
        logging.info("In mPTest_parser_create_data_packet(): Create Data Packet            ")
        logging.info("=====================================================================")

        dict_final_process = self.mPTest_parser_json(dict_master_process)

        # Initialize final format
        dict_final_data_packet = {}
        logging.info("In mPTest_parser_create_data_packet(): Build JSON FinalProcessPacket")

        try:
            # 1. If type is ASSY, INSP, QA
            if dict_final_process['subprocess_type'] == 'ASSY' or dict_final_process['subprocess_type'] == 'INSP' or \
                    dict_final_process['subprocess_type'] == 'QA':
                if dict_input_raw_data == 0 or dict_input_raw_data == 1 or dict_input_raw_data == 2:
                    dict_final_data_packet = str(dict_input_raw_data)
                    return dict_final_data_packet
                else:
                    raise Exception("ASSY/INSP/QA should only be 0,1,or 2")

            # 2.If type is SN or SN_ignore or ALIGN
            elif dict_final_process['subprocess_type'] == 'SN' or dict_final_process['subprocess_type'] == 'SN_ignore' or \
                    dict_final_process['subprocess_type'] == 'ALIGN':
                raise Exception("Handler is currently not supporting pushes for SN/SN_ignore/ALIGN")

            # 3. If type is TEST1x1
            elif dict_final_process['subprocess_type'] == 'TEST_1x1':
                # Initialize
                dict_final_data_packet = {"value": str(dict_input_raw_data)}

                # Include spec_bool param is spec_type == spec_bool
                if dict_final_process['subprocess_spec_type'] == 'spec_bool':
                    dict_final_data_packet['spec_bool'] = str(dict_input_raw_data)

                return dict_final_data_packet

            # 4. If type is TEST_mxn
            elif dict_final_process['subprocess_type'] == 'TEST_mxn':

                # Initialize final format
                dict_final_data_packet = {}

                # Generate empty final format and handle spec vs spec_bool types
                print(range(len(dict_final_process['rows'])))
                for i in range(len(dict_final_process['rows'])):
                    # Parse row keys and initilize col dict
                    current_row = dict_final_process['rows'][i]
                    col_dict = {}

                    for j in range(len(dict_final_process['cols'].keys())):
                        print(j)
                        # Parse col keys
                        col_key = list(dict_final_process['cols'].keys())[j]
                        current_col = dict_final_process['cols'][col_key]

                        # Handle spec types
                        if 'spec' in current_col:
                            # Build col dict for row
                            col_dict_temp = {col_key: {"value": ""}}
                            col_dict.update(col_dict_temp)
                        if 'spec_bool' in current_col :
                            # Build col dict for row
                            col_dict_temp = {col_key: {"value": ""}, 'spec_bool': "1"}
                            col_dict.update(col_dict_temp)

                    # Update dictFinalFormat by row
                    dict_final_data_packet[current_row] = col_dict

            else:

                logging.error("In mPTest_parser_create_data_packet(): Parser failed to create Data Packet")
                # QMessageBox.information(QMessageBox(), "Info", "Parser failed to create Data Packet")
                # raise PTest_common.CustomException(1, "mPTest_parser_create_data_packet() : Failed to SubProcess")
                #raise

        except Exception as error:
            logging.error("In mPTest_parser_create_data_packet(): Error:{}", error)
            # QMessageBox.information(QMessageBox(), "Info", "Error:{}".format(error))
            #raise

        return self.mPTest_parser_fill_data_packet(dict_input_raw_data, dict_final_data_packet)

    def mPTest_parser_fill_data_packet(self, dict_input_raw_data, dict_final_data_packet):
        print(dict_input_raw_data)
        # Fill dictFinalFormat with inputDataFrame
        logging.info("In mPTest_fill_data_packet(): Fill JSON FinalProcessPacket with InputDataPacket")
        if "Range_Calibration" in self.subprocess_name and "mq" in self.model:
            for ii, i in enumerate(dict_final_data_packet):
                for ij, j in enumerate(dict_final_data_packet[i]):
                    print(dict_final_data_packet[i])
                    print(i, " - ", j, " : ")
                    if "spec_bool" in j:
                        break
                    elif "offset" in j:
                        print(dict_input_raw_data[j][i])
                        if str(dict_input_raw_data[j][i]) == "-0.0":
                            dict_input_raw_data[j][i] = "0.0"
                        if str(dict_input_raw_data[j][i]) == "0.0":
                            dict_input_raw_data[j][i] = "0"
                    dict_final_data_packet[i][j]['value'] = dict_input_raw_data[j][i]
        else:
            for ii, i in enumerate(dict_final_data_packet):
                for ij, j in enumerate(dict_final_data_packet[i]):
                    print(i, " - ", j, " : ")
                    print(dict_input_raw_data[j][i])
                    print(dict_final_data_packet)
                    if str(dict_input_raw_data[j][i]) == "-0.0":
                        dict_input_raw_data[j][i] = "0.0"
                    if str(dict_input_raw_data[j][i]) == "0.0":
                        dict_input_raw_data[j][i] = "0"
                    dict_final_data_packet[i][j]['value'] = dict_input_raw_data[j][i]


        print("In mPTest_fill_data_packet():  Dictionary of Final Data Packet", dict_final_data_packet)

        return dict_final_data_packet

