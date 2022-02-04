import os
import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from projectManager import ProjectManager
from generate import Generate
from help import Help


class HDLGen(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("HDLGen")

        # Initializing UI Elements
        self.mainLayout = QVBoxLayout()

        self.tabs = QTabWidget()

        # Creating a container
        self.container = QWidget()

        self.setup_ui()

    def setup_ui(self):

        print("Setting up UI")
        self.tabs.addTab(ProjectManager(), "Project Manager")
        self.tabs.addTab(Generate(), "Generate")
        self.tabs.addTab(Help(), "Help")
        self.mainLayout.addWidget(self.tabs)
        self.setLayout(self.mainLayout)

        self.container.setLayout(self.mainLayout)

        self.setCentralWidget(self.container)


def main():
    app = QApplication(sys.argv)
    window = HDLGen()
    window.resize(720, 480)
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()

