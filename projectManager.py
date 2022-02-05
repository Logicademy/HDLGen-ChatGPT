import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *


class ProjectManager(QWidget):

    def __init__(self):
        super().__init__()

        self.small_spacing = 10
        self.large_spacing = 30
        self.medium_spacing = 25

        # Initializing Widgets

        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)

        self.proj_setting_title = QLabel("Project Settings")
        self.proj_setting_title.setFont(title_font)
        self.proj_setting_title.setStyleSheet("color: white;")
        self.eda_tools_title = QLabel("EDA Tools")
        self.eda_tools_title.setFont(title_font)
        self.eda_tools_title.setStyleSheet("color: white;")
        self.generate_title = QLabel("Generate")
        self.generate_title.setFont(title_font)
        self.generate_title.setStyleSheet("color: white;")


        self.name_label = QLabel('Project Name')
        self.name_label.setStyleSheet("color: white;")
        self.dir_label = QLabel('Project Directory')
        self.dir_label.setStyleSheet("color: white;")
        self.folder_input = QLineEdit()
        self.proj_name_input = QLineEdit()
        self.select_folder_btn = QPushButton()
        self.select_folder_btn .setIcon(QIcon("resources/icons/folder.svg"))
        self.select_folder_btn.setStyleSheet("background-color: white; border-style: plain;")
        self.select_folder_btn.setFixedSize(25, 20)
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

        self.intel_check = QCheckBox("Intel Quartus")
        self.intel_ver_label = QLabel("Version")
        self.intel_ver_combo = QComboBox()
        self.intel_ver_combo.addItem("1")
        self.intel_ver_combo.addItem("2")
        self.intel_dir_label = QLabel('Intel Quartus Installation Directory')
        self.intel_dir_input = QLineEdit()
        self.intel_select_dir = QPushButton()
        self.intel_select_dir.setIcon(QIcon("resources/icons/folder.svg"))
        self.intel_select_dir.setStyleSheet("background-color: white; border-style: plain;")
        self.intel_select_dir.setFixedSize(25, 20)

        self.vivado_check = QCheckBox("Xilinx Vivado")
        self.vivado_ver_label = QLabel("Version")
        self.vivado_ver_combo = QComboBox()
        self.vivado_ver_combo.addItem("2019.1")
        self.vivado_ver_combo.addItem("2020.2")
        self.vivado_dir_label = QLabel('Vivado Installation Directory')
        self.vivado_dir_input = QLineEdit()
        self.vivado_select_dir = QPushButton()
        self.vivado_select_dir.setIcon(QIcon("resources/icons/folder.svg"))
        self.vivado_select_dir.setStyleSheet("background-color: white; border-style: plain;")
        self.vivado_select_dir.setFixedSize(25, 20)

        self.proj_open_btn = QPushButton("Open")
        self.proj_open_btn.setFixedHeight(40)
        self.proj_open_btn.setStyleSheet("background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain;")
        self.proj_save_btn = QPushButton("Save")
        self.proj_save_btn.setFixedHeight(40)
        self.proj_save_btn.setStyleSheet("background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain;")
        self.proj_reset_btn = QPushButton("Reset")
        self.proj_reset_btn.setFixedHeight(40)
        self.proj_reset_btn.setStyleSheet("background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain;")

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

        self.setup_ui()

    def setup_ui(self):


        self.projSettingLayout.addWidget(self.proj_setting_title)
        self.projSettingLayout.addSpacing(self.small_spacing)
        self.projDetailIpLayout.addWidget(self.name_label, 0, 0, 1, 1)
        self.projDetailIpLayout.addWidget(self.proj_name_input, 1, 0, 1, 4)
        self.projDetailIpLayout.addWidget(self.dir_label, 2, 0, 1, 1)
        self.projDetailIpLayout.addWidget(self.folder_input, 3, 0, 1, 4)
        self.projDetailIpLayout.addWidget(self.select_folder_btn, 3, 3, 1, 1, Qt.AlignRight)
        self.projSettingLayout.addLayout(self.projDetailIpLayout)

        self.projSettingFrame.setFrameShape(QFrame.StyledPanel)
        self.projSettingFrame.setStyleSheet(".QFrame{background-color: rgb(97, 107, 129); border-radius: 8px;}")
        self.projSettingFrame.setLayout(self.projSettingLayout)
        self.leftColLayout.addWidget(self.projSettingFrame)
        self.leftColLayout.addStretch()


        self.edaToolsLayout.addWidget(self.eda_tools_title)
        self.edaToolsLayout.addSpacing(self.small_spacing)
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

        self.edaToolsLayout.addSpacing(self.medium_spacing)

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
        self.edaToolsFrame.setStyleSheet(".QFrame{background-color: rgb(97, 107, 129); border-radius: 8px;}")
        self.edaToolsFrame.setLayout(self.edaToolsLayout)

        self.midColLayout.addWidget(self.edaToolsFrame)

        self.generateLayout.addWidget(self.generate_title)
        self.generateLayout.addSpacing(self.small_spacing)
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
        self.generateFrame.setStyleSheet(".QFrame{background-color: rgb(97, 107, 129); border-radius: 8px;}")
        self.generateFrame.setLineWidth(3)
        self.generateFrame.setLayout(self.generateLayout)

        self.rightColLayout.addWidget(self.generateFrame)
        self.rightColLayout.addSpacing(self.medium_spacing)

        self.proj_action_layout.addWidget(self.proj_reset_btn)
        self.proj_action_layout.addWidget(self.proj_open_btn)
        self.proj_action_layout.addWidget(self.proj_save_btn)
        self.rightColLayout.addLayout(self.proj_action_layout)

        self.mainLayout.addLayout(self.leftColLayout)
        self.mainLayout.addSpacing(self.medium_spacing)
        self.mainLayout.addLayout(self.midColLayout)
        self.mainLayout.addSpacing(self.medium_spacing)
        self.mainLayout.addLayout(self.rightColLayout)

        self.setLayout(self.mainLayout)

        # Setting actions for buttons
        #self.select_folder_btn.clicked.connect(self.get_dir)
        #self.save_btn.clicked.connect(self.create_xml)
        #self.gen_btn.clicked.connect(self.generate_folders)
