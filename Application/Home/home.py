from PySide2.QtGui import QFont
from PySide2.QtWidgets import *
import os
import sys
sys.path.append("..")
import zipfile
from ProjectManager.project_manager import ProjectManager
from Generator.generator import Generator
from Help.help import Help
from HDLDesigner.hdl_designer import HDLDesigner
from HDLDesigner.Architecture.note_dialog import note_Dialog
from xml.dom import minidom


class Home(QMainWindow):

    def __init__(self, proj_dir=None):

        super().__init__()
        small_text_font = QFont()
        small_text_font.setPointSize(10)
        self.setWindowTitle("HDLGen V2022.0.1")

        self.cornerWidget = QWidget()
        self.generate_btn = QPushButton("Generate")
        self.generate_btn.setFont(small_text_font)
        self.start_vivado_btn = QPushButton("Open EDA Project")
        self.start_vivado_btn.setFont(small_text_font)
        self.export_project_btn = QPushButton("Export Project")
        self.export_project_btn.setFont(small_text_font)
        self.cornerWidgetLayout = QHBoxLayout()
        self.cornerWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.cornerWidgetLayout.addWidget(self.generate_btn)
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
        self.generate_btn.clicked.connect(self.generate_btn_clicked)
        self.tabs.setCornerWidget(self.cornerWidget)
        self.start_vivado_btn.clicked.connect(self.start_eda_tool)
        self.export_project_btn.clicked.connect(self.export_project)

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
            overwrite, instances = self.generator.create_vhdl_file()
            self.generator.create_tcl_file("VHDL", instances)
            self.generator.create_testbench_file(overwrite)
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("VHDL and Testbench Generated")
            msgBox.exec_()
        elif self.project_manager.verilog_check.isChecked():
            self.generator.generate_folders()
            overwrite, instances = self.generator.create_verilog_file()
            self.generator.create_tcl_file("Verilog", instances)
            self.generator.create_verilog_testbench_file(overwrite)
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("Verilog and Testbench Generated")
            msgBox.exec_()
    def start_eda_tool(self):
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

    def export_project(self):
        # Get the base name of the folder
        folder_path = os.path.dirname(os.path.dirname(self.proj_dir[0]))
        base_name = os.path.basename(folder_path)
        # Get the directory path of the folder
        folder_dir = os.path.dirname(folder_path)

        # Prompt the user to enter a zip file name
        while True:
            options = QFileDialog.Options()
           # options |= QFileDialog.DontUseNativeDialog
            zip_file_name, _ = QFileDialog.getSaveFileName(
                None, "Export project", os.path.join(folder_dir, f"{base_name}.zip"), "Zip files (*.zip)",
                options=options
            )
            if not zip_file_name:
                return  # User cancelled
            if not zip_file_name.endswith(".zip"):
                zip_file_name += ".zip"
            break  # Exit the loop

        # Create a ZipFile object
        zip_file = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)

        # Walk through the folder and add files to the zip file
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, folder_path)
                zip_file.write(file_path, arcname=rel_path)

        # Close the zip file
        zip_file.close()

        msgBox = QMessageBox()
        msgBox.setWindowTitle("Alert")
        msgBox.setText("Zipped to " + zip_file_name)
        msgBox.exec_()
        print(f"Successfully created {zip_file_name}!")

    def handle_tab_change(self, index):
        if index != 0:
            self.project_manager.save_xml()



