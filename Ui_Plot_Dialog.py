from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QApplication, QDialog, QDialogButtonBox, QHBoxLayout, QWidget
import sys


class Ui_Plot_Dialog(QDialog):

    def __init__(self, dict_input_raw_data, parent=None):
        super(Ui_Plot_Dialog, self).__init__(parent)
        self.setWindowTitle("Performance Test")
        self.df_dict_list = dict_input_raw_data
        self.setupUi(self)
        self.setupPlot()

    def setupUi(self, Dialog):
        # Add Dialog Window
        # Dialog = QApplication(sys.argv)
        # print(main_gui.nameLineEdit)

        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 600)

        # Create Dialog Button Box on Dialog Window
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

    def setupPlot(self):
        # Create QVBoxLayout
        layout = QtWidgets.QVBoxLayout()

        # Create our pandas DataFrame
        for df in self.df_dict_list:
            # Create the maptlotlib FigureCanvas object
            sc = MplCanvas(self, width=10, height=11, dpi=50)
            self.df_dict_list[df].plot(ax=sc.axes)
            layout.addWidget(sc)

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(layout)

        # Add main widget to layout
        self.layout().addWidget(self.widget)
        self.layout().addWidget(self.buttonBox)
        self.show()  # draw plot on canvas


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)