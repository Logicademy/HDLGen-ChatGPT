#This class is a tab in the home.py class of the GUI. it displays Project setting, EDA tools and Generate sections.
#It will store information on the project and will save if tab is changed to HDL Designer, or will prompt user to save if the application is closed if changes are made.
import os
from xml.dom import minidom
from pathlib import Path
from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QLineEdit, QRadioButton, QCheckBox, QComboBox, QHBoxLayout, QVBoxLayout, QFrame, QMessageBox, QFileDialog, QToolTip
from PySide2.QtGui import QFont, Qt, QRegExpValidator
from PySide2.QtCore import QRegExp
import qtawesome as qta
import configparser
import webbrowser
import shutil
import zipfile
from ProjectManager.eda_help import EDAHelpDialog
from ProjectManager.settings_help import SettingsHelpDialog
from ProjectManager.language_help import LanguageHelpDialog
from ProjectManager.projectLink import LinkDialog

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
        self.proj_dir = None
        self.proj_name = None
        self.proj_enviro = None
        self.info = ""
        self.startApp = True
        self.project_manager_change = True
        self.vivado_bat_path = None
        self.intel_exe_path = None
        self.MainWindow = MainWindow
        self.xml_data_path = None
        self.package_xml_data_path = None

        # Initializing Widgets
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)
        bold_font.setPointSize(10)
        input_font = QFont()
        input_font.setPointSize(10)

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

        self.enviro_label = QLabel('Project Folder*')
        self.enviro_label.setToolTip("The folder containing all components of this project")
        self.enviro_label.setStyleSheet("color: white;")
        self.enviro_label.setFont(input_font)

        self.enviro_name = QLabel('Project Name')
        self.enviro_name.setToolTip("The name of the project")
        self.enviro_name.setStyleSheet("color: white;")
        self.enviro_name.setFont(input_font)

        self.name_label = QLabel('Component Name*')
        self.name_label.setToolTip("The name of the component")
        self.name_label.setStyleSheet("color: white;")
        self.name_label.setFont(input_font)

        self.dir_label = QLabel('Component Folder*')
        self.dir_label.setToolTip("A folder in the Project Folder where the component is stored")
        self.dir_label.setStyleSheet("color: white;")
        self.dir_label.setFont(input_font)

        self.proj_folder_input = QLineEdit()
        self.proj_folder_input.setReadOnly(True)
        self.proj_folder_input.setFont(input_font)

        self.proj_enviro_name_input = QLineEdit()
        self.proj_enviro_name_input.setReadOnly(True)
        self.proj_enviro_name_input.setFont(input_font)

        self.proj_enviro_input = QLineEdit()
        self.proj_enviro_input.setReadOnly(True)
        self.proj_enviro_input.setFont(input_font)

        self.proj_name_input = QLineEdit()
        self.proj_name_input.setFont(input_font)
        # Disallow invalid characters in the component name (any characters not allowed in a Vivado entity)
        self.validator = QRegExpValidator(QRegExp(r'[^\s\t\r\n-]*'))
        # Have to do this by checking all characters when cursor position changes, validating entire string at once causes weirdness
        self.proj_name_input.cursorPositionChanged.connect(lambda oldPos, newPos: self.show_character_input_error(newPos))

        self.proj_folder_btn = QPushButton("Browse")
        self.proj_folder_btn.setFont(input_font)
        self.proj_folder_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 5px; border-style: plain; padding; 10px; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 5px; border-style: plain;padding; 10px;}")
        
        self.proj_enviro_btn = QPushButton("Browse")
        self.proj_enviro_btn.setFont(input_font)
        self.proj_enviro_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 5px; border-style: plain;padding; 10px; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 5px; border-style: plain;padding; 10px;}")

        self.copy_proj_btn = QPushButton("Copy project")
        self.copy_proj_btn.setFont(input_font)
        self.copy_proj_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 5px; border-style: plain;padding; 10px; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 5px; border-style: plain;padding; 10px;}")
        self.copy_proj_btn.setVisible(False)

        self.proj_info_label = QLabel("Project Information Link")
        self.proj_info_label.setFont(input_font)
        self.proj_info_label.setStyleSheet(WHITE_COLOR)
        self.proj_info_link = QPushButton("Project Link")
        self.proj_info_link.setFont(input_font)
        self.proj_info_link.setEnabled(False)
        self.proj_info_addlink = QPushButton("Add Project Link")
        self.proj_info_addlink.setFont(input_font)

        self.lang_label = QLabel("Languages")
        self.lang_label.setFont(bold_font)
        self.lang_label.setStyleSheet(BLACK_COLOR)
        self.vhdl_check = QRadioButton("VHDL")
        self.vhdl_check.setFont(input_font)
        self.vhdl_check.setStyleSheet(BLACK_COLOR)
        self.verilog_check = QRadioButton("Verilog")
        self.verilog_check.setFont(input_font)
        self.verilog_check.setStyleSheet(BLACK_COLOR)
        self.sverilog_check = QRadioButton("System Verilog (In development)")
        self.sverilog_check.setFont(input_font)
        self.sverilog_check.setStyleSheet(BLACK_COLOR)
        self.sverilog_check.setEnabled(False)
        self.chisel_check = QRadioButton("Chisel (In development)")
        self.chisel_check.setFont(input_font)
        self.chisel_check.setStyleSheet(BLACK_COLOR)
        self.chisel_check.setEnabled(False)

        self.intel_check = QCheckBox("Intel Quartus (In development)")
        self.intel_check.setFont(bold_font)
        self.intel_check.setStyleSheet(BLACK_COLOR)
        self.intel_check.setEnabled(False)

        self.intel_ver_label = QLabel("Version")
        self.intel_ver_label.setFont(input_font)
        self.intel_ver_label.setStyleSheet(BLACK_COLOR)
        self.intel_ver_combo = QComboBox()
        self.intel_ver_combo.setFont(input_font)
        self.intel_ver_combo.setStyleSheet(BLACK_COLOR)
        self.intel_ver_combo.addItem("21.1 Lite")
        self.intel_dir_label = QLabel('Intel Quartus executable File path')
        self.intel_dir_label.setFont(input_font)
        self.intel_dir_label.setStyleSheet(BLACK_COLOR)
        self.intel_dir_input = QLineEdit()
        self.intel_dir_input.setFont(input_font)
        self.intel_dir_input.setReadOnly(True)
        self.intel_select_dir = QPushButton("Browse")
        self.intel_select_dir.setFont(input_font)

        self.vivado_check = QCheckBox("Xilinx Vivado")
        self.vivado_check.setFont(bold_font)
        self.vivado_check.setStyleSheet(BLACK_COLOR)
        self.vivado_check.setChecked(True)
        self.vivado_ver_label = QLabel("Version")
        self.vivado_ver_label.setFont(input_font)
        self.vivado_ver_label.setStyleSheet(BLACK_COLOR)
        self.vivado_ver_combo = QComboBox()
        self.vivado_ver_combo.setFont(input_font)
        self.vivado_ver_combo.setStyleSheet(BLACK_COLOR)
        self.vivado_ver_combo.addItem("2019.1")
        self.vivado_dir_label = QLabel('Xilinx Vivado Batch File path')
        self.vivado_dir_label.setFont(input_font)
        self.vivado_dir_label.setStyleSheet(BLACK_COLOR)
        self.vivado_dir_input = QLineEdit()
        self.vivado_dir_input.setFont(input_font)
        self.vivado_dir_input.setReadOnly(True)
        self.vivado_select_dir = QPushButton("Browse")
        self.vivado_select_dir.setFont(input_font)

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

        self.proj_close_btn = QPushButton("Close Project")
        self.proj_close_btn.setFont(input_font)
        self.proj_close_btn.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain;padding: 10px; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;padding: 10px;}")

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
        config = configparser.ConfigParser()
        config.read('config.ini')
        vivadoPath = config.get('user', 'vivado.bat')
        vivadoPath = vivadoPath.strip()
        self.vivado_dir_input.setText(vivadoPath)
        quartusPath = config.get('user', 'quartus')
        quartusPath = quartusPath.strip()
        self.intel_dir_input.setText(quartusPath)
        self.config = configparser.ConfigParser()
        self.setup_ui()

        if proj_dir != None:
            self.load_proj_data(proj_dir)

        else:
            self.fill_default_proj_details()
        self.startApp=False

    def show_character_input_error(self, newPos):
        valid = self.validator.validate(self.proj_name_input.text(), newPos)
        if valid[0] == 0:
            self.proj_name_input.setText(self.proj_name_input.text()[:-1])
            QToolTip.showText(self.proj_name_input.mapToGlobal(self.proj_name_input.rect().bottomLeft()), "Character not allowed")
        else:
            QToolTip.hideText()

    def setup_ui(self):
        self.Settings_top_layout.addWidget(self.proj_setting_title, 0, 0, 1, 1)
        self.Settings_top_layout.addWidget(self.settings_info_btn, 0, 1, 1, 1)

        self.projSettingLayout.addLayout(self.Settings_top_layout)
        self.projSettingLayout.addSpacing(SMALL_SPACING)

        # Show Project Name label and Project Name immutable input
        self.projDetailIpLayout.addWidget(self.enviro_name, 0, 0, 1, 1)
        self.projDetailIpLayout.addWidget(self.proj_enviro_name_input, 1, 0, 1, 3)

        # Show Project Folder label and Project Folder immutable input, with Browse Button
        self.projDetailIpLayout.addWidget(self.enviro_label, 2, 0, 1, 1)
        self.projDetailIpLayout.addWidget(self.proj_enviro_input, 3, 0, 1, 3)
        self.projDetailIpLayout.addWidget(self.proj_enviro_btn, 3, 3, 1, 1, Qt.AlignRight)

        self.projDetailIpLayout.addWidget(self.copy_proj_btn, 1, 3, 1, 1, Qt.AlignRight)

        # Show Component Name label and Component Name immutable input
        self.projDetailIpLayout.addWidget(self.name_label, 4, 0, 1, 1)
        self.projDetailIpLayout.addWidget(self.proj_name_input, 5, 0, 1, 3)

        # Show Component Folder label and Component Folder input, with Browse Button
        self.projDetailIpLayout.addWidget(self.dir_label, 6, 0, 1, 1)
        self.projDetailIpLayout.addWidget(self.proj_folder_input, 7, 0, 1, 3)
        self.projDetailIpLayout.addWidget(self.proj_folder_btn, 7, 3, 1, 1, Qt.AlignRight)
        
        # Project Information Link
        self.projDetailIpLayout.addWidget(self.proj_info_label, 8, 0, 1, 1)
        self.projDetailIpLayout.addWidget(self.proj_info_link, 8, 1, 1, 1)
        self.projDetailIpLayout.addWidget(self.proj_info_addlink, 8, 2, 1, 1)
        
        self.projSettingLayout.addLayout(self.projDetailIpLayout)

        self.proj_name_input.textChanged.connect(self.proj_detail_change)
        self.proj_enviro_input.textChanged.connect(self.proj_detail_change)
        self.proj_folder_input.textChanged.connect(self.proj_detail_change)
        self.proj_folder_input.textChanged.connect(self.proj_folder_change)

        self.copy_proj_btn.clicked.connect(self.copy_project)

        self.projSettingFrame.setFrameShape(QFrame.StyledPanel)
        self.projSettingFrame.setStyleSheet(".QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}")
        self.projSettingFrame.setLayout(self.projSettingLayout)
        self.leftColLayout.addWidget(self.projSettingFrame)
        self.leftColLayout.addWidget(self.proj_close_btn)
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

        self.mainLayout.addLayout(self.leftColLayout)
        self.mainLayout.addSpacing(MEDIUM_SPACING)
        self.mainLayout.addLayout(self.midColLayout)
        self.mainLayout.addSpacing(MEDIUM_SPACING)
        self.mainLayout.addLayout(self.rightColLayout)

        self.setLayout(self.mainLayout)

        # Setting actions for buttons
        self.proj_folder_btn.clicked.connect(self.set_proj_dir)
        #self.name_change_btn.clicked.connect(self.name_edit)
        self.proj_enviro_btn.clicked.connect(self.set_proj_environment)
        self.proj_enviro_btn.clicked.connect(self.proj_enviro_change)
        self.vivado_select_dir.clicked.connect(self.get_vivado_dir)
        self.intel_select_dir.clicked.connect(self.get_intel_dir)
        self.proj_info_link.clicked.connect(self.openLink)
        self.proj_info_addlink.clicked.connect(self.addLink)

        self.proj_close_btn.clicked.connect(self.close_project)
        #self.vhdl_check.clicked.connect(self.save_xml)
        #self.verilog_check.clicked.connect(self.save_xml)
        #self.vhdl_check.clicked.connect(self.named_edit_done)
        #self.verilog_check.clicked.connect(self.named_edit_done)
        self.intel_check.clicked.connect(self.edaCheckbox)
        self.vivado_check.clicked.connect(self.edaCheckbox)
        #self.intel_check.clicked.connect(self.save_xml)
        #self.vivado_check.clicked.connect(self.save_xml)
    
    def fill_default_proj_details(self):
        self.config.read('config.ini')
        self.proj_enviro = self.config.get('user', 'recentEnviro')
        self.proj_dir = self.proj_enviro
        if not os.path.exists(self.proj_enviro):
            path = Path(os.getcwd())
            parent_path = path.parent.absolute()
            self.proj_enviro = os.path.join(parent_path, "User_Projects")
            self.proj_dir = os.path.join(parent_path, "User_Projects")
            self.config.set("user", "recentEnviro", self.proj_enviro)


        self.proj_folder_input.setText(self.proj_dir)
        self.proj_enviro_input.setText(self.proj_enviro)
        self.proj_enviro_name_input.setText(os.path.dirname(self.proj_enviro))
        self.proj_name_input.setText("Untitled")
        self.info="None"


    def proj_enviro_change(self):
        if self.proj_name_input.text() != "" and self.proj_enviro_input.text() != "" and self.proj_folder_input.text() != "":
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("If changing a Project Environment in an existing project, the types or subcomponents will not be included in the created VHDL package file. You may wish to include types and subcomponents in the new environment, using the Types and Subcomponent menus.")
            msgBox.exec_()
            #self.save_xml()
    
    def proj_detail_change(self):
        self.project_manager_change = True
        if self.proj_name_input.text() != "" and self.proj_enviro_input.text() != "" and self.proj_folder_input.text() != "":
            # Get project name from text field
            ProjectManager.proj_name = self.proj_name_input.text()

            # Get project location from text field
            ProjectManager.proj_dir = Path(self.proj_folder_input.text())

            # Get project environment from text field
            ProjectManager.proj_enviro = Path(self.proj_enviro_input.text())

            # Set Project HDLGen Path and Package HDLGen Path based on new name, directory, environment
            ProjectManager.xml_data_path = ProjectManager.get_proj_hdlgen()
            ProjectManager.package_xml_data_path = ProjectManager.get_package_hdlgen()

    def proj_folder_change(self):
        if self.startApp != True:
            if self.proj_name_input.text() != "" and self.proj_enviro_input.text() != "" and self.proj_folder_input.text() != "":
                while not str(ProjectManager.proj_enviro) in self.proj_folder_input.text():
                    msgBox = QMessageBox()
                    msgBox.setWindowTitle("Alert")
                    msgBox.setText(
                        "Project Folder is not in Project Environment. Do you want to change Project Environment or Project Folder")
                    msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    msgBox.setDefaultButton(QMessageBox.No)
                    msgBox.setButtonText(QMessageBox.Yes, "Environment")
                    msgBox.setButtonText(QMessageBox.No, "Folder")
                    choice = msgBox.exec()
                    if choice == QMessageBox.Yes:
                        self.set_proj_environment()
                    else:
                        self.set_proj_dir()

            #self.save_xml()

    @staticmethod
    def get_xml_data_path():
        return ProjectManager.xml_data_path

    @staticmethod
    def get_package_xml_data_path():
        return ProjectManager.package_xml_data_path

    @staticmethod
    def get_proj_name():
        return ProjectManager.proj_name

    @staticmethod
    def get_proj_dir():
        return ProjectManager.proj_dir

    def set_proj_dir(self):
        self.project_manager_change = True
        file = QFileDialog.getExistingDirectory(self, "Choose Directory", str(self.proj_dir))

        if file:
            ProjectManager.proj_dir = Path(file)
            self.proj_folder_input.setText(str(ProjectManager.proj_dir))

    def get_vivado_dir(self):
        self.project_manager_change = True
       # self.named_edit_done()
        file = QFileDialog.getOpenFileName(self, "Select Xilinx Vivado Batch file (vivado.bat)", "C:/", filter="Batch (*.bat)")
        file = file[0]
        if file != "":
            ProjectManager.vivado_bat_path = file
            self.vivado_dir_input.setText(ProjectManager.vivado_bat_path)
            #self.save_xml()

    @staticmethod
    def get_vivado_bat_path():
        return ProjectManager.vivado_bat_path

    @staticmethod
    def get_proj_environment():
        return ProjectManager.proj_enviro
    
    @staticmethod
    def get_package_hdlgen():
        return os.path.join(ProjectManager.proj_enviro, "Package", "mainPackage.hdlgen")
    
    @staticmethod
    def get_package_vhd():
        return os.path.join(ProjectManager.proj_enviro, "Package", "MainPackage.vhd")

    @staticmethod
    def get_proj_hdlgen():
        return os.path.join(ProjectManager.proj_dir, "HDLGenPrj", ProjectManager.proj_name + ".hdlgen")

    @staticmethod
    def get_proj_specification_dir():
        return os.path.join(ProjectManager.proj_dir, "Specification")
    
    def set_proj_environment(self):
        self.project_manager_change = True
        #self.named_edit_done()
        file = QFileDialog.getExistingDirectory(self, "Choose Environment Folder", str(self.proj_enviro))
        if file != "":
            ProjectManager.proj_enviro = file
            ProjectManager.proj_enviro = ProjectManager.proj_enviro.replace("\\", "/")
            self.proj_enviro_input.setText(str(ProjectManager.get_proj_environment()))
            self.proj_enviro_name_input.setText(str(os.path.dirname(ProjectManager.get_proj_environment())))
            self.proj_folder_input.setText(str(ProjectManager.get_proj_dir()))

    def get_intel_dir(self):
        self.project_manager_change = True
        #self.named_edit_done()
        file = QFileDialog.getOpenFileName(self, "Select Intel Quartus exe", "C:/", filter="EXE (*.exe)")
        file = file[0]
        if file != "":
            ProjectManager.intel_exe_path = file
            self.intel_dir_input.setText(ProjectManager.intel_exe_path)
            #self.save_xml()

    @staticmethod
    def get_intel_exe_path():
        return ProjectManager.intel_exe_path

    def save_xml(self):
        self.project_manager_change = False
        ProjectManager.vivado_bat_path = self.vivado_dir_input.text()
        ProjectManager.intel_exe_path = self.intel_dir_input.text()
        self.vivado_dir = self.vivado_dir_input.text()
        self.intel_dir = self.intel_dir_input.text()
        spec_dir = os.path.join(ProjectManager.get_proj_dir(), "Specification")
        xml_data_dir = os.path.join(ProjectManager.get_proj_dir(), "HDLGenPrj")
        print("Saving project details at ", xml_data_dir)

        temp_xml_data_path = ProjectManager.get_proj_hdlgen()

        # Creating XML doc
        rootPack = minidom.Document()
        # Creating XML top Element
        HDLGen_data_pack = rootPack.createElement('HDLGen')
        rootPack.appendChild(HDLGen_data_pack)
        # Creating hdlDesign tag
        hdlDesign_data_pack= rootPack.createElement('hdlDesign')
        HDLGen_data_pack.appendChild(hdlDesign_data_pack)
        hdlDesign_data_pack.appendChild(rootPack.createElement('mainPackage'))
        hdlDesign_data_pack.appendChild(rootPack.createElement('components'))

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
        project_env = root.createElement('environment')
        project_loc = root.createElement('location')
        project_info = root.createElement('info')
        # Inserting project name to the name element
        project_name.appendChild(root.createTextNode(ProjectManager.proj_name))
        project_env.appendChild(root.createTextNode(self.proj_enviro_input.text()))
        # Inserting project location to the location element
        project_loc.appendChild(root.createTextNode(str(ProjectManager.get_proj_dir())))
        project_info.appendChild(root.createTextNode(self.info))
        # Adding name and location as child to settings element
        settings_data.appendChild(project_name)
        settings_data.appendChild(project_env)
        settings_data.appendChild(project_loc)
        settings_data.appendChild(project_info)

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
            vhdl_ChatGPT_HDLGen_dir = root.createTextNode(ProjectManager.proj_name + '/VHDL/ChatGPT/Backups')
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
            verilog_ChatGPT_HDLGen_dir = root.createTextNode(ProjectManager.proj_name + '/Verilog/ChatGPT/Backups')

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
            hdlDesign_data.appendChild(root.createElement('chatgpt'))


            # converting the doc into a string in xml format
            xml_str = root.toprettyxml(indent="\t")

            ProjectManager.xml_data_path = ProjectManager.get_proj_hdlgen()

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
            xml_str = '\n'.join([line for line in xml_str.splitlines() if line.strip()])

            ProjectManager.xml_data_path = ProjectManager.get_proj_hdlgen()

            # Writing xml file
            with open(ProjectManager.xml_data_path, "w") as f:
                f.write(xml_str)

        ProjectManager.xml_data_path = ProjectManager.get_proj_hdlgen()
        ProjectManager.package_xml_data_path = ProjectManager.get_package_hdlgen()

        if not os.path.exists(ProjectManager.package_xml_data_path):
            if not os.path.exists(os.path.join(ProjectManager.proj_enviro, "Package")):
                os.makedirs(os.path.join(ProjectManager.proj_enviro, "Package"))
            # converting the doc into a string in xml format
            package_xml_str = rootPack.toprettyxml(indent="\t")
            with open(ProjectManager.package_xml_data_path, "w") as f:
                f.write(package_xml_str)
        self.config.read('config.ini')
        self.config.set("user", "recentEnviro", self.proj_enviro_input.text())
        print(self.proj_enviro_input.text())
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
        print("Successfully saved!")

    def close_project(self):
        from Application.main import HDLGen
        self.MainWindow.close()
        if self.MainWindow.isVisible() == False:
            self.window = HDLGen()
            self.window.move(0, 0)
            self.window.show()
        print("Project Closed!")

    def find_project_folder_directory(self, proj_dir, enviro):
        while proj_dir != os.path.dirname(proj_dir):
            if os.path.basename(proj_dir) == enviro:
                return proj_dir
            proj_dir = os.path.dirname(proj_dir)
        return None

    def load_proj_data(self, load_proj_dir):

        print(f"Loading project from {str(load_proj_dir)}")

        # Parse the .hdlgen file into a Minidom document and fetch the root element
        data = minidom.parse(str(load_proj_dir))
        HDLGen = data.documentElement

        # Get the <projectManager/> element inside of the <HDLGen/> element
        project_manager = HDLGen.getElementsByTagName("projectManager")[0]

        # Get the <settings/> element inside of the <projectManager/> element
        settings = project_manager.getElementsByTagName("settings")[0]

        self.proj_name = settings.getElementsByTagName("name")[0].firstChild.data
        self.proj_enviro = Path(settings.getElementsByTagName("environment")[0].firstChild.data)
        self.proj_env_name = Path(self.proj_enviro).stem
        self.proj_dir = settings.getElementsByTagName("location")[0].firstChild.data
        self.proj_info = settings.getElementsByTagName("info")[0].firstChild.data

        # If the project location saved in the XML file, doesn't match the XML file's actual path
        # then the whole project has been moved. The parents attribute of a Path() is a list of parents to the Path().
        if str(self.proj_dir) != str(load_proj_dir.parents[1]):
            print(f"Project Location Change Detected!\nNew location: {str(load_proj_dir.parents[1])}")
            print(f"New environment: {str(load_proj_dir.parents[2])}")

            # Set the new project location and environment in the settings block of the XML file
            settings.getElementsByTagName("location")[0].firstChild.data = str(load_proj_dir.parents[1])
            settings.getElementsByTagName("environment")[0].firstChild.data = str(load_proj_dir.parents[2])
            self.proj_dir = str(load_proj_dir.parents[1])
            self.proj_enviro = str(load_proj_dir.parents[2])
            self.proj_env_name = str(load_proj_dir.parents[2].stem)

            # Convert the raw XML data into a formatted XML document
            xml_str = data.toprettyxml()
            
            # Strip out blank lines left behind by the formatter
            xml_str = '\n'.join([line for line in xml_str.splitlines() if line.strip()])
            
            # Write the updated and formatted XML file back to the disk
            with open(load_proj_dir, "w", encoding="utf-8") as f:
                f.write(xml_str)

        self.proj_name_input.setText(self.proj_name)
        self.proj_enviro_input.setText(str(self.proj_enviro))
        self.proj_enviro_name_input.setText(self.proj_env_name)

        self.proj_folder_input.setText(str(self.proj_dir))
        self.info = self.proj_info

        if self.proj_info != "None":
            self.proj_info_addlink.setText("Edit Project Link")
            self.proj_info_link.setEnabled(True)

        eda_data = project_manager.getElementsByTagName("EDA")[0]
        tools_data = eda_data.getElementsByTagName("tool")
        for tool in tools_data:
            if tool.getElementsByTagName("name")[0].firstChild.data == "Xilinx Vivado":
                self.vivado_check.setChecked(True)
                self.intel_check.setChecked(False)
                self.vivado_ver_combo.setCurrentText(tool.getElementsByTagName("version")[0].firstChild.data)
                vivado_dir_node = tool.getElementsByTagName("dir")
                if vivado_dir_node != 0 and vivado_dir_node[0].firstChild is not None:
                    self.vivado_dir_input.setText(vivado_dir_node[0].firstChild.data)
                    ProjectManager.vivado_bat_path = vivado_dir_node[0].firstChild.data
            elif tool.getElementsByTagName("name")[0].firstChild.data == "Intel Quartus":
                self.intel_check.setChecked(True)
                self.vivado_check.setChecked(False)
                self.intel_ver_combo.setCurrentText(tool.getElementsByTagName("version")[0].firstChild.data)
                intel_dir_node = tool.getElementsByTagName("dir")
                if len(intel_dir_node) != 0 and intel_dir_node[0].firstChild is not None:
                    self.intel_dir_input.setText(intel_dir_node[0].firstChild.data)
                    ProjectManager.intel_exe_path = intel_dir_node[0].firstChild.data

        hdl_data = project_manager.getElementsByTagName("HDL")[0]
        hdl_langs = hdl_data.getElementsByTagName("language")
        for hdl_lang in hdl_langs:
            if hdl_lang.getElementsByTagName('name')[0].firstChild.data == "VHDL":
                self.vhdl_check.setChecked(True)
                ProjectManager.hdl = "VHDL"
            elif hdl_lang.getElementsByTagName('name')[0].firstChild.data == "Verilog":
                self.verilog_check.setChecked(True)
                ProjectManager.hdl = "Verilog"
        self.config.read('config.ini')
        self.config.set("user", "recentEnviro", str(self.proj_enviro))
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
        print("Project successfully loaded!")
        self.save_xml()

    def vivado_help_window(self):
        eda_help_dialog = EDAHelpDialog()
        eda_help_dialog.exec_()

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

    def addLink(self):
       # self.named_edit_done()
        self.project_manager_change = True
        add_link = LinkDialog("edit", self.info)
        add_link.exec_()

        if not add_link.cancelled:
            add_link = add_link.get_data()
            self.info = add_link
            if self.info != "None":
                self.proj_info_addlink.setText("Edit Project Link")
                self.proj_info_link.setEnabled(True)
            else:
                self.proj_info_addlink.setText("Add Project Link")
                self.proj_info_link.setEnabled(False)
    
    def openLink(self):
        #self.named_edit_done()
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText("Do you trust this link? "+ self.info)
        msgBox.setWindowTitle("Confirmation")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        response = msgBox.exec_()
        if response == QMessageBox.Yes:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("Opening project information link")
            msgBox.exec_()
            webbrowser.open(self.info)

    def copy_project(self):
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
    
    def export_project(self):
        # Get the base name of the folder
        dir = Path(ProjectManager.get_proj_hdlgen())
        folder_path = dir.parents[1]
        base_name = ProjectManager.get_proj_name()
        # Get the directory path of the folder
        folder_dir = self.proj_enviro

        # Prompt the user to enter a zip file name
        while True:
            options = QFileDialog.Options()
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
        for root, _, files in os.walk(folder_path):
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
    
    def edaCheckbox(self):
        self.project_manager_change = True
        button = self.sender()
        if button == self.intel_check:
            if button.isChecked():
                self.vivado_check.setChecked(False)
        else:
            if button.isChecked():
                self.intel_check.setChecked(False)