#main.py is the file that is called when HDLGen-ChatGPT is started. From here the home.py, settings.py and help.py are called. This displays the splash page on start up
import os
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import sys
sys.path.append(".")
from Home.home import Home
from Help.help import HelpDialog
from Settings.settings import settingsDialog
import configparser


APP_AUTHORS = "Created by Fearghal Morgan, Abishek Bupathi & JP Byrne"
VICI_DESCRIPTION = "Online learning and assessment, Remote FPGA\nprototyping and course builder"
APP_DESCRIPTION = "<ul><li>Open source application and tutorials found on <a href='https://github.com/fearghal1/HDLGen'>GitHub</a></li>" \
                 "<li>Fast digital systems design capture from design and test specifications</li>" \
                 "<li>Generate HDL model templates and low-level logic pseudo code</li>" \
                 "<li>Generate HDL testbench templates (stimulus and signal checking)</li>" \
                 "<li>Assemble <a href='https://chat.openai.com/auth/login'>ChatGPT</a> prompt<li>" \
                 "<li>Execute <a href='https://chat.openai.com/auth/login'>ChatGPT</a> prompts to complete HDL model and testbench stimulus / signal checking</li>" \
                 "<li>Create EDA project, simulate HDL, synthesis HDL, prototype FPGA hardware</li>"

APP_DESCRIPTION1 = "<ul><li>Fast capture and generation of HDL model and testbench templates</li>" \
                 "<li>Generation of ChatGPT messages, including header and HDL templates</li>" \
                 "<li>ChatGPT-directed HDL model and testbench generation</li>" \
                 "<li>EDA project creation and launch</li>" \
                 "<li>Supports VHDL and Verilog / AMD Xilinx Vivado</li>" \
                 "<li>Open source application</li></ul>"
