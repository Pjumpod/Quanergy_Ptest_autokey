import time, re
from PTest_results_process import cPTest_results
from PTest_parser_json import cPTest_parser_json
from PTest_database import cPTest_database
from choiseBox import choiseBox
import pandas as pd
import platform
import json
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk


def askQP():
    serial_num = "xx"
    while (len(serial_num) != 6) or (serial_num[:2].upper() != "QP"):
        serial_num = simpledialog.askstring("Question", "Enter your qpnum: ")
        if serial_num == None:
            serial_num = "xx"
    if platform.system().upper() == "WINDOWS":
        serial_num = serial_num.upper()
    else:
        serial_num = serial_num.lower()
    return serial_num

def askAccount():
    password = ""
    username = ""
    while len(password) < 3:
        username = simpledialog.askstring("Question", "Enter your ptest username: ")
        with open("user.json", "r") as read_file:
            user = json.load(read_file)
        accounts = user["employees"]
        for account in accounts:
            if account['username'] == username:
                password = account['password']
    return username, password

def askModel():
    OPTIONS = [
        "m8prime",
        "m1edge"
    ]
    master = tk.Tk()
    promtptext = tk.Text(master, height = 2, width = 52)
    promtptext.insert(tk.INSERT, "What is the QP type?")
    promtptext.pack()
    variable = tk.StringVar(master)
    variable.set(OPTIONS[0])  # default value
    w = tk.OptionMenu(master, variable, *OPTIONS)
    w.config(width=20, height=3)
    w.pack()
    def model_ok():
        global model_type
        model_type = variable.get()
        master.withdraw()
        master.destroy()
    button = tk.Button(master, text="OK", command=model_ok, height=2, width=10)
    button.pack()
    master.wait_window()
    return True

def askProcess():
    OPTIONS = [
        "Alignment => Vertical_Angle"
    ]
    master = tk.Tk()
    promtptext = tk.Text(master, height = 2, width = 52)
    promtptext.insert(tk.INSERT, "What is the data would like to key to ptest?")
    promtptext.pack()
    variable = tk.StringVar(master)
    variable.set(OPTIONS[0])  # default value
    w = tk.OptionMenu(master, variable, *OPTIONS)
    w.config(width=50, height=3)
    w.pack()
    def process_ok():
        global process_type
        process_type = variable.get()
        master.withdraw()
        master.destroy()
    button = tk.Button(master, text="OK", command=process_ok, height=2, width=10 )
    button.pack()
    master.wait_window()
    return True

if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()

    model_type = ""
    askModel()
    print("Model = ", model_type)
    model = model_type

    process_type = ""
    askProcess()
    process_name = process_type.split('=>')[0].strip()
    subprocess_name = process_type.split('=>')[1].strip()
    print("Process = ", process_name, " and ", subprocess_name, ".")

    username, password = askAccount()
    print("User Name = ", username)
    print("password = ", password)

    serial_num = askQP()
    print("QP = ", serial_num)

    ptest_server_path = 'http://ptest.quanergy.com/'

    Test_results = cPTest_results()
    results_dir_path = Test_results.mResults_dir_path(serial_num)

    ptestHandler = cPTest_database(serial_num, username, password, ptest_server_path, model)
    parser = cPTest_parser_json(process_name, subprocess_name)
    dict_master_process, dict_master_process_keys = ptestHandler.mPTest_database_get_json_process_file()
    # ptest_dict_static_xml_subprocess = dict_master_process[process_name]
    # print(ptest_dict_static_xml_subprocess)
    df_dict_raw_data = Test_results.mResults_get_input_files(subprocess_name,results_dir_path)
    # print(x.keys())
    dict_finalDataPacket = {}
    # PREPARE THE DATA FROM SHARED DRIVE - CSV files.
    if bool(re.search("Performance_Test", process_name, re.IGNORECASE)):

        # Find the Location of regression match
        for data in df_dict_raw_data.copy():
            if bool(re.search("_eeprom_config.ini", data, re.IGNORECASE)):
                df_eeprom_ini_file_path = df_dict_raw_data[data]
                del df_dict_raw_data[data]  # Remove ini file

        # Pop up Dialog for Plot dataframes
        print("In mDialog_post_to_ptest().In Performance Test")
        dlg = Ui_Plot_Dialog(df_dict_raw_data)
        if dlg.exec():
            logger.info("In mDialog_post_to_ptest(). Dialog OK Clicked!")
            # Post data to Ptest
            list_of_files = list(df_dict_raw_data.keys())
            list_of_files.append(df_eeprom_ini_file_path)
        else:
            print("In mDialog_post_to_ptest(). Cancel clicked!")
            # Don't Post Data
            message = "In mDialog_post_to_ptest(): Results not Pushed to PTest "
            print(message)

    else:

        # 4. Parser both process and sub-process . Creates final process packet dictionary . Fills Data Packet
        #  To index into dict , convert dict to list of values
        dict_raw_data_values = df_dict_raw_data.values()
        # print("Last input before parse: {}".format(dict_raw_data_values))
        parser = cPTest_parser_json(process_name, subprocess_name)
        dict_finalDataPacket = parser.mPTest_parser_create_data_packet(dict_master_process,
                                                                       (list(dict_raw_data_values)[0]))
        message = "In mGui_post_all_input_files: {0} {1}".format(subprocess_name, dict_finalDataPacket)
        print(message)
    # PUSH data
    push_return = ptestHandler.mPTest_database_post_json(process_name, subprocess_name, dict_finalDataPacket)
    print("result = ", push_return['err'])
    if push_return['err'] != '':
        messagebox.showerror("ERROR", "KEY DATA TO PTEST IS ERROR " + str(push_return['err']))
    else:
        print("PUSH DATA TO PTEST DONE.")
        messagebox.showinfo("PUSH DATA TO PTEST DONE.")





