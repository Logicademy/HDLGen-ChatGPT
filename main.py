import os
import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from genFolder import *
from help import *


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
        self.tabs.addTab(GenFolderTab(), "Generate Folders")
        self.tabs.addTab(HelpTab(), "Help")
        self.mainLayout.addWidget(self.tabs)
        self.setLayout(self.mainLayout)

        self.container.setLayout(self.mainLayout)

        self.setCentralWidget(self.container)


def main():
    app = QApplication(sys.argv)
    window = HDLGen()
    window.resize(600, 150)
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()

