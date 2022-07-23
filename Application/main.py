import sys
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import sys
sys.path.append(".")
from Home.home import Home

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"

class HDLGen(QMainWindow):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("HDLGen")

        title_font = QFont()
        title_font.setPointSize(30)
        title_font.setBold(True)

        # Initializing UI Elements
        self.mainLayout = QHBoxLayout()
        self.button_layout = QVBoxLayout()
        self.info_layout = QVBoxLayout()

        self.open_btn = QPushButton("Open Existing project")
        self.new_btn = QPushButton("Create New project")

        self.hdlgen_logo = QLabel("HDLGen")
        self.hdlgen_logo.setFont(title_font)
        self.app_description = QLabel("Application Description")
        self.github_link = QLabel('<a href="https://github.com/abishek-bupathi/HDLGen">HDLGen GitHub Repository</a>')
        self.github_link.linkActivated.connect(self.link)

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

        self.info_layout.addSpacerItem(QSpacerItem(1, 70))
        self.info_layout.addWidget(self.hdlgen_logo, alignment= Qt.AlignCenter)
        self.info_layout.addWidget(self.app_description, alignment= Qt.AlignCenter)
        self.info_layout.addWidget(self.github_link, alignment= Qt.AlignCenter)
        self.info_layout.addSpacerItem(QSpacerItem(1, 70))


        self.mainLayout.addLayout(self.button_layout)
        self.mainLayout.addLayout(self.info_layout)

        self.setLayout(self.mainLayout)

        self.container.setLayout(self.mainLayout)

        self.setCentralWidget(self.container)

    def new_project(self):
        self.window = Home()
        self.window.resize(1000, 500)
        self.window.show()
        self.close()

    def open_project(self):
        self.load_proj_dir = QFileDialog.getOpenFileName(self, "Select the Project XML File", "E:\\",
                                                         filter="HDLGen (*.hdlgen)")
        print("Loading project from ", self.load_proj_dir[0])

        self.window = Home(self.load_proj_dir)
        self.window.resize(1000, 500)
        self.window.show()
        self.close()

    def link(self, url_str):
        QDesktopServices.openUrl(QUrl(url_str))

def main():
    app = QApplication(sys.argv)
    window = HDLGen()
    window.setFixedSize(600, 300)
    window.show()
    app.setStyle('windowsvista')
    app.exec_()


if __name__ == '__main__':
    main()

