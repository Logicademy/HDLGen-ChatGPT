import os
import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from xml.dom import minidom

from home import Home

class HDLGen(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("HDLGen")

        # Initializing UI Elements
        self.mainLayout = QHBoxLayout()

        self.open_btn = QPushButton("Open Existing project")

        self.new_btn = QPushButton("Create New project")

        # Creating a container
        self.container = QWidget()

        self.setup_ui()

    def setup_ui(self):

        print("Setting up UI")

        self.open_btn.setFixedSize(200, 80)
        self.open_btn.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.mainLayout.addWidget(self.open_btn)
        self.open_btn.clicked.connect(self.open_project)
        self.new_btn.setFixedSize(200, 80)
        self.new_btn.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.mainLayout.addWidget(self.new_btn)
        self.new_btn.clicked.connect(self.new_project)

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

def main():
    app = QApplication(sys.argv)
    window = HDLGen()
    window.resize(1000, 500)
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()

