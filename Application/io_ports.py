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

        self.mainLayout = QHBoxLayout()

        self.mainLayout = QVBoxLayout()

        self.input_layout = QGridLayout()
        self.port_list_layout = QVBoxLayout()

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

        self.io_list_label = QLabel("List of Input/Output Ports")
        self.io_list_label.setFont(title_font)

        self.save_btn = QPushButton("Save")
        self.save_btn.setFixedSize(60, 30)
        self.save_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}")

        self.input_frame = QFrame()
        self.port_list_frame = QFrame()

        self.setup_ui()

    def setup_ui(self):

        self.input_layout.addWidget(self.sig_name_label, 0, 0, 1, 1)
        self.input_layout.addWidget(self.sig_name_input, 1, 0, 1, 3)
        self.input_layout.addWidget(self.sig_mode_label, 2, 0, 1, 1)
        self.input_layout.addWidget(self.sig_mode_input, 3, 0, 1, 1)
        self.input_layout.addWidget(self.sig_type_label, 2, 1, 1, 1)
        self.input_layout.addWidget(self.sig_type_input, 3, 1, 1, 1)
        self.input_layout.addWidget(self.sig_size_label, 2, 2, 1, 1)
        self.input_layout.addWidget(self.sig_size_input, 3, 2, 1, 1)
        self.input_layout.addWidget(self.sig_description_label, 4, 0, 1, 1)
        self.input_layout.addWidget(self.sig_description_input, 5, 0, 1, 3)

        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setFixedSize(400, 200)
        self.input_frame.setLayout(self.input_layout)

        self.sig_type_input.currentTextChanged.connect(self.enable_size_option)


        # Port List section
        self.port_list_layout.addWidget(self.io_list_label, alignment=Qt.AlignLeft)

        self.port_list_layout.addWidget(self.save_btn, alignment=Qt.AlignRight)

        self.port_list_frame.setFrameShape(QFrame.StyledPanel)
        self.port_list_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.port_list_frame.setContentsMargins(5, 5, 5, 5)
        self.port_list_frame.setFixedSize(400, 200)
        self.port_list_frame.setLayout(self.port_list_layout)

        self.mainLayout.addWidget(self.input_frame, alignment=Qt.AlignCenter)
        self.mainLayout.addWidget(self.port_list_frame, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)

    def enable_size_option(self):
        if self.sig_type_input.currentText() == "std_logic_vector":
            self.sig_size_input.setEnabled(True)
            self.sig_size_input.clear()
        else:
            self.sig_size_input.setEnabled(False)