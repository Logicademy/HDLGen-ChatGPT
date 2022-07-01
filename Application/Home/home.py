from PySide2.QtWidgets import *

from Application.ProjectManager.projectManager import ProjectManager
from Application.Generator.generator import Generator
from Application.Help.help import Help
from Application.HDLDesigner.hdlDesigner import HDLDesigner


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
        self.tabs.addTab(HDLDesigner(self.proj_dir, load_data), "HDL Designer")
        self.tabs.addTab(Generator(self.proj_dir), "Generator")
        self.tabs.addTab(Help(), "Help")
        self.mainLayout.addWidget(self.tabs)
        self.setLayout(self.mainLayout)

        self.container.setLayout(self.mainLayout)

        self.setCentralWidget(self.container)


