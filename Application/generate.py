import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from projectManager import ProjectManager


class Generate(QWidget):

    def __init__(self):
        super().__init__()

        self.gen_folder_btn = QPushButton("Generate Folders")
        self.gen_folder_btn.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")

        self.mainLayout = QHBoxLayout()

        self.setup_ui()

    def setup_ui(self):

        self.gen_folder_btn.setFixedSize(150, 50)
        self.gen_folder_btn.clicked.connect(self.generate_folders)

        self.mainLayout.addWidget(self.gen_folder_btn)

        self.setLayout(self.mainLayout)

    def generate_folders(self):

        print("Generating Project folders...")

        proj_name =  ProjectManager.get_proj_name();

        proj_path = os.path.join(ProjectManager.get_proj_dir(),)
        xml_data_path = os.path.join(proj_path, proj_name + '.HDLGen',  proj_name, '.HDLGen_data.xml')

        # Parsing the xml file
        data = minidom.parse(xml_data_path)
        HDLGen = data.documentElement

        # Accessing the projectManager and genFolder Elements
        project_Manager = HDLGen.getElementsByTagName("projectManager")
        settings = project_Manager[0].getElementsByTagName("settings")[0]
        location = settings.getElementsByTagName("location")[0].firstChild.data
        genFolder_data = HDLGen.getElementsByTagName("genFolder")
        hdl_data = project_Manager[0].getElementsByTagName("HDL")[0]
        hdl_langs = hdl_data.getElementsByTagName("language")

        for hdl_lang in hdl_langs:
            # If vhdl is present in the hdl settings then directory with vhdl_folder tag are read
            if hdl_lang.getElementsByTagName('name')[0].firstChild.data == "VHDL":
                for folder in genFolder_data[0].getElementsByTagName("vhdl_folder"):
                    # Creating the directory
                    path = os.path.join(location, folder.firstChild.data)
                    os.makedirs(path, exist_ok=True)
                    # If verilog is present in the hdl settings then directory with verilog_folder are read
            if hdl_lang.getElementsByTagName('name')[0].firstChild.data == "Verilog":
                for folder in genFolder_data[0].getElementsByTagName("verilog_folder"):
                    # Creating the directory
                    path = os.path.join(location, folder.firstChild.data)
                    os.makedirs(path, exist_ok=True)

        print("All project folders have been successfully generated at ", proj_path)
