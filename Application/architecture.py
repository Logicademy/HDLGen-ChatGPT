import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from projectManager import ProjectManager

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"
ICONS_DIR = "./resources/icons/"

class Architecture(QWidget):

    def __init__(self, proj_dir):
        super().__init__()

        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)

        self.mainLayout = QVBoxLayout()

        self.top_layout = QGridLayout()
        self.arch_action_layout = QVBoxLayout()

        self.arch_input = QLineEdit()
        self.arch_label = QLabel("Architecture Name")
        self.arch_label.setStyleSheet(WHITE_COLOR)

        self.new_proc_btn = QPushButton("New process")
        self.new_proc_btn.setFixedSize(100, 25)
        self.new_proc_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 5px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 5px; border-style: plain;}")

        self.new_conc_btn = QPushButton("New Concurrent statement")
        self.new_conc_btn.setFixedSize(175, 25)
        self.new_conc_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 5px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 5px; border-style: plain;}")

        self.new_strg_btn = QPushButton("New StateReg")
        self.new_strg_btn.setFixedSize(100, 25)
        self.new_strg_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 5px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 5px; border-style: plain;}")

        self.save_btn = QPushButton("Save")
        self.save_btn.setFixedSize(100, 25)
        self.save_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 5px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 5px; border-style: plain;}")

        self.name_label = QLabel("Name")
        self.name_label.setFont(bold_font)
        self.type_label = QLabel("Type")
        self.type_label.setFont(bold_font)
        self.in_sig_label = QLabel("Input Signals")
        self.in_sig_label.setFont(bold_font)

        self.list_div = QFrame()
        self.list_div.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129);}')
        self.list_div.setFixedHeight(1)

        self.proc_table = QTableWidget()


        self.list_header_layout = QHBoxLayout()
        self.list_layout = QVBoxLayout()

        self.list_frame = QFrame()
        self.main_frame = QFrame()

        self.setup_ui()



    def setup_ui(self):

        self.top_layout.addWidget(self.arch_label, 0, 0, alignment=Qt.AlignLeft)
        self.top_layout.addWidget(self.arch_input, 1, 0)
        self.top_layout.addWidget(self.new_proc_btn, 1, 1)
        # self.top_layout.addWidget(self.new_conc_btn, 2, 0)
        # self.top_layout.addWidget(self.new_strg_btn, 2, 1)

        self.arch_action_layout.addLayout(self.top_layout)

        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.main_frame.setContentsMargins(5, 5, 5, 5)
        self.main_frame.setFixedSize(400, 400)
        self.main_frame.setLayout(self.arch_action_layout)

        self.list_header_layout.addWidget(self.name_label, alignment=Qt.AlignLeft)
        self.list_header_layout.addWidget(self.type_label, alignment=Qt.AlignLeft)
        self.list_header_layout.addWidget(self.in_sig_label, alignment=Qt.AlignLeft)
        self.list_layout.addLayout(self.list_header_layout)
        self.list_layout.addWidget(self.list_div)

        self.proc_table.setColumnCount(4)
        self.proc_table.setShowGrid(False)
        self.proc_table.setColumnWidth(0, 102)
        self.proc_table.setColumnWidth(1, 55)
        self.proc_table.setColumnWidth(2, 105)
        self.proc_table.setColumnWidth(3, 5)
        self.proc_table.horizontalScrollMode()
        self.proc_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.proc_table.horizontalScrollBar().hide()
        header = self.proc_table.horizontalHeader()
        header.hide()
        header = self.proc_table.verticalHeader()
        header.hide()
        self.proc_table.setFrameStyle(QFrame.NoFrame)
        self.list_layout.addWidget(self.proc_table)


        self.list_frame.setFrameShape(QFrame.StyledPanel)
        self.list_frame.setStyleSheet('.QFrame{background-color: white; border-radius: 5px;}')
        self.list_frame.setFixedSize(370, 275)
        self.list_frame.setLayout(self.list_layout)

        self.arch_action_layout.addItem(QSpacerItem(10, 5))
        self.arch_action_layout.addWidget(self.list_frame)
        self.arch_action_layout.addItem(QSpacerItem(10, 15))
        self.arch_action_layout.addWidget(self.save_btn, alignment=Qt.AlignRight)

        self.mainLayout.addWidget(self.main_frame)

        self.setLayout(self.mainLayout)
