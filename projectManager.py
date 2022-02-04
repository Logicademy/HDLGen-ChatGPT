import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *


class ProjectManager(QWidget):

    def __init__(self):
        super().__init__()

        self.small_spacing = 10
        self.large_spacing = 50

        # Initializing Widgets

        title_font = QFont()
        title_font.setPointSize(10)
        bold_font = QFont()

        bold_font.setBold(True)

        self.proj_setting_title = QLabel("Project Settings")
        self.proj_setting_title.setFont(title_font)
        self.eda_tools_title = QLabel("EDA Tools")
        self.eda_tools_title.setFont(title_font)
        self.generate_title = QLabel("Generate")
        self.generate_title.setFont(title_font)

        self.name_label = QLabel('Project Name')
        self.dir_label = QLabel('Project Directory')
        self.folder_input = QLineEdit()
        self.proj_name_input = QLineEdit()
        self.select_folder_btn = QPushButton("Browse")
        self.save_btn = QPushButton("Save")
        self.gen_btn = QPushButton("Generate Folders")

        self.lang_label = QLabel("Languages")
        self.lang_label.setFont(bold_font)
        self.vhdl_check = QCheckBox("VHDL")
        self.verilog_check = QCheckBox("Verilog")
        self.sverilog_check = QCheckBox("System Verilog")
        self.chisel_check = QCheckBox("Chisel")

        self.eda_label = QLabel("EDA Tools")
        self.eda_label.setFont(bold_font)
        self.verion_label = QLabel("Version")

        self.intel_check = QCheckBox("Intel Quartus")
        self.intel_ver_combo = QComboBox()
        self.intel_ver_combo.addItem("1")
        self.intel_ver_combo.addItem("2")
        self.intel_dir_label = QLabel('Intel Quartus Installation Directory')
        self.intel_dir_input = QLineEdit()
        self.intel_select_dir = QPushButton("Browse")

        self.vivado_check = QCheckBox("Xilinx Vivado")
        self.vivado_ver_combo = QComboBox()
        self.vivado_ver_combo.addItem("2019.1")
        self.vivado_ver_combo.addItem("2020.2")
        self.vivado_dir_label = QLabel('Vivado Installation Directory')
        self.vivado_dir_input = QLineEdit()
        self.vivado_select_dir  = QPushButton("Browse")


        # Initializing layouts
        self.mainLayout = QHBoxLayout()

        self.leftColLayout = QVBoxLayout()
        self.midColLayout = QVBoxLayout()
        self.rightColLayout = QVBoxLayout()

        self.projSettingLayout = QVBoxLayout()
        self.projDetailIpLayout = QGridLayout()

        self.edaToolsLayout = QVBoxLayout()
        self.vivadoToolLayout = QGridLayout()
        self.intelToolLayout = QGridLayout()
        self.generateLayout = QVBoxLayout()
        self.langLayout = QGridLayout()

        self.setup_ui()

    def setup_ui(self):

        self.projSettingLayout.addWidget(self.proj_setting_title)
        self.projSettingLayout.addSpacing(self.small_spacing)
        self.projDetailIpLayout.addWidget(self.name_label, 0, 0, 1, 1)
        self.projDetailIpLayout.addWidget(self.proj_name_input, 1, 0, 1, 4)
        self.projDetailIpLayout.addWidget(self.dir_label, 2, 0, 1, 1)
        self.projDetailIpLayout.addWidget(self.folder_input, 3, 0, 1, 3)
        self.projDetailIpLayout.addWidget(self.select_folder_btn, 3, 3, 1, 1)
        self.projSettingLayout.addLayout(self.projDetailIpLayout)
        self.leftColLayout.addLayout(self.projSettingLayout)
        self.leftColLayout.addStretch()

        self.edaToolsLayout.addWidget(self.eda_tools_title)
        self.edaToolsLayout.addSpacing(self.small_spacing)
        self.vivadoToolLayout.addWidget(self.vivado_check, 0, 0, 1, 1)
        self.vivadoToolLayout.addWidget(self.verion_label, 0, 2, 1, 1)
        self.vivadoToolLayout.addWidget(self.vivado_ver_combo, 0, 3, 1, 1)
        self.vivadoToolLayout.addWidget(self.vivado_dir_label, 1, 0, 1, 1)
        self.vivadoToolLayout.addWidget(self.vivado_dir_input, 2, 0, 1, 3)
        self.vivadoToolLayout.addWidget(self.vivado_select_dir, 2, 3, 1, 1)
        self.edaToolsLayout.addLayout(self.vivadoToolLayout)

        self.edaToolsLayout.addSpacing(self.small_spacing)

        self.intelToolLayout.addWidget(self.intel_check, 0, 0, 1, 1)
        self.intelToolLayout.addWidget(self.verion_label, 0, 2, 1, 1)
        self.intelToolLayout.addWidget(self.intel_ver_combo, 0, 3, 1, 1)
        self.intelToolLayout.addWidget(self.intel_dir_label, 1, 0, 1, 1)
        self.intelToolLayout.addWidget(self.intel_dir_input, 2, 0, 1, 3)
        self.intelToolLayout.addWidget(self.intel_select_dir, 2, 3, 1, 1)
        self.edaToolsLayout.addLayout(self.intelToolLayout)

        self.edaToolsLayout.addStretch()
        self.midColLayout.addLayout(self.edaToolsLayout)

        self.generateLayout.addWidget(self.generate_title)
        self.generateLayout.addSpacing(self.small_spacing)
        self.langLayout.addWidget(self.lang_label, 0, 1, 1, 1)
        self.langLayout.addWidget(self.vhdl_check, 1, 0, 1, 1)
        self.langLayout.addWidget(self.verilog_check, 2, 0, 1, 1)
        self.langLayout.addWidget(self.sverilog_check, 1, 2, 1, 1)
        self.langLayout.addWidget(self.chisel_check, 2, 2, 1, 1)
        self.langLayout.setVerticalSpacing(10)
        self.generateLayout.addLayout(self.langLayout)
        self.generateLayout.addStretch()
        self.rightColLayout.addLayout(self.generateLayout)

        self.mainLayout.addLayout(self.leftColLayout)
        self.mainLayout.addSpacing(self.large_spacing)
        self.mainLayout.addLayout(self.midColLayout)
        self.mainLayout.addSpacing(self.large_spacing)
        self.mainLayout.addLayout(self.rightColLayout)

        self.setLayout(self.mainLayout)

        # Setting actions for buttons
        #self.select_folder_btn.clicked.connect(self.get_dir)
        #self.save_btn.clicked.connect(self.create_xml)
        #self.gen_btn.clicked.connect(self.generate_folders)
