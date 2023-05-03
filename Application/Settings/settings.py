from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import sys
# make sure to add to requirements.txt
import configparser
sys.path.append("..")

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

        self.vivado_label = QLabel("Vivado.bat path")
        self.vivado_label.setStyleSheet(WHITE_COLOR)
        self.vivado_input = QLineEdit()

        self.ChatGPT_header_label = QLabel("ChatGPT Header Commands")
        self.ChatGPT_header_label.setStyleSheet(WHITE_COLOR)
        self.ChatGPT_header_input = QPlainTextEdit()
        self.ChatGPT_header_input.setLineWrapMode(QPlainTextEdit.WidgetWidth)

        self.ChatGPT_model_label = QLabel("ChatGPT Model Commands")
        self.ChatGPT_model_label.setStyleSheet(WHITE_COLOR)
        self.ChatGPT_model_input = QPlainTextEdit()
        self.ChatGPT_model_input.setLineWrapMode(QPlainTextEdit.WidgetWidth)

        self.ChatGPT_testbench_label = QLabel("ChatGPT Testbench Commands")
        self.ChatGPT_testbench_label.setStyleSheet(WHITE_COLOR)
        self.ChatGPT_testbench_input = QPlainTextEdit()
        self.ChatGPT_testbench_input.setLineWrapMode(QPlainTextEdit.WidgetWidth)

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
        self.ok_btn.setFixedSize(60, 25)
        self.ok_btn.setStyleSheet(
            "QPushButton {background-color: rgb(169,169,169);  color: black; border-radius: 8px; border-style: plain;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}"
            "QPushButton:enabled {background-color: white; color: black; border-radius: 8px; border-style: plain; }")
        self.input_frame = QFrame()

        self.cancelled = True
        self.config = configparser.ConfigParser()

        self.setup_ui()
    def setup_ui(self):
        self.config.read('config.ini')
        vivadoPath= self.config.get('user', 'vivado.bat')
        author = self.config.get('user', 'author')
        email = self.config.get('user', 'email')
        company = self.config.get('user', 'company')
        #chatGPTHeader = self.config.get('user', 'chatGPTHeader')
        #chatGPTModel = self.config.get('user', 'chatGPTModel')
        #chatGPTTestbench = self.config.get('user', 'chatGPTTestbench')

        self.vivado_input.setText(vivadoPath.strip())
        self.author_input.setText(author.strip())
        self.email_input.setText(email.strip())
        self.company_input.setText(company.strip())
        #self.ChatGPT_header_input.setPlainText(chatGPTHeader)
        #self.ChatGPT_model_input.setPlainText(chatGPTModel)
        #self.ChatGPT_testbench_input.setPlainText(chatGPTTestbench)
        self.input_layout.addWidget(self.author_label, 0, 0, 1, 1)
        self.input_layout.addWidget(self.author_input, 1, 0, 1, 1)
        self.input_layout.addWidget(self.email_label, 0, 1, 1, 1)
        self.input_layout.addWidget(self.email_input, 1, 1, 1, 1)
        self.input_layout.addWidget(self.company_label, 0, 2, 1, 2)
        self.input_layout.addWidget(self.company_input, 1, 2, 1, 2)
        self.input_layout.addWidget(self.vivado_label, 2, 0, 1, 3)
        self.input_layout.addWidget(self.vivado_input, 3, 0, 1, 3)
        self.input_layout.addWidget(self.browse_btn, 3, 3, 1, 1)
        #self.input_layout.addWidget(self.ChatGPT_header_label, 4, 0, 1, 4)
        #self.input_layout.addWidget(self.ChatGPT_header_input, 5, 0, 4, 4)
        #self.input_layout.addWidget(self.ChatGPT_model_label, 9, 0, 1, 4)
        #self.input_layout.addWidget(self.ChatGPT_model_input, 10, 0, 4, 4)
        #self.input_layout.addWidget(self.ChatGPT_testbench_label, 14, 0, 1, 4)
        #self.input_layout.addWidget(self.ChatGPT_testbench_input, 15, 0, 4, 4)

        self.input_layout.addWidget(self.cancel_btn, 4, 2, 1, 1, alignment=Qt.AlignRight)#20, 2, 1, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 4, 3, 1, 1, alignment=Qt.AlignRight)#20, 2, 1, 1, alignment=Qt.AlignRight)#20, 3, 1, 1, alignment=Qt.AlignRight)
        #self.vivado_input.textChanged.connect(self.enable_ok_btn)
        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setFixedSize(600, 600)
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
        if self.vivado_input.text().strip() == "":
            self.vivado_input.setText("To be completed")
        if self.author_input.text().strip() == "":
            self.author_input.setText("To be completed")
        if self.email_input.text().strip() == "":
            self.email_input.setText("To be completed")
            print(self.email_input.text())
        if self.company_input.text().strip() == "":
            self.company_input.setText("To be completed")

        self.config.set("user", "author", self.author_input.text())
        self.config.set("user", "email", self.email_input.text())
        self.config.set("user", "company", self.company_input.text())
        self.config.set("user", "vivado.bat", self.vivado_input.text())
        #self.config.set("user", "chatGPTHeader", self.ChatGPT_header_input.toPlainText())
        #self.config.set("user", "chatGPTModel", self.ChatGPT_model_input.toPlainText())
        #self.config.set("user", "chatGPTTestbench", self.ChatGPT_testbench_input.toPlainText())
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
        self.cancelled = False
        self.close()