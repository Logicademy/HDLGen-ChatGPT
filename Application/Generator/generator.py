import os
from xml.dom import minidom
from PySide2.QtWidgets import *
import sys
sys.path.append("..")
from ProjectManager.project_manager import ProjectManager


class Generator(QWidget):

    def __init__(self, proj_dir):
        super().__init__()

        if proj_dir != None:
            self.proj_dir = proj_dir
        else:
            self.proj_dir = ProjectManager.get_proj_dir()

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
        self.gen_vhdl_btn.clicked.connect(self.create_vhdl_file)
        self.mainLayout.addWidget(self.gen_vhdl_btn)

        self.setLayout(self.mainLayout)

    def generate_folders(self):

        print("Generating Project folders...")

        # Parsing the xml file
        xml_data_path = ProjectManager.get_xml_data_path()
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

        print("All project folders have been successfully generated at ", self.proj_dir)

    @staticmethod
    def generate_vhdl():

        gen_vhdl = ""

        xml_data_path = ProjectManager.get_xml_data_path()

        test_xml = os.path.join("../Resources", "SampleProject.xml")

        vhdl_database_path = "./Generator/HDL_Database/vhdl_database.xml"

        # Parsing the xml file
        project_data = minidom.parse(xml_data_path)
        HDLGen = project_data.documentElement

        vhdl_database = minidom.parse(vhdl_database_path)
        vhdl_root = vhdl_database.documentElement

        hdl_design = HDLGen.getElementsByTagName("hdlDesign")

        entity_name = ""

        # Header Section

        header_node = hdl_design[0].getElementsByTagName("header")
        if header_node is not None:
            comp_node = header_node[0].getElementsByTagName("compName")[0]
            if comp_node.firstChild.data != "null":
                entity_name = comp_node.firstChild.data

                gen_header = "-- Header Section\n"
                gen_header += "-- Component Name : " + entity_name + "\n"
                title = header_node[0].getElementsByTagName("title")[0].firstChild.data
                gen_header += "-- Title          : " + (title if title != "null" else "") + "\n"
                desc = header_node[0].getElementsByTagName("description")[0].firstChild.data
                gen_header += "-- Description    : " + (desc if desc != "null" else "") + "\n"
                authors = header_node[0].getElementsByTagName("authors")[0].firstChild.data
                gen_header += "-- Author(s)      : " + (authors if authors != "null" else "") + "\n"
                company = header_node[0].getElementsByTagName("company")[0].firstChild.data
                gen_header += "-- Company        : " + (company if company != "null" else "") + "\n"
                email = header_node[0].getElementsByTagName("email")[0].firstChild.data
                gen_header += "-- Email          : " + (email if email != "null" else "") + "\n"
                gen_header += "-- Date           : " + header_node[0].getElementsByTagName("date")[
                    0].firstChild.data + "\n\n\n"

                gen_vhdl += gen_header

                # Libraries Section

                libraries_node = vhdl_root.getElementsByTagName("libraries")
                libraries = libraries_node[0].getElementsByTagName("library")
                gen_library = "-- Library Section\n"

                for library in libraries:
                    gen_library += library.firstChild.data + "\n"

                gen_library += "\n"
                gen_vhdl += gen_library

                # Entity Section

                gen_signals = ""
                io_port_node = hdl_design[0].getElementsByTagName("entityIOPorts")

                if len(io_port_node) != 0 and io_port_node[0].firstChild is not None:
                    for signal in io_port_node[0].getElementsByTagName('signal'):
                        signal_declare_syntax = vhdl_root.getElementsByTagName("signalDeclaration")[0].firstChild.data

                        signal_declare_syntax = signal_declare_syntax.replace("$sig_name",
                                                                              signal.getElementsByTagName('name')[
                                                                                  0].firstChild.data)
                        signal_declare_syntax = signal_declare_syntax.replace("$mode",
                                                                              signal.getElementsByTagName('mode')[
                                                                                  0].firstChild.data)
                        signal_declare_syntax = signal_declare_syntax.replace("$type",
                                                                              signal.getElementsByTagName('type')[
                                                                                  0].firstChild.data)

                        gen_signals += "\t" + signal_declare_syntax + "\n"

                    gen_signals = gen_signals.rstrip()
                    gen_signals = gen_signals[0:-1]

                    entity_syntax = vhdl_root.getElementsByTagName("entity")
                    gen_entity = "-- Entity Section\n"
                    gen_entity += entity_syntax[0].firstChild.data

                    gen_entity = gen_entity.replace("$comp_name", entity_name)
                    gen_entity = gen_entity.replace("$signals", gen_signals)

                    gen_vhdl += gen_entity + "\n\n"

                # Architecture section

                # Internal signals
                gen_int_sig = "-- Internal Signals\n"
                int_sig_node = hdl_design[0].getElementsByTagName("internalSignals")
                if int_sig_node is not None:
                    for signal in int_sig_node[0].getElementsByTagName("signal"):
                        int_sig_syntax = vhdl_root.getElementsByTagName("intSigDeclaration")[0].firstChild.data
                        int_sig_syntax = int_sig_syntax.replace("$int_sig_name",
                                                                signal.getElementsByTagName('name')[0].firstChild.data)
                        int_sig_syntax = int_sig_syntax.replace("$int_sig_type",
                                                                signal.getElementsByTagName('type')[0].firstChild.data)

                        gen_int_sig += int_sig_syntax + "\n"

                    gen_int_sig.rstrip()

                # Process
                arch_node = hdl_design[0].getElementsByTagName("architecture")
                gen_process = ""

                if len(arch_node) != 0 and arch_node[0].firstChild is not None:

                    child = arch_node[0].firstChild

                    while child is not None:

                        next = child.nextSibling

                        if (child.nodeType == arch_node[0].ELEMENT_NODE and child.tagName == "process"):

                            process_syntax = vhdl_root.getElementsByTagName("process")[0].firstChild.data

                            process_syntax = process_syntax.replace("$process_label",
                                                                    child.getElementsByTagName("label")[
                                                                        0].firstChild.data)

                            gen_in_sig = ""

                            for input_signal in child.getElementsByTagName("inputSignal"):
                                gen_in_sig += input_signal.firstChild.data + ","

                            gen_in_sig = gen_in_sig[:-1]

                            process_syntax = process_syntax.replace("$input_signals", gen_in_sig)

                            gen_defaults = ""
                            for default_out in child.getElementsByTagName("defaultOutput"):
                                assign_syntax = vhdl_root.getElementsByTagName("sigAssingn")[0].firstChild.data
                                signals = default_out.firstChild.data.split(",")
                                assign_syntax = assign_syntax.replace("$output_signal", signals[0])
                                assign_syntax = assign_syntax.replace("$value", signals[1])

                                gen_defaults += "\t" + assign_syntax + "\n"

                            process_syntax = process_syntax.replace("$default_assignments", gen_defaults)
                            gen_process += process_syntax + "\n\n"

                        elif (child.nodeType == arch_node[0].ELEMENT_NODE and child.tagName == "concurrentStmt"):

                            gen_stmts = ""
                            conc_syntax = vhdl_root.getElementsByTagName("concurrentstmt")[0].firstChild.data

                            conc_syntax = conc_syntax.replace("$concurrentstmt_label",
                                                                    child.getElementsByTagName("label")[
                                                                        0].firstChild.data)

                            for statement in child.getElementsByTagName("statement"):
                                assign_syntax = vhdl_root.getElementsByTagName("sigAssingn")[0].firstChild.data
                                signals = statement.firstChild.data.split(",")
                                assign_syntax = assign_syntax.replace("$output_signal", signals[0])
                                assign_syntax = assign_syntax.replace("$value", signals[1])

                                gen_stmts += assign_syntax + "\n"

                            conc_syntax = conc_syntax.replace("$statement", gen_stmts)
                            gen_process += conc_syntax + "\n"

                        child = next

                    arch_syntax = vhdl_root.getElementsByTagName("architecture")[0].firstChild.data
                    arch_name_node = arch_node[0].getElementsByTagName("archName")

                    arch_name = "comb"

                    if len(arch_name_node) != 0 and arch_name_node[0].firstChild is not None:
                        arch_name = arch_name_node[0].firstChild.data

                    gen_arch = arch_syntax.replace("$arch_name", arch_name)
                    gen_arch = gen_arch.replace("$comp_name", entity_name)
                    gen_arch = gen_arch.replace("$int_sig_declaration", gen_int_sig)
                    gen_arch = gen_arch.replace("$arch_elements", gen_process[:-1])

                    gen_vhdl += gen_arch

        return entity_name, gen_vhdl

    def create_vhdl_file(self):

        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        entity_name, vhdl_code = self.generate_vhdl()

        vhdl_file_path = os.path.join(proj_path, "VHDL", "model", entity_name + ".vhd")

        print(vhdl_code)

        # Writing xml file
        with open(vhdl_file_path, "w") as f:
            f.write(vhdl_code)

        print("VHDL Model successfully generated at ", vhdl_file_path)



