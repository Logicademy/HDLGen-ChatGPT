import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *



sys.path.append("..")

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"

class seqDialog(QDialog):

    def __init__(self, proj_dir):
        super().__init__()
        input_font = QFont()
        input_font.setPointSize(10)
        self.input_layout = QGridLayout()
        self.setWindowTitle("Set up clk/rst")

        self.mainLayout = QVBoxLayout()


        self.activeClkEdge_label = QLabel("Active Clk Edge")
        self.activeClkEdge_label.setFont(input_font)
        self.activeClkEdge_label.setStyleSheet(WHITE_COLOR)
        self.activeClkEdge_input = QComboBox()
        self.activeClkEdge_input.setFont(input_font)
        self.activeClkEdge_input.setStyleSheet("QComboBox {padding: 2px;}")
        pal = self.activeClkEdge_input.palette()
        pal.setColor(QPalette.Button, QColor(255, 255, 255))
        self.activeClkEdge_input.setPalette(pal)
        self.activeClkEdge_input.addItem("L-H")
        self.activeClkEdge_input.addItem("H-L")

        self.rst_label = QLabel("rst")
        self.rst_label.setFont(input_font)
        self.rst_label.setStyleSheet(WHITE_COLOR)
        self.rst_input = QComboBox()
        self.rst_input.setFont(input_font)
        self.rst_input.setStyleSheet("QComboBox {padding: 2px;}")
        pal = self.rst_input.palette()
        pal.setColor(QPalette.Button, QColor(255, 255, 255))
        self.rst_input.setPalette(pal)
        self.rst_input.addItem("No")
        self.rst_input.addItem("Yes")

        self.rstType_label = QLabel("rst type")
        self.rstType_label.setFont(input_font)
        self.rstType_label.setStyleSheet(WHITE_COLOR)
        self.rstType_label.setVisible(False)
        self.rstType_input = QComboBox()
        self.rstType_input.setFont(input_font)
        self.rstType_input.setStyleSheet("QComboBox {padding: 2px;}")
        pal = self.rstType_input.palette()
        pal.setColor(QPalette.Button, QColor(255, 255, 255))
        self.rstType_input.setPalette(pal)
        self.rstType_input.addItem("asynch")
        self.rstType_input.addItem("synch")
        self.rstType_input.setVisible(False)

        self.activeRstLvlEq1_label = QLabel("Active rst lvl")
        self.activeRstLvlEq1_label.setStyleSheet(WHITE_COLOR)
        self.activeRstLvlEq1_label.setVisible(False)
        self.activeRstLvlEq1_label.setFont(input_font)
        self.activeRstLvlEq1_input = QComboBox()
        pal = self.activeRstLvlEq1_input.palette()
        self.activeRstLvlEq1_input.setFont(input_font)
        self.activeRstLvlEq1_input.setStyleSheet("QComboBox {padding: 2px;}")
        pal.setColor(QPalette.Button, QColor(255, 255, 255))
        self.activeRstLvlEq1_input.setPalette(pal)
        self.activeRstLvlEq1_input.addItem("1")
        self.activeRstLvlEq1_input.addItem("0")
        self.activeRstLvlEq1_input.setVisible(False)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFont(input_font)
        self.cancel_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}")

        self.ok_btn = QPushButton("Ok")
        self.ok_btn.setFont(input_font)
        self.ok_btn.setStyleSheet(
            "QPushButton {background-color: rgb(169,169,169);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            "QPushButton:enabled {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px; }")

        self.input_frame = QFrame()

        self.cancelled = True

        self.setup_ui()

        if proj_dir != None:
            self.load_data(proj_dir)
    def setup_ui(self):
        self.input_layout.addWidget(self.activeClkEdge_label, 0, 0, 1, 1, alignment=Qt.AlignTop)
        self.input_layout.addWidget(self.activeClkEdge_input, 1, 0, 1, 1, alignment=Qt.AlignTop)
        self.input_layout.addWidget(self.rst_label, 0, 1, 1, 1, alignment=Qt.AlignTop)
        self.input_layout.addWidget(self.rst_input, 1, 1, 1, 1, alignment=Qt.AlignTop)
        self.input_layout.addItem(QSpacerItem(0, 100), 2, 0)
        self.input_layout.addWidget(self.rstType_label, 2, 0, 1, 1, alignment=Qt.AlignBottom)
        self.input_layout.addWidget(self.rstType_input, 3, 0, 1, 1, alignment=Qt.AlignTop)
        self.input_layout.addWidget(self.activeRstLvlEq1_label, 2, 1, 1, 1, alignment=Qt.AlignBottom)
        self.input_layout.addWidget(self.activeRstLvlEq1_input, 3, 1, 1, 1, alignment=Qt.AlignTop)
        self.input_layout.addItem(QSpacerItem(0, 100), 4, 0)
        self.input_layout.addWidget(self.cancel_btn, 5, 0, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 5, 1, alignment=Qt.AlignRight)

        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setFixedSize(400, 400)
        self.input_frame.setLayout(self.input_layout)

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

    def load_data(self, proj_dir):

        root = minidom.parse(proj_dir[0])
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")

        clkAndRst = hdlDesign[0].getElementsByTagName('clkAndRst')
        if clkAndRst[0].firstChild is not None:
            for i in range(0, len(clkAndRst)):
                clkEdgeValue = clkAndRst[i].getElementsByTagName('activeClkEdge')[0].firstChild.data
                rstValue = clkAndRst[i].getElementsByTagName('rst')[0].firstChild.data
                self.activeClkEdge_input.setCurrentText(clkEdgeValue)
                self.rst_input.setCurrentText(rstValue)
                if rstValue == "Yes":
                    rstTypeValue = clkAndRst[i].getElementsByTagName('RstType')[0].firstChild.data
                    rstLvlValue = clkAndRst[i].getElementsByTagName('ActiveRstLvl')[0].firstChild.data
                    self.rstType_input.setCurrentText(rstTypeValue)
                    self.activeRstLvlEq1_input.setCurrentText(rstLvlValue)
