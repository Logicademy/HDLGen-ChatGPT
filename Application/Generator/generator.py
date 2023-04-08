import os
import re
from xml.dom import minidom
from PySide2.QtWidgets import *
import subprocess
import sys
from textwrap import indent
sys.path.append("..")
from ProjectManager.project_manager import ProjectManager


class Generator(QWidget):

    def __init__(self):
        super().__init__()
        self.dirs = []
        self.entity_name = ""
        self.arrayPackage = ""
        self.includeArrays = False
        self.tcl_path = ""


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


    #@staticmethod
    def generate_vhdl(self):
        entity_name = ""
        gen_vhdl = ""
        gen_array_vhdl = ""

        xml_data_path = ProjectManager.get_xml_data_path()


        vhdl_database_path = "./Generator/HDL_Database/vhdl_database.xml"

        # Parsing the xml file
        project_data = minidom.parse(xml_data_path)
        HDLGen = project_data.documentElement

        vhdl_database = minidom.parse(vhdl_database_path)
        vhdl_root = vhdl_database.documentElement

        hdl_design = HDLGen.getElementsByTagName("hdlDesign")
        stateTypesList = ""
        gen_int_sig = ""
        gen_internal_signal_result = ""
        arrayList=[]
        single_bitList=[]
        busList=[]
        unsignedList=[]
        signedList=[]
        # Entity Section
        gen_signals = ""
        entity_signal_description = ""
        io_port_node = hdl_design[0].getElementsByTagName("entityIOPorts")
        gen_entity = ""
        self.includeArrays = False
        gen_arrays=""
        stateTypeSig = False

        if len(io_port_node) != 0 and io_port_node[0].firstChild is not None:

            for signal in io_port_node[0].getElementsByTagName('signal'):
                name = signal.getElementsByTagName('name')[0].firstChild.data
                type = signal.getElementsByTagName('type')[0].firstChild.data
                if type[0:5] == "array":
                    self.includeArrays = True
                    arrayList.append(name)
                elif type == "single bit":
                    single_bitList.append(name)
                    type = "std_logic"
                elif type[0:3] == "bus":
                    busList.append(name)
                    type = type.replace("bus","std_logic_vector")
                elif type[0:8] == "unsigned":
                    unsignedList.append(name)
                elif type[0:6] == "signed":
                    signedList.append(name)

                signal_declare_syntax = vhdl_root.getElementsByTagName("signalDeclaration")[0].firstChild.data

                signal_declare_syntax = signal_declare_syntax.replace("$sig_name",
                                                                      signal.getElementsByTagName('name')[
                                                                          0].firstChild.data)
                signal_declare_syntax = signal_declare_syntax.replace("$mode",
                                                                      signal.getElementsByTagName('mode')[
                                                                          0].firstChild.data)
                signal_declare_syntax = signal_declare_syntax.replace("$type",type)
                signal_description = signal.getElementsByTagName('description')[
                    0].firstChild.data
                signal_description = signal_description.replace("&#10;", "\n-- ")
                entity_signal_description += "-- " + signal.getElementsByTagName('name')[
                    0].firstChild.data + "\t" + signal_description + "\n"
                gen_signals += "\t" + signal_declare_syntax + "\n"
            gen_signals = gen_signals.rstrip()
            gen_signals = gen_signals[0:-1]

            entity_syntax = vhdl_root.getElementsByTagName("entity")
            gen_entity = "-- entity declaration\n"
            gen_entity += entity_syntax[0].firstChild.data

            gen_entity = gen_entity.replace("$signals", gen_signals)


            # Internal signals
            gen_int_sig = "-- Internal signal declarations"

            int_sig_node = hdl_design[0].getElementsByTagName("internalSignals")

            if int_sig_node[0].firstChild is not None:
                stateTypesString = ""

                stateTypesList = int_sig_node[0].getElementsByTagName("stateTypes")
                for stateType in int_sig_node[0].getElementsByTagName("stateTypes"):  # stateTypesList:
                    stateTypesString += stateType.firstChild.data + ", "
                stateTypesString = stateTypesString[:-2]

                if stateTypesString != "":
                    stateType_syntax = vhdl_root.getElementsByTagName("stateNamesDeclarations")[0].firstChild.data
                    stateType_syntax = stateType_syntax.replace("$stateNamesList", stateTypesString)
                    gen_int_sig += "\n" + stateType_syntax
                for signal in int_sig_node[0].getElementsByTagName("signal"):
                    name = signal.getElementsByTagName('name')[0].firstChild.data
                    type = signal.getElementsByTagName('type')[0].firstChild.data

                    if type == "Enumerated type state signal pair(NS/CS)":
                        type = "stateType"
                        if name[0:2] == "CS":
                            stateTypeSig = True
                            CSState = name
                    elif type == "single bit":
                        single_bitList.append(name)
                        type = "std_logic"
                    elif type[0:5] == "array":
                        self.includeArrays = True
                        arrayList.append(name)
                    elif type[0:3] == "bus":
                        busList.append(name)
                        type = type.replace("bus","std_logic_vector")
                    elif type[0:8] == "unsigned":
                        unsignedList.append(name)
                    elif type[0:6] == "signed":
                        signedList.append(name)
                    int_sig_syntax = vhdl_root.getElementsByTagName("intSigDeclaration")[0].firstChild.data
                    int_sig_syntax = int_sig_syntax.replace("$int_sig_name", name)
                    int_sig_syntax = int_sig_syntax.replace("$int_sig_type", type)
                    int_signal_description = signal.getElementsByTagName('description')[
                        0].firstChild.data
                    int_signal_description = int_signal_description.replace("&#10;", "\n-- ")

                    gen_int_sig += "\n" + int_sig_syntax
                    gen_internal_signal_result += "-- " + signal.getElementsByTagName('name')[
                        0].firstChild.data + "\t" + int_signal_description + "\n"

                gen_int_sig.rstrip()

            else:
                gen_int_sig += "\n-- None"
                gen_internal_signal_result = "-- None\n"


        # Header Section

        header_node = hdl_design[0].getElementsByTagName("header")
        if header_node is not None:
            comp_node = header_node[0].getElementsByTagName("compName")[0]
            if comp_node.firstChild.data != "null":
                entity_name = comp_node.firstChild.data

                gen_header = "-- Header Section\n"
                gen_header += "--Generated by HDLGen, Github https://github.com/abishek-bupathi/HDLGen\n--Reference: https://tinyurl.com/VHDLTips\n\n"
                gen_header += "-- Component Name : " + entity_name + "\n"
                title = header_node[0].getElementsByTagName("title")[0].firstChild.data
                gen_header += "-- Title          : " + (title if title != "null" else "")+"\n\n"
                desc = header_node[0].getElementsByTagName("description")[0].firstChild.data
                desc = desc.replace("&#10;", "\n-- ")
                gen_header += "-- Description\n-- "
                gen_header += (desc if desc != "null" else "") + "\n"
                authors = header_node[0].getElementsByTagName("authors")[0].firstChild.data
                gen_header += "\n-- Author(s)      : " + (authors if authors != "null" else "") + "\n"
                company = header_node[0].getElementsByTagName("company")[0].firstChild.data
                gen_header += "-- Company        : " + (company if company != "null" else "") + "\n"
                email = header_node[0].getElementsByTagName("email")[0].firstChild.data
                gen_header += "-- Email          : " + (email if email != "null" else "") + "\n"
                gen_header += "-- Date           : " + header_node[0].getElementsByTagName("date")[
                    0].firstChild.data + "\n\n"

                gen_vhdl += gen_header

                # entity signal dictionary
                gen_entity = gen_entity.replace("$comp_name", entity_name)
                gen_entity_signal = "-- entity signal dictionary\n"
                gen_entity_signal += entity_signal_description+"\n"
                gen_vhdl += gen_entity_signal

                # internal signal dictionary
                gen_internal_signal = "-- internal signal dictionary\n"
                gen_internal_signal_result = gen_internal_signal_result +"\n"
                gen_internal_signal += gen_internal_signal_result
                gen_vhdl += gen_internal_signal
                # Libraries Section

                libraries_node = vhdl_root.getElementsByTagName("libraries")
                libraries = libraries_node[0].getElementsByTagName("library")
                gen_library = "-- library declarations\n"

                for library in libraries:
                    gen_library += library.firstChild.data + "\n"


                # Process
                arch_node = hdl_design[0].getElementsByTagName("architecture")
                gen_process = ""
                clkAndRst = hdl_design[0].getElementsByTagName('clkAndRst')
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
                            gen_defaults = "\t"
                            if_gen_defaults = "\t"
                            clkgen_defaults = ""
                            caseEmpty=True
                            for default_out in child.getElementsByTagName("defaultOutput"):
                                assign_syntax = vhdl_root.getElementsByTagName("sigAssingn")[0].firstChild.data
                                signals = default_out.firstChild.data.split(",")
                                assign_syntax = assign_syntax.replace("$output_signal", signals[0])
                                value=signals[1]
                                if value == "rst state":
                                    if stateTypesList != "":
                                        stateNames = stateTypesString.split(",")
                                        value = stateNames[0]
                                elif value == "zero":
                                    if signals[0] in arrayList:
                                        value = "(others =>(others => '0'))"
                                    elif signals[0] in single_bitList:
                                        value = "'" + '0' + "'"
                                    elif signals[0] in busList or signals[0] in signedList or signals[0] in unsignedList:
                                        value = "(others => '0')"
                                    else:
                                        value = str(0)
                                elif value == "one":
                                    if signals[0] in arrayList:
                                        value = "(others =>(others => '1'))"
                                    elif signals[0] in single_bitList:
                                        value = "'" + '1' + "'"
                                    elif signals[0] in busList or signals[0] in signedList or signals[
                                        0] in unsignedList:
                                        value = "(others => '1')"
                                    else:
                                        value = str(1)
                                elif value.isdigit():
                                    if value == "1" or value == "0":
                                        value = "'" + value + "'"
                                    else:
                                        value = '"'+value+'"'

                                elif stateTypeSig == True and value == CSState:
                                    caseEmpty = False
                                    case_syntax = vhdl_root.getElementsByTagName("case")[0].firstChild.data
                                    case_syntax = case_syntax.replace("$stateType", value)
                                    stateNames = stateTypesString.split(",")
                                    whenCase=""
                                    for states in stateNames:
                                        whenCase +="\n\t\twhen "+ states + "=>" + "\n\t\t\tnull;"
                                    case_syntax = case_syntax.replace("$whenCase", whenCase)

                                assign_syntax = assign_syntax.replace("$value", value)
                                if_gen_defaults += "\t" + assign_syntax + "\n\t"
                                gen_defaults +=  assign_syntax + "-- default\n\t"
                                if len(signals) == 3:
                                    clkAssign_syntax = vhdl_root.getElementsByTagName("sigAssingn")[0].firstChild.data
                                    clkAssign_syntax = clkAssign_syntax.replace("$output_signal", signals[0])
                                    value = signals[2]
                                    if value == "zero":
                                        if signals[0] in arrayList:
                                            value = "(others =>(others => '0'))"
                                        elif signals[0] in single_bitList:
                                            value = "'" + '0' + "'"
                                        elif signals[0] in busList or signals[0] in signedList or signals[
                                            0] in unsignedList:
                                            value = "(others => '0')"
                                        else:
                                            value = str(0)
                                    clkAssign_syntax = clkAssign_syntax.replace("$value", value)# signals[2])
                                    clkgen_defaults += "\t\t" + clkAssign_syntax + "\n"
                            if gen_defaults != "":
                                if clkgen_defaults != "":
                                    for clkRst in clkAndRst[0].getElementsByTagName("clkAndRst"):
                                        clkEdge = "rising_edge"
                                        if clkRst.getElementsByTagName('activeClkEdge')[0].firstChild.data == "H-L":
                                            clkEdge = "falling_edge"
                                        clkif_syntax = vhdl_root.getElementsByTagName("clkIfStatement")[0].firstChild.data
                                        clkif_syntax = clkif_syntax.replace("$edge", clkEdge)
                                        if clkRst.getElementsByTagName('rst')[0].firstChild.data == "Yes":
                                            if_syntax = vhdl_root.getElementsByTagName("ifStatement")[0].firstChild.data
                                            if_syntax = if_syntax.replace("$assignment", "rst")
                                            if_syntax = if_syntax.replace("$value", clkRst.getElementsByTagName('ActiveRstLvl')[0].firstChild.data)
                                            if_syntax = if_syntax.replace("$default_assignments", if_gen_defaults)#gen_defaults )
                                           # if_gen_defaults = "\t" + if_syntax + "\n"
                                            if clkRst.getElementsByTagName('RstType')[0].firstChild.data == "asynch":
                                                elsif_syntax = vhdl_root.getElementsByTagName("elsifStatement")[0].firstChild.data
                                                elsif_syntax = elsif_syntax.replace("$edge", clkEdge)
                                                elsif_syntax = elsif_syntax.replace("$default_assignments",clkgen_defaults)
                                                if_syntax = if_syntax.replace("$else", elsif_syntax)
                                                clkgen_defaults = "\t" + if_syntax + "\n"
                                            else:
                                                else_syntax = vhdl_root.getElementsByTagName("elseStatement")[0].firstChild.data
                                                else_syntax = else_syntax.replace("$default_assignments", clkgen_defaults )
                                                if_syntax = if_syntax.replace("$else", else_syntax)
                                                clkgen_defaults = "\t" + if_syntax + "\n"
                                                clkgen_defaults = indent(clkgen_defaults,'    ')
                                                clkif_syntax = clkif_syntax.replace("$default_assignments", clkgen_defaults)
                                                clkgen_defaults = "\t" + clkif_syntax + "\n"
                                        else:
                                            clkif_syntax = clkif_syntax.replace("$default_assignments", clkgen_defaults)
                                            clkgen_defaults = "\t" + clkif_syntax + "\n"
                                    clkgen_defaults=clkgen_defaults.rstrip()
                                    process_syntax = process_syntax.replace("$default_assignments", clkgen_defaults)
                                else:
                                    if caseEmpty == False:
                                        gen_defaults += "\n" + case_syntax
                                    gen_defaults = gen_defaults.rstrip()
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
                                value=signals[1]
                                if value.isdigit():
                                    if value == "1" or value == "0":
                                        value = "'" + value + "'"
                                    else:
                                        value = '"' + value + '"'
                                elif value == "zero":
                                    if signals[0] in arrayList:
                                        value = "(others =>(others => '0'))"
                                    elif signals[0] in single_bitList:
                                        value = "'" + '0' + "'"
                                    elif signals[0] in busList or signals[0] in signedList or signals[
                                        0] in unsignedList:
                                        value = "(others => '0')"
                                    else:
                                        value = str(0)
                                assign_syntax = assign_syntax.replace("$value", value)

                                gen_stmts += assign_syntax

                            conc_syntax = conc_syntax.replace("$statement", gen_stmts)
                            gen_process += conc_syntax + "\n"

                        elif (child.nodeType == arch_node[0].ELEMENT_NODE and child.tagName == "instance"):
                            self.includeArrays = True
                            gen_stmts = ""
                            instance_syntax = vhdl_root.getElementsByTagName("instance")[0].firstChild.data

                            instance_syntax = instance_syntax.replace("$instance_label",
                                                              child.getElementsByTagName("label")[
                                                                  0].firstChild.data)
                            for instance in child.getElementsByTagName("port"):
                                assign_syntax = vhdl_root.getElementsByTagName("portAssign")[0].firstChild.data
                                signals = instance.firstChild.data.split(",")
                                assign_syntax = assign_syntax.replace("$output_signal", signals[0])
                                assign_syntax = assign_syntax.replace("$value", signals[1])

                                gen_stmts += "\t" + assign_syntax + ",\n"
                            gen_stmts = gen_stmts.rstrip()
                            gen_stmts = gen_stmts[0:-1]
                            instance_syntax = instance_syntax.replace("$portAssign", gen_stmts)
                            instance_syntax = instance_syntax.replace("$instance",
                                                                      child.getElementsByTagName("model")[
                                                                          0].firstChild.data)
                            gen_process += instance_syntax + "\n"

                        child = next
                    arch_syntax = vhdl_root.getElementsByTagName("architecture")[0].firstChild.data
                    arch_name_node = arch_node[0].getElementsByTagName("archName")

                    arch_name = "Combinational"

                    if len(arch_name_node) != 0 and arch_name_node[0].firstChild is not None:
                        arch_name = arch_name_node[0].firstChild.data

                    gen_arch = arch_syntax.replace("$arch_name", arch_name)
                    gen_arch = gen_arch.replace("$comp_name", entity_name)
                    gen_arch = gen_arch.replace("$int_sig_declaration", gen_int_sig)
                    gen_arch = gen_arch.replace("$arch_elements", gen_process[:-1])
                    gen_vhdl += gen_library
                    if self.includeArrays == True:
                        gen_vhdl += "use work.MainPackage.all;"

                    # Entity Section placement
                    gen_vhdl += "\n\n" + gen_entity + "\n\n"
                    gen_vhdl += gen_arch

        return entity_name, gen_vhdl

    def create_vhdl_file(self):

        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        entity_name, vhdl_code = self.generate_vhdl()

        vhdl_file_path = os.path.join(proj_path, "VHDL", "model", entity_name + ".vhd")
        vhdl_file_HDLGen_path = os.path.join(proj_path, "VHDL", "model", entity_name + "_HDLGen.vhd")
        overwrite = False
        instances=[]
        if os.path.exists(vhdl_file_path):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setText("Do you want to overwrite manually edited file?")
            msgBox.setWindowTitle("Confirmation")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgBox.setDefaultButton(QMessageBox.No)
            response = msgBox.exec_()
            if response == QMessageBox.Yes:
                overwrite = True
                # Writing xml file
                with open(vhdl_file_path, "w") as f:
                    f.write(vhdl_code)
                print("VHDL Model successfully generated at ", vhdl_file_path)

        else:
            with open(vhdl_file_path, "w") as f:
                f.write(vhdl_code)
            print("VHDL Model successfully generated at ", vhdl_file_path)

        with open(vhdl_file_HDLGen_path, "w") as f:
            f.write(vhdl_code)

        print("VHDL HDLGen Model successfully generated at ", vhdl_file_HDLGen_path)
        self.entity_name = entity_name
        return overwrite


    def create_tcl_file(self, lang):
        print("creating tcl")

        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        if lang == "VHDL":
            vhdl_path = proj_path + "/VHDL/model/" + self.entity_name + ".vhd"
            self.tcl_path = proj_path + "/VHDL/AMDPrj/" + self.entity_name + ".tcl"
            ext = "vhd"
        else:
            vhdl_path = proj_path + "/Verilog/model/" + self.entity_name + ".v"
            self.tcl_path = proj_path + "/Verilog/AMDPrj/" + self.entity_name + ".tcl"
            ext = "v"
        tcl_database_path = "./Generator/TCL_Database/tcl_database.xml"

        tcl_database = minidom.parse(tcl_database_path)
        tcl_root = tcl_database.documentElement

        tcl_file_template = tcl_root.getElementsByTagName("vivado_vhdl_tcl")[0]
        tcl_file_template = tcl_file_template.firstChild.data
        comp = self.entity_name
        tb_file_name = self.entity_name + "_TB"
        tcl_vivado_code = tcl_file_template.replace("$tcl_path", self.tcl_path)
        tcl_vivado_code = tcl_vivado_code.replace("$comp_name", comp)
        wd = os.getcwd()
        wd = wd.replace("\\","/")
        mainPackagePath = "add_files -norecurse  "+ wd
        mainPackagePath = mainPackagePath.replace("Application","Package/mainPackage.vhd")
        if self.includeArrays == True:
            tcl_vivado_code = tcl_vivado_code.replace("$arrayPackage", mainPackagePath)
        else:
            tcl_vivado_code = tcl_vivado_code.replace("$arrayPackage","")
        files=""
        mainPackageDir = os.getcwd() + "\HDLDesigner\Package\mainPackage.hdlgen"
        root = minidom.parse(mainPackageDir)
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
        mainPackage = hdlDesign[0].getElementsByTagName("mainPackage")
        components = hdlDesign[0].getElementsByTagName("components")
        comp_nodes = components[0].getElementsByTagName('component')
        for i in range(0, len(comp_nodes)):
            #if comp_nodes[i].getElementsByTagName('model')[0].firstChild.data in instances:
            dir = comp_nodes[i].getElementsByTagName('dir')[0].firstChild.data
            self.dirs.append(dir)
        if self.dirs is not None:
            for dir in self.dirs:
                files += "add_files -norecurse  "+ dir + " \n"
            tcl_vivado_code = tcl_vivado_code.replace("$files", files)
        else:
            tcl_vivado_code = tcl_vivado_code.replace("$files", "")
        tcl_vivado_code = tcl_vivado_code.replace("$tb_name", tb_file_name)
        tcl_vivado_code = tcl_vivado_code.replace("$proj_name", proj_name)
        proj_path = "{" + proj_path + "}"
        tcl_vivado_code = tcl_vivado_code.replace("$proj_dir", proj_path)
        tcl_vivado_code = tcl_vivado_code.replace("$lang", lang)
        tcl_vivado_code = tcl_vivado_code.replace("$ext", ext)


        # Writing xml file
        with open(self.tcl_path, "w") as f:
            f.write(tcl_vivado_code)

        print("TCL file successfully generated at ", self.tcl_path)

        return 1

    def run_tcl_file(self, lang):

        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        subprocess.Popen("cd " + proj_path, shell=True)
        vivado_bat_file_path = ProjectManager.get_vivado_bat_path()

        if lang == "VHDL":
            tcl_path=proj_path+"\VHDL\AMDprj\\"+str(ProjectManager.get_proj_name())+".tcl"

        elif lang == "Verilog":

            tcl_path = proj_path + "\Verilog\AMDprj\\" + str(ProjectManager.get_proj_name()) + ".tcl"
        if os.path.exists(tcl_path):
            start_vivado_cmd = vivado_bat_file_path + " -source " + tcl_path
            subprocess.Popen(start_vivado_cmd, shell=True)
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("Please Generate model and TB HDL")
            msgBox.exec_()

    def create_vhdl_testbench_code(self):
        tb_code = ""
        clkrst = 0
        xml_data_path = ProjectManager.get_xml_data_path()

        vhdl_tb_database_path = "./Generator/TB_Database/vhdl_tb_database.xml"

        wcfg_database_path = "./Generator/WCFG_Database/wcfg_database.xml"

        # Parsing the xml file
        project_data = minidom.parse(xml_data_path)
        HDLGen = project_data.documentElement

        vhdl_tb_database = minidom.parse(vhdl_tb_database_path)
        vhdl_root = vhdl_tb_database.documentElement

        hdl_design = HDLGen.getElementsByTagName("hdlDesign")
        wcfg = ""
        #TB = ""
        UUTEnt = ""
        header_node = hdl_design[0].getElementsByTagName("header")
        comp_node = header_node[0].getElementsByTagName("compName")[0]
        entity_name = comp_node.firstChild.data

        with open(wcfg_database_path, "r") as f:
            xml_string = f.read()

        head_regex = r"<head>(.*?)</head>"
        head_contents = re.search(head_regex, xml_string, re.DOTALL).group(1)

        #TB_regex = r"<TB>(.*?)</TB>"
        #B_contents = re.search(TB_regex, xml_string, re.DOTALL).group(1)

        UUT_regex = r"<UUT>(.*?)</UUT>"
        UUT_contents = re.search(UUT_regex, xml_string, re.DOTALL).group(1)

        UUTEnt_regex = r"<UUTEnt>(.*?)</UUTEnt>"
        UUTEnt_contents = re.search(UUTEnt_regex, xml_string, re.DOTALL).group(1)
        end_regex = r"<end>(.*?)</end>"
        end_contents = re.search(end_regex, xml_string, re.DOTALL).group(1)
        head_contents = re.sub(r"\[componentName]", entity_name, head_contents)
        wcfg += head_contents

        # Entity Section
        inputArray = []
        arrayPackage=False
        gen_signals = ""
        sig_decl = "-- testbench signal declarations\n"
        sig_decl += "signal testNo: integer; -- aids locating test in simulation waveform\n"
        sig_decl += "signal endOfSim : boolean := false; -- assert at end of simulation to highlight simuation done. Stops clk signal generation.\n\n"
        sig_decl += "-- Typically use the same signal names as in the VHDL entity, with keyword signal added, and without in/out mode keyword\n"
        io_signals = ""
        entity_signal_description = ""
        io_port_node = hdl_design[0].getElementsByTagName("entityIOPorts")
        gen_entity = ""
        io_port_map = ""
        inputsToZero = ""
        inputsToOne = ""
        other_signals = ""
        control_signals = ""
        if len(io_port_node) != 0 and io_port_node[0].firstChild is not None:

            for signal in io_port_node[0].getElementsByTagName('signal'):
                signal_declare_syntax = vhdl_root.getElementsByTagName("signalDeclaration")[0].firstChild.data
                io_signal_declare_syntax = vhdl_root.getElementsByTagName("IOSignalDeclaration")[0].firstChild.data
                io_port_map_syntax = vhdl_root.getElementsByTagName("portMap")[0].firstChild.data
                signal_declare_syntax = signal_declare_syntax.replace("$sig_name",
                                                                      signal.getElementsByTagName('name')[
                                                                          0].firstChild.data)
                io_port_map_syntax = io_port_map_syntax.replace("$sig_name",
                                                                      signal.getElementsByTagName('name')[
                                                                          0].firstChild.data)
                io_signal_declare_syntax = io_signal_declare_syntax.replace("$sig_name",
                                                                      signal.getElementsByTagName('name')[
                                                                          0].firstChild.data)
                signal_declare_syntax = signal_declare_syntax.replace("$mode",
                                                                      signal.getElementsByTagName('mode')[
                                                                          0].firstChild.data)
                type = signal.getElementsByTagName('type')[0].firstChild.data
                if type == "single bit":
                    type = "std_logic"
                elif type[0:3] == "bus":
                    type = type.replace("bus","std_logic_vector")
                
                signal_declare_syntax = signal_declare_syntax.replace("$type", type)
                io_signal_declare_syntax = io_signal_declare_syntax.replace("$type", type)
                name = signal.getElementsByTagName('name')[0].firstChild.data
                type = signal.getElementsByTagName('type')[0].firstChild.data
                size = ""
                #TB_content = re.sub(r"\[componentName]", entity_name, TB_contents)
                #TB_content = re.sub(r"\[signal]", name, TB_content)
                UUTEnt_content = re.sub(r"\[componentName]", entity_name, UUTEnt_contents)
                UUTEnt_content = re.sub(r"\[signal]", name, UUTEnt_content)

                if type[0:5] == "array":
                    size = ""
                    type = "array"
                elif type == "single bit":
                    size = ""
                    type = "logic"
                elif type[0:3] == "bus":
                    digits_list = re.findall(r'\d+', type)
                    size = "[" + str(digits_list[0]) + ":" + str(digits_list[1]) + "]"
                    type = "array"
                elif type[0:8] == "unsigned":
                    digits_list = re.findall(r'\d+', type)
                    size = "[" + str(digits_list[0]) + ":" + str(digits_list[1]) + "]"
                    type = "array"
                elif type[0:6] == "signed":
                    digits_list = re.findall(r'\d+', type)
                    size = "[" + str(digits_list[0]) + ":" + str(digits_list[1]) + "]"
                    type = "array"
                #TB_content = re.sub(r"\[type]", type, TB_content)
                #TB_content = re.sub(r"\[size]", size, TB_content)
                #TB += TB_content
                UUTEnt_content = re.sub(r"\[type]", type, UUTEnt_content)
                UUTEnt_content = re.sub(r"\[size]", size, UUTEnt_content)
                UUTEnt += UUTEnt_content

                if signal.getElementsByTagName('mode')[0].firstChild.data == "in":
                    if signal.getElementsByTagName('name')[0].firstChild.data != "clk" and signal.getElementsByTagName('name')[0].firstChild.data != "rst":
                        if signal.getElementsByTagName('type')[0].firstChild.data == "single bit":
                            inputArray.append(signal.getElementsByTagName('name')[0].firstChild.data)
                            inputsToZero += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " <= \'0\';\n"
                            inputsToOne += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " <= \'1\';\n"
                        elif signal.getElementsByTagName('type')[0].firstChild.data[0:3] == "bus":
                            inputsToZero += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " <= (others => \'0\');\n"
                            inputsToOne += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " <= (others => \'1\');\n"
                        else:
                            inputsToZero += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " <= (others =>(others => \'0\'));\n"
                            arrayPackage=True
                else:
                    if signal.getElementsByTagName('type')[0].firstChild.data != "single bit" and signal.getElementsByTagName('type')[0].firstChild.data[0:3] != "bus":
                        arrayPackage = True
                signal_description = signal.getElementsByTagName('description')[
                    0].firstChild.data
                entity_signal_description += "-- " + signal.getElementsByTagName('name')[
                    0].firstChild.data + "\t" + signal_description + "\n"
                gen_signals += "\t" + signal_declare_syntax + "\n"
                io_port_map += "\t" + io_port_map_syntax + "\n"
                if signal.getElementsByTagName('name')[0].firstChild.data == "clk" or signal.getElementsByTagName('name')[0].firstChild.data == "rst":
                    clkrst=clkrst+1
                else:
                    io_signals += io_signal_declare_syntax + "\n"
            #wcfg += TB
            wcfg += UUT_contents
            wcfg += UUTEnt
            io_port_map = io_port_map.rstrip()
            io_port_map = io_port_map[0:-1]
            io_signals = io_signals.rstrip()
            other_signals = ""
            if clkrst > 0:
                other_signals = "signal clk: std_logic := '1';\n"
            if clkrst == 2:
                other_signals += "signal rst: std_logic;        \n"

            control_signals = "constant period: time := 20 ns; -- Default simulation time. Use as simulation delay constant, or clk period if sequential model ((50MHz clk here)\n"

            gen_signals = gen_signals.rstrip()
            gen_signals = gen_signals[0:-1]

            entity_syntax = vhdl_root.getElementsByTagName("entity")
            gen_entity = "-- Testbench entity declaration. No inputs or outputs\n"
            gen_entity += entity_syntax[0].firstChild.data
            UUTInternal = "\t</wvobject>"
            # Internal signals
            int_sig_node = hdl_design[0].getElementsByTagName("internalSignals")
            if int_sig_node[0].firstChild is not None:
                UUTInternal = ""
                UUTInt_regex = r"<UUTInt>(.*?)</UUTInt>"
                UUTInt_contents = re.search(UUTInt_regex, xml_string, re.DOTALL).group(1)
                wcfg += UUTInt_contents
                UUTInternal_regex = r"<UUTInternal>(.*?)</UUTInternal>"
                UUTInternal_contents = re.search(UUTInternal_regex, xml_string, re.DOTALL).group(1)
                for signal in int_sig_node[0].getElementsByTagName("signal"):
                    name = signal.getElementsByTagName('name')[0].firstChild.data
                    type = signal.getElementsByTagName('type')[0].firstChild.data
                    UUTInternal_content = re.sub(r"\[componentName]", entity_name, UUTInternal_contents)
                    UUTInternal_content = re.sub(r"\[signal]", name, UUTInternal_content)
                    if type == "Enumerated type state signal pair(NS/CS)":
                        type = "logic"
                        size=""
                    elif type == "single bit":
                        size = ""
                        type = "logic"
                    elif type[0:5] == "array":
                        self.includeArrays = True
                        digits_list = re.findall(r'\d+', type)
                        size = "[" + str(digits_list[0]) + ":" + str(digits_list[1]) + "]"
                        type = "array"
                    elif type[0:3] == "bus":
                        digits_list = re.findall(r'\d+', type)
                        size = "[" + str(digits_list[0]) + ":" + str(digits_list[1]) + "]"
                        type = "array"
                    elif type[0:8] == "unsigned":
                        digits_list = re.findall(r'\d+', type)
                        size = "[" + str(digits_list[0]) + ":" + str(digits_list[1]) + "]"
                        type = "array"
                    elif type[0:6] == "signed":
                        digits_list = re.findall(r'\d+', type)
                        size = "[" + str(digits_list[0]) + ":" + str(digits_list[1]) + "]"
                        type = "array"
                    UUTInternal_content = re.sub(r"\[type]", type, UUTInternal_content)
                    UUTInternal_content = re.sub(r"\[size]", size, UUTInternal_content)
                    UUTInternal += UUTInternal_content
                UUTInternal += "\t</wvobject>"
            wcfg += UUTInternal
            wcfg = wcfg.strip()
            wcfg += end_contents

        # Header Section

        header_node = hdl_design[0].getElementsByTagName("header")
        if header_node is not None:
            comp_node = header_node[0].getElementsByTagName("compName")[0]
            if comp_node.firstChild.data != "null":
                entity_name = comp_node.firstChild.data

                gen_header = "-- Header Section\n"
                gen_header += "-- VHDL testbench "+ entity_name +"_TB\n"
                gen_header += "-- Generated by HDLGen, Github https://github.com/abishek-bupathi/HDLGen\n"
                gen_header +="-- Reference: https://tinyurl.com/vicilogicVHDLTips \n\n"
                gen_header += "-- Component Name : " + entity_name + "\n"
                title = header_node[0].getElementsByTagName("title")[0].firstChild.data
                gen_header += "-- Title          : " + (title if title != "null" else "") + "\n"
                gen_header += "-- Description    : refer to component hdl model fro function description and signal dictionary\n"
                authors = header_node[0].getElementsByTagName("authors")[0].firstChild.data
                gen_header += "-- Author(s)      : " + (authors if authors != "null" else "") + "\n"
                company = header_node[0].getElementsByTagName("company")[0].firstChild.data
                gen_header += "-- Company        : " + (company if company != "null" else "") + "\n"
                email = header_node[0].getElementsByTagName("email")[0].firstChild.data
                gen_header += "-- Email          : " + (email if email != "null" else "") + "\n"
                gen_header += "-- Date           : " + header_node[0].getElementsByTagName("date")[
                    0].firstChild.data + "\n\n"

                tb_code += gen_header
                # Libraries Section

                libraries_node = vhdl_root.getElementsByTagName("libraries")
                libraries = libraries_node[0].getElementsByTagName("library")
                gen_library = "-- library declarations\n"
                for library in libraries:
                    gen_library += library.firstChild.data + "\n"
                if arrayPackage == True:
                    gen_library += "use work.MainPackage.all;"
                gen_library += "\n"
                tb_code += gen_library

                # Entity declaration
                gen_entity = gen_entity.replace("$comp_name", entity_name)
                tb_code += gen_entity +"\n\n"
                tbSignalDeclaration=""
                if sig_decl != "":
                    tbSignalDeclaration += sig_decl +"\n"
                if other_signals != "":
                    tbSignalDeclaration += other_signals +"\n"
                tbSignalDeclaration += io_signals + "\n\n" + control_signals
                # Architecture section

                # Process
                arch_node = hdl_design[0].getElementsByTagName("architecture")
                gen_process = ""
                if clkrst > 0:
                    gen_process += "-- Generate clk signal, when endOfSim = FALSE / 0\n"
                    gen_process += "clkStim: clk <= not clk after period/2 when endOfSim = false else '0';\n\n"
                gen_process += "-- instantiate unit under test (UUT)\n"
                gen_process += "UUT: "+entity_name+ "-- map component internal sigs => testbench signals\n"
                gen_process += "port map\n\t(\n"
                gen_process += io_port_map+"\n\t);\n\n"
                gen_process += "-- Signal stimulus process\n"
                gen_process += "stim_p: process -- process sensitivity list is empty, so process automatically executes at start of simulation. Suspend process at the wait; statement\n"
                gen_process += "begin\n"
                gen_process += "\treport \"%N Simulation start, time = \"& time'image(now);\n\n"
                gen_process += "\t-- Apply default INPUT signal values. Do not assign output signals (generated by the UUT) in this stim_p process\n"
                gen_process += "\t-- Each stimulus signal change occurs 0.2*period after the active low-to-high clk edge\n"
                gen_process += "\t-- if signal type is\n\t-- std_logic, use '0'\n\t-- std_logic_vector use (others => '0')\n\t-- integer use 0\n"
                gen_process += inputsToZero

                if clkrst == 2:
                    gen_process += "\treport \"Assert and toggle rst\";\n\ttestNo <= 0;\n\trst    <= '1';\n"
                    gen_process += "\twait for period*1.2; -- assert rst for 1.2*period, deasserting rst 0.2*period after active clk edge\n"
                    gen_process += "\trst   <= '0';\n\twait for period; -- wait 1 clock period\n\t"#-- <delete (End)\n\n"
                gen_process += "\n\t-- manually added code START\n"
                gen_process += "\t-- include testbench stimulus sequence here. Use new testNo for each test set\n"
                gen_process += "\t-- individual tests. Generate input signal combinations and wait for period.\n"
                gen_process += "\ttestNo <= 1;\n"
                gen_process += "\twait for 3*period;\n"
                gen_process += "\t-- manually added code END\n\n"
                gen_process += "\t-- Print picosecond (ps) = 1000*ns (nanosecond) time to simulation transcript\n"
                gen_process += "\t-- Use to find time when simulation ends (endOfSim is TRUE)\n"
                gen_process += "\t-- Re-run the simulation for this time\n"
                gen_process += "\t-- Select timing diagram and use View>Zoom Fit\n"
                gen_process += "\treport \"%N Simulation end, time = \"& time'image(now);\n"
                gen_process += "\tendOfSim <= TRUE; -- assert flag to stop clk signal generation\n\n"
                gen_process += "\twait; -- wait forever\n"
                if len(arch_node) != 0 and arch_node[0].firstChild is not None:
                    arch_syntax = vhdl_root.getElementsByTagName("architecture")[0].firstChild.data

                    gen_arch = arch_syntax.replace("$comp_name", entity_name)
                    gen_arch = gen_arch.replace("$component_declarations", "-- unit under test (UUT) component declaration. Identical to component entity, with 'entity' replaced with 'component'")
                    gen_arch = gen_arch.replace("$port", gen_signals)
                    gen_arch = gen_arch.replace("$tbSignalDeclaration", tbSignalDeclaration)
                    gen_arch = gen_arch.replace("$arch_elements", gen_process[:-1])

                    tb_code += gen_arch
        return entity_name, tb_code, wcfg

    def create_testbench_file(self, overwrite):
        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)

        entity_name, vhdl_tb_code, waveform = self.create_vhdl_testbench_code()

        vhdl_tb_path = os.path.join(proj_path, "VHDL", "testbench", self.entity_name + "_TB.vhd")
        vhdl_tb_HDLGen_path = os.path.join(proj_path, "VHDL", "testbench", self.entity_name + "_HDLGen_TB.vhd")
        waveform_path = os.path.join(proj_path, "VHDL", "AMDprj", self.entity_name + "_TB_behav.wcfg")

        if os.path.exists(vhdl_tb_path) == False:
            with open(vhdl_tb_path, "w") as f:
                f.write(vhdl_tb_code)
            print("VHDL Testbench file successfully generated at ", vhdl_tb_path)

        if overwrite == True:
            # Writing xml file
            with open(vhdl_tb_path, "w") as f:
                f.write(vhdl_tb_code)

            print("VHDL Testbench file successfully generated at ", vhdl_tb_path)
        with open(vhdl_tb_HDLGen_path, "w") as f:
            f.write(vhdl_tb_code)
        print("VHDL Testbench HDLGen file successfully generated at ", vhdl_tb_HDLGen_path)

        with open(waveform_path, "w") as f:
            f.write(waveform)
    def generate_mainPackage(self):
        gen_arrays =""
        comp = ""
        vhdl_database_path = "./Generator/HDL_Database/vhdl_database.xml"
        # Parsing the xml file
        vhdl_database = minidom.parse(vhdl_database_path)
        vhdl_root = vhdl_database.documentElement
        mainPackageDir = os.getcwd() + "\HDLDesigner\Package\mainPackage.hdlgen"
        root = minidom.parse(mainPackageDir)
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
        mainPackage = hdlDesign[0].getElementsByTagName("mainPackage")
        array_nodes = mainPackage[0].getElementsByTagName('array')
        components = hdlDesign[0].getElementsByTagName("components")
        comp_nodes = components[0].getElementsByTagName('component')
        for i in range(0, len(array_nodes)):
            name = array_nodes[i].getElementsByTagName('name')[0].firstChild.data
            depth = array_nodes[i].getElementsByTagName('depth')[0].firstChild.data
            width = array_nodes[i].getElementsByTagName('width')[0].firstChild.data
            sigType = array_nodes[i].getElementsByTagName('signalType')[0].firstChild.data

            gen_arrayType_syntax = vhdl_root.getElementsByTagName("arrayType")[0].firstChild.data
            gen_arrayType_syntax = gen_arrayType_syntax.replace("$arrayName", name)
            gen_arrayType_syntax = gen_arrayType_syntax.replace("$signalType", sigType)
            gen_arrayType_syntax = gen_arrayType_syntax.replace("$arraySize", depth)
            gen_arrayType_syntax = gen_arrayType_syntax.replace("$arrayLength", width)
            gen_arrays += gen_arrayType_syntax
        for i in range(0, len(comp_nodes)):
            model = comp_nodes[i].getElementsByTagName('model')[0].firstChild.data
            dir = comp_nodes[i].getElementsByTagName('dir')[0].firstChild.data
            ports=""
            for port_signal in comp_nodes[i].getElementsByTagName("port"):
                signals = port_signal.firstChild.data.split(",")
                gen_compType_assign_syntax = vhdl_root.getElementsByTagName("signalDeclaration")[0].firstChild.data
                gen_compType_assign_syntax = gen_compType_assign_syntax.replace("$sig_name", signals[0])
                gen_compType_assign_syntax = gen_compType_assign_syntax.replace("$mode", signals[1])
                gen_compType_assign_syntax = gen_compType_assign_syntax.replace("$type", signals[2])
                ports += "\t" + gen_compType_assign_syntax + "\n"
            ports = ports.rstrip()
            ports = ports[0:-1]
            #signals = comp_nodes[i].getElementsByTagName('SignalName')[0].firstChild.data
            gen_compType_syntax = vhdl_root.getElementsByTagName("component")[0].firstChild.data
            gen_compType_syntax = gen_compType_syntax.replace("$model",model)
            gen_compType_syntax = gen_compType_syntax.replace("$ports", ports)
            comp += gen_compType_syntax + "\n"

        array_vhdl_code = vhdl_root.getElementsByTagName("arrayPackage")[0].firstChild.data
        array_vhdl_code = array_vhdl_code.replace("$arrays", gen_arrays)

        array_vhdl_code = array_vhdl_code.replace("$Component", comp)
        # Creating arrayPackage file
        array_vhdl_file_path = os.getcwd()
        array_vhdl_file_path = array_vhdl_file_path.replace("Application","Package\MainPackage.vhd",)
        print(array_vhdl_file_path)
        # Write array code to file
        with open(array_vhdl_file_path, "w") as f:
            f.write(array_vhdl_code)

    def generate_verilog(self):
        gen_verilog = ""

        xml_data_path = ProjectManager.get_xml_data_path()

        verilog_database_path = "./Generator/HDL_Database/verilog_database.xml"

        # Parsing the xml file
        project_data = minidom.parse(xml_data_path)
        HDLGen = project_data.documentElement

        verilog_database = minidom.parse(verilog_database_path)
        verilog_root = verilog_database.documentElement

        hdl_design = HDLGen.getElementsByTagName("hdlDesign")
        stateTypesList = ""
        entity_name = ""
        gen_int_sig = ""
        gen_internal_signal_result = ""
        arrayList=[]
        single_bitList=[]
        busList=[]
        unsignedList=[]
        signedList=[]
        # Entity Section
        gen_signals = ""
        port_signals = ""
        output_reg_signals = ""
        entity_signal_description = ""
        io_port_node = hdl_design[0].getElementsByTagName("entityIOPorts")
        gen_entity = ""
        self.includeArrays = False
        portSignals=[]
        internalSignals=[]

        stateTypeSig = False
        if len(io_port_node) != 0 and io_port_node[0].firstChild is not None:

            for signal in io_port_node[0].getElementsByTagName('signal'):
                name = signal.getElementsByTagName('name')[0].firstChild.data
                type = signal.getElementsByTagName('type')[0].firstChild.data
                mode = signal.getElementsByTagName('mode')[0].firstChild.data

                portData=[name,type,mode]
                portSignals.append(portData)
                if type[0:5] == "array":
                    self.includeArrays = True
                    arrayList.append(name)
                elif type == "single bit":
                    single_bitList.append(name)
                    type = ""
                elif type[0:3] == "bus":
                    busList.append(name)
                    digits_list = re.findall(r'\d+', type)
                    type = "[" + str(digits_list[0]) + ":" + str(digits_list[1]) + "]"
                elif type[0:8] == "unsigned":
                    unsignedList.append(name)
                    digits_list = re.findall(r'\d+', type)
                    type = "[" + str(digits_list[0]) + ":" + str(digits_list[1]) + "]"
                elif type[0:6] == "signed":
                    signedList.append(name)
                    digits_list = re.findall(r'\d+', type)
                    type = "[" + str(digits_list[0]) + ":" + str(digits_list[1]) + "]"
                port_declare_syntax = verilog_root.getElementsByTagName("portDeclaration")[0].firstChild.data

                port_declare_syntax = port_declare_syntax.replace("$name", name)
                port_declare_syntax = port_declare_syntax.replace("$size", type)
                port_declare_syntax = port_declare_syntax.replace("$mode", mode)

                if mode == "out":
                    reg_syntax = verilog_root.getElementsByTagName("intSigDeclaration")[0].firstChild.data
                    reg_syntax = reg_syntax.replace("$int_sig_name", name)
                    reg_syntax = reg_syntax.replace("$int_sig_type", type)
                    output_reg_signals += reg_syntax + "\n"

                signal_declare_syntax = verilog_root.getElementsByTagName("signalDeclaration")[0].firstChild.data

                signal_declare_syntax = signal_declare_syntax.replace("$sig_name",
                                                                      signal.getElementsByTagName('name')[
                                                                          0].firstChild.data)
                signal_description = signal.getElementsByTagName('description')[
                    0].firstChild.data
                signal_description = signal_description.replace("&#10;", "\n// ")
                entity_signal_description += "// " + signal.getElementsByTagName('name')[
                    0].firstChild.data + "\t" + signal_description + "\n"
                gen_signals += "\t\t" + signal_declare_syntax + ",\n"
                port_signals += "\t" + port_declare_syntax + "\n"
            port_signals = port_signals.rstrip()
            gen_signals = gen_signals.rstrip()
            gen_signals = gen_signals[0:-1]

            entity_syntax = verilog_root.getElementsByTagName("module")
            gen_entity = "// module declaration\n"
            gen_entity += entity_syntax[0].firstChild.data

            gen_entity = gen_entity.replace("$signals", gen_signals)
            port_def = "\t// Port definitions\n"
            port_def += port_signals

            gen_entity = gen_entity.replace("$portDef", port_def)
            gen_int_sig = output_reg_signals + "\n"
            # Internal signals
            gen_int_sig += "// Internal signal declarations"

            int_sig_node = hdl_design[0].getElementsByTagName("internalSignals")

            if int_sig_node[0].firstChild is not None:
                stateTypesString = ""

                stateTypesList = int_sig_node[0].getElementsByTagName("stateTypes")
                stateSize = len(stateTypesList)-1
                binaryStateSize = bin(stateSize)
                binaryStateSize = len(binaryStateSize)-2
                number = 0
                for stateType in int_sig_node[0].getElementsByTagName("stateTypes"):
                    stateTypesString += stateType.firstChild.data + ", "
                    stateType_syntax = verilog_root.getElementsByTagName("stateNamesDeclarations")[0].firstChild.data
                    stateType_syntax = stateType_syntax.replace("$stateName", stateType.firstChild.data)
                    num = bin(number)[2:]
                    num = num.zfill(binaryStateSize)
                    stateType_syntax = stateType_syntax.replace("$bits", str(binaryStateSize)+"'b"+num)
                    number = number + 1
                    gen_int_sig += "\n" + stateType_syntax
                stateTypesString = stateTypesString[:-2]

                for signal in int_sig_node[0].getElementsByTagName("signal"):
                    name = signal.getElementsByTagName('name')[0].firstChild.data
                    type = signal.getElementsByTagName('type')[0].firstChild.data
                    internalData = [name, type]
                    internalSignals.append(internalData)
                    if type == "Enumerated type state signal pair(NS/CS)":
                        type = ""
                        if name[0:2] == "CS":
                            stateTypeSig = True
                            CSState = name
                    elif type == "single bit":
                        single_bitList.append(name)
                        type = ""
                    elif type[0:5] == "array":
                        self.includeArrays = True
                        arrayList.append(name)
                    elif type[0:3] == "bus":
                        busList.append(name)
                        digits_list = re.findall(r'\d+', type)
                        type ="["+str(digits_list[0])+":"+str(digits_list[1])+"]"
                    elif type[0:8] == "unsigned":
                        unsignedList.append(name)
                        digits_list = re.findall(r'\d+', type)
                        type = "[" + str(digits_list[0]) + ":" + str(digits_list[1]) + "]"
                    elif type[0:6] == "signed":
                        signedList.append(name)
                        digits_list = re.findall(r'\d+', type)
                        type = "[" + str(digits_list[0]) + ":" + str(digits_list[1]) + "]"
                    int_sig_syntax = verilog_root.getElementsByTagName("intSigDeclaration")[0].firstChild.data
                    int_sig_syntax = int_sig_syntax.replace("$int_sig_name", name)
                    int_sig_syntax = int_sig_syntax.replace("$int_sig_type", type)
                    int_signal_description = signal.getElementsByTagName('description')[
                        0].firstChild.data
                    int_signal_description = int_signal_description.replace("&#10;", "\n// ")

                    gen_int_sig += "\n" + int_sig_syntax
                    gen_internal_signal_result += "// " + signal.getElementsByTagName('name')[
                        0].firstChild.data + "\t" + int_signal_description + "\n"

                gen_int_sig.rstrip()

            else:
                gen_int_sig += "\n// None"
                gen_internal_signal_result = "// None\n"

        # Header Section
        header_node = hdl_design[0].getElementsByTagName("header")
        if header_node is not None:
            comp_node = header_node[0].getElementsByTagName("compName")[0]
            if comp_node.firstChild.data != "null":
                entity_name = comp_node.firstChild.data

                gen_header = "// Header Section\n"
                gen_header += "// Generated by HDLGen, Github https://github.com/abishek-bupathi/HDLGen\n// Reference: https://tinyurl.com/VHDLTips\n\n"
                gen_header += "// Component Name : " + entity_name + "\n"
                title = header_node[0].getElementsByTagName("title")[0].firstChild.data
                gen_header += "// Title          : " + (title if title != "null" else "") + "\n\n"
                desc = header_node[0].getElementsByTagName("description")[0].firstChild.data
                desc = desc.replace("&#10;", "\n// ")
                gen_header += "// Description\n// "
                gen_header += (desc if desc != "null" else "") + "\n"
                authors = header_node[0].getElementsByTagName("authors")[0].firstChild.data
                gen_header += "\n// Author(s)      : " + (authors if authors != "null" else "") + "\n"
                company = header_node[0].getElementsByTagName("company")[0].firstChild.data
                gen_header += "// Company        : " + (company if company != "null" else "") + "\n"
                email = header_node[0].getElementsByTagName("email")[0].firstChild.data
                gen_header += "// Email          : " + (email if email != "null" else "") + "\n"
                gen_header += "// Date           : " + header_node[0].getElementsByTagName("date")[
                    0].firstChild.data + "\n\n"

                gen_verilog += gen_header

                # entity signal dictionary
                gen_entity = gen_entity.replace("$comp_name", entity_name)
                gen_entity_signal = "// entity signal dictionary\n"
                gen_entity_signal += entity_signal_description + "\n"
                gen_verilog += gen_entity_signal

                # internal signal dictionary
                gen_internal_signal = "// internal signal dictionary\n"
                gen_internal_signal_result = gen_internal_signal_result + "\n"
                gen_internal_signal += gen_internal_signal_result
                gen_verilog += gen_internal_signal

                # Process
                arch_node = hdl_design[0].getElementsByTagName("architecture")
                gen_process = ""
                clkAndRst = hdl_design[0].getElementsByTagName('clkAndRst')
                if len(arch_node) != 0 and arch_node[0].firstChild is not None:

                    child = arch_node[0].firstChild

                    while child is not None:

                        next = child.nextSibling

                        if (child.nodeType == arch_node[0].ELEMENT_NODE and child.tagName == "process"):
                            process_syntax = verilog_root.getElementsByTagName("process")[0].firstChild.data
                            gen_in_sig = ""
                            gen_defaults = ""
                            if_gen_defaults = ""
                            clkgen_defaults = ""
                            caseEmpty = True
                            for default_out in child.getElementsByTagName("defaultOutput"):
                                assign_syntax = verilog_root.getElementsByTagName("processAssign")[0].firstChild.data
                                signals = default_out.firstChild.data.split(",")
                                assign_syntax = assign_syntax.replace("$output_signal", signals[0])
                                value = signals[1]
                                if value == "rst state":
                                    if stateTypesList != "":
                                        stateNames = stateTypesString.split(",")
                                        value = stateNames[0]
                                elif value == "zero":
                                    if signals[0] in arrayList:
                                        value = "(others =>(others => '0'))"
                                    elif signals[0] in single_bitList:
                                        value = "1'b0"
                                    elif signals[0] in busList or signals[0] in signedList or signals[0] in unsignedList:
                                        for signal in portSignals:
                                            if signals[0] == signal[0]:
                                                match = re.search(r'\((\d+)\sdownto\s(\d+)\)', signal[1])
                                                start = int(match.group(1))
                                                end = int(match.group(2))
                                                size = start - end + 1
                                                #size = signal[1]
                                                #size = int(size[4]) + 1
                                        for signal in internalSignals:
                                            if signals[0] == signal[0]:
                                                match = re.search(r'\((\d+)\sdownto\s(\d+)\)', signal[1])
                                                start = int(match.group(1))
                                                end = int(match.group(2))
                                                size = start - end + 1
                                                #size = signal[1]
                                                #size = int(size[4]) + 1
                                        value = str(size) + "'b0"
                                    else:
                                        value = str(0)
                                elif value.isdigit():
                                    size = len(value)
                                    value = str(size) + "'b" + value

                                elif stateTypeSig == True and value == CSState:
                                    caseEmpty = False
                                    case_syntax = verilog_root.getElementsByTagName("case")[0].firstChild.data
                                    case_syntax = case_syntax.replace("$stateType", value)
                                    stateNames = stateTypesString.split(",")
                                    whenCase = ""
                                    for states in stateNames:
                                        whenCase += "\n\t\t" + states + " :" + "\n\t\t\tbegin\n\n\t\t\tend"
                                    case_syntax = case_syntax.replace("$whenCase", whenCase)

                                assign_syntax = assign_syntax.replace("$value", value)
                                if_gen_defaults += "\n\t\t" + assign_syntax + "\n"
                                gen_defaults += "\n\t"+assign_syntax + " // default assignment"
                                if len(signals) == 3:
                                    clkAssign_syntax = verilog_root.getElementsByTagName("processAssign")[0].firstChild.data
                                    clkAssign_syntax = clkAssign_syntax.replace("$output_signal", signals[0])
                                    clkAssign_syntax = clkAssign_syntax.replace("$value", signals[2])
                                    clkgen_defaults += "\n\t\t" + clkAssign_syntax
                            if gen_defaults != "":
                                if clkgen_defaults != "":
                                    for clkRst in clkAndRst[0].getElementsByTagName("clkAndRst"):
                                        clkEdge = "posedge"
                                        if clkRst.getElementsByTagName('activeClkEdge')[0].firstChild.data == "H-L":
                                            clkEdge = "negedge"
                                        if clkRst.getElementsByTagName('rst')[0].firstChild.data == "Yes":
                                            if_syntax = verilog_root.getElementsByTagName("ifStatement")[0].firstChild.data
                                            if_syntax = if_syntax.replace("$assignment", "rst")
                                            rstlvl="posedge"
                                            if clkRst.getElementsByTagName('ActiveRstLvl')[0].firstChild.data == '0':
                                                rstlvl="negedge"
                                            if_syntax = if_syntax.replace("$default_assignments",
                                                                          if_gen_defaults)
                                            #if_gen_defaults = "\n\t" + if_syntax

                                            else_syntax = verilog_root.getElementsByTagName("elseStatement")[
                                                    0].firstChild.data
                                            else_syntax = else_syntax.replace("$default_assignments",
                                                                                  clkgen_defaults)
                                            if_syntax = if_syntax.replace("$else", else_syntax)
                                            clkgen_defaults = "\t" + if_syntax
                                        clkgen_defaults = clkgen_defaults.rstrip()
                                    process_syntax = process_syntax.replace("$default_assignments", clkgen_defaults)
                                else:
                                    if caseEmpty == False:
                                        gen_defaults += "\n" + case_syntax
                                    gen_defaults = gen_defaults.rstrip()
                                    process_syntax = process_syntax.replace("$default_assignments", gen_defaults)
                            for input_signal in child.getElementsByTagName("inputSignal"):
                                if input_signal.firstChild.data == "clk":
                                    gen_in_sig += clkEdge + " " + input_signal.firstChild.data + " or "
                                elif input_signal.firstChild.data == "rst":
                                    gen_in_sig += rstlvl + " " + input_signal.firstChild.data + " or "
                                else:
                                    gen_in_sig += input_signal.firstChild.data + " or "
                            gen_in_sig = gen_in_sig.strip()
                            gen_in_sig = gen_in_sig[:-2]

                            process_syntax = process_syntax.replace("$input_signals", gen_in_sig)
                            process_syntax = process_syntax.replace("$process_label",child.getElementsByTagName("label")[
                                                                        0].firstChild.data)
                            gen_process += process_syntax + "\n\n"


                        elif (child.nodeType == arch_node[0].ELEMENT_NODE and child.tagName == "concurrentStmt"):

                            gen_stmts = ""
                            conc_syntax = verilog_root.getElementsByTagName("concurrentstmt")[0].firstChild.data

                            conc_syntax = conc_syntax.replace("$concurrentstmt_label",
                                                              child.getElementsByTagName("label")[
                                                                  0].firstChild.data)

                            for statement in child.getElementsByTagName("statement"):
                                assign_syntax = verilog_root.getElementsByTagName("sigAssingn")[0].firstChild.data
                                signals = statement.firstChild.data.split(",")
                                assign_syntax = assign_syntax.replace("$output_signal", signals[0])
                                # find the signal and change it to wire
                                # Define the regular expression pattern with optional bit width specification
                                var_name = signals[0]
                                pattern = f"(reg)\s*(\[\s*\d+\s*:\s*\d+\s*\])?\s+({var_name})"

                                # Replace "reg" with "wire" in the matching line
                                gen_int_sig = re.sub(pattern, r"wire \2 \3", gen_int_sig)
                                value = signals[1]
                                if value.isdigit():
                                    size=len(value)
                                    value = str(size)+"'b" + value
                                elif value == "zero":
                                    if signals[0] in arrayList:
                                        value = "(others =>(others => '0'))"
                                    elif signals[0] in single_bitList:
                                        value = "1'b0"
                                    elif signals[0] in busList or signals[0] in signedList or signals[
                                        0] in unsignedList:
                                        for signal in portSignals:
                                            if signals[0] == signal[0]:
                                                match = re.search(r'\((\d+)\sdownto\s(\d+)\)', signal[1])
                                                start = int(match.group(1))
                                                end = int(match.group(2))
                                                size = start - end + 1
                                                #size = signal[1]
                                                #size = int(size[4]) + 1
                                        for signal in internalSignals:
                                            if signals[0] == signal[0]:
                                                match = re.search(r'\((\d+)\sdownto\s(\d+)\)', signal[1])
                                                start = int(match.group(1))
                                                end = int(match.group(2))
                                                size = start - end + 1
                                                #size = signal[1]
                                                #size = int(size[4])+1
                                        value = str(size)+"'b0"
                                    else:
                                        value = str(0)
                                assign_syntax = assign_syntax.replace("$value", value)

                                gen_stmts += assign_syntax

                            conc_syntax = conc_syntax.replace("$statement", gen_stmts)
                            gen_process += conc_syntax + "\n"

                        elif (child.nodeType == arch_node[0].ELEMENT_NODE and child.tagName == "instance"):
                            self.includeArrays = True
                            gen_stmts = ""

                            instance_syntax = verilog_root.getElementsByTagName("instance")[0].firstChild.data

                            instance_syntax = instance_syntax.replace("$instance_label",
                                                                      child.getElementsByTagName("label")[
                                                                          0].firstChild.data)
                            for instance in child.getElementsByTagName("port"):
                                assign_syntax = verilog_root.getElementsByTagName("portAssign")[0].firstChild.data
                                signals = instance.firstChild.data.split(",")
                                assign_syntax = assign_syntax.replace("$output_signal", signals[0])
                                assign_syntax = assign_syntax.replace("$value", signals[1])
                                var_name = signals[0]
                                pattern = f"(reg)\s*(\[\s*\d+\s*:\s*\d+\s*\])?\s+({var_name})"

                                # Replace "reg" with "wire" in the matching line
                                gen_int_sig = re.sub(pattern, r"wire \2 \3", gen_int_sig)
                                gen_stmts += "\t" + assign_syntax + ",\n"
                            gen_stmts = gen_stmts.rstrip()
                            gen_stmts = gen_stmts[0:-1]
                            instance_syntax = instance_syntax.replace("$portAssign", gen_stmts)
                            instance_syntax = instance_syntax.replace("$instance",
                                                                      child.getElementsByTagName("model")[
                                                                          0].firstChild.data)
                            gen_process += instance_syntax + "\n"

                        child = next
                    arch_syntax = verilog_root.getElementsByTagName("architecture")[0].firstChild.data

                    gen_arch = arch_syntax.replace("$int_sig_declaration", gen_int_sig)
                    gen_arch = gen_arch.replace("$arch_elements", gen_process[:-1])
                    gen_entity = gen_entity.replace("$arch", indent(gen_arch,'    '))
                    #if self.includeArrays == True:
                       # gen_verilog += "use work.arrayPackage.all;"

                    # Entity Section placement
                    gen_verilog += "\n\n" + gen_entity + "\n\n"

        return entity_name, gen_verilog

    def create_verilog_file(self):

        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        entity_name, verilog_code = self.generate_verilog()

        verilog_file_path = os.path.join(proj_path, "Verilog", "model", entity_name + ".v")
        verilog_file_HDLGen_path = os.path.join(proj_path, "Verilog", "model", entity_name + "_HDLGen.v")
        overwrite = False

        if os.path.exists(verilog_file_path):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setText("Do you want to overwrite manually edited file?")
            msgBox.setWindowTitle("Confirmation")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgBox.setDefaultButton(QMessageBox.No)
            response = msgBox.exec_()
            if response == QMessageBox.Yes:
                overwrite = True
                # Writing xml file
                with open(verilog_file_path, "w") as f:
                    f.write(verilog_code)
            else:
                with open(verilog_file_HDLGen_path, "w") as f:
                    f.write(verilog_code)
        else:
            # Writing xml file
            with open(verilog_file_path, "w") as f:
                f.write(verilog_code)
        with open(verilog_file_HDLGen_path, "w") as f:
            f.write(verilog_code)
        self.entity_name = entity_name
        return overwrite
    def create_verilog_testbench_code(self):
        tb_code = ""
        clkrst = 0
        xml_data_path = ProjectManager.get_xml_data_path()

        verilog_tb_database_path = "./Generator/TB_Database/verilog_tb_database.xml"

        wcfg_database_path = "./Generator/WCFG_Database/wcfg_database.xml"

        # Parsing the xml file
        project_data = minidom.parse(xml_data_path)
        HDLGen = project_data.documentElement

        verilog_tb_database = minidom.parse(verilog_tb_database_path)
        verilog_root = verilog_tb_database.documentElement

        hdl_design = HDLGen.getElementsByTagName("hdlDesign")
        wcfg = ""
        #TB = ""
        UUTEnt = ""
        header_node = hdl_design[0].getElementsByTagName("header")
        comp_node = header_node[0].getElementsByTagName("compName")[0]
        entity_name = comp_node.firstChild.data

        with open(wcfg_database_path, "r") as f:
            xml_string = f.read()

        head_regex = r"<head>(.*?)</head>"
        head_contents = re.search(head_regex, xml_string, re.DOTALL).group(1)

        #TB_regex = r"<TB>(.*?)</TB>"
        #TB_contents = re.search(TB_regex, xml_string, re.DOTALL).group(1)

        UUT_regex = r"<UUT>(.*?)</UUT>"
        UUT_contents = re.search(UUT_regex, xml_string, re.DOTALL).group(1)

        UUTEnt_regex = r"<UUTEnt>(.*?)</UUTEnt>"
        UUTEnt_contents = re.search(UUTEnt_regex, xml_string, re.DOTALL).group(1)
        end_regex = r"<end>(.*?)</end>"
        end_contents = re.search(end_regex, xml_string, re.DOTALL).group(1)
        head_contents = re.sub(r"\[componentName]", entity_name, head_contents)
        wcfg += head_contents

        # Entity Section
        inputArray = []
        arrayPackage=False
        #gen_signals = ""
        sig_decl = "// testbench signal declarations\n"
        sig_decl += "integer testNo; // aids locating test in simulation waveform\n"
        sig_decl += "reg endOfSim; // assert at end of simulation to highlight simuation done. Stops clk signal generation.\n\n"
        sig_decl += "// Typically use the same signal names as in the Verilog module"
        io_signals = ""
        entity_signal_description = ""
        io_port_node = hdl_design[0].getElementsByTagName("entityIOPorts")
        gen_entity = ""
        io_port_map = ""
        inputsToZero = ""
        inputsToOne = ""
        other_signals = ""
        control_signals = ""
        if len(io_port_node) != 0 and io_port_node[0].firstChild is not None:

            for signal in io_port_node[0].getElementsByTagName('signal'):
                io_signal_declare_syntax = verilog_root.getElementsByTagName("IOSignalDeclaration")[0].firstChild.data
                io_port_map_syntax = verilog_root.getElementsByTagName("portMap")[0].firstChild.data

                io_port_map_syntax = io_port_map_syntax.replace("$sig_name",
                                                                      signal.getElementsByTagName('name')[
                                                                          0].firstChild.data)
                io_signal_declare_syntax = io_signal_declare_syntax.replace("$sig_name",
                                                                      signal.getElementsByTagName('name')[
                                                                          0].firstChild.data)
                if signal.getElementsByTagName('mode')[0].firstChild.data == "in":
                    regOrwire = "reg"
                else:
                    regOrwire = "wire"
                io_signal_declare_syntax = io_signal_declare_syntax.replace("$regOrwire", regOrwire)
                name = signal.getElementsByTagName('name')[0].firstChild.data
                type = signal.getElementsByTagName('type')[0].firstChild.data
                #TB_content = re.sub(r"\[componentName]", entity_name, TB_contents)
                #TB_content = re.sub(r"\[signal]", name, TB_content)
                UUTEnt_content = re.sub(r"\[componentName]", entity_name, UUTEnt_contents)
                UUTEnt_content = re.sub(r"\[signal]", name, UUTEnt_content)

                if type[0:5] == "array":
                    size = ""
                    type = "array"
                elif type == "single bit":
                    size = ""
                    type = "logic"
                elif type[0:3] == "bus":
                    digits_list = re.findall(r'\d+', type)
                    size = "[" + str(digits_list[0]) + ":" + str(digits_list[1]) + "]"
                    type = "array"
                elif type[0:8] == "unsigned":
                    digits_list = re.findall(r'\d+', type)
                    size = "[" + str(digits_list[0]) + ":" + str(digits_list[1]) + "]"
                    type = "array"
                elif type[0:6] == "signed":
                    digits_list = re.findall(r'\d+', type)
                    size = "[" + str(digits_list[0]) + ":" + str(digits_list[1]) + "]"
                    type = "array"
                io_signal_declare_syntax = io_signal_declare_syntax.replace("$size",size)
                #TB_content = re.sub(r"\[type]", type, TB_content)
                #TB_content = re.sub(r"\[size]", size, TB_content)
                #TB += TB_content
                UUTEnt_content = re.sub(r"\[type]", type, UUTEnt_content)
                UUTEnt_content = re.sub(r"\[size]", size, UUTEnt_content)
                UUTEnt += UUTEnt_content

                if signal.getElementsByTagName('mode')[0].firstChild.data == "in":
                    if signal.getElementsByTagName('name')[0].firstChild.data != "clk" and signal.getElementsByTagName('name')[0].firstChild.data != "rst":
                        if signal.getElementsByTagName('type')[0].firstChild.data == "single bit":
                            inputArray.append(signal.getElementsByTagName('name')[0].firstChild.data)
                            inputsToZero += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " = 1'b0;\n"
                            inputsToOne += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " = '1'b1;\n"
                        elif signal.getElementsByTagName('type')[0].firstChild.data[0:3] == "bus":
                            size = signal.getElementsByTagName('type')[0].firstChild.data
                            digits_list = re.findall(r'\d+', size)
                            size = int(digits_list[0]) + 1
                            inputsToZero += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " = " + str(size) + "'b0;\n"
                            inputsToOne += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " = " + str(size) + "'b1;\n"
                        else:
                            inputsToZero += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " <= (others =>(others => \'0\'));\n"
                            arrayPackage=True
                else:
                    if signal.getElementsByTagName('type')[0].firstChild.data != "single bit" and signal.getElementsByTagName('type')[0].firstChild.data[0:3] != "bus":
                        arrayPackage = True
                signal_description = signal.getElementsByTagName('description')[
                    0].firstChild.data
                entity_signal_description += "-- " + signal.getElementsByTagName('name')[
                    0].firstChild.data + "\t" + signal_description + "\n"
               # gen_signals += "\t" + signal_declare_syntax + "\n"
                io_port_map += "\t" + io_port_map_syntax + "\n"
                if signal.getElementsByTagName('name')[0].firstChild.data == "clk" or signal.getElementsByTagName('name')[0].firstChild.data == "rst":
                    clkrst=clkrst+1
                else:
                    io_signals += io_signal_declare_syntax + "\n"
            #wcfg += TB
            wcfg += UUT_contents
            wcfg += UUTEnt
            io_port_map = io_port_map.rstrip()
            io_port_map = io_port_map[0:-1]
            io_signals = io_signals.rstrip()
            control_signals = "parameter  period = 20; // 20 ns\n"
            other_signals = ""
            if clkrst > 0:
                other_signals = "reg clk;\n"
                control_signals += "initial clk = 1'b1;\n"
            if clkrst == 2:
                other_signals += "reg rst;\n"
            control_signals += "initial endOfSim = 1'b0;\n"
            #gen_signals = gen_signals.rstrip()
            #gen_signals = gen_signals[0:-1]

            entity_syntax = verilog_root.getElementsByTagName("entity")
            gen_entity = entity_syntax[0].firstChild.data
            UUTInternal = "\t</wvobject>"
            # Internal signals
            int_sig_node = hdl_design[0].getElementsByTagName("internalSignals")
            if int_sig_node[0].firstChild is not None:
                UUTInternal = ""
                UUTInt_regex = r"<UUTInt>(.*?)</UUTInt>"
                UUTInt_contents = re.search(UUTInt_regex, xml_string, re.DOTALL).group(1)
                wcfg += UUTInt_contents
                UUTInternal_regex = r"<UUTInternal>(.*?)</UUTInternal>"
                UUTInternal_contents = re.search(UUTInternal_regex, xml_string, re.DOTALL).group(1)
                for signal in int_sig_node[0].getElementsByTagName("signal"):
                    name = signal.getElementsByTagName('name')[0].firstChild.data
                    type = signal.getElementsByTagName('type')[0].firstChild.data
                    UUTInternal_content = re.sub(r"\[componentName]", entity_name, UUTInternal_contents)
                    UUTInternal_content = re.sub(r"\[signal]", name, UUTInternal_content)
                    if type == "Enumerated type state signal pair(NS/CS)":
                        type = "logic"
                        size=""
                    elif type == "single bit":
                        size = ""
                        type = "logic"
                    elif type[0:5] == "array":
                        self.includeArrays = True
                        digits_list = re.findall(r'\d+', type)
                        size = "[" + str(digits_list[0]) + ":" + str(digits_list[1]) + "]"
                        type = "array"
                    elif type[0:3] == "bus":
                        digits_list = re.findall(r'\d+', type)
                        size = "[" + str(digits_list[0]) + ":" + str(digits_list[1]) + "]"
                        type = "array"
                    elif type[0:8] == "unsigned":
                        digits_list = re.findall(r'\d+', type)
                        size = "[" + str(digits_list[0]) + ":" + str(digits_list[1]) + "]"
                        type = "array"
                    elif type[0:6] == "signed":
                        digits_list = re.findall(r'\d+', type)
                        size = "[" + str(digits_list[0]) + ":" + str(digits_list[1]) + "]"
                        type = "array"
                    UUTInternal_content = re.sub(r"\[type]", type, UUTInternal_content)
                    UUTInternal_content = re.sub(r"\[size]", size, UUTInternal_content)
                    UUTInternal += UUTInternal_content
                UUTInternal += "\t</wvobject>"
            wcfg += UUTInternal
            wcfg = wcfg.strip()
            wcfg += end_contents

        # Header Section

        header_node = hdl_design[0].getElementsByTagName("header")
        if header_node is not None:
            comp_node = header_node[0].getElementsByTagName("compName")[0]
            if comp_node.firstChild.data != "null":
                entity_name = comp_node.firstChild.data

                gen_header = "// Header Section\n"
                gen_header += "// VHDL testbench "+ entity_name +"_TB\n"
                gen_header += "// Generated by HDLGen, Github https://github.com/abishek-bupathi/HDLGen\n"
                gen_header +="// Reference: https://tinyurl.com/vicilogicVHDLTips \n"
                gen_header += "// Component Name : " + entity_name + "\n"
                title = header_node[0].getElementsByTagName("title")[0].firstChild.data
                gen_header += "// Title          : " + (title if title != "null" else "") + "\n"
                gen_header += "// Description    : refer to component hdl model fro function description and signal dictionary\n"
                authors = header_node[0].getElementsByTagName("authors")[0].firstChild.data
                gen_header += "// Author(s)      : " + (authors if authors != "null" else "") + "\n"
                company = header_node[0].getElementsByTagName("company")[0].firstChild.data
                gen_header += "// Company        : " + (company if company != "null" else "") + "\n"
                email = header_node[0].getElementsByTagName("email")[0].firstChild.data
                gen_header += "// Email          : " + (email if email != "null" else "") + "\n"
                gen_header += "// Date           : " + header_node[0].getElementsByTagName("date")[
                    0].firstChild.data + "\n\n"

                tb_code += gen_header


                # Entity declaration
                gen_entity = gen_entity.replace("$comp_name", entity_name)
                tb_code += gen_entity +"\n\n"
                tbSignalDeclaration = sig_decl + "\n" + other_signals + "\n" + io_signals + "\n\n" + control_signals
                # Architecture section

                # Process
                gen_process = ""
                if clkrst > 0:
                    gen_process += "// Generate clk signal, if sequential component, and endOfSim is 0.\n"
                    gen_process += "always # (period/2.0) if (~endOfSim) clk = ~ clk;\n\n"
                gen_process += entity_name+" UUT\n\t(\n"
                gen_process += io_port_map+"\n\t);\n\n"
                gen_process += "initial\nbegin\n"
                gen_process += "$timeformat(-9, 2, \" ns\", 20);\n"
                gen_process += "$display(\"Simulation start :: time is %0t\",$time);\n"
                gen_process += "\t// Apply default INPUT signal values. Do not assign output signals (generated by the UUT) here\n"
                gen_process += "\t// Each stimulus signal change occurs 0.2*period after the active low-to-high clk edge\n"
                gen_process += "\ttestNo <= 0;\n"
                gen_process += inputsToZero
                if clkrst == 2:
                    gen_process += "\trst    <= 1'b1;\n"
                    gen_process += "\t@(posedge clk);\n"
                    gen_process += "\trst   <= 1'b0;\n"
                gen_process += "\t#period\n"
                if clkrst >= 1:
                    gen_process += "\t@(posedge clk);\n"
                gen_process += "\t// include testbench stimulus sequence here, i.e, input signal combinations\n"
                gen_process += "\t// manually added code START\n"
                gen_process += "\t// include testbench stimulus sequence here. Use new testNo for each test set\n"
                gen_process += "\t// individual tests. Generate input signal combinations and\n"
                gen_process += "\t// repeat(number of times) #period\n"
                gen_process += "\ttestNo <= 1;\n"
                gen_process += "\trepeat(2)\n"
                gen_process += "\t#period"
                gen_process += "\t// manually added code END\n\n"
                gen_process += "\t// Print nanosecond (ns) time to simulation transcript\n"
                gen_process += "\t// Use to find time when simulation ends (endOfSim is TRUE)\n"
                gen_process += "\t// Re-run the simulation for this time\n"
                gen_process += "\t// Select timing diagram and use View>Zoom Fit\n"
                gen_process += "\t$display(\"Simulation end :: time is %0t\",$time);\n"
                gen_process += "\tendOfSim = 1'b1; // assert to stop clk signal generation\n\n"

                arch_syntax = verilog_root.getElementsByTagName("architecture")[0].firstChild.data

                #gen_arch = arch_syntax.replace("$port", gen_signals)
                gen_arch = arch_syntax.replace("$tbSignalDeclaration", tbSignalDeclaration)
                gen_arch = gen_arch.replace("$arch_elements", gen_process[:-1])

                tb_code += gen_arch
        return entity_name, tb_code, wcfg

    def create_verilog_testbench_file(self, overwrite):
        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)

        entity_name, verilog_tb_code, waveform = self.create_verilog_testbench_code()

        verilog_tb_path = os.path.join(proj_path, "Verilog", "testbench", self.entity_name + "_TB.v")
        verilog_tb_HDLGen_path = os.path.join(proj_path, "Verilog", "testbench", self.entity_name + "_HDLGen_TB.v")
        waveform_path = os.path.join(proj_path, "Verilog", "AMDprj", self.entity_name + "_TB_behav.wcfg")
        if os.path.exists(verilog_tb_path) == False:
            with open(verilog_tb_path, "w") as f:
                f.write(verilog_tb_code)
            print("Verilog Testbench file successfully generated at ", verilog_tb_path)

        if overwrite == True:
            # Writing xml file
            with open(verilog_tb_path, "w") as f:
                f.write(verilog_tb_code)

            print("Verilog Testbench file successfully generated at ", verilog_tb_path)
        with open(verilog_tb_HDLGen_path, "w") as f:
            f.write(verilog_tb_code)
        print("Verilog Testbench HDLGen file successfully generated at ", verilog_tb_HDLGen_path)

        with open(waveform_path, "w") as f:
            f.write(waveform)