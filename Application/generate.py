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

        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        xml_data_path = os.path.join(proj_path, proj_name + '.HDLGen', proj_name + '_data.xml')

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
        vhdl_file_path = os.path.join(proj_path, "VHDL", "model", entity_name + ".vhd")

        gen_header = "-- Header Section\n"
        gen_header += "-- Component Name : " + entity_name + "\n"
        gen_header += "-- Title          : " + header_node[0].getElementsByTagName("title")[0].firstChild.data + "\n"
        gen_header += "-- Description    : " + header_node[0].getElementsByTagName("description")[0].firstChild.data + "\n"
        gen_header += "-- Author(s)      : " + header_node[0].getElementsByTagName("authors")[0].firstChild.data + "\n"
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
        io_port_node = hdl_design[0].getElementsByTagName("entityIOPorts")

        for signal in io_port_node[0].getElementsByTagName('signal'):
            signal_declare_syntax = vhdl_root.getElementsByTagName("signalDeclaration")[0].firstChild.data

            signal_declare_syntax = signal_declare_syntax.replace("$sig_name", signal.getElementsByTagName('name')[0].firstChild.data)
            signal_declare_syntax = signal_declare_syntax.replace("$mode", signal.getElementsByTagName('mode')[0].firstChild.data)
            signal_declare_syntax = signal_declare_syntax.replace("$type", signal.getElementsByTagName('type')[0].firstChild.data)

            gen_signals += "\t" + signal_declare_syntax + "\n"

        gen_signals = gen_signals.rstrip()

        entity_syntax = vhdl_root.getElementsByTagName("entity")
        gen_entity = "-- Entity Section\n"
        gen_entity += entity_syntax[0].firstChild.data

        gen_entity = gen_entity.replace("$comp_name", entity_name)
        gen_entity = gen_entity.replace("$signals", gen_signals)

        self.gen_vhdl += gen_entity + "\n\n"


        # Architecture section

        # Internal signals
        gen_int_sig = ""
        int_sig_node = hdl_design[0].getElementsByTagName("internalSignals")

        for signal in int_sig_node[0].getElementsByTagName("signal"):
            int_sig_syntax = vhdl_root.getElementsByTagName("intSigDeclaration")[0].firstChild.data
            int_sig_syntax = int_sig_syntax.replace("$int_sig_name", signal.getElementsByTagName('name')[0].firstChild.data)
            int_sig_syntax = int_sig_syntax.replace("$int_sig_type", signal.getElementsByTagName('type')[0].firstChild.data)

            gen_int_sig += int_sig_syntax

        gen_int_sig.rstrip()

        # Process
        arch_node = hdl_design[0].getElementsByTagName("architecture")

        gen_process = ""

        for process_node in arch_node[0].getElementsByTagName("process"):
            process_syntax = vhdl_root.getElementsByTagName("process")[0].firstChild.data

            process_syntax = process_syntax.replace("$process_label", process_node.getElementsByTagName("label")[0].firstChild.data)

            gen_in_sig = ""

            for input_signal in process_node.getElementsByTagName("inputSignal"):
                gen_in_sig += input_signal.firstChild.data + ","

            gen_in_sig = gen_in_sig[:-1]

            process_syntax = process_syntax.replace("$input_signals", gen_in_sig)

            gen_defaults = ""
            for default_out in process_node.getElementsByTagName("defaultOutput"):
                assign_syntax = vhdl_root.getElementsByTagName("sigAssingn")[0].firstChild.data
                signals = default_out.firstChild.data.split(",")
                assign_syntax = assign_syntax.replace("$output_signal", signals[0])
                assign_syntax = assign_syntax.replace("$value", signals[1])

                gen_defaults += "\t" + assign_syntax + "\n"

            process_syntax = process_syntax.replace("$default_assignments", gen_defaults)
            gen_process += process_syntax + "\n\n"

        arch_syntax = vhdl_root.getElementsByTagName("architecture")[0].firstChild.data
        arch_name = arch_node[0].getElementsByTagName("archName")[0].firstChild.data

        gen_arch = arch_syntax.replace("$arch_name", arch_name)
        gen_arch = gen_arch.replace("$comp_name", entity_name)
        gen_arch = gen_arch.replace("$int_sig_declaration", gen_int_sig)
        gen_arch = gen_arch.replace("$arch_elements", gen_process[:-1])

        self.gen_vhdl += gen_arch

        print(self.gen_vhdl)

        # Writing xml file
        with open(vhdl_file_path, "w") as f:
            f.write(self.gen_vhdl)

        print("VHDL Model successfully generated at ", vhdl_file_path)



