from PySide2.QtGui import QFont
from PySide2.QtWidgets import *
import os
import sys
sys.path.append("..")
import zipfile
import pyperclip
from ProjectManager.project_manager import ProjectManager
from Generator.generator import Generator
from Help.help import Help
from HDLDesigner.hdl_designer import HDLDesigner
from ProjectManager.generate_dialog import GenerationDialog
from HDLDesigner.Architecture.note_dialog import note_Dialog
from xml.dom import minidom


class Home(QMainWindow):

    def __init__(self, proj_dir=None):

        super().__init__()
        small_text_font = QFont()
        small_text_font.setPointSize(10)
        self.setWindowTitle("HDLGen V2022.0.1")

        self.cornerWidget = QWidget()
        #self.generate_btn = QPushButton("Generate")
        #self.generate_btn.setFont(small_text_font)
        self.start_vivado_btn = QPushButton("Open EDA Project")
        self.start_vivado_btn.setFont(small_text_font)
        self.export_project_btn = QPushButton("Export Project")
        self.export_project_btn.setFont(small_text_font)
        self.cornerWidgetLayout = QHBoxLayout()
        self.cornerWidgetLayout.setContentsMargins(0, 0, 0, 0)
        #self.cornerWidgetLayout.addWidget(self.generate_btn)
        self.cornerWidgetLayout.addWidget(self.start_vivado_btn)
        self.cornerWidgetLayout.addWidget(self.export_project_btn)
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
        print(self.proj_dir)
        load_data = False

        if self.proj_dir is not None:
            load_data = True
        else:
            self.project_manager.vhdl_check.setChecked(True)
        self.hdl_designer = HDLDesigner(self.proj_dir, load_data)

        self.tabs.addTab(self.project_manager, "Project Manager")
        self.tabs.addTab(self.hdl_designer, "HDL Designer")
        self.tabs.addTab(Help(), "Help")
        self.tabs.currentChanged.connect(self.handle_tab_change)
        font = self.tabs.font()
        font.setPointSize(10)
        self.tabs.setFont(font)
        #self.generate_btn.clicked.connect(self.generate_btn_clicked)
        self.tabs.setCornerWidget(self.cornerWidget)
        self.start_vivado_btn.clicked.connect(self.start_eda_tool)
        self.export_project_btn.clicked.connect(self.export_project)

        self.project_manager.vhdl_check.clicked.connect(lambda: self.hdl_designer.update_preview("VHDL"))
        #self.project_manager.vhdl_check.clicked.connect(lambda: self.hdl_designer.chatGPT.VHDLVisible())
        self.project_manager.vhdl_check.clicked.connect(lambda: self.hdl_designer.generate.VHDLVisible())
        self.project_manager.verilog_check.clicked.connect(lambda: self.hdl_designer.update_preview("Verilog"))
        #self.project_manager.verilog_check.clicked.connect(lambda: self.hdl_designer.chatGPT.VerilogVisible())
        self.project_manager.verilog_check.clicked.connect(lambda: self.hdl_designer.generate.VerilogVisible())
        self.tabs.currentChanged.connect(self.hdl_designer.compDetails.update_comp_name)

        self.hdl_designer.generate.generate_model.clicked.connect(self.HDL_model_generate)
        self.hdl_designer.generate.generate_chatgpt_model.clicked.connect(self.chatgpt_model_generate)
        self.hdl_designer.generate.generate_testbench.clicked.connect(self.HDL_testbench_generate)
        self.hdl_designer.generate.generate_chatgpt_testbench.clicked.connect(self.chatgpt_testbench_generate)

        self.mainLayout.addWidget(self.tabs)
        self.setLayout(self.mainLayout)

        self.container.setLayout(self.mainLayout)

        self.setCentralWidget(self.container)

    def chatgpt_model_generate(self):
        if self.hdl_designer.generate.chatgpt_model_bk_checkBox.isChecked():
            self.model_generate("6,7")
        else:
            self.model_generate("6")

    def HDL_model_generate(self):
        if self.hdl_designer.generate.model_bk_checkBox.isChecked():
            self.model_generate("0,1")
        else:
            self.model_generate("0")
    def chatgpt_testbench_generate(self):
        if self.hdl_designer.generate.chatgpt_testbench_bk_checkBox.isChecked():
            self.testbench_generate("8,9")
        else:
            self.testbench_generate("8")

    def HDL_testbench_generate(self):
        if self.hdl_designer.generate.testbench_bk_checkBox.isChecked() and self.hdl_designer.generate.wcfg_checkBox.isChecked():
            self.testbench_generate("2,3,10")
        elif self.hdl_designer.generate.testbench_bk_checkBox.isChecked():
            self.testbench_generate("2,3")
        elif self.hdl_designer.generate.wcfg_checkBox.isChecked():
            self.testbench_generate("2,10")
        else:
            self.testbench_generate("2")
    def testbench_generate(self, files):
        if self.project_manager.vhdl_check.isChecked():
            self.generator.generate_folders()
            self.generator.create_testbench_file(files)
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("Generated")
            msgBox.exec_()
        elif self.project_manager.verilog_check.isChecked():
            self.generator.generate_folders()
            self.generator.create_verilog_testbench_file(files)
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("Generated")
            msgBox.exec_()
    def model_generate(self, files):
        if self.project_manager.vhdl_check.isChecked():
            self.generator.generate_folders()
            instances = self.generator.create_vhdl_file(files)
            if self.project_manager.vivado_check.isChecked():
                self.generator.create_tcl_file("VHDL", instances)
            else:
                self.generator.create_quartus_tcl_file("VHDL", instances)
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("Generated")
            msgBox.exec_()
        elif self.project_manager.verilog_check.isChecked():
            self.generator.generate_folders()
            instances = self.generator.create_verilog_file(files)
            if self.project_manager.vivado_check.isChecked():
                self.generator.create_tcl_file("VERiLOG", instances)
            else:
                self.generator.create_quartus_tcl_file("VERILOG", instances)
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("Generated")
            msgBox.exec_()

    def generate_btn_clicked(self):
        gen = GenerationDialog()
        gen.exec_()
        if not gen.cancelled:
            if self.project_manager.vhdl_check.isChecked():
                self.generator.generate_folders()
                instances = self.generator.create_vhdl_file(gen.get_selected_files())
                if self.project_manager.vivado_check.isChecked():
                    self.generator.create_tcl_file("VHDL", instances)
                else:
                    self.generator.create_quartus_tcl_file("VHDL", instances)
                self.generator.create_testbench_file(gen.get_selected_files())
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("Selected Files Generated")
                msgBox.exec_()
            elif self.project_manager.verilog_check.isChecked():
                self.generator.generate_folders()
                instances = self.generator.create_verilog_file(gen.get_selected_files())
                if self.project_manager.vivado_check.isChecked():
                    self.generator.create_tcl_file("VERILOG", instances)
                else:
                    self.generator.create_quartus_tcl_file("VERILOG", instances)
                self.generator.create_verilog_testbench_file(gen.get_selected_files())
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("Verilog and Testbench Generated")
                msgBox.exec_()
    def copy_file_contents_to_clipboard(self, file_path):
        try:
            with open(file_path, 'r') as file:
                file_contents = file.read()
                pyperclip.copy(file_contents)
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("File contents copied to clipboard successfully")
                msgBox.exec_()
        except FileNotFoundError:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("File not found. Press Generate button")
            msgBox.exec_()
        except Exception as e:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("An error occurred. Check terminal for details")
            msgBox.exec_()
            print("An error occurred:", str(e))
    def start_eda_tool(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Alert")
        if self.project_manager.vivado_check.isChecked():
            if self.project_manager.vivado_dir_input.text()[-10:] == "vivado.bat":
                if self.project_manager.vhdl_check.isChecked():
                    msgBox.setText("Starting EDA tool")
                    msgBox.exec_()
                    #self.generator.create_tcl_file()
                    self.generator.run_tcl_file("VHDL","Vivado")
                else:
                    msgBox.setText("Starting EDA tool")
                    msgBox.exec_()
                    # self.generator.create_tcl_file()
                    self.generator.run_tcl_file("Verilog", "Vivado")
            else:
                msgBox.setText("No vivado.bat path set")
        else:
            #if self.project_manager.intel_dir_input.text()[-11:] == "quartus.exe":
            if self.project_manager.vhdl_check.isChecked():
                msgBox.setText("Starting EDA tool")
                msgBox.exec_()
                self.generator.run_tcl_file("VHDL", "Quartus")
            else:
                msgBox.setText("Starting EDA tool")
                msgBox.exec_()
                self.generator.run_tcl_file("Verilog", "Quartus")
            #else:
                #msgBox.setText("No quartus.exe path set")

    def export_project(self):
        self.project_manager.export_project()


    def handle_tab_change(self, index):
        if index != 0:
            self.project_manager.save_xml()
            self.hdl_designer.package.load_data()
            self.hdl_designer.subcomponents.load_data()
            self.hdl_designer.compDetails.save_data()
            self.hdl_designer.compDetails.save_data()
            self.hdl_designer.ioPorts.save_data()
            self.hdl_designer.architecture.save_data()
            self.hdl_designer.generate.save_data()
            self.hdl_designer.internalSignal.save_data()




