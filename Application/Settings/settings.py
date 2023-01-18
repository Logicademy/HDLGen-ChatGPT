from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import sys
import os
sys.path.append("..")
from ProjectManager.project_manager import ProjectManager

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"

class settingsDialog(QDialog):

    def __init__(self):#, add_or_edit, conc_data = None):
        super().__init__()

        self.setWindowTitle("Settings")
        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)

        self.input_layout = QGridLayout()
        self.mainLayout = QVBoxLayout()

        self.author_label = QLabel("Author")
        self.author_label.setStyleSheet(WHITE_COLOR)
        self.author_input = QLineEdit()

        self.email_label = QLabel("Email")
        self.email_label.setStyleSheet(WHITE_COLOR)
        self.email_input = QLineEdit()

        self.company_label = QLabel("Company")
        self.company_label.setStyleSheet(WHITE_COLOR)
        self.company_input = QLineEdit()

        self.vivado_label = QLabel("Vivado.bin path")
        self.vivado_label.setStyleSheet(WHITE_COLOR)
        self.vivado_input = QLineEdit()

        self.browse_btn = QPushButton("Browse")
        self.browse_btn.setFixedSize(60, 25)
        self.browse_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}")

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFixedSize(60, 25)
        self.cancel_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}")


        self.ok_btn = QPushButton("Ok")
        self.ok_btn.setEnabled(False)
        self.ok_btn.setFixedSize(60, 25)
        self.ok_btn.setStyleSheet(
            "QPushButton {background-color: rgb(169,169,169);  color: black; border-radius: 8px; border-style: plain;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}"
            "QPushButton:enabled {background-color: white; color: black; border-radius: 8px; border-style: plain; }")
        self.enable_ok_btn()
        self.input_frame = QFrame()

        self.cancelled = True

        self.setup_ui()
    def setup_ui(self):
        settingsDir = os.getcwd() + "\Settings\settings.txt"
        settings = open(settingsDir, "r")
        vivadoPath=settings.readline()
        author=settings.readline()
        email=settings.readline()
        company=settings.readline()
        settings.close()

        self.vivado_input.setText(vivadoPath)
        self.author_input.setText(author)
        self.email_input.setText(email)
        self.company_input.setText(company)
        self.input_layout.addWidget(self.author_label, 0, 0, 1, 1)
        self.input_layout.addWidget(self.author_input, 1, 0, 1, 1)
        self.input_layout.addWidget(self.email_label, 0, 1, 1, 1)
        self.input_layout.addWidget(self.email_input, 1, 1, 1, 1)
        self.input_layout.addWidget(self.company_label, 0, 2, 1, 2)
        self.input_layout.addWidget(self.company_input, 1, 2, 1, 2)
        self.input_layout.addWidget(self.vivado_label, 2, 0, 1, 3)
        self.input_layout.addWidget(self.vivado_input, 3, 0, 1, 3)
        self.input_layout.addWidget(self.browse_btn, 3, 3, 1, 1)
        self.input_layout.addWidget(self.cancel_btn, 4, 2, 1, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 4, 3, 1, 1, alignment=Qt.AlignRight)
        self.vivado_input.textChanged.connect(self.enable_ok_btn)
        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setFixedSize(600, 175)
        self.input_frame.setLayout(self.input_layout)
        self.cancel_btn.clicked.connect(self.cancel_selected)

        self.mainLayout.addWidget(self.input_frame, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)
        self.browse_btn.clicked.connect(self.set_vivado_bat_path)
        self.ok_btn.clicked.connect(self.save)
    def set_vivado_bat_path(self):
        vivado_bat_path = QFileDialog.getOpenFileName(self,"Select Xilinx Vivado Batch file (vivado.bat)","C:/", filter="Batch (*.bat)")
        vivado_bat_path = vivado_bat_path[0]
        self.vivado_input.setText(vivado_bat_path)


    def cancel_selected(self):
        self.cancelled = True
        self.close()

    def enable_ok_btn(self):
        if self.vivado_input.text() != "" and self.vivado_input.text() != "To be completed":
            self.ok_btn.setEnabled(True)
        else:
            self.ok_btn.setEnabled(False)

    def save(self):
        settingsDir = os.getcwd() + "\Settings\settings.txt"
        settings = open(settingsDir, "w")
        #settings = open("C:\\Users\\User\\HDLGen\\Application\\Settings\\settings.txt", "w")
        lines = [self.vivado_input.text() +"\n",self.author_input.text() +"\n", self.email_input.text() +"\n",self.company_input.text() +"\n"]
        settings.writelines(lines)
        settings.close()
        self.cancelled = False
        self.close()