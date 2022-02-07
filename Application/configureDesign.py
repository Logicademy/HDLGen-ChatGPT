import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from projectManager import ProjectManager


class ConfigureDesign(QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QHBoxLayout()

        self.setup_ui()

    def setup_ui(self):

        self.setLayout(self.mainLayout)
