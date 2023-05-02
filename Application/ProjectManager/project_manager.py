import os
import sys
from xml.dom import minidom
from pathlib import Path
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import qtawesome as qta
import configparser
import shutil
from ProjectManager.vivado_help import VivadoHelpDialog
from ProjectManager.settings_help import SettingsHelpDialog
from ProjectManager.language_help import LanguageHelpDialog

SMALL_SPACING = 10
LARGE_SPACING = 30
MEDIUM_SPACING = 25
LARGE_CORNER_R = 15
SMALL_CORNER_R = 15

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"

ICONS_DIR = "../Resources/icons/"

class ProjectManager(QWidget):

    def __init__(self, proj_dir, MainWindow):
        super().__init__()
        print("directory\n")
        print(os.getcwd())
        ProjectManager.proj_dir = None
        ProjectManager.proj_name = None
        #ProjectManager.hdl = None
        ProjectManager.vivado_bat_path = None
        self.MainWindow = MainWindow
        ProjectManager.xml_data_path = None

        # Initializing Widgets

        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)

        self.EDA_top_layout = QGridLayout()
        self.Settings_top_layout = QGridLayout()
        self.language_top_layout = QGridLayout()

        self.proj_setting_title = QLabel("Project Settings")
        self.proj_setting_title.setFont(title_font)
        self.proj_setting_title.setStyleSheet(WHITE_COLOR)
        self.eda_tools_title = QLabel("EDA Tools")
        self.eda_tools_title.setFont(title_font)
        self.eda_tools_title.setStyleSheet(WHITE_COLOR)
        self.generate_title = QLabel("Generate")
        self.generate_title.setFont(title_font)
        self.generate_title.setStyleSheet(WHITE_COLOR)

        self.name_label = QLabel('Project Name*')
        self.name_label.setStyleSheet("color: white;")
        self.dir_label = QLabel('Project Directory*')
        self.dir_label.setStyleSheet("color: white;")
        self.proj_folder_input = QLineEdit()
        self.proj_name_input = QLineEdit()
        self.proj_folder_btn = QPushButton("Browse")
        self.proj_folder_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 5px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 5px; border-style: plain;}")
        self.proj_folder_btn.setFixedSize(50, 22)
        self.copy_proj_btn = QPushButton("Copy project")
        self.copy_proj_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 5px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 5px; border-style: plain;}")
        self.copy_proj_btn.setFixedSize(80, 22)

        self.lang_label = QLabel("Languages")
        self.lang_label.setFont(bold_font)
        self.lang_label.setStyleSheet(BLACK_COLOR)
        self.vhdl_check = QRadioButton("VHDL")
        #self.vhdl_check.setChecked(True)
        self.vhdl_check.setStyleSheet(BLACK_COLOR)
        self.verilog_check = QRadioButton("Verilog")
        self.verilog_check.setStyleSheet(BLACK_COLOR)
        self.sverilog_check = QRadioButton("System Verilog")
        self.sverilog_check.setStyleSheet(BLACK_COLOR)
        self.sverilog_check.setEnabled(False)
        self.chisel_check = QRadioButton("Chisel")
        self.chisel_check.setStyleSheet(BLACK_COLOR)
        self.chisel_check.setEnabled(False)

        self.intel_check = QCheckBox("Intel Quartus")
        self.intel_check.setFont(bold_font)
        self.intel_check.setStyleSheet(BLACK_COLOR)
        self.intel_check.setEnabled(False)
        self.intel_ver_label = QLabel("Version")
        self.intel_ver_label.setStyleSheet(BLACK_COLOR)
        self.intel_ver_combo = QComboBox()
        self.intel_ver_combo.setStyleSheet(BLACK_COLOR)
        self.intel_ver_combo.addItem("21.1 Lite")
        self.intel_dir_label = QLabel('Intel Quartus executable File path')
        self.intel_dir_label.setStyleSheet(BLACK_COLOR)
        self.intel_dir_input = QLineEdit()
        self.intel_select_dir = QPushButton("Browse")
        self.intel_select_dir.setFixedSize(60, 26)

        self.vivado_check = QCheckBox("Xilinx Vivado")
        self.vivado_check.setChecked(True)
        self.vivado_check.setFont(bold_font)
        self.vivado_check.setStyleSheet(BLACK_COLOR)
        self.vivado_ver_label = QLabel("Version")
        self.vivado_ver_label.setStyleSheet(BLACK_COLOR)
        self.vivado_ver_combo = QComboBox()
        self.vivado_ver_combo.setStyleSheet(BLACK_COLOR)
        self.vivado_ver_combo.addItem("2019.1")
        self.vivado_dir_label = QLabel('Xilinx Vivado Batch File path')
        self.vivado_dir_label.setStyleSheet(BLACK_COLOR)
        self.vivado_dir_input = QLineEdit()
        self.vivado_select_dir = QPushButton("Browse")
        self.vivado_select_dir.setFixedSize(60, 26)

        self.vivado_info_btn = QPushButton()
        self.vivado_info_btn.setIcon(qta.icon("mdi.help"))
        self.vivado_info_btn.setFixedSize(25, 25)
        self.vivado_info_btn.clicked.connect(self.vivado_help_window)

        self.settings_info_btn = QPushButton()
        self.settings_info_btn.setIcon(qta.icon("mdi.help"))
        self.settings_info_btn.setFixedSize(25, 25)
        self.settings_info_btn.clicked.connect(self.settings_help_window)

        self.language_info_btn = QPushButton()
        self.language_info_btn.setIcon(qta.icon("mdi.help"))
        self.language_info_btn.setFixedSize(25, 25)
        self.language_info_btn.clicked.connect(self.language_help_window)

        self.note_label = QLabel("Save the project before moving to other tabs")

        self.proj_close_btn = QPushButton("Close Project")
        self.proj_close_btn.setFixedHeight(50)
        self.proj_close_btn.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.proj_save_btn = QPushButton("Save Project")
        self.proj_save_btn.setFixedHeight(50)
        self.proj_save_btn.setStyleSheet(
            "QPushButton {background-color: rgb(129, 134, 145);  color: white; border-radius: 8px; border-style: plain;}"
            "QPushButton:enabled {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")

        # Initializing layouts
        self.mainLayout = QHBoxLayout()

        self.leftColLayout = QVBoxLayout()
        self.midColLayout = QVBoxLayout()
        self.rightColLayout = QVBoxLayout()

        self.projSettingLayout = QVBoxLayout()
        self.projDetailIpLayout = QGridLayout()

        self.projSettingFrame = QFrame()
        self.edaToolsFrame = QFrame()
        self.vivadoToolFrame = QFrame()
        self.intelToolFrame = QFrame()
        self.generateFrame = QFrame()
        self.langFrame = QFrame()

        self.edaToolsLayout = QVBoxLayout()
        self.vivadoToolLayout = QGridLayout()
        self.intelToolLayout = QGridLayout()
        self.generateLayout = QVBoxLayout()
        self.langLayout = QGridLayout()

        self.proj_action_layout = QHBoxLayout()
        # settingsDir=os.getcwd() + "\Settings\settings.txt"
        # settings = open(settingsDir, "r")
        config = configparser.ConfigParser()
        config.read('config.ini')
        vivadoPath = config.get('user', 'vivado.bat')
        # settings.close()
        vivadoPath = vivadoPath.strip()
        self.vivado_dir_input.setText(vivadoPath)
        self.setup_ui()

        if proj_dir != None:
            self.load_proj_data(proj_dir)
        else:
            self.fill_default_proj_details()

    def setup_ui(self):
        #self.projSettingLayout.addWidget(self.proj_setting_title)
        self.Settings_top_layout.addWidget(self.proj_setting_title, 0, 0, 1, 1)
        self.Settings_top_layout.addWidget(self.settings_info_btn, 0, 1, 1, 1)
        self.projSettingLayout.addLayout(self.Settings_top_layout)
        self.projSettingLayout.addSpacing(SMALL_SPACING)
        self.projDetailIpLayout.addWidget(self.name_label, 0, 0, 1, 1)
        self.projDetailIpLayout.addWidget(self.proj_name_input, 1, 0, 1, 3)
        self.projDetailIpLayout.addWidget(self.copy_proj_btn, 1, 3, 1, 1, Qt.AlignRight)
        self.projDetailIpLayout.addWidget(self.dir_label, 2, 0, 1, 1)
        self.projDetailIpLayout.addWidget(self.proj_folder_input, 3, 0, 1, 3)
        self.projDetailIpLayout.addWidget(self.proj_folder_btn, 3, 3, 1, 1, Qt.AlignRight)
        self.projSettingLayout.addLayout(self.projDetailIpLayout)

        self.proj_name_input.textChanged.connect(self.proj_detail_change)
        self.proj_folder_input.textChanged.connect(self.proj_detail_change)
        self.copy_proj_btn.clicked.connect(self.copy_project)

        self.projSettingFrame.setFrameShape(QFrame.StyledPanel)
        self.projSettingFrame.setStyleSheet(".QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}")
        self.projSettingFrame.setLayout(self.projSettingLayout)
        self.leftColLayout.addWidget(self.projSettingFrame)
        self.leftColLayout.addStretch()

        self.EDA_top_layout.addWidget(self.eda_tools_title, 0, 0, 1, 1)
        self.EDA_top_layout.addWidget(self.vivado_info_btn, 0, 1, 1, 1)
        self.edaToolsLayout.addLayout(self.EDA_top_layout)
        self.edaToolsLayout.addSpacing(SMALL_SPACING)
        self.vivadoToolLayout.addWidget(self.vivado_check, 0, 0, 1, 1)
        self.vivadoToolLayout.addWidget(self.vivado_ver_label, 0, 2, 1, 1)
        self.vivadoToolLayout.addWidget(self.vivado_ver_combo, 0, 3, 1, 1)
        self.vivadoToolLayout.addWidget(self.vivado_dir_label, 1, 0, 1, 1)
        self.vivadoToolLayout.addWidget(self.vivado_dir_input, 2, 0, 1, 3)
        #self.vivadoToolLayout.addWidget(self.vivado_info_btn, 1, 3, 1, 1, Qt.AlignRight)
        self.vivadoToolLayout.addWidget(self.vivado_select_dir, 2, 3, 1, 1, Qt.AlignRight)
        self.vivadoToolFrame.setLayout(self.vivadoToolLayout)
        self.vivadoToolFrame.setStyleSheet(
            ".QFrame{background-color: white; border-radius: 5px;}")
        self.edaToolsLayout.addWidget(self.vivadoToolFrame)

        self.edaToolsLayout.addSpacing(MEDIUM_SPACING)

        self.intelToolLayout.addWidget(self.intel_check, 0, 0, 1, 1)
        self.intelToolLayout.addWidget(self.intel_ver_label, 0, 2, 1, 1)
        self.intelToolLayout.addWidget(self.intel_ver_combo, 0, 3, 1, 1)
        self.intelToolLayout.addWidget(self.intel_dir_label, 1, 0, 1, 1)
        self.intelToolLayout.addWidget(self.intel_dir_input, 2, 0, 1, 3)
        self.intelToolLayout.addWidget(self.intel_select_dir, 2, 3, 1, 1, Qt.AlignRight)
        self.intelToolFrame.setLayout(self.intelToolLayout)
        self.intelToolFrame.setStyleSheet(
            ".QFrame{background-color: white; border-radius: 5px;}")

        self.edaToolsLayout.addWidget(self.intelToolFrame)
        self.edaToolsLayout.addStretch()
        self.edaToolsFrame.setFrameShape(QFrame.StyledPanel)
        self.edaToolsFrame.setStyleSheet(".QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}")
        self.edaToolsFrame.setLayout(self.edaToolsLayout)

        self.midColLayout.addWidget(self.edaToolsFrame)

        self.language_top_layout.addWidget(self.generate_title, 0, 0, 1, 1)
        self.language_top_layout.addWidget(self.language_info_btn, 0, 1, 1, 1)
        self.generateLayout.addLayout(self.language_top_layout)
        #self.generateLayout.addWidget(self.generate_title)
        self.generateLayout.addSpacing(SMALL_SPACING)
        self.langLayout.addWidget(self.lang_label, 0, 1, 1, 1, Qt.AlignCenter)
        self.langLayout.addWidget(self.vhdl_check, 1, 0, 1, 1)
        self.langLayout.addWidget(self.verilog_check, 2, 0, 1, 1)
        self.langLayout.addWidget(self.sverilog_check, 1, 2, 1, 1)
        self.langLayout.addWidget(self.chisel_check, 2, 2, 1, 1)
        self.langLayout.setVerticalSpacing(10)
        self.langFrame.setFrameShape(QFrame.StyledPanel)
        self.langFrame.setStyleSheet(
            ".QFrame{background-color: white; border-radius: 5px;}")
        self.langFrame.setLayout(self.langLayout)

        self.generateLayout.addWidget(self.langFrame)
        self.generateLayout.addStretch()
        self.generateFrame.setFrameShape(QFrame.StyledPanel)
        self.generateFrame.setStyleSheet(".QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}")
        self.generateFrame.setLineWidth(3)
        self.generateFrame.setLayout(self.generateLayout)

        self.rightColLayout.addWidget(self.generateFrame)
        self.rightColLayout.addSpacing(MEDIUM_SPACING)

        self.rightColLayout.addWidget(self.note_label)

        self.proj_action_layout.addWidget(self.proj_close_btn)
        self.proj_action_layout.addWidget(self.proj_save_btn)
        self.rightColLayout.addLayout(self.proj_action_layout)

        self.mainLayout.addLayout(self.leftColLayout)
        self.mainLayout.addSpacing(MEDIUM_SPACING)
        self.mainLayout.addLayout(self.midColLayout)
        self.mainLayout.addSpacing(MEDIUM_SPACING)
        self.mainLayout.addLayout(self.rightColLayout)

        self.setLayout(self.mainLayout)

        # Setting actions for buttons
        self.proj_folder_btn.clicked.connect(self.set_proj_dir)
        self.vivado_select_dir.clicked.connect(self.set_vivado_bat_path)
        self.intel_select_dir.clicked.connect(self.get_intel_dir)

        self.proj_close_btn.clicked.connect(self.close_project)
        self.proj_save_btn.clicked.connect(self.create_xml)
        self.vhdl_check.clicked.connect(self.create_xml)
        self.verilog_check.clicked.connect(self.create_xml)

    def fill_default_proj_details(self):

        path = Path(os.getcwd())
        parent_path = path.parent.absolute()
        self.proj_dir = os.path.join(parent_path, "User_Projects")
        self.proj_folder_input.setText(self.proj_dir)
        self.proj_name_input.setText("Untitled")


    def proj_detail_change(self):

        if self.proj_name_input.text() != "" and self.proj_folder_input.text() != "":
            # Getting project name from the text field
            ProjectManager.proj_name = self.proj_name_input.text()
            # Getting project location from the text field
            ProjectManager.proj_dir = self.proj_folder_input.text() + "/"

            ProjectManager.xml_data_path = self.proj_dir + self.proj_name + "/" + "HDLGenPrj" + "/" + self.proj_name + ".hdlgen"

            self.proj_save_btn.setEnabled(True)
        else:
            self.proj_save_btn.setEnabled(False)

    @staticmethod
    def get_xml_data_path():
        return ProjectManager.xml_data_path

    @staticmethod
    def get_proj_name():
        return ProjectManager.proj_name

    @staticmethod
    def get_proj_dir():
        return ProjectManager.proj_dir

    def set_proj_dir(self):
        ProjectManager.proj_dir = QFileDialog.getExistingDirectory(self, "Choose Directory", self.proj_dir)
        if ProjectManager.proj_dir:
            self.proj_folder_input.setText(ProjectManager.proj_dir)

    def set_vivado_bat_path(self):
        ProjectManager.vivado_bat_path = QFileDialog.getOpenFileName(self, "Select Xilinx Vivado Batch file (vivado.bat)", "C:/", filter="Batch (*.bat)")
        ProjectManager.vivado_bat_path = ProjectManager.vivado_bat_path[0]
        self.vivado_dir_input.setText(ProjectManager.vivado_bat_path)

    @staticmethod
    def get_vivado_bat_path():
        return ProjectManager.vivado_bat_path

    def get_intel_dir(self):
        self.intel_dir = QFileDialog.getOpenFileName(self, "Select Intel Quartus exe", "C:/", filter="EXE (*.exe)")
        self.intel_dir_input.setText(self.intel_dir[0])

    def create_xml(self):

        ProjectManager.vivado_bat_path = self.vivado_dir_input.text()

        self.vivado_dir = self.vivado_dir_input.text()
        self.intel_dir = self.intel_dir_input.text()
        spec_dir = os.path.join(ProjectManager.proj_dir, ProjectManager.proj_name, "Specification")
        xml_data_dir = os.path.join(ProjectManager.proj_dir, ProjectManager.proj_name, "HDLGenPrj")
        print("Saving project details at ", xml_data_dir)

        temp_xml_data_path = ProjectManager.proj_dir + ProjectManager.proj_name + "/" + "HDLGenPrj" + "/" + ProjectManager.proj_name + ".hdlgen"

        # Creating XML doc
        root = minidom.Document()
        # Creating XML top Element
        HDLGen_data = root.createElement('HDLGen')
        root.appendChild(HDLGen_data)
        # Creating and adding genFolder Element
        genFolder_data = root.createElement('genFolder')


        # Creating and adding projectManager Element
        projectManager_data = root.createElement('projectManager')
        # Creating main project folder
        os.makedirs(xml_data_dir, exist_ok=True)
        # Create specification folder
        os.makedirs(spec_dir, exist_ok=True)
        # Set project name and location details
        # Adding Setting Element
        settings_data = root.createElement('settings')
        projectManager_data.appendChild(settings_data)
        # Creating name and location elements to settings
        project_name = root.createElement('name')
        project_loc = root.createElement('location')
        # Inserting project name to the name element
        project_name.appendChild(root.createTextNode(ProjectManager.proj_name))
        # Inserting project location to the location element
        project_loc.appendChild(root.createTextNode(ProjectManager.proj_dir[:-1]))
        # Adding name and location as child to settings element
        settings_data.appendChild(project_name)
        settings_data.appendChild(project_loc)

        # Creating EDA element
        eda_data = root.createElement('EDA')
        projectManager_data.appendChild(eda_data)

        # If xilinx vivado is selected then it's details is added to the EDA Element
        if self.vivado_check.isChecked():
            eda_tool_data = root.createElement('tool')
            tool_name = root.createElement('name')
            tool_name.appendChild(root.createTextNode('Xilinx Vivado'))
            tool_dir = root.createElement('dir')
            tool_dir.appendChild(root.createTextNode(self.vivado_dir))
            tool_ver = root.createElement('version')
            tool_ver.appendChild(root.createTextNode(self.vivado_ver_combo.currentText()))
            eda_tool_data.appendChild(tool_name)
            eda_tool_data.appendChild(tool_dir)
            eda_tool_data.appendChild(tool_ver)
            eda_data.appendChild(eda_tool_data)

        # If Intel Quartus is selected then it's details is added to the EDA Element
        if self.intel_check.isChecked():
            eda_tool_data = root.createElement('tool')
            tool_name = root.createElement('name')
            tool_name.appendChild(root.createTextNode('Intel Quartus'))
            tool_dir = root.createElement('dir')
            tool_dir.appendChild(root.createTextNode(self.intel_dir))
            tool_ver = root.createElement('version')
            tool_ver.appendChild(root.createTextNode(self.intel_ver_combo.currentText()))
            eda_tool_data.appendChild(tool_name)
            eda_tool_data.appendChild(tool_dir)
            eda_tool_data.appendChild(tool_ver)
            eda_data.appendChild(eda_tool_data)

        # Creating Element tag to store the selected languages
        hdl_data = root.createElement('HDL')
        projectManager_data.appendChild(hdl_data)

        # If vhdl is selected then vhdl folders to be created are written inside genFolder element
        # and the vhdl language detail is written into hdl element
        if self.vhdl_check.isChecked():
            ProjectManager.hdl = "VHDL"
            vhdl_dir = root.createElement('vhdl_folder')
            vhdl_model_dir = root.createTextNode(ProjectManager.proj_name + '/VHDL/model')
            vhdl_testbench_dir = root.createTextNode(ProjectManager.proj_name + '/VHDL/testbench')
            vhdl_ChatGPT_dir = root.createTextNode(ProjectManager.proj_name + '/VHDL/ChatGPT')
            vhdl_ChatGPT_HDLGen_dir = root.createTextNode(ProjectManager.proj_name + '/VHDL/ChatGPT/HDLGen')
            lang_data = root.createElement('language')
            hdl_data.appendChild(lang_data)
            lang_name = root.createElement('name')
            lang_name.appendChild(root.createTextNode('VHDL'))
            lang_data.appendChild(lang_name)

            vhdl_folders = [vhdl_model_dir, vhdl_testbench_dir,vhdl_ChatGPT_dir,vhdl_ChatGPT_HDLGen_dir]
            no_of_folders = 4

            # If xilinx is chosen then the xilinxprj folder is added
            if self.vivado_check.isChecked():
                vhdl_xlnxprj_dir = root.createTextNode(ProjectManager.proj_name + '/VHDL/AMDprj')
                vhdl_folders.append(vhdl_xlnxprj_dir)
                no_of_folders = no_of_folders + 1

            # If intel is chosen then the intelxprj folder is added
            if self.intel_check.isChecked():
                vhdl_intel_dir = root.createTextNode(ProjectManager.proj_name + '/VHDL/intelprj')
                vhdl_folders.append(vhdl_intel_dir)
                no_of_folders = no_of_folders + 1

            # Adding the vhdl folder directories with vhdl_folder tag
            for i in range(0, no_of_folders):
                vhdl_dir = root.createElement('vhdl_folder')
                vhdl_dir.appendChild(vhdl_folders[i])
                genFolder_data.appendChild(vhdl_dir)

        # If verilog is selected then verilog folders to be created are written inside genFolder element
        # and the verliog language detail is written into hdl element
        if self.verilog_check.isChecked():
            ProjectManager.hdl = "Verilog"
            verilog_dir = root.createElement('verilog_folder')
            verilog_model_dir = root.createTextNode(ProjectManager.proj_name + '/Verilog/model')
            verilog_tstbnch_dir = root.createTextNode(ProjectManager.proj_name + '/Verilog/testbench')
            verilog_ChatGPT_dir = root.createTextNode(ProjectManager.proj_name + '/Verilog/ChatGPT')
            verilog_ChatGPT_HDLGen_dir = root.createTextNode(ProjectManager.proj_name + '/Verilog/ChatGPT/HDLGen')

            lang_data = root.createElement('language')
            hdl_data.appendChild(lang_data)
            lang_name = root.createElement('name')
            lang_name.appendChild(root.createTextNode('Verilog'))
            lang_data.appendChild(lang_name)

            verilog_folders = [verilog_model_dir, verilog_tstbnch_dir, verilog_ChatGPT_dir, verilog_ChatGPT_HDLGen_dir]
            no_of_folders = 4

            # If xilinx is chosen then the xilinxprj folder is added
            if self.vivado_check.isChecked():
                verilog_xlnxprj_dir = root.createTextNode(ProjectManager.proj_name + '/Verilog/AMDprj')
                verilog_folders.append(verilog_xlnxprj_dir)
                no_of_folders = no_of_folders + 1

            # If intel is chosen then the intelxprj folder is added
            if self.intel_check.isChecked():
                verilog_intel_dir = root.createTextNode(ProjectManager.proj_name + '/Verilog/intelprj')
                verilog_folders.append(verilog_intel_dir)
                no_of_folders = no_of_folders + 1

            # Adding the verilog folder directories with vhdl_folder tag
            for i in range(0, no_of_folders):
                verilog_dir = root.createElement('verilog_folder')
                verilog_dir.appendChild(verilog_folders[i])
                genFolder_data.appendChild(verilog_dir)

        if not os.path.exists(temp_xml_data_path):
            HDLGen_data.appendChild(genFolder_data)
            HDLGen_data.appendChild(projectManager_data)

            # Creating hdlDesign tag
            hdlDesign_data = root.createElement('hdlDesign')
            HDLGen_data.appendChild(hdlDesign_data)

            header_data = root.createElement('header')

            comp_name = root.createElement('compName')
            comp_name.appendChild(root.createTextNode("null"))
            header_data.appendChild(comp_name)

            comp_title = root.createElement('title')
            comp_title.appendChild(root.createTextNode("null"))
            header_data.appendChild(comp_title)

            comp_desc = root.createElement('description')
            comp_desc.appendChild(root.createTextNode("null"))
            header_data.appendChild(comp_desc)

            comp_authors = root.createElement('authors')
            comp_authors.appendChild(root.createTextNode("null"))
            header_data.appendChild(comp_authors)

            comp_company = root.createElement('company')
            comp_company.appendChild(root.createTextNode("null"))
            header_data.appendChild(comp_company)

            comp_email = root.createElement('email')
            comp_email.appendChild(root.createTextNode("null"))
            header_data.appendChild(comp_email)

            comp_date = root.createElement('date')
            comp_date.appendChild(root.createTextNode("null"))
            header_data.appendChild(comp_date)

            hdlDesign_data.appendChild(header_data)

            hdlDesign_data.appendChild(root.createElement('clkAndRst'))
            hdlDesign_data.appendChild(root.createElement('entityIOPorts'))
            hdlDesign_data.appendChild(root.createElement('internalSignals'))
            arch_node = root.createElement('architecture')
            hdlDesign_data.appendChild(arch_node)
            hdlDesign_data.appendChild(root.createElement('testbench'))

            # converting the doc into a string in xml format
            xml_str = root.toprettyxml(indent="\t")

            ProjectManager.xml_data_path = ProjectManager.proj_dir + ProjectManager.proj_name + "/" + "HDLGenPrj" + "/" + ProjectManager.proj_name + ".hdlgen"

            # Writing xml file
            with open(ProjectManager.xml_data_path, "w") as f:
                f.write(xml_str)

        else:

            # Parsing the xml file
            data = minidom.parse(temp_xml_data_path)
            HDLGen = data.documentElement

            HDLGen.replaceChild(genFolder_data, HDLGen.getElementsByTagName("genFolder")[0])
            HDLGen.replaceChild(projectManager_data, HDLGen.getElementsByTagName("projectManager")[0])

            # converting the doc into a string in xml format
            xml_str = data.toprettyxml()
            xml_str = os.linesep.join([s for s in xml_str.splitlines() if s.strip()])

            ProjectManager.xml_data_path = ProjectManager.proj_dir + ProjectManager.proj_name + "/" + "HDLGenPrj" + "/" + ProjectManager.proj_name + ".hdlgen"

            # Writing xml file
            with open(ProjectManager.xml_data_path, "w") as f:
                f.write(xml_str)

        ProjectManager.xml_data_path = ProjectManager.proj_dir + ProjectManager.proj_name + "/" + "HDLGenPrj" + "/" + ProjectManager.proj_name + ".hdlgen"

        print("Successfully saved!")

    def close_project(self):

        from Application.main import HDLGen
        self.MainWindow.close()
        self.window = HDLGen()
        #self.window.resize(600, 300)
        self.window.show()
        #self.window.showMaximized()
        print("Project Closed!")

    def load_proj_data(self, load_proj_dir):

        print("Loading project from ", load_proj_dir[0])

        # Parsing the xml file
        data = minidom.parse(load_proj_dir[0])
        HDLGen = data.documentElement

        # Accessing the projectManager and genFolder Elements
        project_Manager = HDLGen.getElementsByTagName("projectManager")

        settings = project_Manager[0].getElementsByTagName("settings")[0]

        proj_name = settings.getElementsByTagName("name")[0].firstChild.data
        proj_loc = settings.getElementsByTagName("location")[0].firstChild.data

        new_xml_path = load_proj_dir[0].split("/")

        new_proj_loc = new_xml_path[0]

        for i in range(1, len(new_xml_path) - 3):
            new_proj_loc = new_proj_loc + "/" + new_xml_path[i]

        if proj_loc != new_proj_loc:
            print("Project Location Change Detected!\nNew location:" + new_proj_loc)
            settings.getElementsByTagName("location")[0].firstChild.data = new_proj_loc
            # converting the doc into a string in xml format
            xml_str = data.toprettyxml()
            xml_str = os.linesep.join([s for s in xml_str.splitlines() if s.strip()])
            # Writing xml file
            with open(load_proj_dir[0], "w") as f:
                f.write(xml_str)

            proj_loc = new_proj_loc


        self.proj_name_input.setText(proj_name)
        self.proj_folder_input.setText(proj_loc)

        eda_data = project_Manager[0].getElementsByTagName("EDA")[0]
        tools_data = eda_data.getElementsByTagName("tool")
        for tool in tools_data:
            if tool.getElementsByTagName("name")[0].firstChild.data == "Xilinx Vivado":
                self.vivado_check.setChecked(True)
                self.vivado_ver_combo.setCurrentText(tool.getElementsByTagName("version")[0].firstChild.data)
                vivado_dir_node = tool.getElementsByTagName("dir")
                if vivado_dir_node != 0 and vivado_dir_node[0].firstChild is not None:
                    self.vivado_dir_input.setText(vivado_dir_node[0].firstChild.data)
                    ProjectManager.vivado_bat_path = vivado_dir_node[0].firstChild.data
            elif tool.getElementsByTagName("name")[0].firstChild.data == "Intel Quartus":
                self.intel_check.setChecked(True)
                self.intel_ver_combo.setCurrentText(tool.getElementsByTagName("version")[0].firstChild.data)
                intel_dir_node = tool.getElementsByTagName("dir")
                if len(intel_dir_node) != 0 and intel_dir_node[0].firstChild is not None:
                    self.intel_dir_input.setText(intel_dir_node[0].firstChild.data)

        hdl_data = project_Manager[0].getElementsByTagName("HDL")[0]
        hdl_langs = hdl_data.getElementsByTagName("language")
        for hdl_lang in hdl_langs:
            if hdl_lang.getElementsByTagName('name')[0].firstChild.data == "VHDL":
                self.vhdl_check.setChecked(True)
                ProjectManager.hdl = "VHDL"
            elif hdl_lang.getElementsByTagName('name')[0].firstChild.data == "Verilog":
                self.verilog_check.setChecked(True)
                ProjectManager.hdl = "Verilog"

        print("Project successfully loaded!")

    def vivado_help_window(self):
        vivado_help_dialog = VivadoHelpDialog()
        vivado_help_dialog.exec_()

    def settings_help_window(self):
        settings_help_dialog = SettingsHelpDialog()
        settings_help_dialog.exec_()

    def language_help_window(self):
        language_help_dialog = LanguageHelpDialog()
        language_help_dialog.exec_()
    @staticmethod
    def get_hdl():
        if ProjectManager.hdl == "VHDL":
            return "VHDL"
        else:
            return "Verilog"

    def copy_project(self):
        # Get the source file path using a QFileDialog
        #source_path, _ = QFileDialog.getOpenFileName(None, 'Select File to Copy',
         #                                            filter="All Files (*);;HDLGen Files (*.hdlgen)")
        try:
            source_path = self.proj_dir +"/"+self.proj_name_input.text()+"/HDLGenPrj/"+self.proj_name_input.text()+".hdlgen"
            # Get the new file name using a QFileDialog
            new_name, _ = QFileDialog.getSaveFileName(None, 'Browse to destination and enter new project name', '',
                                                      'HDLGen Files (*.hdlgen)')

            if new_name:
                # Remove the .hdlgen extension from the new file name if it has it
                if new_name.endswith('.hdlgen'):
                    new_name = new_name[:-7]

                # Create a folder with the same name as the new file name
                folder_path = os.path.join(os.path.dirname(new_name), os.path.basename(new_name))
                os.makedirs(folder_path, exist_ok=True)

                # Create a sub-folder called HDLGenPrj
                sub_folder_path = os.path.join(folder_path, 'HDLGenPrj')
                os.makedirs(sub_folder_path, exist_ok=True)

                # Get the new name of the file and copy it to the HDLGenPrj folder
                new_file_name = os.path.join(sub_folder_path, os.path.basename(new_name) + '.hdlgen')
                shutil.copy(source_path, new_file_name)

                # Open the new file and replace the old file name with the new one
                with open(new_file_name, 'r+') as f:
                    content = f.read()
                    new_content = content.replace(os.path.basename(source_path)[:-7],
                                                  os.path.basename(new_file_name)[:-7])
                    f.seek(0)
                    f.write(new_content)
                    f.truncate()

                # Print a message when the copy operation is completed
                print(f'File copied successfully. New file name: {new_file_name}')
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("Project copied!")
                msgBox.exec_()
        except:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("Error with folder set up")
            msgBox.exec_()