import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from projectManager import ProjectManager

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"

class AddProcess(QDialog):

    def __init__(self):
        super().__init__()
