import os
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

        # print("All project folders have been successfully generated at ", self.proj_dir)

    #@staticmethod
    def generate_vhdl(self):

        gen_vhdl = ""
        gen_array_vhdl = ""

        xml_data_path = ProjectManager.get_xml_data_path()

        test_xml = os.path.join("../Resources", "SampleProject.xml")

        vhdl_database_path = "./Generator/HDL_Database/vhdl_database.xml"

        # Parsing the xml file
        project_data = minidom.parse(xml_data_path)
        HDLGen = project_data.documentElement

        vhdl_database = minidom.parse(vhdl_database_path)
        vhdl_root = vhdl_database.documentElement

        hdl_design = HDLGen.getElementsByTagName("hdlDesign")
        stateTypesList = ""
        entity_name = ""
        gen_int_sig = ""
        gen_internal_signal_result = ""
        arrayList=[]
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
                signal_description = signal.getElementsByTagName('description')[
                    0].firstChild.data
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
                for stateType in int_sig_node[0].getElementsByTagName("stateTypes"): #stateTypesList:
                    stateTypesString += stateType.firstChild.data +", "
                stateTypesString = stateTypesString[:-2]

                if stateTypesString != "":
                    stateType_syntax = vhdl_root.getElementsByTagName("stateNamesDeclarations")[0].firstChild.data
                    stateType_syntax = stateType_syntax.replace("$stateNamesList",stateTypesString)
                    gen_int_sig += "\n" + stateType_syntax
                for signal in int_sig_node[0].getElementsByTagName("signal"):
                    name = signal.getElementsByTagName('name')[0].firstChild.data
                    type = signal.getElementsByTagName('type')[0].firstChild.data

                    if type == "Enumerated type state signals":
                        type = "stateType"
                        if name[0:2] == "CS":
                            stateTypeSig = True
                            CSState = name
                    int_sig_syntax = vhdl_root.getElementsByTagName("intSigDeclaration")[0].firstChild.data
                    int_sig_syntax = int_sig_syntax.replace("$int_sig_name", name)
                    # signal.getElementsByTagName('name')[0].firstChild.data)
                    int_sig_syntax = int_sig_syntax.replace("$int_sig_type", type)
                    # signal.getElementsByTagName('type')[0].firstChild.data)
                    int_signal_description = signal.getElementsByTagName('description')[
                        0].firstChild.data

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

                #gen_library += "\n"
                gen_vhdl += gen_library
                if self.includeArrays == True:

                    gen_vhdl += "use work.arrayPackage.all;"

                # Entity Section placement
                gen_vhdl += "\n\n" + gen_entity + "\n\n"
                # Architecture section

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

                                if value == "Idle":
                                    if stateTypesList != "":
                                        stateNames = stateTypesString.split(",")
                                        value = stateNames[0]
                                elif value == "all zeros":
                                    if signals[0] in arrayList:
                                        value = "(others =>(others => '0'))"
                                    else:
                                        value = "(others => '0')"
                                elif value == "all ones":
                                    value = "(others => '1')"
                                elif stateTypeSig == True:
                                    if value == CSState:
                                        caseEmpty = False
                                        case_syntax = vhdl_root.getElementsByTagName("case")[0].firstChild.data
                                        case_syntax = case_syntax.replace("$stateType", value)
                                        stateNames = stateTypesString.split(",")
                                        whenCase=""
                                        for states in stateNames:
                                            whenCase +="\n\t\twhen "+ states + "=>" + "\n\t\t\tnull;"
                                        case_syntax = case_syntax.replace("$whenCase", whenCase)
                                if value.isdigit():
                                    if value == "1" or value == "0":
                                        value = "'" + value + "'"
                                    else:
                                        value = '"'+value+'"'

                                assign_syntax = assign_syntax.replace("$value", value)
                                if_gen_defaults += "\t" + assign_syntax + "\n\t"
                                gen_defaults +=  assign_syntax + "\n\t"
                                if len(signals) == 3:
                                    clkAssign_syntax = vhdl_root.getElementsByTagName("sigAssingn")[0].firstChild.data
                                    clkAssign_syntax = clkAssign_syntax.replace("$output_signal", signals[0])
                                    clkAssign_syntax = clkAssign_syntax.replace("$value", signals[2])
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
                                            if_gen_defaults = "\t" + if_syntax + "\n"
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
                                    process_syntax = process_syntax.replace("$default_assignments", clkgen_defaults)
                                else:
                                    if caseEmpty == False:
                                        gen_defaults += "\n" + case_syntax
                                    process_syntax = process_syntax.replace("$default_assignments", gen_defaults)
                            #if caseEmpty == False:
                            #    process_syntax = process_syntax.replace("$case", case_syntax)
                            #else:
                            #    process_syntax = process_syntax.replace("$case", "")
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
                                elif value == "all zeros":
                                    if signals[0] in arrayList:
                                        value = "(others =>(others => '0'))"
                                    else:
                                        value = "(others => '0')"
                                assign_syntax = assign_syntax.replace("$value", value)

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
                    gen_arch = gen_arch.replace("$component_declarations", "-- Component declarations")
                    gen_arch = gen_arch.replace("$arch_elements", gen_process[:-1])

                    gen_vhdl += gen_arch
        #if includeArrays == True:


        return entity_name, gen_vhdl#, gen_array_vhdl

    def create_vhdl_file(self):

        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        entity_name, vhdl_code = self.generate_vhdl()

        vhdl_file_path = os.path.join(proj_path, "VHDL", "model", entity_name + ".vhd")

        # Writing xml file
        with open(vhdl_file_path, "w") as f:
            f.write(vhdl_code)

        print("VHDL Model successfully generated at ", vhdl_file_path)

        self.entity_name = entity_name


    def create_tcl_file(self):
        print("creating tcl")
        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)

        vhdl_path = proj_path + "/VHDL/model/" + self.entity_name + ".vhd"
        self.tcl_path = proj_path + "/VHDL/AMDPrj/" + self.entity_name + ".tcl"
        tcl_database_path = "./Generator/TCL_Database/tcl_database.xml"

        tcl_database = minidom.parse(tcl_database_path)
        tcl_root = tcl_database.documentElement

        tcl_file_template = tcl_root.getElementsByTagName("vivado_vhdl_tcl")[0]
        #print(tcl_file_template)
        tcl_file_template = tcl_file_template.firstChild.data
        #print(tcl_file_template)

        tb_file_name = self.entity_name + "_tb"
        tcl_vivado_code = tcl_file_template.replace("$tcl_path", self.tcl_path)
        tcl_vivado_code = tcl_vivado_code.replace("$comp_name", self.entity_name)
        #add_files -norecurse C:/Users/User/HDLGen/Application/HDLDesigner/Package/mainPackage.vhd
        wd = os.getcwd()
        wd = wd.replace("\\","/")
        mainPackagePath = "add_files -norecurse  "+ wd +"/HDLDesigner/Package/mainPackage.vhd"
        if self.includeArrays == True:
            tcl_vivado_code = tcl_vivado_code.replace("$arrayPackage", mainPackagePath)
        else:
            tcl_vivado_code = tcl_vivado_code.replace("$arrayPackage","")
        tcl_vivado_code = tcl_vivado_code.replace("$tb_name", tb_file_name)
        tcl_vivado_code = tcl_vivado_code.replace("$proj_name", proj_name)
        proj_path = "{" + proj_path + "}"
        tcl_vivado_code = tcl_vivado_code.replace("$proj_dir", proj_path)
        tcl_vivado_code = tcl_vivado_code.replace("$vhdl_path", vhdl_path)

        # Writing xml file
        with open(self.tcl_path, "w") as f:
            f.write(tcl_vivado_code)

        print("TCL file successfully generated at ", self.tcl_path)

        return 1

    def run_tcl_file(self):

        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        subprocess.Popen("cd " + proj_path, shell=True)
        vivado_bat_file_path = ProjectManager.get_vivado_bat_path()
        start_vivado_cmd = vivado_bat_file_path + " -source " + self.tcl_path
        subprocess.Popen(start_vivado_cmd, shell=True)

    def create_vhdl_testbench_code(self):
        tb_code = ""
        clkrst = 0
        xml_data_path = ProjectManager.get_xml_data_path()

        test_xml = os.path.join("../Resources", "SampleProject.xml")

        vhdl_tb_database_path = "./Generator/TB_Database/vhdl_tb_database.xml"

        # Parsing the xml file
        project_data = minidom.parse(xml_data_path)
        HDLGen = project_data.documentElement

        vhdl_tb_database = minidom.parse(vhdl_tb_database_path)
        vhdl_root = vhdl_tb_database.documentElement

        hdl_design = HDLGen.getElementsByTagName("hdlDesign")

        entity_name = ""
        gen_int_sig = ""
        gen_internal_signal_result = ""
        # Entity Section
        inputArray = []
        arrayPackage=False
        gen_signals = ""
        io_signals = "-- testbench signal declarations\n"
        io_signals += "-- Typically use the same signal names as in the VHDL entity, with keyword signal added, and without in/out mode keyword\n"
        io_signals += "-- excluding clk and rst, if used\n"
        entity_signal_description = ""
        io_port_node = hdl_design[0].getElementsByTagName("entityIOPorts")
        gen_entity = ""
        io_port_map = ""
        inputsToZero = ""
        inputsToOne = ""
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
                signal_declare_syntax = signal_declare_syntax.replace("$type",
                                                                      signal.getElementsByTagName('type')[
                                                                          0].firstChild.data)
                io_signal_declare_syntax = io_signal_declare_syntax.replace("$type",
                                                                            signal.getElementsByTagName('type')[
                                                                                0].firstChild.data)

                if signal.getElementsByTagName('mode')[0].firstChild.data == "in":
                    if signal.getElementsByTagName('name')[0].firstChild.data != "clk" and signal.getElementsByTagName('name')[0].firstChild.data != "rst":
                        if signal.getElementsByTagName('type')[0].firstChild.data == "std_logic":
                            inputArray.append(signal.getElementsByTagName('name')[0].firstChild.data)
                            inputsToZero += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " <= \'0\';\n"
                            inputsToOne += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " <= \'1\';\n"
                        elif signal.getElementsByTagName('type')[0].firstChild.data == "std_logic_vector":
                            inputsToZero += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " <= (others => \'0\');\n"
                            inputsToOne += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " <= (others => \'1\');\n"
                        else:
                            inputsToZero += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " <= (others =>(others => \'0\'));\n"
                            arrayPackage=True
                signal_description = signal.getElementsByTagName('description')[
                    0].firstChild.data
                entity_signal_description += "-- " + signal.getElementsByTagName('name')[
                    0].firstChild.data + "\t" + signal_description + "\n"
                gen_signals += "\t" + signal_declare_syntax + "\n"
                io_port_map += "\t" + io_port_map_syntax + "\n"
                if signal.getElementsByTagName('name')[0].firstChild.data == "clk" or signal.getElementsByTagName('name')[0].firstChild.data == "rst" :
                    clkrst=clkrst+1
                else:
                    io_signals += io_signal_declare_syntax + "\n"
            io_port_map = io_port_map.rstrip()
            io_port_map = io_port_map[0:-1]
            io_signals = io_signals.rstrip()
            #io_signals = io_signals[0:-1]
            #other_signals = "\n-- <delete (Start) If UUT is a combinational component>\n"
            other_signals = ""
            if clkrst > 0:
                other_signals = "signal clk: std_logic := '1';\n" #-- entity includes signal clk, so declare (and initialise) tetbench clk signal\n"
            if clkrst == 2:
                other_signals += "signal rst: std_logic;        \n"#-- entity may include signal rst (reset), so declare in testbench\n"
            #other_signals += "-- <delete (End)\n\n-- testbench control signal declarations\n"
            control_signals = "signal endOfSim : boolean := false; -- assert at end of simulation to highlight simuation done. Stops clk signal generation.\n"
            control_signals += "signal testNo: integer; -- aids locating test in simulation waveform\n\n"
            control_signals += "constant period: time := 20 ns; -- Default simulation time. Use as simulation delay constant, or clk period if sequential model ((50MHz clk here)\n"

            gen_signals = gen_signals.rstrip()
            gen_signals = gen_signals[0:-1]

            entity_syntax = vhdl_root.getElementsByTagName("entity")
            gen_entity = "-- entity declaration\n"
            gen_entity += entity_syntax[0].firstChild.data

            # Internal signals
            gen_int_sig = ""
            int_sig_node = hdl_design[0].getElementsByTagName("internalSignals")
            if int_sig_node[0].firstChild is not None:
                for signal in int_sig_node[0].getElementsByTagName("signal"):
                    int_sig_syntax = vhdl_root.getElementsByTagName("intSigDeclaration")[0].firstChild.data
                    int_sig_syntax = int_sig_syntax.replace("$int_sig_name",
                                                            signal.getElementsByTagName('name')[0].firstChild.data)
                    int_sig_syntax = int_sig_syntax.replace("$int_sig_type",
                                                            signal.getElementsByTagName('type')[0].firstChild.data)
                    int_signal_description = signal.getElementsByTagName('description')[
                        0].firstChild.data

                    gen_int_sig += "\n" + int_sig_syntax
                    gen_internal_signal_result += "-- " + signal.getElementsByTagName('name')[
                        0].firstChild.data + "\t" + int_signal_description + "\n"
                gen_int_sig.rstrip()
            else:
                gen_internal_signal_result = "-- None\n"

        # Header Section

        header_node = hdl_design[0].getElementsByTagName("header")
        if header_node is not None:
            comp_node = header_node[0].getElementsByTagName("compName")[0]
            if comp_node.firstChild.data != "null":
                entity_name = comp_node.firstChild.data

                gen_header = "-- Header Section\n"
                gen_header += "-- VHDL testbench "+ entity_name +"_TB\n"
                gen_header += "-- Generated by HDLGen, Github https://github.com/abishek-bupathi/HDLGen\n"
                gen_header +="-- Reference: https://tinyurl.com/vicilogicVHDLTips \n"
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

                # entity signal dictionary
                gen_entity_signal = "-- entity signal dictionary\n"
                gen_entity_signal += entity_signal_description + "\n"
                #tb_code += gen_entity_signal

                # internal signal dictionary
                gen_internal_signal = "-- internal signal dictionary\n"
                gen_internal_signal_result = gen_internal_signal_result + "\n"
                gen_internal_signal += gen_internal_signal_result
                #tb_code += gen_internal_signal
                # Libraries Section

                libraries_node = vhdl_root.getElementsByTagName("libraries")
                libraries = libraries_node[0].getElementsByTagName("library")
                gen_library = "-- library declarations\n"
                for library in libraries:
                    gen_library += library.firstChild.data + "\n"
                if arrayPackage == True:
                    gen_library += "use work.arrayPackage.all;"
                gen_library += "\n"
                tb_code += gen_library

                # Entity declaration
                gen_entity = gen_entity.replace("$comp_name", entity_name)
                tb_code += gen_entity +"\n\n"
                tbSignalDeclaration = io_signals +"\n" + other_signals + "\n" + control_signals
                # Architecture section

                # Process
                arch_node = hdl_design[0].getElementsByTagName("architecture")
                gen_process = ""
                if clkrst > 0:
                    #gen_process += "-- <delete (Start) If UUT is a combinational component>\n"
                    gen_process += "-- Generate clk signal, if sequential component, and endOfSim is FALSE.\n"
                    gen_process += "clkStim: clk <= not clk after period/2 when endOfSim = false else '0';\n"
                    #gen_process += "-- <delete (End)\n\n"
                gen_process += "-- instantiate unit under test (UUT)\n"
                gen_process += "UUT: "+entity_name+ "-- map component internal sigs => testbench signals\n"
                gen_process += "port map\n\t(\n"
                gen_process += io_port_map+"\n\t);\n\n"
                gen_process += "-- Signal stimulus process\n"
                gen_process += "stim_p: process -- process sensitivity list is empty, so process automatically executes at start of simulation. Suspend process at the wait; statement\n"
                #gen_process += "-- <delete (Start) if note using variables\n"
                #gen_process += "variable stimVec : std_logic_vector(" + str(len(inputArray)-1)+" downto 0);\n"
                gen_process += "begin\n"
                gen_process += "\t-- Apply default INPUT signal values. Do not assign output signals (generated by the UUT) in this stim_p process\n"
                gen_process += "\t-- Each stimulus signal change occurs 0.2*period after the active low-to-high clk edge\n"
                gen_process += "\t-- if signal type is\n\t-- std_logic, use '0'\n\t-- std_logic_vector use (others => '0')\n\t-- integer use 0\n"
                gen_process += inputsToZero
                gen_process += "\treport \"%N Simulation start\";\n\n"
                if clkrst == 2:
                    #gen_process += "\t-- <delete (Start) If UUT is a combinational component>\n"
                    gen_process += "\treport \"Assert and toggle rst\";\n\ttestNo <= 0;\n\trst    <= '1';\n"
                    gen_process += "\twait for period*1.2; -- assert rst for 1.2*period, deasserting rst 0.2*period after active clk edge\n"
                    gen_process += "\trst   <= '0';\n\twait for period; -- wait 1 clock period\n\t"#-- <delete (End)\n\n"
                gen_process += "-- include testbench stimulus sequence here. USe new testNo for each test set"
                gen_process += "\t-- individual tests. Generate input signal combinations and wait for period.\n"
                gen_process += "\ttestNo <= 1;\n"
                #gen_process += "\t-- <delete (Start) if note using variables\n"
                #gen_process += "\tfor i in 0 to " + str(pow(2,len(inputArray))-1) + " loop\n"
                #gen_process += "\t\tstimVec := std_logic_vector( to_unsigned(i," + str(len(inputArray)) +") );\n"
                #indexOfArray = len(inputArray)
                #for x in inputArray:
                #    indexOfArray = indexOfArray-1
                #    gen_process += "\t\t"+ x + " <= stimVec("+str(indexOfArray)+");\n"
                #gen_process += "\t\twait for period;\n"
                #gen_process += "\tend loop;\n"
                #gen_process += "\t-- <delete (End)\n\n"
                #gen_process += "\t-- <delete (Start) if not required\n"
                #gen_process += inputsToOne
                gen_process += "\twait for 3*period;\n"
                gen_process += "\n\t-- include testbench stimulus sequence here. USe new testNo for each test set\n\n"
                #gen_process += "\t-- <delete (End)\n\n"
                gen_process += "\treport \"%N Simulation done\";\n"
                gen_process += "\tendOfSim <= TRUE; -- assert flag to stop clk signal generation\n\n"
                gen_process += "\twait; -- wait forever\n"
                if len(arch_node) != 0 and arch_node[0].firstChild is not None:

                    arch_syntax = vhdl_root.getElementsByTagName("architecture")[0].firstChild.data
                    arch_name_node = arch_node[0].getElementsByTagName("archName")

                    #arch_name = "comb"

                    if len(arch_name_node) != 0 and arch_name_node[0].firstChild is not None:
                        arch_name = arch_name_node[0].firstChild.data

                    gen_arch = arch_syntax.replace("$comp_name", entity_name)
                    gen_arch = gen_arch.replace("$component_declarations", "-- unit under test (UUT) component declaration. Identical to component entity, with 'entity' replaced with 'component'")
                    gen_arch = gen_arch.replace("$port", gen_signals)
                    gen_arch = gen_arch.replace("$tbSignalDeclaration", tbSignalDeclaration)
                    gen_arch = gen_arch.replace("$arch_elements", gen_process[:-1])

                    tb_code += gen_arch

        return entity_name, tb_code

    def create_testbench_file(self):
        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)

        entity_name, vhdl_tb_code = self.create_vhdl_testbench_code()

        vhdl_tb_path = os.path.join(proj_path, "VHDL", "testbench", self.entity_name + "_tb.vhd")

        #print(vhdl_tb_code)

        # Writing xml file
        with open(vhdl_tb_path, "w") as f:
            f.write(vhdl_tb_code)

        print("VHDL Testbench file successfully generated at ", vhdl_tb_path)

    def generate_mainPackage(self):
        gen_arrays =""
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
            # arrayPackage
        # if gen_arrays != "":
        array_vhdl_code = vhdl_root.getElementsByTagName("arrayPackage")[0].firstChild.data
        array_vhdl_code = array_vhdl_code.replace("$arrays", gen_arrays)
        # Creating arrayPackage file
        array_vhdl_file_path = os.getcwd() + "\HDLDesigner\Package\mainPackage.vhd"
        # array_vhdl_file_path = os.path.join(proj_path, "VHDL", "model", "arrayPackage.vhd")
        # Write array code to file
        with open(array_vhdl_file_path, "w") as f:
            f.write(array_vhdl_code)