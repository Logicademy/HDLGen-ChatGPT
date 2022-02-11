import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *

SMALL_SPACING = 10
LARGE_SPACING = 30
MEDIUM_SPACING = 25
LARGE_CORNER_R = 15
SMALL_CORNER_R = 15

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white;"

ICONS_DIR = "resources/icons/"

class ProjectManager(QWidget):

    def __init__(self):
        super().__init__()

        # Initializing Widgets

        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)

        self.proj_setting_title = QLabel("Project Settings")
        self.proj_setting_title.setFont(title_font)
        self.proj_setting_title.setStyleSheet(WHITE_COLOR)
        self.eda_tools_title = QLabel("EDA Tools")
        self.eda_tools_title.setFont(title_font)
        self.eda_tools_title.setStyleSheet(WHITE_COLOR)
        self.generate_title = QLabel("Generate")
        self.generate_title.setFont(title_font)
        self.generate_title.setStyleSheet(WHITE_COLOR)

        self.name_label = QLabel('Project Name')
        self.name_label.setStyleSheet("color: white;")
        self.dir_label = QLabel('Project Directory')
        self.dir_label.setStyleSheet("color: white;")
        self.proj_folder_input = QLineEdit()
        self.proj_name_input = QLineEdit()
        self.proj_folder_btn = QPushButton()
        self.proj_folder_btn.setIcon(QIcon(ICONS_DIR + "folder.svg"))
        self.proj_folder_btn.setStyleSheet("background-color: white; border-style: plain;")
        self.proj_folder_btn.setFixedSize(25, 20)

        self.lang_label = QLabel("Languages")
        self.lang_label.setFont(bold_font)
        self.lang_label.setStyleSheet(BLACK_COLOR)
        self.vhdl_check = QCheckBox("VHDL")
        self.vhdl_check.setStyleSheet(BLACK_COLOR)
        self.verilog_check = QCheckBox("Verilog")
        self.verilog_check.setStyleSheet(BLACK_COLOR)
        self.sverilog_check = QCheckBox("System Verilog")
        self.sverilog_check.setStyleSheet(BLACK_COLOR)
        self.sverilog_check.setEnabled(False)
        self.chisel_check = QCheckBox("Chisel")
        self.chisel_check.setStyleSheet(BLACK_COLOR)
        self.chisel_check.setEnabled(False)

        self.intel_check = QCheckBox("Intel Quartus")
        self.intel_check.setFont(bold_font)
        self.intel_check.setStyleSheet(BLACK_COLOR)
        self.intel_ver_label = QLabel("Version")
        self.intel_ver_label.setStyleSheet(BLACK_COLOR)
        self.intel_ver_combo = QComboBox()
        self.intel_ver_combo.setStyleSheet(BLACK_COLOR)
        self.intel_ver_combo.addItem("21.1 Lite")
        self.intel_dir_label = QLabel('Intel Quartus Installation Directory')
        self.intel_dir_label.setStyleSheet(BLACK_COLOR)
        self.intel_dir_input = QLineEdit()
        self.intel_select_dir = QPushButton()
        self.intel_select_dir.setIcon(QIcon(ICONS_DIR + "folder.svg"))
        self.intel_select_dir.setStyleSheet("background-color: white; border-style: plain;")
        self.intel_select_dir.setFixedSize(25, 20)

        self.vivado_check = QCheckBox("Xilinx Vivado")
        self.vivado_check.setFont(bold_font)
        self.vivado_check.setStyleSheet(BLACK_COLOR)
        self.vivado_ver_label = QLabel("Version")
        self.vivado_ver_label.setStyleSheet(BLACK_COLOR)
        self.vivado_ver_combo = QComboBox()
        self.vivado_ver_combo.setStyleSheet(BLACK_COLOR)
        self.vivado_ver_combo.addItem("2019.1")
        self.vivado_dir_label = QLabel('Vivado Installation Directory')
        self.vivado_dir_label.setStyleSheet(BLACK_COLOR)
        self.vivado_dir_input = QLineEdit()
        self.vivado_select_dir = QPushButton()
        self.vivado_select_dir.setIcon(QIcon(ICONS_DIR + "folder.svg"))
        self.vivado_select_dir.setStyleSheet("background-color: white; border-style: plain;")
        self.vivado_select_dir.setFixedSize(25, 20)

        self.proj_open_btn = QPushButton("Open")
        self.proj_open_btn.setFixedHeight(40)
        self.proj_open_btn.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.proj_save_btn = QPushButton("Save")
        self.proj_save_btn.setFixedHeight(40)
        self.proj_save_btn.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.proj_reset_btn = QPushButton("Reset")
        self.proj_reset_btn.setFixedHeight(40)
        self.proj_reset_btn.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
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

        proj_name = self.proj_name_input.text()
        proj_dir = self.proj_folder_input.text()

        self.setup_ui()

    def setup_ui(self):

        self.projSettingLayout.addWidget(self.proj_setting_title)
        self.projSettingLayout.addSpacing(SMALL_SPACING)
        self.projDetailIpLayout.addWidget(self.name_label, 0, 0, 1, 1)
        self.projDetailIpLayout.addWidget(self.proj_name_input, 1, 0, 1, 4)
        self.projDetailIpLayout.addWidget(self.dir_label, 2, 0, 1, 1)
        self.projDetailIpLayout.addWidget(self.proj_folder_input, 3, 0, 1, 4)
        self.projDetailIpLayout.addWidget(self.proj_folder_btn, 3, 3, 1, 1, Qt.AlignRight)
        self.projSettingLayout.addLayout(self.projDetailIpLayout)

        self.proj_name_input.textChanged.connect(self.proj_detail_change)
        self.proj_folder_input.textChanged.connect(self.proj_detail_change)

        self.projSettingFrame.setFrameShape(QFrame.StyledPanel)
        self.projSettingFrame.setStyleSheet(".QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}")
        self.projSettingFrame.setLayout(self.projSettingLayout)
        self.leftColLayout.addWidget(self.projSettingFrame)
        self.leftColLayout.addStretch()

        self.edaToolsLayout.addWidget(self.eda_tools_title)
        self.edaToolsLayout.addSpacing(SMALL_SPACING)
        self.vivadoToolLayout.addWidget(self.vivado_check, 0, 0, 1, 1)
        self.vivadoToolLayout.addWidget(self.vivado_ver_label, 0, 2, 1, 1)
        self.vivadoToolLayout.addWidget(self.vivado_ver_combo, 0, 3, 1, 1)
        self.vivadoToolLayout.addWidget(self.vivado_dir_label, 1, 0, 1, 1)
        self.vivadoToolLayout.addWidget(self.vivado_dir_input, 2, 0, 1, 4)
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
        self.intelToolLayout.addWidget(self.intel_dir_input, 2, 0, 1, 4)
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

        self.generateLayout.addWidget(self.generate_title)
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


        self.proj_action_layout.addWidget(self.proj_reset_btn)
        self.proj_action_layout.addWidget(self.proj_open_btn)
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
        self.vivado_select_dir.clicked.connect(self.get_vivado_dir)
        self.intel_select_dir.clicked.connect(self.get_intel_dir)

        self.proj_reset_btn.clicked.connect(self.reset_all_data)
        self.proj_save_btn.clicked.connect(self.create_xml)
        self.proj_open_btn.clicked.connect(self.load_proj_data)

    def proj_detail_change(self):
        # Getting project name from the text field
        ProjectManager.proj_name = self.proj_name_input.text()
        # Getting project location from the text field
        ProjectManager.proj_dir = self.proj_folder_input.text()

    @staticmethod
    def get_proj_name():
        return ProjectManager.proj_name

    @staticmethod
    def get_proj_dir():
        return ProjectManager.proj_dir

    # get_dir() opens up folder chooser and gets selected folder directory
    def set_proj_dir(self):
        self.proj_dir = QFileDialog.getExistingDirectory(self, "Choose Directory", "E:\\")
        self.proj_folder_input.setText(self.proj_dir)

    def get_vivado_dir(self):
        self.vivado_dir = QFileDialog.getExistingDirectory(self, "Choose Directory", "C:\\")
        self.vivado_dir_input.setText(self.vivado_dir)

    def get_intel_dir(self):
        self.intel_dir = QFileDialog.getExistingDirectory(self, "Choose Directory", "C:\\")
        self.intel_dir_input.setText(self.intel_dir)

    def create_xml(self):


        # Getting project name from the text field
        proj_name = self.proj_name_input.text()
        # Getting project location from the text field
        proj_dir = self.proj_folder_input.text()

        self.vivado_dir = self.vivado_dir_input.text()
        self.intel_dir = self.intel_dir_input.text()

        xml_data_dir = os.path.join(proj_dir, proj_name, proj_name + ".HDLGen")
        print("Saving project details at ", xml_data_dir)
        # Creating main project folder
        os.makedirs(xml_data_dir, exist_ok=True)

        # Creating XML doc
        root = minidom.Document()

        # Creating XML top Element
        HDLGen_data = root.createElement('HDLGen')
        root.appendChild(HDLGen_data)

        # Creating and adding genFolder Element
        genFolder_data = root.createElement('genFolder')
        HDLGen_data.appendChild(genFolder_data)

        # Creating and adding projectManager Element
        projectManager_data = root.createElement('projectManager')
        HDLGen_data.appendChild(projectManager_data)

        # Set project name and location details

        # Adding Setting Element
        settings_data = root.createElement('settings')
        projectManager_data.appendChild(settings_data)
        # Creating name and location elements to settings
        project_name = root.createElement('name')
        project_loc = root.createElement('location')
        # Inserting project name to the name element
        project_name.appendChild(root.createTextNode(proj_name))
        # Inserting project location to the location element
        project_loc.appendChild(root.createTextNode(proj_dir))
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
            vhdl_dir = root.createElement('vhdl_folder')
            vhdl_model_dir = root.createTextNode(self.proj_name + '\\VHDL\\model')
            vhdl_testbench_dir = root.createTextNode(self.proj_name + '\\VHDL\\testbench')

            lang_data = root.createElement('language')
            hdl_data.appendChild(lang_data)
            lang_name = root.createElement('name')
            lang_name.appendChild(root.createTextNode('VHDL'))
            lang_data.appendChild(lang_name)

            vhdl_folders = [vhdl_model_dir, vhdl_testbench_dir]
            no_of_folders = 2

            # If xilinx is chosen then the xilinxprj folder is added
            if self.vivado_check.isChecked():
                vhdl_xlnxprj_dir = root.createTextNode(self.proj_name + '\\VHDL\\EDAprj\\xilinxprj')
                vhdl_folders.append(vhdl_xlnxprj_dir)
                no_of_folders = no_of_folders + 1

            # If intel is chosen then the intelxprj folder is added
            if self.intel_check.isChecked():
                vhdl_intel_dir = root.createTextNode(self.proj_name + '\\VHDL\EDAprj\\intelprj')
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
            verilog_dir = root.createElement('verilog_folder')
            verilog_model_dir = root.createTextNode(self.proj_name + '\\Verilog\\model')
            verilog_tstbnch_dir = root.createTextNode(self.proj_name + '\\Verilog\\testbench')

            lang_data = root.createElement('language')
            hdl_data.appendChild(lang_data)
            lang_name = root.createElement('name')
            lang_name.appendChild(root.createTextNode('Verilog'))
            lang_data.appendChild(lang_name)

            verilog_folders = [verilog_model_dir, verilog_tstbnch_dir]
            no_of_folders = 2

            # If xilinx is chosen then the xilinxprj folder is added
            if self.vivado_check.isChecked():
                verilog_xlnxprj_dir = root.createTextNode(self.proj_name + '\\Verilog\\EDAprj\\xilinxprj')
                verilog_folders.append(verilog_xlnxprj_dir)
                no_of_folders = no_of_folders + 1

            # If intel is chosen then the intelxprj folder is added
            if self.intel_check.isChecked():
                verilog_intel_dir = root.createTextNode(self.proj_name + '\\Verilog\\EDAprj\\intelprj')
                verilog_folders.append(verilog_intel_dir)
                no_of_folders = no_of_folders + 1

            # Adding the verilog folder directories with vhdl_folder tag
            for i in range(0, no_of_folders):
                verilog_dir = root.createElement('verilog_folder')
                verilog_dir.appendChild(verilog_folders[i])
                genFolder_data.appendChild(verilog_dir)


        # converting the doc into a string in xml format
        xml_str = root.toprettyxml(indent="\t")

        save_path_file = self.proj_dir + "\\" + self.proj_name + "\\" + self.proj_name + ".HDLGen\\" + self.proj_name + "_data.xml"

        # Writing xml file
        with open(save_path_file, "w") as f:
            f.write(xml_str)

        print("Successfully saved!")

    def load_proj_data(self):

        self.load_proj_dir = QFileDialog.getOpenFileName(self, "Select the Project XML File", "E:\\", filter= "XML (*.xml)")

        print("Loading project from ", self.load_proj_dir[0])

        # Parsing the xml file
        data = minidom.parse(self.load_proj_dir[0])
        HDLGen = data.documentElement

        # Accessing the projectManager and genFolder Elements
        project_Manager = HDLGen.getElementsByTagName("projectManager")

        settings = project_Manager[0].getElementsByTagName("settings")[0]

        proj_name = settings.getElementsByTagName("name")[0].firstChild.data
        proj_loc = settings.getElementsByTagName("location")[0].firstChild.data
        self.proj_name_input.setText(proj_name)
        self.proj_folder_input.setText(proj_loc)

        eda_data = project_Manager[0].getElementsByTagName("EDA")[0]
        tools_data = eda_data.getElementsByTagName("tool")
        for tool in tools_data:
            if tool.getElementsByTagName("name")[0].firstChild.data == "Xilinx Vivado":
                self.vivado_check.setChecked(True)
                self.vivado_ver_combo.setCurrentText(tool.getElementsByTagName("version")[0].firstChild.data)
                self.vivado_dir_input.setText(tool.getElementsByTagName("dir")[0].firstChild.data)
            elif tool.getElementsByTagName("name")[0].firstChild.data == "Intel Quartus":
                self.intel_check.setChecked(True)
                self.intel_ver_combo.setCurrentText(tool.getElementsByTagName("version")[0].firstChild.data)
                self.intel_dir_input.setText(tool.getElementsByTagName("dir")[0].firstChild.data)

        hdl_data = project_Manager[0].getElementsByTagName("HDL")[0]
        hdl_langs = hdl_data.getElementsByTagName("language")

        for hdl_lang in hdl_langs:
            if hdl_lang.getElementsByTagName('name')[0].firstChild.data == "VHDL":
                self.vhdl_check.setChecked(True)
            elif hdl_lang.getElementsByTagName('name')[0].firstChild.data == "Verilog":
                self.verilog_check.setChecked(True)

        print("Project successfully loaded!")

    def reset_all_data(self):
        self.proj_name_input.clear()
        self.proj_folder_input.clear()

        self.vivado_dir_input.clear()
        self.intel_dir_input.clear()
        self.vivado_check.setChecked(False)
        self.intel_check.setChecked(False)
        self.vivado_ver_combo.setCurrentIndex(0)
        self.intel_ver_combo.setCurrentIndex(0)

        self.vhdl_check.setChecked(False)
        self.verilog_check.setChecked(False)
        self.sverilog_check.setChecked(False)
        self.chisel_check.setChecked(False)

