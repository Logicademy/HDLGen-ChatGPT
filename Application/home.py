import os
import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from projectManager import ProjectManager
from generate import Generate
from help import Help
from design import Design


class Home(QMainWindow):

    def __init__(self, proj_dir=None):

        super().__init__()
        self.setWindowTitle("HDLGen")

        # Initializing UI Elements
        self.mainLayout = QVBoxLayout()

        self.tabs = QTabWidget()

        # Creating a container
        self.container = QWidget()

        self.proj_dir = proj_dir

        self.setup_ui()


    def setup_ui(self):

        load_data = False

        if self.proj_dir is not None:
            load_data = True
        project_manager = ProjectManager(self.proj_dir, self)

        print("Setting up UI")
        self.tabs.addTab(project_manager, "Project Manager")
        self.tabs.addTab(Design(self.proj_dir, load_data), "Design")
        self.tabs.addTab(Generate(self.proj_dir), "Generate")
        # self.tabs.addTab(Help(), "Help")
        self.mainLayout.addWidget(self.tabs)
        self.setLayout(self.mainLayout)

        self.container.setLayout(self.mainLayout)

        self.setCentralWidget(self.container)


