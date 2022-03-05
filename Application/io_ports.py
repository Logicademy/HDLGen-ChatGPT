import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from projectManager import ProjectManager

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"

class IOPorts(QWidget):

    def __init__(self, proj_dir):
        super().__init__()

        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)

        self.mainLayout = QHBoxLayout()

        self.mainLayout = QVBoxLayout()

        self.input_layout = QGridLayout()
        self.port_action_layout = QVBoxLayout()
        self.port_list_layout = QVBoxLayout()
        self.port_list_title_layout = QHBoxLayout()

        self.sig_name_label = QLabel("Signal Name")
        self.sig_name_label.setStyleSheet(WHITE_COLOR)
        self.sig_name_input = QLineEdit()

        self.sig_mode_label = QLabel("Mode")
        self.sig_mode_label.setStyleSheet(WHITE_COLOR)
        self.sig_mode_input = QComboBox()
        pal = self.sig_mode_input.palette()
        pal.setColor(QPalette.Button, QColor(255, 255, 255))
        self.sig_mode_input.setPalette(pal)
        self.sig_mode_input.addItem("Input")
        self.sig_mode_input.addItem("Output")

        self.sig_type_label = QLabel("Type")
        self.sig_type_label.setStyleSheet(WHITE_COLOR)
        self.sig_type_input = QComboBox()
        pal = self.sig_type_input.palette()
        pal.setColor(QPalette.Button, QColor(255, 255, 255))
        self.sig_type_input.setPalette(pal)
        self.sig_type_input.addItem("std_logic_vector")
        self.sig_type_input.addItem("logic")

        self.sig_size_label = QLabel("Size (eg. 32)")
        self.sig_size_label.setStyleSheet(WHITE_COLOR)
        self.sig_size_input = QLineEdit()
        self.onlyInt = QIntValidator()
        self.sig_size_input.setValidator(self.onlyInt)

        self.sig_description_label = QLabel("Signal Description")
        self.sig_description_label.setStyleSheet(WHITE_COLOR)
        self.sig_description_input = QLineEdit()

        self.add_btn = QPushButton("Add")
        self.add_btn.setFixedSize(60, 25)
        self.add_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}")


        self.io_list_label = QLabel("List of Input/Output Ports")
        self.io_list_label.setFont(title_font)
        self.io_list_label.setStyleSheet(WHITE_COLOR)

        self.save_btn = QPushButton("Save")
        self.save_btn.setFixedSize(60, 25)
        self.save_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}")


        # Port list layout widgets
        self.name_label = QLabel("Name")
        self.name_label.setFont(bold_font)
        self.mode_label = QLabel("Mode")
        self.mode_label.setFont(bold_font)
        self.type_label = QLabel("Type")
        self.type_label.setFont(bold_font)
        self.size_label = QLabel("Size")
        self.size_label.setFont(bold_font)

        self.list_div = QFrame()
        self.list_div.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129);}')
        self.list_div.setFixedHeight(1)

        self.port_table = QTableWidget()

        self.input_frame = QFrame()

        self.port_list_frame = QFrame()
        self.port_action_frame = QFrame()

        self.setup_ui()

    def setup_ui(self):

        self.sig_size_input.setFixedWidth(80)
        self.input_layout.addWidget(self.sig_name_label, 0, 0, 1, 1)
        self.input_layout.addWidget(self.sig_name_input, 1, 0, 1, 2)
        self.input_layout.addWidget(self.sig_mode_label, 0, 2, 1, 1)
        self.input_layout.addWidget(self.sig_mode_input, 1, 2, 1, 1)
        self.input_layout.addWidget(self.sig_type_label, 2, 0, 1, 1)
        self.input_layout.addWidget(self.sig_type_input, 3, 0, 1, 2)
        self.input_layout.addWidget(self.sig_size_label, 2, 2, 1, 1)
        self.input_layout.addWidget(self.sig_size_input, 3, 2, 1, 1)
        self.input_layout.addWidget(self.sig_description_label, 4, 0, 1, 1)
        self.input_layout.addWidget(self.sig_description_input, 5, 0, 1, 3)
        self.input_layout.addWidget(self.add_btn, 6, 2, 1, 1, alignment=Qt.AlignRight)

        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setFixedSize(400, 200)
        self.input_frame.setLayout(self.input_layout)

        self.sig_type_input.currentTextChanged.connect(self.enable_size_option)
        self.add_btn.clicked.connect(self.add_signal)


        # Port List section
        self.port_action_layout.addWidget(self.io_list_label, alignment=Qt.AlignTop)

        self.name_label.setFixedWidth(102)
        self.mode_label.setFixedWidth(50)
        self.type_label.setFixedWidth(120)
        self.size_label.setFixedWidth(30)

        self.port_list_title_layout.addWidget(self.name_label, alignment=Qt.AlignLeft)
        self.port_list_title_layout.addWidget(self.mode_label, alignment=Qt.AlignLeft)
        self.port_list_title_layout.addWidget(self.type_label, alignment=Qt.AlignLeft)
        self.port_list_title_layout.addWidget(self.size_label, alignment=Qt.AlignLeft)

        self.port_list_layout.setAlignment(Qt.AlignTop)
        self.port_list_layout.addLayout(self.port_list_title_layout)
        self.port_list_layout.addWidget(self.list_div)

        self.port_table.setColumnCount(4)
        self.port_table.setShowGrid(False)
        self.port_table.setColumnWidth(0, 104)
        self.port_table.setColumnWidth(1, 60)
        self.port_table.setColumnWidth(2, 126)
        self.port_table.setColumnWidth(3, 2)

        self.port_table.horizontalScrollBar().hide()
        header = self.port_table.horizontalHeader()
        header.hide()
        header = self.port_table.verticalHeader()
        header.hide()
        self.port_list_layout.addWidget(self.port_table)


        self.port_list_frame.setFrameShape(QFrame.StyledPanel)
        self.port_list_frame.setStyleSheet('.QFrame{background-color: white; border-radius: 5px;}')
        self.port_list_frame.setFixedSize(370, 115)
        self.port_list_frame.setLayout(self.port_list_layout)

        self.port_action_layout.addWidget(self.port_list_frame, alignment=Qt.AlignCenter)
        self.port_action_layout.addWidget(self.save_btn, alignment=Qt.AlignRight)

        self.port_action_frame.setFrameShape(QFrame.StyledPanel)
        self.port_action_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.port_action_frame.setContentsMargins(5, 5, 5, 5)
        self.port_action_frame.setFixedSize(400, 200)
        self.port_action_frame.setLayout(self.port_action_layout)

        self.mainLayout.addWidget(self.input_frame, alignment=Qt.AlignCenter)
        self.mainLayout.addWidget(self.port_action_frame, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)


    def add_signal(self):

        port_item_widget = QListWidgetItem()

        port_list_item_layout = QHBoxLayout()

        port_list_item_frame = QFrame()

        sig_details = [self.sig_name_input.text(),
                       self.sig_mode_input.currentText(),
                       self.sig_type_input.currentText(),
                       self.sig_size_input.text(),
                       self.sig_description_input.text()
                       ]
        print(sig_details[0])
        print(sig_details[1])
        print(sig_details[2])
        print(sig_details[3])
        print(sig_details[4])

        row_position = self.port_table.rowCount()
        self.port_table.insertRow(0)
        self.port_table.setRowHeight(0, 8)

        self.port_table.setItem(0, 0, QTableWidgetItem(sig_details[0]))
        self.port_table.setItem(0, 1, QTableWidgetItem(sig_details[1]))
        self.port_table.setItem(0, 2, QTableWidgetItem(sig_details[2]))
        self.port_table.setItem(0, 3, QTableWidgetItem(sig_details[3]))



    def enable_size_option(self):
        if self.sig_type_input.currentText() == "std_logic_vector":
            self.sig_size_input.setEnabled(True)
            self.sig_size_input.clear()
        else:
            self.sig_size_input.setEnabled(False)