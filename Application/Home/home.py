from PySide2.QtWidgets import *
import sys
sys.path.append("..")
from ProjectManager.project_manager import ProjectManager
from Generator.generator import Generator
from Help.help import Help
from HDLDesigner.hdl_designer import HDLDesigner


class Home(QMainWindow):

    def __init__(self, proj_dir=None):

        super().__init__()

        self.setWindowTitle("HDLGen V2022.0.1")

        self.cornerWidget = QWidget()
        self.generate_btn = QPushButton("Generate model and TB HDL")
        self.generate_btn.setFixedHeight(20)
        self.start_vivado_btn = QPushButton("Generate/Open Vivado")
        self.start_vivado_btn.setFixedHeight(20)
        self.cornerWidgetLayout = QHBoxLayout()
        self.cornerWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.cornerWidgetLayout.addWidget(self.generate_btn)
        self.cornerWidgetLayout.addWidget(self.start_vivado_btn)
        self.cornerWidget.setLayout(self.cornerWidgetLayout)

        # Initializing UI Elements
        self.mainLayout = QVBoxLayout()

        self.tabs = QTabWidget()

        # Creating a container
        self.container = QWidget()

        self.proj_dir = proj_dir
        self.generator = Generator()

        self.setup_ui()


    def setup_ui(self):

        load_data = False

        if self.proj_dir is not None:
            load_data = True
        project_manager = ProjectManager(self.proj_dir, self)
        hdl_designer = HDLDesigner(self.proj_dir, load_data)

        print("Setting up UI")
        self.tabs.addTab(project_manager, "Project Manager")
        self.tabs.addTab(hdl_designer, "HDL Designer")
        self.tabs.addTab(Help(), "Help")
        self.generate_btn.clicked.connect(self.generate_btn_clicked)
        self.tabs.setCornerWidget(self.cornerWidget)
        self.start_vivado_btn.clicked.connect(self.start_vivado_btn_clicked)


        self.tabs.currentChanged.connect(hdl_designer.compDetails.update_comp_name)

        self.mainLayout.addWidget(self.tabs)
        self.setLayout(self.mainLayout)

        self.container.setLayout(self.mainLayout)

        self.setCentralWidget(self.container)


    def generate_btn_clicked(self):

        self.generator.generate_folders()
        self.generator.create_vhdl_file()
        self.generator.create_tcl_file()
        self.generator.create_testbench_file()
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Alert")
        msgBox.setText("VHDL and Testbench Generated")
        msgBox.exec_()

    def start_vivado_btn_clicked(self):
        self.generator.run_tcl_file()
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Alert")
        msgBox.setText("Starting EDA tool  \nPlease wait!")
        msgBox.exec_()

