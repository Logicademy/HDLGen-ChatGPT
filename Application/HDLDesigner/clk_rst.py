import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from Application.ProjectManager.project_manager import ProjectManager


class ClkRst(QWidget):

    def __init__(self, proj_dir):
        super().__init__()

        self.mainLayout = QHBoxLayout()

        self.setup_ui()

    def setup_ui(self):

        self.setLayout(self.mainLayout)
