import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from projectManager import ProjectManager


class Generate(QWidget):

    def __init__(self):
        super().__init__()

        self.gen_vhdl = ""

        self.gen_folder_btn = QPushButton("Generate Folders")
        self.gen_folder_btn.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")

        self.gen_vhdl_btn = QPushButton("Generate VHDL")
        self.gen_vhdl_btn.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")

        self.mainLayout = QHBoxLayout()

        self.setup_ui()


    def setup_ui(self):

        self.gen_folder_btn.setFixedSize(150, 50)
        self.gen_folder_btn.clicked.connect(self.generate_folders)
        self.mainLayout.addWidget(self.gen_folder_btn)

        self.gen_vhdl_btn.setFixedSize(150, 50)
        self.gen_vhdl_btn.clicked.connect(self.generate_vhdl)
        self.mainLayout.addWidget(self.gen_vhdl_btn)

        self.setLayout(self.mainLayout)

    def generate_folders(self):

        print("Generating Project folders...")

        proj_name = ProjectManager.get_proj_name();

        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        xml_data_path = os.path.join(proj_path, proj_name + '.HDLGen', proj_name + '_data.xml')

        # Parsing the xml file
        project_data = minidom.parse(xml_data_path)
        HDLGen = project_data.documentElement

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

        print("All project folders have been successfully generated at ", proj_path, )

    def generate_vhdl(self):

        #proj_name = ProjectManager.get_proj_name();
        #proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        #xml_data_path = os.path.join(proj_path, proj_name + '.HDLGen', proj_name + '_data.xml')
        test_xml = os.path.join("resources", "SampleProject.xml")

        vhdl_database_path = os.path.join("resources", "HDL_Database", "vhdl_database.xml")

        # Parsing the xml file
        project_data = minidom.parse(test_xml)
        HDLGen = project_data.documentElement

        vhdl_database = minidom.parse(vhdl_database_path)
        vhdl_root = vhdl_database.documentElement

        hdl_design = HDLGen.getElementsByTagName("hdlDesign")


        # Header Section

        header_node = hdl_design[0].getElementsByTagName("header")
        entity_name = header_node[0].getElementsByTagName("compName")[0].firstChild.data

        gen_header = "-- Header Section\n"
        gen_header += "-- Component Name : " + entity_name + "\n"
        gen_header += "-- Title          : " + header_node[0].getElementsByTagName("title")[0].firstChild.data + "\n"
        gen_header += "-- Description    : " + header_node[0].getElementsByTagName("description")[0].firstChild.data + "\n"

        author_str = ""
        for author in header_node[0].getElementsByTagName("author"):
            author_str += author.firstChild.data + ", "

        gen_header += "-- Author(s)      : " + author_str[:-2] + "\n"
        gen_header += "-- Company        : " + header_node[0].getElementsByTagName("company")[0].firstChild.data + "\n"
        gen_header += "-- Email          : " + header_node[0].getElementsByTagName("email")[0].firstChild.data + "\n"
        gen_header += "-- Date           : " + header_node[0].getElementsByTagName("date")[0].firstChild.data + "\n\n\n"

        self.gen_vhdl += gen_header


        # Libraries Section

        libraries_node = vhdl_root.getElementsByTagName("libraries")
        libraries = libraries_node[0].getElementsByTagName("library")
        gen_library = "-- Library Section\n"

        for library in libraries:
            gen_library += library.firstChild.data + "\n"

        gen_library += "\n"
        self.gen_vhdl += gen_library


        # Entity Section

        gen_signals = ""

        entity_node = vhdl_root.getElementsByTagName("entity")
        gen_entity = "-- Entity Section\n"
        gen_entity += entity_node[0].firstChild.data

        gen_entity.replace("$comp_name", entity_name)
        gen_entity.replace("$signals", gen_signals)

        self.gen_vhdl += gen_entity

        print(self.gen_vhdl)