class HDLGen(QMainWindow):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("HDLGen-ChatGPT Version 1.0.0")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)

        title_1_font = QFont()
        title_1_font.setPointSize(15)

        bold_font = QFont()
        bold_font.setPointSize(10)
        bold_font.setBold(True)

        text_font = QFont()
        text_font.setPointSize(10)

        # Initializing UI Elements
        self.mainLayout = QHBoxLayout()
        self.button_layout = QGridLayout()
        self.info_layout = QVBoxLayout()
        self.Settings_top_layout = QGridLayout()

        self.open_btn = QPushButton("Open Existing Project")
        self.open_btn.setFont(text_font)
        self.new_btn = QPushButton("Create New Project")
        self.new_btn.setFont(text_font)
        self.help_btn = QPushButton("Help")
        self.help_btn.setFont(text_font)
        self.settings_btn = QPushButton("Settings")
        self.settings_btn.setFont(text_font)
        self.open_btn.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain;padding: 10px; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;padding: 10px;}")
        self.open_btn.clicked.connect(self.open_project)
        #self.new_btn.setFixedSize(150, 50)
        self.new_btn.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain;padding: 10px; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;padding: 10px;}")
        self.new_btn.clicked.connect(self.new_project)
        self.help_btn.clicked.connect(self.help_window)

        self.settings_btn.clicked.connect(self.settings_window)


        self.help_btn_spacer = QLabel("")
        self.settings_btn_spacer = QLabel("")
        self.settings_btn_spacer.setFixedSize(60, 25)
        self.help_btn_spacer.setFixedSize(35, 25)

        self.hdlgen_logo = QLabel("HDLGen-ChatGPT")#\nDigital Systems Design Capture\nEDA Project Creation Automation")
        self.hdlgen_logo.setFont(title_font)
        self.hdlgen_logo.setAlignment(Qt.AlignCenter)
        self.hdlgen_logo_1 = QLabel("Digital Systems Design Capture Automation")
        self.hdlgen_logo_1.setFont(title_1_font)
        self.hdlgen_logo_1.setAlignment(Qt.AlignCenter)
        self.app_description = QLabel(APP_DESCRIPTION)
        self.app_description.setFont(text_font)
        self.app_description.linkActivated.connect(self.link)
        self.processphoto = QLabel()
        curr_direct = os.getcwd()
        photo_direct = curr_direct + "/Resources/processdiagram.png"
        pixmap = QPixmap(photo_direct)

        self.processphoto.setPixmap(pixmap)
        "https://vicicourse.s3.eu-west-1.amazonaws.com/HDLGen/RSP2023/RSP2023_Top.pdf"
        self.tutorial_link = QLabel(
            '<a href="https://vicicourse.s3.eu-west-1.amazonaws.com/HDLGen/RSP2023/RSP2023_Top.pdf">Tutorials</a> Tutorial videos on HDLGen/ChatGPT, for a range of design examples')
        self.tutorial_link.setFont(text_font)
        self.tutorial_link.linkActivated.connect(self.link)
        self.github_link = QLabel('<a href="https://github.com/fearghal1/HDLGen">GitHub</a>\nIf you use the HDLGen application, please include the Github reference to our work')
        self.github_link.setFont(text_font)
        self.app_authors = QLabel(APP_AUTHORS)
        self.app_authors.setFont(bold_font)
        self.github_link.linkActivated.connect(self.link)
        self.vici_link = QLabel('<a href="https://vicilogic.com">VICILOGIC</a> online courses: digital systems design and RISC-V architecture and applications')
        self.vici_link.setFont(text_font)
        self.vici_link.linkActivated.connect(self.link)
        self.chatgpt_link = QLabel('<a href="https://chat.openai.com/auth/login">ChatGPT</a> Online large language model-based chatbot developed by OpenAI')
        self.chatgpt_link.setFont(text_font)
        self.chatgpt_link.linkActivated.connect(self.link)
        # Creating a container
        self.container = QWidget()
        self.config = configparser.ConfigParser()
        self.setup_ui()

    def setup_ui(self):

        print("Setting up UI")

        self.button_layout.addWidget(self.new_btn, 0, 1,  alignment= Qt.AlignLeft)
        self.button_layout.addWidget(self.open_btn, 0, 0, alignment= Qt.AlignRight)

        #self.button_layout.addWidget(self.open_btn, 0, 0, 1, 1)  # addWidget(self.open_btn, alignment= Qt.AlignCenter)
        self.info_layout.addSpacerItem(QSpacerItem(1, 25))

        self.info_layout.addWidget(self.hdlgen_logo, alignment= Qt.AlignCenter)
        #self.info_layout.addWidget(self.hdlgen_logo_1, alignment=Qt.AlignCenter)
        self.info_layout.addSpacerItem(QSpacerItem(1, 25))
        #self.info_layout.addWidget(self.app_authors, alignment=Qt.AlignCenter)
        #self.info_layout.addSpacerItem(QSpacerItem(1, 25))
        self.info_layout.addWidget(self.app_description, alignment=Qt.AlignCenter)
        #self.info_layout.addWidget(self.processphoto, alignment=Qt.AlignCenter)
        self.info_layout.addSpacerItem(QSpacerItem(1, 25))
        #self.info_layout.addWidget(self.app_description, alignment= Qt.AlignCenter)
        self.info_layout.addWidget(self.processphoto, alignment=Qt.AlignCenter)
        self.info_layout.addSpacerItem(QSpacerItem(1, 25))
        self.info_layout.addLayout(self.button_layout)
        self.info_layout.addSpacerItem(QSpacerItem(1, 25))
        #self.info_layout.addWidget(self.tutorial_link, alignment=Qt.AlignCenter)
        #self.info_layout.addSpacerItem(QSpacerItem(1, 10))
        #self.info_layout.addWidget(self.github_link, alignment= Qt.AlignCenter)
        #self.info_layout.addSpacerItem(QSpacerItem(1, 10))
        self.info_layout.addWidget(self.vici_link, alignment=Qt.AlignCenter)
        self.info_layout.addSpacerItem(QSpacerItem(1, 10))
        #self.info_layout.addWidget(self.chatgpt_link, alignment=Qt.AlignCenter)
        #self.info_layout.addSpacerItem(QSpacerItem(1, 50))

       # self.mainLayout.addLayout(self.button_layout)
        self.mainLayout.addWidget(self.settings_btn_spacer, alignment=Qt.AlignTop)
        self.mainLayout.addWidget(self.help_btn_spacer, alignment=Qt.AlignTop)
        self.mainLayout.addLayout(self.info_layout)
        self.mainLayout.addWidget(self.settings_btn, alignment=Qt.AlignTop)
        self.mainLayout.addWidget(self.help_btn, alignment=Qt.AlignTop)


        self.setLayout(self.mainLayout)

        self.container.setLayout(self.mainLayout)

        self.setCentralWidget(self.container)

    def help_window(self):
        help_dialog = HelpDialog()
        help_dialog.exec_()

    def new_project(self):
        self.window = Home()
        self.window.showMaximized()
        self.close()

    def open_project(self):
        self.config.read('config.ini')
        lastDir = self.config.get('user', 'recentEnviro')
        if not os.path.exists(lastDir):
            lastDir = "../User_Projects/"
                                                         #filter="HDLGen (*.hdlgen)")
        self.load_proj_dir = QFileDialog.getOpenFileName(self, "Select the Project XML File", lastDir,
                                                         filter="HDLGen (*.hdlgen)")
        if self.load_proj_dir[0]:
            print("Loading project from ", self.load_proj_dir[0])
            self.window = Home(self.load_proj_dir)
            self.window.showMaximized()
            self.close()

    def link(self, url_str):
        QDesktopServices.openUrl(QUrl(url_str))
    def settings_window(self):
        settings_dialog = settingsDialog()
        settings_dialog.exec_()

def main():
    app = QApplication(sys.argv)
    window = HDLGen()
    window.move(0, 0)
    window.show()
    app.setStyle('windowsvista')
    app.exec_()


if __name__ == '__main__':
    main()