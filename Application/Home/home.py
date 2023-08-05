from PySide2.QtGui import QFont
from PySide2.QtWidgets import *
import os
import platform
import subprocess
import glob
import webbrowser
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

    def closeEvent(self, event):
        if self.project_manager.project_manager_change == True:
            reply = self.prompt_to_save_changes()
            if reply == QMessageBox.Save:
                # Perform the save operation here or call a method to save data
                print("Saving changes and closing window...")
            elif reply == QMessageBox.Discard:
                print("Discarding changes and closing the application...")
            else:
                # User clicked "Cancel," prevent the application from closing
                event.ignore()

        else:
            print("")

    def prompt_to_save_changes(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText("Do you want to save your changes before closing?")
        msg_box.setWindowTitle("Save Changes")
        msg_box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        msg_box.setDefaultButton(QMessageBox.Save)

        result = msg_box.exec_()

        if result == QMessageBox.Save:
            self.project_manager.save_xml()
            return QMessageBox.Save
        elif result == QMessageBox.Discard:
            return QMessageBox.Discard
        else:
            return QMessageBox.Cancel


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
        self.tabs.setCornerWidget(self.cornerWidget)
        self.start_vivado_btn.clicked.connect(self.start_eda_tool)
        self.export_project_btn.clicked.connect(self.export_project)

        self.project_manager.vhdl_check.clicked.connect(lambda: self.hdl_designer.update_preview("VHDL"))
        self.project_manager.vhdl_check.clicked.connect(lambda: self.hdl_designer.generate.VHDLVisible())
        self.project_manager.verilog_check.clicked.connect(lambda: self.hdl_designer.update_preview("Verilog"))
        self.project_manager.verilog_check.clicked.connect(lambda: self.hdl_designer.generate.VerilogVisible())
        self.tabs.currentChanged.connect(self.hdl_designer.compDetails.update_comp_name)

        self.hdl_designer.generate.generate_model.clicked.connect(self.HDL_model_generate)
        self.hdl_designer.generate.generate_chatgpt_model.clicked.connect(self.chatgpt_model_generate)
        self.hdl_designer.generate.generate_testbench.clicked.connect(self.HDL_testbench_generate)
        self.hdl_designer.generate.generate_chatgpt_testbench.clicked.connect(self.chatgpt_testbench_generate)
        self.hdl_designer.generate.generate_chatgpt_title.clicked.connect(self.chatgpt_title_generate)

        self.hdl_designer.generate.loc_model.clicked.connect(self.open_model_folder)
        self.hdl_designer.generate.chatgpt_loc_model.clicked.connect(self.open_chatgpt_folder)
        self.hdl_designer.generate.loc_testbench.clicked.connect(self.open_testbench_folder)
        self.hdl_designer.generate.chatgpt_loc_testbench.clicked.connect(self.open_chatgpt_folder)
        self.hdl_designer.generate.chatgpt_loc_title.clicked.connect(self.open_chatgpt_folder)

        self.hdl_designer.generate.delete_bk_title_chatgpt.clicked.connect(self.delete_title_msg_backups)
        self.hdl_designer.generate.delete_bk_model_chatgpt.clicked.connect(self.delete_model_msg_backups)
        self.hdl_designer.generate.delete_bk_testbench_chatgpt.clicked.connect(self.delete_testbench_msg_backups)
        self.hdl_designer.generate.testbench_log.clicked.connect(self.openEDALog)
        self.hdl_designer.generate.delete_bk_model.clicked.connect(self.delete_model_backups)
        self.hdl_designer.generate.delete_bk_testbench.clicked.connect(self.delete_testbench_backups)


        self.mainLayout.addWidget(self.tabs)
        self.setLayout(self.mainLayout)

        self.container.setLayout(self.mainLayout)

        self.setCentralWidget(self.container)

    def chatgpt_model_generate(self):
        if self.hdl_designer.generate.chatgpt_model_bk_checkBox.isChecked():
            self.model_generate("6,7")
        else:
            self.model_generate("6")

    def chatgpt_title_generate(self):
        if self.hdl_designer.generate.chatgpt_title_bk_checkBox.isChecked():
            self.model_generate("4,5")
        else:
            self.model_generate("4")

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
            if "8" in files or "9" in files:
                msgBox.setText("Generated and copied to clipboard.\nPaste in ChatGPT to generate complete HDL testbench")
            else:
                msgBox.setText("Generated")
            msgBox.exec_()
        elif self.project_manager.verilog_check.isChecked():
            self.generator.generate_folders()
            self.generator.create_verilog_testbench_file(files)
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            if "8" in files or "9" in files:
                msgBox.setText("Generated and copied to clipboard.\nPaste in ChatGPT to generate complete HDL testbench")
            else:
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
            if "4" in files or "5" in files:
                msgBox.setText("Generated and copied to clipboard.\nPaste in ChatGPT to generate complete HDL model")
            elif "6" in files or "7" in files:
                msgBox.setText("Generated and copied to clipboard.\nPaste in ChatGPT to generate complete HDL title")
            else:
                msgBox.setText("Generated")
            msgBox.exec_()
        elif self.project_manager.verilog_check.isChecked():
            self.generator.generate_folders()
            instances = self.generator.create_verilog_file(files)
            if self.project_manager.vivado_check.isChecked():
                self.generator.create_tcl_file("Verilog", instances)
            else:
                self.generator.create_quartus_tcl_file("Verilog", instances)
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            if "4" in files or "5" in files or "6" in files or "7" in files:
                msgBox.setText("Generated and copied to clipboard.\nPaste in ChatGPT to generate complete HDL model")
            else:
                msgBox.setText("Generated")
            msgBox.exec_()

    def open_model_folder(self):
        proj_folder = os.path.join(self.project_manager.get_proj_dir(),self.project_manager.get_proj_name())
        if self.project_manager.vhdl_check.isChecked():
            path = proj_folder+"/VHDL/model"
            self.open_file_explorer(path)
        elif self.project_manager.verilog_check.isChecked():
            path = proj_folder+"/Verilog/model"
            self.open_file_explorer(path)

    def open_chatgpt_folder(self):
        proj_folder = os.path.join(self.project_manager.get_proj_dir(), self.project_manager.get_proj_name())
        if self.project_manager.vhdl_check.isChecked():
            path = proj_folder+"/VHDL/ChatGPT"
            self.open_file_explorer(path)
        elif self.project_manager.verilog_check.isChecked():
            path = proj_folder+"/Verilog/ChatGPT"
            self.open_file_explorer(path)

    def open_testbench_folder(self):
        proj_folder = os.path.join(self.project_manager.get_proj_dir(), self.project_manager.get_proj_name())
        if self.project_manager.vhdl_check.isChecked():
            path = proj_folder+"/VHDL/testbench"
            self.open_file_explorer(path)
        elif self.project_manager.verilog_check.isChecked():
            path = proj_folder+"/Verilog/testbench"
            self.open_file_explorer(path)

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
                    self.generator.create_tcl_file("Verilog", instances)
                else:
                    self.generator.create_quartus_tcl_file("Verilog", instances)
                self.generator.create_verilog_testbench_file(gen.get_selected_files())
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("Verilog Testbench Generated")
                msgBox.exec_()

    def delete_title_msg_backups(self):
        backup_files = ""
        bk = False
        proj_folder = os.path.join(self.project_manager.get_proj_dir(), self.project_manager.get_proj_name())
        if self.project_manager.vhdl_check.isChecked():
            path = proj_folder+"/VHDL/ChatGPT/Backups"
            backup_files = glob.glob(os.path.join(path,self.project_manager.get_proj_name() + "_VHDL_header_ChatGPT_backup_*.txt"))
            backup_files.append(os.path.join(path,self.project_manager.get_proj_name() + "_VHDL_header_ChatGPT_backup.txt"))
        elif self.project_manager.verilog_check.isChecked():
            path = proj_folder+"/Verilog/ChatGPT/Backups"
            backup_files = glob.glob(os.path.join(path, self.project_manager.get_proj_name() + "_Verilog_header_ChatGPT_backup_*.txt"))
            backup_files.append(os.path.join(path, self.project_manager.get_proj_name() + "_Verilog_header_ChatGPT_backup.txt"))
        if backup_files:
            for file in backup_files:
                if os.path.isfile(file):
                    bk = True
                    os.remove(file)
                    print(f"File deleted: {file}")
                else:
                    print(f"Not a valid file: {file}")
            if bk == True:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("Title Chatgpt Message Backup Files Deleted")
                msgBox.exec_()
            else:
                print("No backup files found.")
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("No Title Chatgpt Message Backup Files found")
                msgBox.exec_()
        else:
            print("No backup files found.")
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("No Title Chatgpt Message Backup Files found")
            msgBox.exec_()

    def delete_model_msg_backups(self):
        backup_files = ""
        bk=False
        proj_folder = os.path.join(self.project_manager.get_proj_dir(), self.project_manager.get_proj_name())
        if self.project_manager.vhdl_check.isChecked():
            path = proj_folder+"/VHDL/ChatGPT/Backups"
            backup_files = glob.glob(os.path.join(path,self.project_manager.get_proj_name() + "_VHDL_ChatGPT_backup_*.txt"))
            backup_files.append(os.path.join(path,self.project_manager.get_proj_name() + "_VHDL_ChatGPT_backup.txt"))
        elif self.project_manager.verilog_check.isChecked():
            path = proj_folder+"/Verilog/ChatGPT/Backups"
            backup_files = glob.glob(os.path.join(path, self.project_manager.get_proj_name() + "_Verilog_ChatGPT_backup_*.txt"))
            backup_files.append(os.path.join(path, self.project_manager.get_proj_name() + "_Verilog_ChatGPT_backup.txt"))
        if backup_files:
            for file in backup_files:
                if os.path.isfile(file):
                    bk = True
                    os.remove(file)
                    print(f"File deleted: {file}")
                else:
                    print(f"Not a valid file: {file}")
            if bk == True:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("Model Chatgpt Message Backup Files Deleted")
                msgBox.exec_()
            else:
                print("No backup files found.")
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("No Model Chatgpt Message Backup Files found")
                msgBox.exec_()
        else:
            print("No backup files found.")
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("No Model Chatgpt Message Backup Files found")
            msgBox.exec_()

    def openEDALog(self):
        if self.project_manager.vhdl_check.isChecked():
            if self.project_manager.vivado_check.isChecked():
                proj_folder = os.path.join(self.project_manager.get_proj_dir(), self.project_manager.get_proj_name())
                xvhdlpath = proj_folder + "/VHDL/AMDprj/" + self.project_manager.get_proj_name() + ".sim/sim_1/behav/xsim/xvhdl.log"
                elabpath = proj_folder + "/VHDL/AMDprj/" + self.project_manager.get_proj_name() + ".sim/sim_1/behav/xsim/elaborate.log"
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Question)
                msg_box.setText("Choose a log option:")
                msg_box.setWindowTitle("Log Options")
                msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                #msg_box.setDefaultButton(QMessageBox.Yes)
                msg_box.setButtonText(QMessageBox.Yes, "xvhdl.log")
                msg_box.setButtonText(QMessageBox.No, "elaborate.log")

                result = msg_box.exec_()
                if result == QMessageBox.Yes:
                    print("xvhdl.log selected")
                    if os.path.exists(xvhdlpath):
                        try:
                            system = platform.system()
                            if system == 'Darwin':  # macOS
                                subprocess.run(['open', xvhdlpath])
                            elif system == 'Windows':
                                subprocess.run(['start', xvhdlpath], shell=True)
                            elif system == 'Linux':
                                subprocess.run(['xdg-open', xvhdlpath])
                            else:
                                print("Unsupported operating system.")
                        except:
                            print("Unexpected error")
                    else:
                        msgBox = QMessageBox()
                        msgBox.setWindowTitle("Alert")
                        msgBox.setText("No xvhdl.log file genertaed")
                        msgBox.exec_()
                elif result == QMessageBox.No:
                    print("elaborate.log selected")
                    if os.path.exists(elabpath):
                        try:
                            system = platform.system()
                            if system == 'Darwin':  # macOS
                                subprocess.run(['open', elabpath])
                            elif system == 'Windows':
                                subprocess.run(['start', elabpath], shell=True)
                            elif system == 'Linux':
                                subprocess.run(['xdg-open', elabpath])
                            else:
                                print("Unsupported operating system.")
                        except:
                            print("Unexpected error")
                    else:
                        msgBox = QMessageBox()
                        msgBox.setWindowTitle("Alert")
                        msgBox.setText("No elaborate.log file genertaed")
                        msgBox.exec_()
            elif self.project_manager.intel_check.isChecked():
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("Intel Quartus is still a work in progress")
                msgBox.exec_()



        elif self.project_manager.verilog_check.isChecked():
            if self.project_manager.vivado_check.isChecked():
                proj_folder = os.path.join(self.project_manager.get_proj_dir(), self.project_manager.get_proj_name())
                xvhdlpath = proj_folder + "/Verilog/AMDprj/" + self.project_manager.get_proj_name() + ".sim/sim_1/behav/xsim/xvhdl.log"
                elabpath = proj_folder + "/Verilog/AMDprj/" + self.project_manager.get_proj_name() + ".sim/sim_1/behav/xsim/elaborate.log"
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Question)
                msg_box.setText("Choose a log option:")
                msg_box.setWindowTitle("Log Options")
                msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                # msg_box.setDefaultButton(QMessageBox.Yes)
                msg_box.setButtonText(QMessageBox.Yes, "xvhdl.log")
                msg_box.setButtonText(QMessageBox.No, "elaborate.log")

                result = msg_box.exec_()
                if result == QMessageBox.Yes:
                    print("xvhdl.log selected")
                    if os.path.exists(xvhdlpath):
                        try:
                            system = platform.system()
                            if system == 'Darwin':  # macOS
                                subprocess.run(['open', xvhdlpath])
                            elif system == 'Windows':
                                subprocess.run(['start', xvhdlpath], shell=True)
                            elif system == 'Linux':
                                subprocess.run(['xdg-open', xvhdlpath])
                            else:
                                print("Unsupported operating system.")
                        except:
                            print("Unexpected error")
                    else:
                        msgBox = QMessageBox()
                        msgBox.setWindowTitle("Alert")
                        msgBox.setText("No xvhdl.log file genertaed")
                        msgBox.exec_()
                elif result == QMessageBox.No:
                    print("elaborate.log selected")
                    if os.path.exists(elabpath):
                        try:
                            system = platform.system()
                            if system == 'Darwin':  # macOS
                                subprocess.run(['open', elabpath])
                            elif system == 'Windows':
                                subprocess.run(['start', elabpath], shell=True)
                            elif system == 'Linux':
                                subprocess.run(['xdg-open', elabpath])
                            else:
                                print("Unsupported operating system.")
                        except:
                            print("Unexpected error")
                    else:
                        msgBox = QMessageBox()
                        msgBox.setWindowTitle("Alert")
                        msgBox.setText("No elaborate.log file genertaed")
                        msgBox.exec_()
            elif self.project_manager.intel_check.isChecked():
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("Intel Quartus is still a work in progress")
                msgBox.exec_()
    def delete_testbench_msg_backups(self):
        backup_files = ""
        bk = False
        proj_folder = os.path.join(self.project_manager.get_proj_dir(), self.project_manager.get_proj_name())
        if self.project_manager.vhdl_check.isChecked():
            path = proj_folder+"/VHDL/ChatGPT/Backups"
            backup_files = glob.glob(os.path.join(path,self.project_manager.get_proj_name() + "_VHDL_TB_ChatGPT_backup_*.txt"))
            backup_files.append(os.path.join(path,self.project_manager.get_proj_name() + "_VHDL_TB_ChatGPT_backup.txt"))
        elif self.project_manager.verilog_check.isChecked():
            path = proj_folder+"/Verilog/ChatGPT/Backups"
            backup_files = glob.glob(os.path.join(path, self.project_manager.get_proj_name() + "_Verilog_TB_ChatGPT_backup_*.txt"))
            backup_files.append(os.path.join(path, self.project_manager.get_proj_name() + "_Verilog_TB_ChatGPT_backup.txt"))
        if backup_files:
            for file in backup_files:
                if os.path.isfile(file):
                    bk = True
                    os.remove(file)
                    print(f"File deleted: {file}")
                else:
                    print(f"Not a valid file: {file}")
            if bk == True:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("Testbench Chatgpt Message Backup Files Deleted")
                msgBox.exec_()
            else:
                print("No backup files found.")
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("No Testbench Chatgpt Message Backup Files found")
                msgBox.exec_()
        else:
            print("No backup files found.")
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("No Testbench Chatgpt Message Backup Files found")
            msgBox.exec_()

    def delete_model_backups(self):
        backup_files = ""
        bk=False
        proj_folder = os.path.join(self.project_manager.get_proj_dir(), self.project_manager.get_proj_name())
        if self.project_manager.vhdl_check.isChecked():
            path = proj_folder+"/VHDL/model"
            backup_files = glob.glob(os.path.join(path,self.project_manager.get_proj_name() + "_backup_*.vhd"))
            backup_files.append(os.path.join(path,self.project_manager.get_proj_name() + "_backup.vhd"))
        elif self.project_manager.verilog_check.isChecked():
            path = proj_folder+"/Verilog/model"
            backup_files = glob.glob(os.path.join(path, self.project_manager.get_proj_name() + "_backup_*.v"))
            backup_files.append(os.path.join(path, self.project_manager.get_proj_name() + "_backup.v"))
        if backup_files:
            for file in backup_files:
                if os.path.isfile(file):
                    bk = True
                    os.remove(file)
                    print(f"File deleted: {file}")
                else:
                    print(f"Not a valid file: {file}")
            if bk == True:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("Model Backup Files Deleted")
                msgBox.exec_()
            else:
                print("No backup files found.")
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("No Model Backup Files found")
                msgBox.exec_()
        else:
            print("No backup files found.")
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("No Model Backup Files found")
            msgBox.exec_()

    def delete_testbench_backups(self):
        backup_files = ""
        bk = False
        proj_folder = os.path.join(self.project_manager.get_proj_dir(), self.project_manager.get_proj_name())
        if self.project_manager.vhdl_check.isChecked():
            path = proj_folder+"/VHDL/testbench"
            backup_files = glob.glob(os.path.join(path,self.project_manager.get_proj_name() + "_TB_backup_*.vhd"))
            backup_files.append(os.path.join(path,self.project_manager.get_proj_name() + "_TB_backup.vhd"))
        elif self.project_manager.verilog_check.isChecked():
            path = proj_folder+"/Verilog/testbench"
            backup_files = glob.glob(os.path.join(path, self.project_manager.get_proj_name() + "_TB_backup_*.v"))
            backup_files.append(os.path.join(path, self.project_manager.get_proj_name() + "_TB_backup.v"))
        if backup_files:
            for file in backup_files:
                if os.path.isfile(file):
                    bk = True
                    os.remove(file)
                    print(f"File deleted: {file}")
                else:
                    print(f"Not a valid file: {file}")
            if bk == True:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("Testbench Backup Files Deleted")
                msgBox.exec_()
            else:
                print("No backup files found.")
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("No Testbench Backup Files found")
                msgBox.exec_()
        else:
            print("No backup files found.")
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("No Testbench Backup Files found")
            msgBox.exec_()

    def open_file_explorer(self,path):
        if not os.path.exists(path):
            print(f"Directory does not exist: {path}")
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("Directory does not exist, please generate files")
            msgBox.exec_()
            return
        if sys.platform == 'win32':
            subprocess.Popen(f'explorer {os.path.realpath(path)}')
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', path])
        elif sys.platform == 'linux':
            subprocess.Popen(['xdg-open', path])
        else:
            print(f"Unsupported platform: {sys.platform}")

    def start_eda_tool(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Alert")
        if self.project_manager.vivado_check.isChecked():
            if self.project_manager.vivado_dir_input.text()[-10:] == "vivado.bat":
                if self.project_manager.vhdl_check.isChecked():
                    msgBox.setText("Starting EDA tool")
                    msgBox.exec_()
                    self.generator.run_tcl_file("VHDL","Vivado")
                else:
                    msgBox.setText("Starting EDA tool")
                    msgBox.exec_()
                    self.generator.run_tcl_file("Verilog", "Vivado")
            else:
                msgBox.setText("No vivado.bat path set")
        else:
            if self.project_manager.vhdl_check.isChecked():
                msgBox.setText("Starting EDA tool")
                msgBox.exec_()
                self.generator.run_tcl_file("VHDL", "Quartus")
            else:
                msgBox.setText("Starting EDA tool")
                msgBox.exec_()
                self.generator.run_tcl_file("Verilog", "Quartus")

    def export_project(self):
        self.project_manager.export_project()


    def handle_tab_change(self, index):
        #self.project_manager.named_edit_done()
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




