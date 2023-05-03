import sys
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import qtawesome as qta
import sys
sys.path.append(".")
from Home.home import Home
from Help.help import HelpDialog
from Settings.settings import settingsDialog


APP_AUTHORS = "Fearghal Morgan, Abishek Bupathi & JP Byrne"
APP_DESCRIPTION = "Open-source application wizard to generate \ndigital logic component FPGA design projects, \nHDL models, HDL testbenches and TCL scripts"
VICI_DESCRIPTION = "Online learning and assessment, Remote FPGA\nprototyping and course builder"

class HDLGen(QMainWindow):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("HDLGen V.1")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        title_font = QFont()
        title_font.setPointSize(30)
        title_font.setBold(True)

        bold_font = QFont()
        bold_font.setBold(True)

        # Initializing UI Elements
        self.mainLayout = QHBoxLayout()
        self.button_layout = QVBoxLayout()
        self.info_layout = QVBoxLayout()

        self.open_btn = QPushButton("Open Existing project")
        self.new_btn = QPushButton("Create New project")
        self.help_btn = QPushButton("Help")
        self.settings_btn = QPushButton("Settings")

        self.help_btn.setFixedSize(35, 25)
        self.help_btn.clicked.connect(self.help_window)

        self.settings_btn.setFixedSize(60, 25)
        self.settings_btn.clicked.connect(self.settings_window)

        self.hdlgen_logo = QLabel("HDLGen")
        self.hdlgen_logo.setFont(title_font)
        self.app_description = QLabel(APP_DESCRIPTION)
        self.github_link = QLabel('<a href="https://github.com/abishek-bupathi/HDLGen">HDLGen GitHub Repository</a>')
        self.app_authors = QLabel(APP_AUTHORS)
        self.app_authors.setFont(bold_font)
        self.github_link.linkActivated.connect(self.link)
        self.vici_description = QLabel(VICI_DESCRIPTION)
        self.vici_link = QLabel('<a href="https://vicilogic.com">vicilogic.com</a>')
        self.vici_link.linkActivated.connect(self.link)

        # Creating a container
        self.container = QWidget()

        self.setup_ui()

    def setup_ui(self):

        print("Setting up UI")

        self.open_btn.setFixedSize(150, 50)
        self.open_btn.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.button_layout.addSpacerItem(QSpacerItem(1, 70))
        self.button_layout.addWidget(self.open_btn, alignment= Qt.AlignCenter)
        self.open_btn.clicked.connect(self.open_project)
        self.new_btn.setFixedSize(150, 50)
        self.new_btn.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.button_layout.addWidget(self.new_btn, alignment= Qt.AlignCenter)
        self.button_layout.addSpacerItem(QSpacerItem(1, 70))
        self.new_btn.clicked.connect(self.new_project)

        self.info_layout.addSpacerItem(QSpacerItem(1, 50))
        self.info_layout.addWidget(self.hdlgen_logo, alignment= Qt.AlignCenter)
        self.info_layout.addWidget(self.app_authors, alignment=Qt.AlignCenter)
        self.info_layout.addWidget(self.app_description, alignment= Qt.AlignCenter)
        self.info_layout.addWidget(self.github_link, alignment= Qt.AlignCenter)
        self.info_layout.addSpacerItem(QSpacerItem(1, 10))
        self.info_layout.addWidget(self.vici_link, alignment=Qt.AlignCenter)
        self.info_layout.addWidget(self.vici_description, alignment=Qt.AlignCenter)

        self.info_layout.addSpacerItem(QSpacerItem(1, 50))

        self.mainLayout.addLayout(self.button_layout)
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
        self.load_proj_dir = QFileDialog.getOpenFileName(self, "Select the Project XML File", "../User_Projects/",
                                                         filter="HDLGen (*.hdlgen)")
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
    window.show()
    app.setStyle('windowsvista')
    app.exec_()


if __name__ == '__main__':
    main()