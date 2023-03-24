from PySide2.QtGui import QFont
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
        small_text_font = QFont()
        small_text_font.setPointSize(10)
        self.setWindowTitle("HDLGen V2022.0.1")

        self.cornerWidget = QWidget()
        self.generate_btn = QPushButton("Generate model and TB HDL")
        self.generate_btn.setFont(small_text_font)
        #self.generate_btn.setFixedHeight(20)
        self.start_vivado_btn = QPushButton("Generate/Open Vivado")
        self.start_vivado_btn.setFont(small_text_font)
        #self.start_vivado_btn.setFixedHeight(20)
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
        self.project_manager = ProjectManager(self.proj_dir, self)

        self.setup_ui()


    def setup_ui(self):

        load_data = False

        if self.proj_dir is not None:
            load_data = True
        else:
            print("setting VHDL_check")
            self.project_manager.vhdl_check.setChecked(True)
        self.hdl_designer = HDLDesigner(self.proj_dir, load_data)

        print("Setting up UI")
        self.tabs.addTab(self.project_manager, "Project Manager")
        self.tabs.addTab(self.hdl_designer, "HDL Designer")
        self.tabs.addTab(Help(), "Help")
        font = self.tabs.font()
        font.setPointSize(10)
        self.tabs.setFont(font)
        self.generate_btn.clicked.connect(self.generate_btn_clicked)
        self.tabs.setCornerWidget(self.cornerWidget)
        self.start_vivado_btn.clicked.connect(self.start_vivado_btn_clicked)

        self.project_manager.vhdl_check.clicked.connect(lambda: self.hdl_designer.update_preview("VHDL"))
        self.project_manager.verilog_check.clicked.connect(lambda: self.hdl_designer.update_preview("Verilog"))
        self.tabs.currentChanged.connect(self.hdl_designer.compDetails.update_comp_name)

        self.mainLayout.addWidget(self.tabs)
        self.setLayout(self.mainLayout)

        self.container.setLayout(self.mainLayout)

        self.setCentralWidget(self.container)




    def generate_btn_clicked(self):
        if self.project_manager.vhdl_check.isChecked():
            self.generator.generate_folders()
            overwrite = self.generator.create_vhdl_file()
            self.generator.create_tcl_file("VHDL")
            self.generator.create_testbench_file(overwrite)
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("VHDL and Testbench Generated")
            msgBox.exec_()
        elif self.project_manager.verilog_check.isChecked():
            self.generator.generate_folders()
            overwrite = self.generator.create_verilog_file()
            self.generator.create_tcl_file("Verilog")
            self.generator.create_verilog_testbench_file(overwrite)
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("Verilog and Testbench Generated")
            msgBox.exec_()
    def start_vivado_btn_clicked(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Alert")
        if self.project_manager.vivado_dir_input.text()[-10:] == "vivado.bat":
            if self.project_manager.vhdl_check.isChecked():
                msgBox.setText("Starting EDA tool")
                msgBox.exec_()
                #self.generator.create_tcl_file()
                self.generator.run_tcl_file("VHDL")
            else:
                msgBox.setText("Starting EDA tool")
                msgBox.exec_()
                # self.generator.create_tcl_file()
                self.generator.run_tcl_file("Verilog")
        else:
            msgBox.setText("No vivado.bat path set")


