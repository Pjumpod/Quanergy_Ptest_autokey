from PTest_results_process import cPTest_results
from PTest_parser_json import cPTest_parser_json
from PTest_database import cPTest_database
import pandas as pd

# resultsHandelr = cPTest_results()
# df_dict_raw_data = resultsHandelr.mResults_get_input_files("TEST_mxn", "C:\tmp")
# df_dict_raw_data = {r"C:\tmp\QP5ADB\QP5ADB_min_range.csv"}
serial_num = "QP5ADB"
username = "dummy"
password = "testdatabase"
ptest_server_path = 'http://ptest.quanergy.com/'
process_name = 'Alignment'
subprocess_name = "Vertical_Angle"
model = "m8prime"

ptestHandler = cPTest_database(serial_num, username, password, ptest_server_path, model)
# 2. PTest Parser
parser = cPTest_parser_json(process_name, subprocess_name)
# 3. Get Master JSON File from Ptest
# ptestHandler = cPTest_database(serial_num, username, password, ptest_server_path)
dict_master_process, dict_master_process_keys = ptestHandler.mPTest_database_get_json_process_file()

# 4. raw data
# Vertical Angle
sample_data = [
    [-17.9505, 0.2994],
    [-15.151, 0.269],
    [-12.221, 0.269],
    [-9.2406, 0.2294],
    [-6.1404, 0.1596],
    [-3.0006, 0.1994],
    [0.1094, 0.1094],
    [3.1896, -0.0104]
]

'''dict_input_raw_data = pd.DataFrame(sample_data, columns=['True_Angle', 'Error'],
                                                index=['beam1', 'beam2', 'beam3', 'beam4', 'beam5', 'beam6', 'beam7','beam8'],
                                                dtype=object)'''
dict_input_raw_data = pd.DataFrame(sample_data)
print(dict_input_raw_data)
# 5. Parser both process and sub-process . Creates final process packet dictionary . Fills Data
dict_finalDataPacket = parser.mPTest_parser_create_data_packet(dict_master_process, dict_input_raw_data)
print("========Going to key this to ptest ============")
print(dict_finalDataPacket)
print("===============================================")

# 6. post data to ptest
push_return = ptestHandler.mPTest_database_post_json(process_name, subprocess_name, dict_finalDataPacket)
print("result = ", push_return)

# Output DataFrame
# Python 2.7 unicode data storage
'''('dictFinalFormat', {u'beam8': {u'True_Angle': {'value': -1.5}, u'Error': {'value': -0.6572}},
                     u'beam2': {u'True_Angle': {'value': -10.3}, u'Error': {'value': -0.4482}},
                     u'beam3': {u'True_Angle': {'value': -8.1}, u'Error': {'value': -0.448}},
                     u'beam1': {u'True_Angle': {'value': -14}, u'Error': {'value': -0.1794}},
                     u'beam6': {u'True_Angle': {'value': -3.1}, u'Error': {'value': -0.6474}},
                     u'beam7': {u'True_Angle': {'value': -2.3}, u'Error': {'value': -0.6474}},
                     u'beam4': {u'True_Angle': {'value': -5.8}, u'Error': {'value': -0.5676}},
                     u'beam5': {u'True_Angle': {'value': -4.4}, u'Error': {'value': -4.95778}}})

                    {'beam1': {'True_Angle': {'value': -14}, 'Error': {'value': -0.1794}},
                     'beam2': {'True_Angle': {'value': -10.3}, 'Error': {'value': -0.4482}},
                     'beam3': {'True_Angle': {'value': -8.1}, 'Error': {'value': -0.448}},
                     'beam4': {'True_Angle': {'value': -5.8}, 'Error': {'value': -0.5676}},
                     'beam5': {'True_Angle': {'value': -4.4}, 'Error': {'value': -4.95778}},
                     'beam6': {'True_Angle': {'value': -3.1}, 'Error': {'value': -0.6474}},
                     'beam7': {'True_Angle': {'value': -2.3}, 'Error': {'value': -0.6474}},
                     'beam8': {'True_Angle': {'value': -1.5}, 'Error': {'value': -0.6572}}} '''


# self.assertEqual(dict_finalDataPacket != None, 1)