import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *



sys.path.append("..")
from ProjectManager.project_manager import ProjectManager
#from HDLDesigner.IOPorts.sequential_dialog import seqDialog

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"

class seqDialog(QDialog):

    def __init__(self, signal_data = None):
        super().__init__()

        self.input_layout = QGridLayout()
        self.setWindowTitle("Set up clk/rst")

        self.mainLayout = QVBoxLayout()
        #self.sig_name_label = QLabel("Signal Name *")
        #self.sig_name_label.setStyleSheet(WHITE_COLOR)
        #self.sig_name_input = QLineEdit()


        self.activeClkEdge_label = QLabel("Active Clk Edge")
        self.activeClkEdge_label.setStyleSheet(WHITE_COLOR)
        self.activeClkEdge_input = QComboBox()
        pal = self.activeClkEdge_input.palette()
        pal.setColor(QPalette.Button, QColor(255, 255, 255))
        self.activeClkEdge_input.setPalette(pal)
        self.activeClkEdge_input.addItem("L-H")
        self.activeClkEdge_input.addItem("H-L")

        self.rst_label = QLabel("rst")
        self.rst_label.setStyleSheet(WHITE_COLOR)
        self.rst_input = QComboBox()
        pal = self.rst_input.palette()
        pal.setColor(QPalette.Button, QColor(255, 255, 255))
        self.rst_input.setPalette(pal)
        self.rst_input.addItem("No")
        self.rst_input.addItem("Yes")

        self.rstType_label = QLabel("rst type")
        self.rstType_label.setStyleSheet(WHITE_COLOR)
        self.rstType_label.setVisible(False)
        self.rstType_input = QComboBox()
        pal = self.rstType_input.palette()
        pal.setColor(QPalette.Button, QColor(255, 255, 255))
        self.rstType_input.setPalette(pal)
        self.rstType_input.addItem("asynch")
        self.rstType_input.addItem("synch")
        self.rstType_input.setVisible(False)

        self.activeRstLvlEq1_label = QLabel("Active rst lvl")
        self.activeRstLvlEq1_label.setStyleSheet(WHITE_COLOR)
        self.activeRstLvlEq1_label.setVisible(False)
        self.activeRstLvlEq1_input = QComboBox()
        pal = self.activeRstLvlEq1_input.palette()
        pal.setColor(QPalette.Button, QColor(255, 255, 255))
        self.activeRstLvlEq1_input.setPalette(pal)
        self.activeRstLvlEq1_input.addItem("1")
        self.activeRstLvlEq1_input.addItem("0")
        self.activeRstLvlEq1_input.setVisible(False)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFixedSize(60, 25)
        self.cancel_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}")


        self.ok_btn = QPushButton("Ok")
        self.ok_btn.setFixedSize(60, 25)
        self.ok_btn.setStyleSheet(
            "QPushButton {background-color: rgb(169,169,169);  color: black; border-radius: 8px; border-style: plain;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}"
            "QPushButton:enabled {background-color: white; color: black; border-radius: 8px; border-style: plain; }")

        self.input_frame = QFrame()

        self.cancelled = True

        self.setup_ui()

        if signal_data != None:
            self.load_signal_data(signal_data)

    def setup_ui(self):
        self.input_layout.addWidget(self.activeClkEdge_label, 0, 0, 1, 1, alignment=Qt.AlignTop)
        self.input_layout.addWidget(self.activeClkEdge_input, 1, 0, 1, 1, alignment=Qt.AlignTop)
        self.input_layout.addWidget(self.rst_label, 0, 1, 1, 2, alignment=Qt.AlignTop)
        self.input_layout.addWidget(self.rst_input, 1, 1, 1, 2, alignment=Qt.AlignTop)
        self.input_layout.addItem(QSpacerItem(0, 100), 2, 0)
        self.input_layout.addWidget(self.rstType_label, 2, 0, 1, 1, alignment=Qt.AlignBottom)
        self.input_layout.addWidget(self.rstType_input, 3, 0, 1, 1, alignment=Qt.AlignTop)
        self.input_layout.addWidget(self.activeRstLvlEq1_label, 2, 1, 1, 2, alignment=Qt.AlignBottom)
        self.input_layout.addWidget(self.activeRstLvlEq1_input, 3, 1, 1, 2, alignment=Qt.AlignTop)
        self.input_layout.addItem(QSpacerItem(0, 100), 4, 0)
        self.input_layout.addWidget(self.cancel_btn, 5, 1, alignment=Qt.AlignRight.AlignBottom)
        self.input_layout.addWidget(self.ok_btn, 5, 2, alignment=Qt.AlignRight.AlignBottom)

        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setFixedSize(300, 175)
        self.input_frame.setLayout(self.input_layout)

        #self.enable_size_option
        self.ok_btn.clicked.connect(self.get_clkAndRst)
        self.cancel_btn.clicked.connect(self.cancel_selected)
        self.rst_input.currentTextChanged.connect(self.rst_options)
        self.mainLayout.addWidget(self.input_frame, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)

    def get_clkAndRst(self):
        if self.rst_input.currentText() == "Yes":
            clkAndRst_details = [self.activeClkEdge_input.currentText(),
                                   self.rst_input.currentText(),
                                   self.rstType_input.currentText(),
                                   self.activeRstLvlEq1_input.currentText()
                                ]
        else:
            clkAndRst_details = [self.activeClkEdge_input.currentText(),
                                 self.rst_input.currentText()
                                 ]
        self.cancelled = False
        self.close()
        return clkAndRst_details
    def cancel_selected(self):
        self.cancelled = True
        self.close()



    def rst_options(self):
        if self.rst_input.currentText() == "Yes":
            self.rstType_label.setVisible(True)
            self.rstType_input.setVisible(True)
            self.activeRstLvlEq1_label.setVisible(True)
            self.activeRstLvlEq1_input.setVisible(True)
        else:
            self.rstType_label.setVisible(False)
            self.rstType_input.setVisible(False)
            self.activeRstLvlEq1_label.setVisible(False)
            self.activeRstLvlEq1_input.setVisible(False)

    def enable_size_option(self):
        if self.sig_type_input.currentText() == "Yes":
            self.sig_size_input.setEnabled(True)
            self.sig_size_input.clear()
        else:
            self.sig_size_input.setEnabled(False)
            self.sig_size_input.setText("1")