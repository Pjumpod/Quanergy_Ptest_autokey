import re
from PTest_results_process import cPTest_results
from PTest_parser_json import cPTest_parser_json
from PTest_database import cPTest_database
import json
import tkinter as tk
from tkinter import simpledialog, messagebox
# from Ui_Plot_Dialog import Ui_Plot_Dialog
# from choiseBox import choiseBox
import pandas as pd
import numpy as np
# import platform
# import time

def ask_APD_Shims():
    def on_closing():
        quit(0)
    root = tk.Tk()
    labels = ["APD_Shims", "shim_A", "shim_B", "shim_C", "shim_D"]
    entry_widgets = []
    for i, label_text in enumerate(labels):
        tk.Label(root, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
    tk.Label(root, text="height").grid(row=0, column=1, padx=5, pady=5, sticky="w")
    for i in range(1, 5):
        entry = tk.Entry(root)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entry_widgets.append(entry)

    def save_close():
        global APD_Shims
        data = {}
        for label, entry in zip(labels[1:], entry_widgets):
            data[label] = str(entry.get())
        APD_Shims = pd.DataFrame(data.values(), columns=["height"], index=data.keys())
        root.quit()
        root.destroy()

    save_button = tk.Button(root, text="SAVE", command=save_close)
    save_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def ask_APD_Peak():
    def on_closing():
        quit(0)
    root = tk.Tk()
    labels = ["APD_Peak", "beam1", "beam8"]
    entry_widgets = []
    for i, label_text in enumerate(labels):
        tk.Label(root, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
    tk.Label(root, text="peak").grid(row=0, column=1, padx=5, pady=5, sticky="w")
    for i in range(1, 3):
        entry = tk.Entry(root)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entry_widgets.append(entry)

    def save_close():
        global APD_Peak
        data = {}
        for label, entry in zip(labels[1:], entry_widgets):
            data[label] = str(entry.get())
        APD_Peak = pd.DataFrame(data.values(), columns=["peak"], index=data.keys())
        root.quit()
        root.destroy()

    save_button = tk.Button(root, text="SAVE", command=save_close)
    save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def ask_APD_Board_Current_Draw():
    def on_closing():
        quit(0)
    root = tk.Tk()
    tk.Label(root, text="APD_Board_Current_Draw").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    tk.Label(root, text="(mA)").grid(row=0, column=1, padx=5, pady=5, sticky="w")

    entry = tk.Entry(root)
    entry.grid(row=0, column=2, padx=5, pady=5)

    def save_close():
        global APD_Board_Current_Draw
        APD_Board_Current_Draw = np.float64(entry.get())
        root.quit()
        root.destroy()

    save_button = tk.Button(root, text="SAVE", command=save_close)
    save_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def ask_APD_Breakdown_Supplier():
    def on_closing():
        quit(0)
    root = tk.Tk()
    tk.Label(root, text="APD_Breakdown_Supplier").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    tk.Label(root, text="(V)").grid(row=0, column=1, padx=5, pady=5, sticky="w")

    entry = tk.Entry(root)
    entry.grid(row=0, column=2, padx=5, pady=5)

    def save_close():
        global APD_Breakdown_Supplier
        APD_Breakdown_Supplier = np.float64(entry.get())
        root.quit()
        root.destroy()

    save_button = tk.Button(root, text="SAVE", command=save_close)
    save_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

def askQP(subname):
    sn = "xx"
    while (len(sn) != 6) or (sn[:2].upper() != "QP"):
        sn = simpledialog.askstring("Question", "Enter your qpnum: ")
        if sn[:2].upper() != "QP":
            sn = "QP" + sn
        if sn is None:
            messagebox.showerror("quit", "User cancel")
            quit(0)
    sn = sn.upper()

    return sn


def askAccount():
    pwd = ""
    user_name = ""
    while len(pwd) < 3:
        user_name = simpledialog.askstring("Question", "Enter your ptest username: ")
        if user_name is None:
            messagebox.showerror("quit", "User cancel")
            quit(0)
        with open("user.json", "r") as read_file:
            user = json.load(read_file)
        accounts = user["employees"]
        for account in accounts:
            if account['username'] == user_name:
                pwd = account['password']
    return user_name, pwd


def askModel():
    OPTIONS = [
        "m8prime",
        "m1edge",
        "mq"
    ]
    master = tk.Tk()
    promtptext = tk.Text(master, height=2, width=52)
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


def askProcess(pmodel):
    OPTIONS = []
    if pmodel == "m8prime":
        OPTIONS = [
            "Alignment => Vertical_Angle",
            "Performance_Test => Receiver_Peak_Test",
            "Performance_Test => Power_Calibration_Over_Temperature",
            "Final_Test => Range_Calibration",
            "Final_Test => Accuracy_Test",
            "Final_Test => Range_Test"
        ]
    elif pmodel == "m1edge":
        OPTIONS = [
            "Performance_Test => Power_Calibration_Over_Temperature",
            "Final_Test => Range_Calibration",
            "Final_Test => Accuracy_Test",
            "Final_Test => Range_Test"
        ]
    elif pmodel == "mq":
        OPTIONS = [
            "Alignment => Vertical_Angle",
            "Alignment => APD_Alignment",
            "Alignment => Laser_Alignment",
            "Performance_Test => Power_Calibration_Over_Temperature",
            "Final_Test => Range_Calibration",
            "Final_Test => Accuracy_Test",
            "Final_Test => Range_Test"
        ]
    master = tk.Tk()
    promtptext = tk.Text(master, height=2, width=52)
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

    button = tk.Button(master, text="OK", command=process_ok, height=2, width=10)
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
    askProcess(model_type)
    process_name = process_type.split('=>')[0].strip()
    subprocess_name = process_type.split('=>')[1].strip()
    print("Process = ", process_name, " and ", subprocess_name, ".")

    username, password = askAccount()
    print("User Name = ", username)
    print("password = ", password)

    serial_num = askQP(subprocess_name)
    print("QP = ", serial_num)

    ptest_server_path = 'http://ptest.quanergy.com/'

    Test_results = cPTest_results()
    results_dir_path = Test_results.mResults_dir_path(serial_num, subprocess_name)

    ptestHandler = cPTest_database(serial_num, username, password, ptest_server_path, model)
    parser = cPTest_parser_json(process_name, subprocess_name)
    dict_master_process, dict_master_process_keys = ptestHandler.mPTest_database_get_json_process_file()

    df_dict_raw_data = Test_results.mResults_get_input_files(subprocess_name, results_dir_path, model)

    dict_finalDataPacket = {}
    push_return = {'err' : ''}
    # PREPARE THE DATA FROM SHARED DRIVE - CSV files.
    if bool(re.search("Performance_Test", process_name, re.IGNORECASE)):
        # Pop up Dialog for Plot dataframes
        print("In mDialog_post_to_ptest().In Performance Test")
        print("==> File ", df_dict_raw_data.keys())
        files_list = list(df_dict_raw_data.keys())
        # PUSH FILE
        push_return = ptestHandler.mPTest_database_post_file(process_name, subprocess_name, files_list, model)
    elif ("Accuracy_Test" in subprocess_name) or ("Range_Test" in subprocess_name):
        yesno = messagebox.askyesno("Review DATA", "This data will push to ptest \n\r {}".format(df_dict_raw_data))
        if yesno:
            dict_raw_data_values = df_dict_raw_data.values()
            parser = cPTest_parser_json(process_name, subprocess_name)
            dict_finalDataPacket = parser.mPTest_parser_create_data_packet(dict_master_process,
                                                                           (list(dict_raw_data_values)[0]))
            message = "In mGui_post_all_input_files: {0} {1}".format(subprocess_name, dict_finalDataPacket)
            print(message)
            # PUSH data
            push_return = ptestHandler.mPTest_database_post_json(process_name, subprocess_name, dict_finalDataPacket)
        else:
            print("User cancel to push the data to ptest.")
            quit(0)
    elif "APD_Alignment" in subprocess_name or "Laser_Alignment" in subprocess_name:
        if model == "mq":
            # Pop up Dialog for Plot dataframes
            print("In mDialog_post_to_ptest().In Performance Test")
            print("==> File ", df_dict_raw_data.keys())
            files_list = list(df_dict_raw_data.keys())
            # PUSH FILE
            push_return = ptestHandler.mPTest_database_post_file(process_name, subprocess_name, files_list, model)
            ask_APD_Board_Current_Draw()
            ask_APD_Shims()
            ask_APD_Breakdown_Supplier()
            ask_APD_Peak()
            TYPING_DATA_APD = [APD_Board_Current_Draw, APD_Shims, APD_Breakdown_Supplier,
                               APD_Peak]
            APD_name = ["APD_Board_Current_Draw", "APD_Shims", "APD_Breakdown_Supplier", "APD_Peak"]
            list_APD = 0
            for data in TYPING_DATA_APD:
                subprocess_name = APD_name[list_APD]
                parser = cPTest_parser_json(process_name, subprocess_name)
                dict_finalDataPacket = parser.mPTest_parser_create_data_packet(dict_master_process, data)
                message = "In mGui_post_all_input_files: {0} {1}".format(subprocess_name, dict_finalDataPacket)
                print(message)
                push_return = ptestHandler.mPTest_database_post_json(process_name, subprocess_name, dict_finalDataPacket)
                list_APD = list_APD+1
    elif "Vertical_Angle" in subprocess_name:
        dict_raw_data_values = df_dict_raw_data.values()
        parser = cPTest_parser_json(process_name, subprocess_name)
        dict_finalDataPacket = parser.mPTest_parser_create_data_packet(dict_master_process,
                                                                       (list(dict_raw_data_values)[0]))
        message = "In mGui_post_all_input_files: {0} {1}".format(subprocess_name, dict_finalDataPacket)
        print(message)
        # PUSH data
        push_return = ptestHandler.mPTest_database_post_json(process_name, subprocess_name, dict_finalDataPacket)
    elif "Range_Calibration" in subprocess_name:
        dict_raw_data_values = df_dict_raw_data.values()
        parser = cPTest_parser_json(process_name, subprocess_name)
        dict_finalDataPacket = parser.mPTest_parser_create_data_packet(dict_master_process,
                                                                       (list(dict_raw_data_values)[0]))
        message = "In mGui_post_all_input_files: {0} {1}".format(subprocess_name, dict_finalDataPacket)
        print(message)
        push_return = ptestHandler.mPTest_database_post_json(process_name, subprocess_name, dict_finalDataPacket)
        if push_return['err'] != '':
            messagebox.showerror("ERROR", "KEY DATA TO PTEST IS ERROR " + str(push_return['err']))
            exit(1)
        if model == "mq":
            subprocess_name = "Encoder_Offset"
            print("=== Input for {} process ===".format(subprocess_name))
            dict_master_process, dict_master_process_keys = ptestHandler.mPTest_database_get_json_process_file()
            df_dict_raw_data = Test_results.mResults_get_input_files(subprocess_name, results_dir_path, model)
            dict_raw_data_values = df_dict_raw_data.values()
            parser = cPTest_parser_json(process_name, subprocess_name)
            dict_finalDataPacket = parser.mPTest_parser_create_data_packet(dict_master_process,
                                                                       (list(dict_raw_data_values)[0]))
            message = "In mGui_post_all_input_files: {0} {1}".format(subprocess_name, dict_finalDataPacket)
            print(message)
            push_return = ptestHandler.mPTest_database_post_json(process_name, subprocess_name, dict_finalDataPacket)
            if push_return['err'] != '':
                messagebox.showerror("ERROR", "KEY DATA TO PTEST IS ERROR " + str(push_return['err']))
                exit(1)

        subprocess_name = "TNOM"
        print("=== Input for {} process ===".format(subprocess_name))
        dict_master_process, dict_master_process_keys = ptestHandler.mPTest_database_get_json_process_file()
        df_dict_raw_data = Test_results.mResults_get_input_files(subprocess_name, results_dir_path, model)
        dict_raw_data_values = df_dict_raw_data.values()
        parser = cPTest_parser_json(process_name, subprocess_name)
        dict_finalDataPacket = parser.mPTest_parser_create_data_packet(dict_master_process,
                                                                       (list(dict_raw_data_values)[0]))
        message = "In mGui_post_all_input_files: {0} {1}".format(subprocess_name, dict_finalDataPacket)
        print(message)
        push_return = ptestHandler.mPTest_database_post_json(process_name, subprocess_name, dict_finalDataPacket)
        if push_return['err'] != '':
            messagebox.showerror("ERROR", "KEY DATA TO PTEST IS ERROR " + str(push_return['err']))
            exit(1)
        subprocess_name = "Encoder_Calibration"
        print("=== Input for {} process ===".format(subprocess_name))
        dict_master_process, dict_master_process_keys = ptestHandler.mPTest_database_get_json_process_file()
        df_dict_raw_data = Test_results.mResults_get_input_files(subprocess_name, results_dir_path, model)
        dict_raw_data_values = df_dict_raw_data.values()
        parser = cPTest_parser_json(process_name, subprocess_name)
        dict_finalDataPacket = parser.mPTest_parser_create_data_packet(dict_master_process,
                                                                       (list(dict_raw_data_values)[0]))
        message = "In mGui_post_all_input_files: {0} {1}".format(subprocess_name, dict_finalDataPacket)
        print(message)
        push_return = ptestHandler.mPTest_database_post_json(process_name, subprocess_name, dict_finalDataPacket)
        if push_return['err'] != '':
            messagebox.showerror("ERROR", "KEY DATA TO PTEST IS ERROR " + str(push_return['err']))
            exit(1)
        subprocess_name = "Min_Range"
        print("=== Input for {} process ===".format(subprocess_name))
        dict_master_process, dict_master_process_keys = ptestHandler.mPTest_database_get_json_process_file()
        df_dict_raw_data = Test_results.mResults_get_input_files(subprocess_name, results_dir_path, model)
        dict_raw_data_values = df_dict_raw_data.values()
        parser = cPTest_parser_json(process_name, subprocess_name)
        dict_finalDataPacket = parser.mPTest_parser_create_data_packet(dict_master_process,
                                                                       (list(dict_raw_data_values)[0]))
        message = "In mGui_post_all_input_files: {0} {1}".format(subprocess_name, dict_finalDataPacket)
        print(message)
        push_return = ptestHandler.mPTest_database_post_json(process_name, subprocess_name, dict_finalDataPacket)
        if push_return['err'] != '':
            messagebox.showerror("ERROR", "KEY DATA TO PTEST IS ERROR " + str(push_return['err']))
            exit(1)
        subprocess_name = "Noise_Test"
        print("=== Input for {} process ===".format(subprocess_name))
        dict_master_process, dict_master_process_keys = ptestHandler.mPTest_database_get_json_process_file()
        df_dict_raw_data = Test_results.mResults_get_input_files(subprocess_name, results_dir_path, model)
        dict_raw_data_values = df_dict_raw_data.values()
        parser = cPTest_parser_json(process_name, subprocess_name)
        dict_finalDataPacket = parser.mPTest_parser_create_data_packet(dict_master_process,
                                                                       (list(dict_raw_data_values)[0]))
        message = "In mGui_post_all_input_files: {0} {1}".format(subprocess_name, dict_finalDataPacket)
        print(message)
        push_return = ptestHandler.mPTest_database_post_json(process_name, subprocess_name, dict_finalDataPacket)
    else:
        print('station not in the list')
        exit(1)
    print("result = ", push_return['err'])
    if push_return['err'] != '':
        messagebox.showerror("ERROR", "KEY DATA TO PTEST IS ERROR " + str(push_return['err']))
    else:
        print("PUSH DATA TO PTEST DONE.")
        messagebox.showinfo("PUSH DATA TO PTEST DONE.", "PUSH DATA TO PTEST DONE.")
        quit()