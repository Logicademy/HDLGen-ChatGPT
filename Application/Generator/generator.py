#This class generates all the hdl code and TCL scripts, comprised of many different methods called by home.py class, generation.py class and hdl_designer.py class

import os
import re
from xml.dom import minidom
import pyperclip
from PySide2.QtWidgets import *
import subprocess
import sys
from datetime import datetime
import textwrap
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
                    # Creating the VHDL directory
                    path = os.path.join(location, folder.firstChild.data)
                    os.makedirs(path, exist_ok=True)
            # If verilog is present in the hdl settings then directory with verilog_folder are read
            if hdl_lang.getElementsByTagName('name')[0].firstChild.data == "Verilog":
                for folder in genFolder_data[0].getElementsByTagName("verilog_folder"):
                    # Creating the Verilog directory
                    path = os.path.join(location, folder.firstChild.data)
                    os.makedirs(path, exist_ok=True)

    def generate_vhdl(self):

        entity_name = ""
        gen_vhdl = ""
        chatgpt_header = ""
        chatgpt_vhdl = ""

        # Load Project XML Data
        xml_data_path = ProjectManager.get_xml_data_path()

        # Load VHDL Syntax Database
        vhdl_database_path = "./Generator/HDL_Database/vhdl_database.xml"

        # Parse the HDLGen Project XML file, and get the root element (<HDLGen> element)
        project_data = minidom.parse(xml_data_path)
        HDLGen = project_data.documentElement

        # Parse the VHDL Database XML file, and get the root element (<vhdl> element)
        vhdl_database = minidom.parse(vhdl_database_path)
        vhdl_root = vhdl_database.documentElement

        # Get the hdlDesign element which contains all info about the component
        hdl_design = HDLGen.getElementsByTagName("hdlDesign")

        # Internal variables
        stateTypesList = ""
        gen_int_sig = ""
        gen_internal_signal_result = ""
        portSignals = []
        internalSignals = []
        arrayList = []
        single_bitList = []
        busList = []
        unsignedList = []
        signedList = []
        integerList = []

        # Entity Section
        gen_signals = ""
        entity_signal_description = ""
        # Get the <entityIOPorts> element
        io_port_node = hdl_design[0].getElementsByTagName("entityIOPorts")
        gen_entity = ""
        self.includeArrays = False
        stateTypeSig = False
        instances = []

        # Loop over all signals in the <entityIOPorts> element
        # The main purpose of this loop is to fill arrayList, busList,
        # single_bitList, unsignedList and signedList with data.
        #
        # It also generates the VHDL signal declarations for each signal
        if len(io_port_node) != 0 and io_port_node[0].firstChild is not None:
            for signal in io_port_node[0].getElementsByTagName('signal'):
                name = signal.getElementsByTagName('name')[0].firstChild.data
                portSignals.append(name)
                type = signal.getElementsByTagName('type')[0].firstChild.data
                if type[0:6] == "array,":
                    type = type.split(",")
                    type = type[1] + "  := ( others => (others => '0') )"
                    self.includeArrays = True
                    arrayList.append(name)
                elif type == "single bit":
                    single_bitList.append(name)
                    type = "std_logic"
                elif type[0:3] == "bus":
                    busList.append(name)
                    type = type.replace("bus", "std_logic_vector")
                elif type[0:8] == "unsigned":
                    unsignedList.append(name)
                elif type[0:6] == "signed":
                    signedList.append(name)

                # Get the syntax to declare a signal from the VHDL Syntax Database
                signal_declare_syntax = vhdl_root.getElementsByTagName("signalDeclaration")[0].firstChild.data

                # Fill in the signal name to be declared
                signal_declare_syntax = signal_declare_syntax.replace("$sig_name", signal.getElementsByTagName('name')[0].firstChild.data)

                # Fill in the signal mode for the signal being declared
                signal_declare_syntax = signal_declare_syntax.replace("$mode", signal.getElementsByTagName('mode')[0].firstChild.data)

                # Fill in the signal type for the signal being declared                                                         
                signal_declare_syntax = signal_declare_syntax.replace("$type", type)
                
                # Grab the signal description for the signal being declared
                signal_description = signal.getElementsByTagName('description')[0].firstChild.data
            
                # Replace XML Escape codes with Escape Characters
                signal_description = signal_description.replace("&#10;", "\n-- ")

                # Assemble the entity signal description (Name  Description)
                entity_signal_description += "-- " + signal.getElementsByTagName('name')[0].firstChild.data + "\t" + signal_description + "\n"

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
                    internalSignals.append(name)
                    type = signal.getElementsByTagName('type')[0].firstChild.data

                    if type == "Enumerated type state signal pair(NS/CS)":
                        type = "stateType"
                        if name[0:2] == "CS":
                            stateTypeSig = True
                            CSState = name
                    elif type == "single bit":
                        single_bitList.append(name)
                        type = "std_logic"
                    elif type[0:3] == "bus":
                        busList.append(name)
                        type = type.replace("bus", "std_logic_vector")
                    elif type[0:8] == "unsigned":
                        unsignedList.append(name)
                    elif type[0:6] == "signed":
                        signedList.append(name)
                    elif type[0:13] == "integer range":
                        integerList.append(name)
                    else:
                        type = type.split(",")
                        type = type[1] + "  := ( others => (others => '0') )"
                        self.includeArrays = True
                        arrayList.append(name)
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

                gen_header = "-- Title Section Start\n"
                gen_header += "-- Generated by HDLGen, Github https://github.com/HDLGen-ChatGPT/HDLGen-ChatGPT, on " + str(
                    datetime.now().strftime("%d-%B-%Y")) + " at " + str(datetime.now().strftime("%H:%M")) + "\n\n"
                gen_header += "-- Component Name : " + entity_name + "\n"
                title = header_node[0].getElementsByTagName("title")[0].firstChild.data
                gen_header += "-- Title          : " + (title if title != "null" else "") + "\n\n"
                authors = header_node[0].getElementsByTagName("authors")[0].firstChild.data
                gen_header += "-- Author(s)      : " + (authors if authors != "null" else "") + "\n"
                company = header_node[0].getElementsByTagName("company")[0].firstChild.data
                gen_header += "-- Organisation   : " + (company if company != "null" else "") + "\n"
                email = header_node[0].getElementsByTagName("email")[0].firstChild.data
                gen_header += "-- Email          : " + (email if email != "null" else "") + "\n"
                gen_header += "-- Date           : " + header_node[0].getElementsByTagName("date")[
                    0].firstChild.data + "\n\n"
                desc = header_node[0].getElementsByTagName("description")[0].firstChild.data
                desc = desc.replace("&#10;", "\n-- ")
                gen_header += "-- Description\n-- "
                gen_header += (desc if desc != "null" else "") + "\n"

                chatgpt_header += gen_header
                gen_vhdl += gen_header

                # entity signal dictionary
                gen_entity = gen_entity.replace("$comp_name", entity_name)
                gen_entity_signal = "\n-- entity signal dictionary\n"
                gen_entity_signal += entity_signal_description + "\n"
                chatgpt_header += gen_entity_signal
                gen_vhdl += gen_entity_signal

                # internal signal dictionary
                gen_internal_signal = "-- internal signal dictionary\n"
                gen_internal_signal_result = gen_internal_signal_result + "\n"
                gen_internal_signal += gen_internal_signal_result
                gen_internal_signal += "-- Title Section End\n"
                chatgpt_header += gen_internal_signal
                gen_vhdl += gen_internal_signal
                # Libraries Section

                libraries_node = vhdl_root.getElementsByTagName("libraries")
                libraries = libraries_node[0].getElementsByTagName("library")
                gen_library = "-- library declarations\n"

                for library in libraries:
                    gen_library += library.firstChild.data + "\n"

                # Process
                arch_node = hdl_design[0].getElementsByTagName("architecture")
                gen_archs = ""
                gen_process = ""
                gen_conc = ""
                gen_seq_process = ""
                gen_instance = ""
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
                            ceInSeq = ""
                            caseEmpty = True
                            notes = child.getElementsByTagName("note")[0].firstChild.data
                            notes = re.sub(r'\s+', ' ', notes)
                            # notes = notes.replace("&#10;", "\n---")
                            notes = notes.replace("&amp;", "&")
                            notes = notes.replace("&quot;", "\"")
                            notes = notes.replace("&apos;", "\'")
                            notes = notes.replace("&lt;", "<")
                            notes = notes.replace("&#x9;", "\t")
                            notes = notes.replace("&gt;", ">")
                            notes = notes.replace("&#44;", ",")
                            notes = notes.replace("[", "(")
                            notes = notes.replace("]", ")")
                            notes = notes.replace(":", " downto ")
                            notes = notes.replace("'", "")
                            notes = re.sub(r'\s+', ' ', notes)
                            notes = notes.replace("&#10;", "\n---")

                            pattern = r'(?<!downto\s)(?<!\d)([01]+)(?!\d)(?!\s*downto)'
                            notes = re.sub(pattern, lambda m: f"'{m.group(1)}'" if len(
                                m.group(1)) == 1 else f'"{m.group(1)}"', notes)
                            pattern1 = r"(\(|\w+)(['\"])(\d+)\2\)"
                            match = re.search(pattern1, notes)
                            while match:
                                notes = notes.replace(match.group(), match.group(1) + match.group(3) + ")")
                                match = re.search(pattern1, notes)
                            pattern2 = r"[^\s]+['\"]\d+['\"]"
                            notes = re.sub(pattern2,
                                           lambda match: match.group(0).replace("'", "").replace('"', ""),
                                           notes)
                            # Define a regular expression pattern to match the content inside { }
                            pattern3 = r'\w+\{([^}]+)\}'
                            # Use re.sub to replace the matched content inside { }
                            notes = re.sub(pattern3, r'(others => \1)', notes)

                            signalList = ""

                            for default_out in child.getElementsByTagName("defaultOutput"):

                                assign_syntax = vhdl_root.getElementsByTagName("sigAssign")[0].firstChild.data
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
                                        value = "'" + '0' + "'"
                                    elif signals[0] in busList or signals[0] in signedList or signals[
                                        0] in unsignedList:
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
                                elif value in portSignals or value in internalSignals:
                                    value = value

                                elif stateTypeSig == True and value == CSState:
                                    caseEmpty = False
                                    case_syntax = vhdl_root.getElementsByTagName("case")[0].firstChild.data
                                    case_syntax = case_syntax.replace("$stateType", value)
                                    stateNames = stateTypesString.split(",")
                                    whenCase = ""
                                    for states in stateNames:
                                        whenCase += "\n\t\twhen " + states + "=>" + "\n\t\t\tnull;"
                                else:
                                    value = re.sub(r'\s+', ' ', value)
                                    value = value.replace("&#10;", "\n--- ")
                                    value = value.replace("&amp;", "&")
                                    value = value.replace("&quot;", "\"")
                                    value = value.replace("&apos;", "\'")
                                    value = value.replace("&lt;", "<")
                                    value = value.replace("&#x9;", "\t")
                                    value = value.replace("&gt;", ">")
                                    value = value.replace("&#44;", ",")
                                    value = value.replace("[", "(")
                                    value = value.replace("]", ")")
                                    value = value.replace(":", " downto ")
                                    value = value.replace("'", "")
                                    value = re.sub(r'\s+', ' ', value)

                                    pattern = r'(?<!downto\s)(?<!\d)([01]+)(?!\d)(?!\s*downto)'
                                    value = re.sub(pattern, lambda m: f"'{m.group(1)}'" if len(
                                        m.group(1)) == 1 else f'"{m.group(1)}"', value)
                                    pattern1 = r"(\(|\w+)(['\"])(\d+)\2\)"
                                    match = re.search(pattern1, value)
                                    while match:
                                        value = value.replace(match.group(), match.group(1) + match.group(3) + ")")
                                        match = re.search(pattern1, value)
                                    pattern2 = r"[^\s]+['\"]\d+['\"]"
                                    value = re.sub(pattern2,
                                                   lambda match: match.group(0).replace("'", "").replace('"', ""),
                                                   value)
                                    # Define a regular expression pattern to match the content inside { }
                                    pattern3 = r'\w+\{([^}]+)\}'
                                    # Use re.sub to replace the matched content inside { }
                                    value = re.sub(pattern3, r'(others => \1)', value)
                                assign_syntax = assign_syntax.replace("$value", value)
                                if_gen_defaults += "\t" + assign_syntax + "\n\t"
                                gen_defaults += assign_syntax + "-- Default assignment \n\t"
                                if len(signals) == 4:
                                    clkAssign_syntax = vhdl_root.getElementsByTagName("sigAssign")[0].firstChild.data
                                    clkAssign_syntax = clkAssign_syntax.replace("$output_signal", signals[0])
                                    value = signals[2]
                                    if signals[3] != "N/A":
                                        ceInSeq = signals[3]
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
                                    clkAssign_syntax = clkAssign_syntax.replace("$value", value)  # signals[2])
                                    clkgen_defaults += "\t\t" + clkAssign_syntax + "\n"
                                else:
                                    signalList += ", " + signals[0]
                            if gen_defaults != "":
                                if clkgen_defaults != "":
                                    for clkRst in clkAndRst[0].getElementsByTagName("clkAndRst"):
                                        clkEdge = "rising_edge"
                                        if clkRst.getElementsByTagName('activeClkEdge')[0].firstChild.data == "H-L":
                                            clkEdge = "falling_edge"
                                        clkif_syntax = vhdl_root.getElementsByTagName("clkIfStatement")[
                                            0].firstChild.data
                                        clkif_syntax = clkif_syntax.replace("$edge", clkEdge)
                                        if clkRst.getElementsByTagName('rst')[0].firstChild.data == "Yes":
                                            if_syntax = vhdl_root.getElementsByTagName("ifStatement")[0].firstChild.data
                                            if_syntax = if_syntax.replace("$assignment", "rst")
                                            if_syntax = if_syntax.replace("$value",
                                                                          clkRst.getElementsByTagName('ActiveRstLvl')[
                                                                              0].firstChild.data)
                                            if_syntax = if_syntax.replace("$default_assignments", if_gen_defaults)
                                            # if_gen_defaults = "\t" + if_syntax + "\n"
                                            if clkRst.getElementsByTagName('RstType')[0].firstChild.data == "asynch":
                                                elsif_syntax = vhdl_root.getElementsByTagName("elsifStatement")[
                                                    0].firstChild.data
                                                elsif_syntax = elsif_syntax.replace("$edge", clkEdge)
                                                if ceInSeq != "":
                                                    clkgen_defaults = "\tif " + ceInSeq + " = '1' then -- enable register\n" + clkgen_defaults + "\tend if;\n"
                                                    clkgen_defaults = indent(clkgen_defaults, '    ')
                                                elsif_syntax = elsif_syntax.replace("$default_assignments",
                                                                                    clkgen_defaults)
                                                if_syntax = if_syntax.replace("$else", elsif_syntax)
                                                clkgen_defaults = "\t" + if_syntax + "\n"
                                            else:
                                                else_syntax = vhdl_root.getElementsByTagName("elseStatement")[
                                                    0].firstChild.data
                                                if ceInSeq != "":
                                                    clkgen_defaults = "\tif " + ceInSeq + " = '1' then -- enable register\n" + clkgen_defaults + "\tend if;\n"
                                                    clkgen_defaults = indent(clkgen_defaults, '    ')
                                                else_syntax = else_syntax.replace("$default_assignments",
                                                                                  clkgen_defaults)
                                                if_syntax = if_syntax.replace("$else", else_syntax)
                                                clkgen_defaults = "\t" + if_syntax + "\n"
                                                clkgen_defaults = indent(clkgen_defaults, '    ')
                                                clkif_syntax = clkif_syntax.replace("$default_assignments",
                                                                                    clkgen_defaults)
                                                clkgen_defaults = "\t" + clkif_syntax + "\n"
                                        else:
                                            clkif_syntax = clkif_syntax.replace("$default_assignments", clkgen_defaults)
                                            clkgen_defaults = "\t" + clkif_syntax + "\n"
                                    clkgen_defaults = clkgen_defaults.rstrip()
                                    process_syntax = process_syntax.replace("$default_assignments", clkgen_defaults)
                                    gen_seq_process += process_syntax + "\n\n"
                                else:
                                    note_syntax = vhdl_root.getElementsByTagName("note")[0].firstChild.data
                                    note_syntax = note_syntax.replace("$notes", notes)
                                    if notes == "None":
                                        gen_defaults += ""
                                        if caseEmpty == False:
                                            case_syntax = case_syntax.replace("$whenCase", whenCase)
                                            gen_defaults += "\n" + case_syntax
                                    else:
                                        gen_defaults += "\n" + note_syntax
                                    gen_defaults = gen_defaults.rstrip()
                                    process_syntax = process_syntax.replace("$default_assignments", gen_defaults)
                                    gen_process += process_syntax + "\n\n"


                        elif (child.nodeType == arch_node[0].ELEMENT_NODE and child.tagName == "concurrentStmt"):

                            for statement in child.getElementsByTagName("statement"):
                                signals = statement.firstChild.data.split(",")
                                notes = child.getElementsByTagName("note")[0].firstChild.data
                                if notes != "None":
                                    notes = re.sub(r'\s+', ' ', notes)
                                    notes = notes.replace("&amp;", "&")
                                    notes = notes.replace("&quot;", "\"")
                                    notes = notes.replace("&apos;", "\'")
                                    notes = notes.replace("&lt;", "<")
                                    notes = notes.replace("&#x9;", "\t")
                                    notes = notes.replace("&gt;", ">")
                                    notes = notes.replace("&#44;", ",")
                                    notes = notes.replace("[", "(")
                                    notes = notes.replace("]", ")")
                                    notes = notes.replace(":", " downto ")
                                    notes = notes.replace("'", "")
                                    notes = re.sub(r'\s+', ' ', notes)
                                    notes = notes.replace("&#10;", "\n--- ")

                                    pattern = r'(?<!downto\s)(?<!\d)([01]+)(?!\d)(?!\s*downto)'

                                    notes = re.sub(pattern, lambda m: f"'{m.group(1)}'" if len(
                                        m.group(1)) == 1 else f'"{m.group(1)}"', notes)

                                    pattern1 = r"(\(|\w+)(['\"])(\d+)\2\)"
                                    match = re.search(pattern1, notes)
                                    while match:
                                        notes = notes.replace(match.group(), match.group(1) + match.group(3) + ")")
                                        match = re.search(pattern1, notes)
                                    pattern2 = r"[^\s]+['\"]\d+['\"]"
                                    notes = re.sub(pattern2,
                                                   lambda match: match.group(0).replace("'", "").replace('"', ""),
                                                   notes)
                                    # Define a regular expression pattern to match the content inside { }
                                    pattern3 = r'\w+\{([^}]+)\}'
                                    # Use re.sub to replace the matched content inside { }
                                    notes = re.sub(pattern3, r'(others => \1)', notes)

                                    note_syntax = vhdl_root.getElementsByTagName("concNote")[0].firstChild.data
                                    note_syntax = note_syntax.replace("$concurrentstmt_label",
                                                                      child.getElementsByTagName("label")[
                                                                          0].firstChild.data)
                                    note_syntax = note_syntax.replace("$output_signal", signals[0])
                                    note_syntax = note_syntax.replace("$notes", notes)
                                    gen_conc += note_syntax + "\n\n"
                                else:
                                    gen_stmts = ""
                                    conc_syntax = vhdl_root.getElementsByTagName("concurrentstmt")[0].firstChild.data
                                    conc_syntax = conc_syntax.replace("$concurrentstmt_label",
                                                                      child.getElementsByTagName("label")[
                                                                          0].firstChild.data)
                                    assign_syntax = vhdl_root.getElementsByTagName("sigAssign")[0].firstChild.data

                                    assign_syntax = assign_syntax.replace("$output_signal", signals[0])
                                    value = signals[1]
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
                                    value = value.replace("&amp;", "&")
                                    value = value.replace("&quot;", "\"")
                                    value = value.replace("&apos;", "\'")
                                    value = value.replace("&lt;", "<")
                                    value = value.replace("&#x9;", "\t")
                                    value = value.replace("&gt;", ">")
                                    assign_syntax = assign_syntax.replace("$value", value)

                                    gen_stmts += assign_syntax
                                    conc_syntax = conc_syntax.replace("$statement", gen_stmts)
                                    gen_conc += conc_syntax
                            gen_conc += "\n"

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
                            instances.append(child.getElementsByTagName("model")[0].firstChild.data)
                            gen_instance += instance_syntax + "\n"

                        child = next
                    gen_archs += gen_process
                    gen_archs += gen_conc
                    gen_archs += gen_seq_process
                    gen_archs += gen_instance
                    arch_syntax = vhdl_root.getElementsByTagName("architecture")[0].firstChild.data
                    arch_name_node = arch_node[0].getElementsByTagName("archName")

                    arch_name = "Combinational"

                    if len(arch_name_node) != 0 and arch_name_node[0].firstChild is not None:
                        arch_name = arch_name_node[0].firstChild.data

                    gen_arch = arch_syntax.replace("$arch_name", arch_name)
                    gen_arch = gen_arch.replace("$comp_name", entity_name)
                    gen_arch = gen_arch.replace("$int_sig_declaration", gen_int_sig)
                    gen_arch = gen_arch.replace("$arch_elements", gen_archs[:-1])
                    gen_vhdl += gen_library
                    chatgpt_vhdl += gen_library
                    gen_vhdl += "use work.MainPackage.all;"
                    chatgpt_vhdl += "use work.MainPackage.all;"
                    # Entity Section placement
                    gen_vhdl += "\n\n" + gen_entity + "\n\n"
                    chatgpt_vhdl += "\n\n" + gen_entity + "\n\n"
                    gen_vhdl += gen_arch
                    chatgpt_vhdl += gen_arch
                    gen_vhdl = gen_vhdl.replace("&#10;", "\n")
                    gen_vhdl = gen_vhdl.replace("&amp;", "&")
                    gen_vhdl = gen_vhdl.replace("&amp;", "&")
                    gen_vhdl = gen_vhdl.replace("&quot;", "\"")
                    gen_vhdl = gen_vhdl.replace("&apos;", "\'")
                    gen_vhdl = gen_vhdl.replace("&lt;", "<")
                    gen_vhdl = gen_vhdl.replace("&#x9;", "\t")
                    gen_vhdl = gen_vhdl.replace("&gt;", ">")
                    gen_vhdl = gen_vhdl.replace("&#44;", ",")

                    chatgpt_vhdl = chatgpt_vhdl.replace("&#10;", "\n")
                    chatgpt_vhdl = chatgpt_vhdl.replace("&amp;", "&")
                    chatgpt_vhdl = chatgpt_vhdl.replace("&amp;", "&")
                    chatgpt_vhdl = chatgpt_vhdl.replace("&quot;", "\"")
                    chatgpt_vhdl = chatgpt_vhdl.replace("&apos;", "\'")
                    chatgpt_vhdl = chatgpt_vhdl.replace("&lt;", "<")
                    chatgpt_vhdl = chatgpt_vhdl.replace("&#x9;", "\t")
                    chatgpt_vhdl = chatgpt_vhdl.replace("&gt;", ">")
                    chatgpt_vhdl = chatgpt_vhdl.replace("&#44;", ",")

                    chatgpt_header = chatgpt_header.replace("&#10;", "\n")
                    chatgpt_header = chatgpt_header.replace("&amp;", "&")
                    chatgpt_header = chatgpt_header.replace("&amp;", "&")
                    chatgpt_header = chatgpt_header.replace("&quot;", "\"")
                    chatgpt_header = chatgpt_header.replace("&apos;", "\'")
                    chatgpt_header = chatgpt_header.replace("&lt;", "<")
                    chatgpt_header = chatgpt_header.replace("&#x9;", "\t")
                    chatgpt_header = chatgpt_header.replace("&gt;", ">")
                    chatgpt_header = chatgpt_header.replace("&#44;", ",")

        return entity_name, gen_vhdl, instances, chatgpt_header, chatgpt_vhdl

    def create_vhdl_file(self, filesNumber):
        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        root = minidom.parse(proj_path + "/HDLGenPrj/" + proj_name + ".hdlgen")
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
        VHDLModel = "None"
        chatgpt = hdlDesign[0].getElementsByTagName('chatgpt')[0]
        if chatgpt.hasChildNodes():
            commands_node = chatgpt.getElementsByTagName('commands')[0]
            VHDLModel = commands_node.getElementsByTagName('VHDLModel')[0].firstChild.data
            VHDLModel = VHDLModel.replace("&#10;", "\n")
            VHDLModel = VHDLModel.replace("&amp;", "&")
            VHDLModel = VHDLModel.replace("&quot;", "\"")
            VHDLModel = VHDLModel.replace("&apos;", "\'")
            VHDLModel = VHDLModel.replace("&lt;", "<")
            VHDLModel = VHDLModel.replace("&#x9;", "\t")
            VHDLModel = VHDLModel.replace("&gt;", ">")
            VHDLModel = VHDLModel.replace("&#44;", ",")
            # does not display lines starting with ~
            lines = VHDLModel.split('\n')
            filtered_lines = [line for line in lines if not line.startswith('~')]
            VHDLModel = '\n'.join(filtered_lines)
        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        entity_name, vhdl_code, instances, chatgpt_header, chatgpt_vhdl = self.generate_vhdl()
        chatgpt_vhdl = VHDLModel + "\n\n" + vhdl_code
        vhdl_file_path = os.path.join(proj_path, "VHDL", "model", entity_name + ".vhd")
        vhdl_file_HDLGen_path = os.path.join(proj_path, "VHDL", "model", entity_name + "_backup.vhd")
        chatgpt_header_file_path = os.path.join(proj_path, "VHDL", "ChatGPT", entity_name + "_VHDL_header_ChatGPT.txt")
        chatgpt_vhdl_file_path = os.path.join(proj_path, "VHDL", "ChatGPT", entity_name + "_VHDL_ChatGPT.txt")
        chatgpt_header_HDLGen_file_path = os.path.join(proj_path, "VHDL", "ChatGPT", "Backups",
                                                       entity_name + "_VHDL_header_ChatGPT_backup.txt")
        chatgpt_vhdl_HDLGen_file_path = os.path.join(proj_path, "VHDL", "ChatGPT", "Backups",
                                                     entity_name + "_VHDL_ChatGPT_backup.txt")

        if "1" in filesNumber:
            base_name, extension = os.path.splitext(vhdl_file_HDLGen_path)
            new_filename = vhdl_file_HDLGen_path
            if os.path.isfile(new_filename):
                # File already exists, modify the name
                index = 1
                while os.path.isfile(new_filename):
                    index += 1
                    new_filename = f"{base_name}_{index}{extension}"
            try:
                # Writing xml file
                with open(vhdl_file_path, 'r') as source:
                    with open(new_filename, "w") as f:
                        content = source.read()
                        f.write(content)
                    print("VHDL Backup Model successfully generated at ", new_filename)
            except FileNotFoundError:
                with open(new_filename, "w") as f:
                    f.write(vhdl_code)
                print("VHDL Backup Model successfully generated at ", new_filename)
        if "0" in filesNumber:
            # Writing xml file
            with open(vhdl_file_path, "w") as f:
                f.write(vhdl_code)
            print("VHDL Model successfully generated at ", vhdl_file_path)
        if "5" in filesNumber:
            base_name, extension = os.path.splitext(chatgpt_header_HDLGen_file_path)
            new_filename = chatgpt_header_HDLGen_file_path
            if os.path.isfile(new_filename):
                # File already exists, modify the name
                index = 1
                while os.path.isfile(new_filename):
                    index += 1
                    new_filename = f"{base_name}_{index}{extension}"
            try:
                # Writing xml file
                with open(chatgpt_header_file_path, 'r') as source:
                    with open(new_filename, "w") as f:
                        content = source.read()
                        f.write(content)
                    print("ChatGPT VHDL title Backup successfully generated at ", new_filename)
            except FileNotFoundError:
                with open(new_filename, "w") as f:
                    f.write(chatgpt_header)
                print("ChatGPT VHDL title Backup successfully generated at ", new_filename)
        if "4" in filesNumber:
            # Writing xml file
            with open(chatgpt_header_file_path, "w") as f:
                f.write(chatgpt_header)
            pyperclip.copy(chatgpt_header)
            print("ChatGPT VHDL title successfully generated at ", chatgpt_header_file_path)
        if "7" in filesNumber:
            base_name, extension = os.path.splitext(chatgpt_vhdl_HDLGen_file_path)
            new_filename = chatgpt_vhdl_HDLGen_file_path
            if os.path.isfile(new_filename):
                # File already exists, modify the name
                index = 1
                while os.path.isfile(new_filename):
                    index += 1
                    new_filename = f"{base_name}_{index}{extension}"
            try:
                # Writing xml file
                with open(chatgpt_vhdl_file_path, 'r') as source:
                    with open(new_filename, "w") as f:
                        content = source.read()
                        f.write(content)
                    print("ChatGPT VHDL model Backup successfully generated at ", new_filename)
            except FileNotFoundError:
                with open(new_filename, "w") as f:
                    f.write(chatgpt_vhdl)
                print("ChatGPT VHDL model Backup successfully generated at ", new_filename)
        if "6" in filesNumber:
            # Writing xml file
            with open(chatgpt_vhdl_file_path, "w") as f:
                f.write(chatgpt_vhdl)
            pyperclip.copy(chatgpt_vhdl)
            print("ChatGPT VHDL model successfully generated at ", chatgpt_vhdl_file_path)
        self.entity_name = entity_name

        # return overwrite, instances
        return instances

    def create_tcl_file(self, lang, instances):
        print("creating tcl")

        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        if lang == "VHDL":
            self.tcl_path = proj_path + "/VHDL/AMDprj/" + self.entity_name + ".tcl"
            ext = "vhd"
        else:
            self.tcl_path = proj_path + "/Verilog/AMDprj/" + self.entity_name + ".tcl"
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
        mainPackagePath = "add_files -norecurse  "
        mainPackagePath = mainPackagePath + ProjectManager.get_package_vhd()
        mainPackagePath = mainPackagePath.replace("\\", "/")
        if lang == "VHDL":
            tcl_vivado_code = tcl_vivado_code.replace("$arrayPackage", mainPackagePath)
        else:
            tcl_vivado_code = tcl_vivado_code.replace("$arrayPackage", "")
        files = ""
        mainPackageDir = ProjectManager.get_package_hdlgen()
        root = minidom.parse(mainPackageDir)
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
        components = hdlDesign[0].getElementsByTagName("components")
        comp_nodes = components[0].getElementsByTagName('component')
        self.dirs = []

        packageDirs = []
        for i in range(0, len(comp_nodes)):
            packageDirs.append([comp_nodes[i].getElementsByTagName('model')[0].firstChild.data,
                                comp_nodes[i].getElementsByTagName('dir')[
                                    0].firstChild.data])

        while (instances):
            instances_unchanged = False
            for namedir in packageDirs:
                if namedir[0] == instances[0]:
                    instances_unchanged = True
                    dir = namedir[1]
                    dir = dir.replace("/VHDL/model/" + namedir[0] + ".vhd",
                                      "/" + lang + "/model/" + namedir[0] + "." + ext)

                    if not os.path.exists(ProjectManager.get_proj_environment() + dir):
                        print(ProjectManager.get_proj_environment() + dir + " Does not exist")
                        msgBox = QMessageBox()
                        msgBox.setWindowTitle("Alert")
                        msgBox.setText(ProjectManager.get_proj_environment() + dir + "\nDoes not exist")
                        msgBox.exec_()
                    self.dirs.append(dir)
                    directories = dir.split('/')

                    # Remove the last two elements (folders)
                    dir = '/'.join(directories[:-3])
                    hdlgenDir = ProjectManager.get_proj_environment() + dir + "/HDLgenPrj/" + namedir[0] + ".hdlgen"
                    modelRoot = minidom.parse(hdlgenDir)
                    modelHDLGen = modelRoot.documentElement
                    modelHdlDesign = modelHDLGen.getElementsByTagName("hdlDesign")
                    modelComponents = modelHdlDesign[0].getElementsByTagName("architecture")
                    modelComp_nodes = modelComponents[0].getElementsByTagName('instance')
                    for i in range(0, len(modelComp_nodes)):
                        instances.append(modelComp_nodes[i].getElementsByTagName('model')[0].firstChild.data)
                    instances.pop(0)
                    if len(instances) == 0:
                        break
            if instances_unchanged == False:
                break
        if self.dirs is not None:
            for dir in self.dirs:
                files += "add_files -norecurse  " + ProjectManager.get_proj_environment() + dir + " \n"
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

    def create_quartus_tcl_file(self, lang, instances):
        print("creating tcl")

        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        if lang == "VHDL":
            self.tcl_path = proj_path + "/VHDL/IntelPrj/" + self.entity_name + ".tcl"
            ext = "vhd"
        else:
            self.tcl_path = proj_path + "/Verilog/IntelPrj/" + self.entity_name + ".tcl"
            ext = "v"
        tcl_database_path = "./Generator/TCL_Database/tcl_database.xml"

        tcl_database = minidom.parse(tcl_database_path)
        tcl_root = tcl_database.documentElement

        tcl_file_template = tcl_root.getElementsByTagName("quartus_tcl")[0]
        tcl_file_template = tcl_file_template.firstChild.data
        comp = self.entity_name
        tb_file_name = self.entity_name + "_TB"
        tcl_quartus_code = tcl_file_template.replace("$tcl_path", self.tcl_path)
        tcl_quartus_code = tcl_quartus_code.replace("$comp_name", comp)
        wd = os.getcwd()
        wd = wd.replace("\\", "/")
        mainPackagePath = "add_files -norecurse  "  # + wd
        mainPackagePath = mainPackagePath + ProjectManager.get_package_vhd()
        mainPackagePath = mainPackagePath.replace("\\", "/")
        # if self.includeArrays == True:
        # tcl_quartus_code = tcl_quartus_code.replace("$arrayPackage", mainPackagePath)
        # else:
        # tcl_quartus_code = tcl_quartus_code.replace("$arrayPackage","")
        files = ""
        # mainPackageDir = os.getcwd() + "\HDLDesigner\Package\mainPackage.hdlgen"
        mainPackageDir = ProjectManager.get_package_hdlgen()
        root = minidom.parse(mainPackageDir)
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
        components = hdlDesign[0].getElementsByTagName("components")
        comp_nodes = components[0].getElementsByTagName('component')
        self.dirs = []
        # for i in range(0, len(comp_nodes)):
        #   if comp_nodes[i].getElementsByTagName('model')[0].firstChild.data in instances:
        #       dir = comp_nodes[i].getElementsByTagName('dir')[0].firstChild.data
        #       self.dirs.append(dir)
        # if self.dirs is not None:
        #    for dir in self.dirs:
        #        files += "add_files -norecurse  "+ dir + " \n"
        #    tcl_quartus_code = tcl_quartus_code.replace("$files", files)
        # else:
        #    tcl_quartus_code = tcl_quartus_code.replace("$files", "")
        # tcl_quartus_code = tcl_quartus_code.replace("$tb_name", tb_file_name)
        tcl_quartus_code = tcl_quartus_code.replace("$proj_name", proj_name)
        # proj_path = "{" + proj_path + "}"
        tcl_quartus_code = tcl_quartus_code.replace("$proj_dir", proj_path)
        tcl_quartus_code = tcl_quartus_code.replace("$lang", lang)
        tcl_quartus_code = tcl_quartus_code.replace("$ext", ext)

        # Writing xml file
        with open(self.tcl_path, "w") as f:
            f.write(tcl_quartus_code)

        print("TCL file successfully generated at ", self.tcl_path)

        return 1

    def run_tcl_file(self, lang, edaTool):
        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        subprocess.Popen("cd " + proj_path, shell=True)
        vivado_bat_file_path = ProjectManager.get_vivado_bat_path()
        intel_exe_file_path = ProjectManager.get_intel_exe_path()
        if edaTool == "Vivado":
            if lang == "VHDL":
                model_path = proj_path + "\VHDL\model\\" + str(ProjectManager.get_proj_name()) + ".vhd"
                tcl_path = proj_path + "\VHDL\AMDprj\\" + str(ProjectManager.get_proj_name()) + ".tcl"
                tb_path = proj_path + "\VHDL\\testbench\\" + str(ProjectManager.get_proj_name()) + "_TB.vhd"
            elif lang == "Verilog":
                model_path = proj_path + "\Verilog\model\\" + str(ProjectManager.get_proj_name()) + ".v"
                tcl_path = proj_path + "\Verilog\AMDprj\\" + str(ProjectManager.get_proj_name()) + ".tcl"
                tb_path = proj_path + "\Verilog\\testbench\\" + str(ProjectManager.get_proj_name()) + "_TB.v"
            if os.path.exists(tcl_path):
                if os.path.exists(model_path):
                    if os.path.exists(tb_path):
                        start_vivado_cmd = vivado_bat_file_path + " -source " + tcl_path
                        subprocess.Popen(start_vivado_cmd, shell=True)
                    else:
                        msgBox = QMessageBox()
                        msgBox.setWindowTitle("Alert")
                        msgBox.setText("No testbench found!\nDo you want to go back and generate the testbench?")
                        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        msgBox.setDefaultButton(QMessageBox.Yes)

                        result = msgBox.exec_()

                        if result == QMessageBox.No:
                            start_vivado_cmd = vivado_bat_file_path + " -source " + tcl_path
                            subprocess.Popen(start_vivado_cmd, shell=True)
                else:
                    msgBox = QMessageBox()
                    msgBox.setWindowTitle("Alert")
                    msgBox.setText("No model found!\nPlease Generate HDL Model Template!")
                    msgBox.exec_()
            else:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("No TCL script found!\nPlease generate model and try again")


        else:
            if lang == "VHDL":
                tcl_path = proj_path + "\VHDL\Intelprj\\" + str(ProjectManager.get_proj_name()) + ".tcl"

            elif lang == "Verilog":

                tcl_path = proj_path + "\Verilog\Intelprj\\" + str(ProjectManager.get_proj_name()) + ".tcl"
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("Intel Quartus for HDLGen is still a work in progress")
            msgBox.exec_()
            if os.path.exists(tcl_path):

                start_quartus_cmd = intel_exe_file_path + " -source " + tcl_path
                subprocess.Popen(start_quartus_cmd, shell=True)

            else:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("Please Generate model and TB HDL")
                msgBox.exec_()

    def create_vhdl_testbench_code(self):
        tb_code = ""
        chatgpt_tb = ""
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
        testbench_node = hdl_design[0].getElementsByTagName("testbench")

        if len(testbench_node) != 0 and testbench_node[0].firstChild is not None:
            self.tb_note = testbench_node[0].getElementsByTagName('TBNote')[0]
            self.tb_note = self.tb_note.firstChild.nodeValue if self.tb_note.firstChild.nodeValue != "None" else None
            self.tb_note = self.tb_note.replace("&#10;", "\n").replace("&amp;", "&").replace("&quot;", "\"").replace("&apos;", "\'").replace("&lt;", "<").replace("&#x9;", "\t").replace("&gt;", ">").replace("&#44;", "\,")

            # Load the testbench table as testbench_table[row][col]
            self.testbench_table = self.tb_note.split("\n")
        
            # Remove any blank rows from the testbench_table, sometimes the XML parser
            # will insert blank lines when pretty-printing the HDLGen XML file
            self.testbench_table = [row for row in self.testbench_table if row != ""]
            for idx, row in enumerate(self.testbench_table):
                self.testbench_table[idx] = row.split("\t")

            # Generate VHDL Testbench based on Testplan
            # No. of tests = length of first row minus 3 to remove the first 4 headers (Signals, Mode, Width, Radix)
            # No. of tests should start at 1 and continue until the Nth test
            # No. of rows = len(testbench)
            # No. of cols = len(testbench[0])
            testbench_code = ""
            for test in range(1, len(self.testbench_table[0]) - 3):
                testbench_code += f'\t-- BEGIN Test Number {test}\n'
                # Print the test number and the comment for that test
                testbench_code += f'\ttestNo <= {test}; -- {self.testbench_table[len(self.testbench_table) - 2][test+3]}\n'

                # Loop over each row in the testbench_table, and check if the 2nd entry in the row is "in", indicating an Input signal
                for _, row in enumerate(self.testbench_table):
                    if row[1] == "in":
                        # If an input signal is found, add the VHDL to set that input to the corrosponding value in the test table
                        testbench_code += f'\t{row[0]} <= {"h" if row[3] == "hex" else ""}\"{row[test + 3]}\";\n'

                # Add the wait statement, inserting the delay value for the test being assembled
                testbench_code += f'\twait for ({self.testbench_table[len(self.testbench_table) - 3][test + 3]} * period);\n'

                # Loop over each row in the testbench_table, and check if the 2nd entry is 
                for _, row in enumerate(self.testbench_table):
                    if row[1] == "out":
                        testbench_code += f'\tassert {row[0]} = {"h" if row[3] == "hex" else ""}\"{row[test+3]}\" report \"TestNo {test} {row[0]} mismatch\" severity warning;\n'

                testbench_code += f'\t-- END Test Number {test}\n\n'

        UUTEnt = ""
        header_node = hdl_design[0].getElementsByTagName("header")
        comp_node = header_node[0].getElementsByTagName("compName")[0]
        entity_name = comp_node.firstChild.data

        with open(wcfg_database_path, "r") as f:
            xml_string = f.read()

        head_regex = r"<head>(.*?)</head>"
        head_contents = re.search(head_regex, xml_string, re.DOTALL).group(1)

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
        arrayPackage = False
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
                    type = type.replace("bus", "std_logic_vector")
                elif type[0:6] == "array,":
                    type = type.split(",")
                    type = type[1]

                signal_declare_syntax = signal_declare_syntax.replace("$type", type)
                io_signal_declare_syntax = io_signal_declare_syntax.replace("$type", type)
                name = signal.getElementsByTagName('name')[0].firstChild.data
                type = signal.getElementsByTagName('type')[0].firstChild.data
                size = ""
                UUTEnt_content = re.sub(r"\[componentName]", entity_name, UUTEnt_contents)
                UUTEnt_content = re.sub(r"\[signal]", name, UUTEnt_content)

                if type[0:6] == "array,":
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
                UUTEnt_content = re.sub(r"\[type]", type, UUTEnt_content)
                UUTEnt_content = re.sub(r"\[size]", size, UUTEnt_content)
                UUTEnt += UUTEnt_content

                if signal.getElementsByTagName('mode')[0].firstChild.data == "in":
                    if signal.getElementsByTagName('name')[0].firstChild.data != "clk" and \
                            signal.getElementsByTagName('name')[0].firstChild.data != "rst":
                        if signal.getElementsByTagName('type')[0].firstChild.data == "single bit":
                            inputArray.append(signal.getElementsByTagName('name')[0].firstChild.data)
                            inputsToZero += "\t" + signal.getElementsByTagName('name')[
                                0].firstChild.data + " <= \'0\';\n"
                            inputsToOne += "\t" + signal.getElementsByTagName('name')[
                                0].firstChild.data + " <= \'1\';\n"
                        elif signal.getElementsByTagName('type')[0].firstChild.data[0:3] == "bus":
                            inputsToZero += "\t" + signal.getElementsByTagName('name')[
                                0].firstChild.data + " <= (others => \'0\');\n"
                            inputsToOne += "\t" + signal.getElementsByTagName('name')[
                                0].firstChild.data + " <= (others => \'1\');\n"
                        else:
                            inputsToZero += "\t" + signal.getElementsByTagName('name')[
                                0].firstChild.data + " <= (others =>(others => \'0\'));\n"
                            arrayPackage = True
                else:
                    if signal.getElementsByTagName('type')[0].firstChild.data != "single bit" and \
                            signal.getElementsByTagName('type')[0].firstChild.data[0:3] != "bus":
                        arrayPackage = True
                signal_description = signal.getElementsByTagName('description')[
                    0].firstChild.data
                entity_signal_description += "-- " + signal.getElementsByTagName('name')[
                    0].firstChild.data + "\t" + signal_description + "\n"
                gen_signals += "\t" + signal_declare_syntax + "\n"
                io_port_map += "\t" + io_port_map_syntax + "\n"
                if signal.getElementsByTagName('name')[0].firstChild.data == "clk" or \
                        signal.getElementsByTagName('name')[0].firstChild.data == "rst":
                    clkrst = clkrst + 1
                else:
                    io_signals += io_signal_declare_syntax + "\n"
            wcfg += UUT_contents
            wcfg += UUTEnt
            io_port_map = io_port_map.rstrip()
            io_port_map = io_port_map[0:-1]

            io_signals = io_signals.rstrip()
            chatgpt_tb = "signal testNo: integer;\n"
            chatgpt_tb += "signal period: time := 20 ns;\n"
            chatgpt_tb += io_signals
            other_signals = ""
            if clkrst > 0:
                other_signals = "signal clk: std_logic := '1';\n"
            if clkrst == 2:
                other_signals += "signal rst: std_logic;        \n"

            control_signals = "constant period: time := 20 ns; -- Default simulation time. Use as simulation delay constant, or clk period if sequential model ((50MHz clk here)\n"

            gen_signals = gen_signals.rstrip()
            gen_signals = gen_signals[0:-1]

            entity_syntax = vhdl_root.getElementsByTagName("entity")
            gen_entity = "-- Testbench entity declaration\n"
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
                        size = ""
                    elif type == "single bit":
                        size = ""
                        type = "logic"
                    elif type[0:6] == "array,":
                        self.includeArrays = True
                        size = ""
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
                    elif type[0:7] == "integer":
                        size = ""
                        type = "other"
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

                gen_header = "-- Title Section Start\n"
                gen_header += "-- VHDL Testbench - " + entity_name + "_TB\n"
                gen_header += "-- Generated by HDLGen-ChatGPT on " + str(
                    datetime.now().strftime("%d-%B-%Y")) + " at " + str(datetime.now().strftime("%H:%M")) + "\n"
                gen_header += "-- Github: https://github.com/HDLGen-ChatGPT/HDLGen-ChatGPT\n\n"
                gen_header += "-- Component Name:\t" + entity_name + "\n"
                title = header_node[0].getElementsByTagName("title")[0].firstChild.data
                gen_header += "-- Title:\t" + (title if title != "null" else "") + "\n\n"

                authors = header_node[0].getElementsByTagName("authors")[0].firstChild.data
                gen_header += "-- Author(s):\t" + (authors if authors != "null" else "") + "\n"
                company = header_node[0].getElementsByTagName("company")[0].firstChild.data
                gen_header += "-- Organisation:\t" + (company if company != "null" else "") + "\n"
                email = header_node[0].getElementsByTagName("email")[0].firstChild.data
                gen_header += "-- Email:\t" + (email if email != "null" else "") + "\n"
                gen_header += "-- Date:\t" + header_node[0].getElementsByTagName("date")[
                    0].firstChild.data + "\n\n"
                gen_header += "-- Description:\t Refer to component's HDL Model for description and signal dictionary\n"
                gen_header += "-- Title Section End\n\n"
                tb_code += gen_header

                # Libraries Section
                libraries_node = vhdl_root.getElementsByTagName("libraries")
                libraries = libraries_node[0].getElementsByTagName("library")
                gen_library = "-- Library declarations\n"
                for library in libraries:
                    gen_library += library.firstChild.data + "\n"
                if arrayPackage == True:
                    gen_library += "use work.MainPackage.all;"
                gen_library += "\n"
                tb_code += gen_library

                # Entity declaration
                gen_entity = gen_entity.replace("$comp_name", entity_name)
                tb_code += gen_entity + "\n\n"
                tbSignalDeclaration = ""
                if sig_decl != "":
                    tbSignalDeclaration += sig_decl + "\n"
                if other_signals != "":
                    tbSignalDeclaration += other_signals + "\n"
                tbSignalDeclaration += io_signals + "\n\n" + control_signals
                # Architecture section

                # Process
                arch_node = hdl_design[0].getElementsByTagName("architecture")
                gen_process = ""

                if clkrst > 0:
                    gen_process += "-- Generate clk signal, when endOfSim = FALSE / 0\n"
                    gen_process += "clkStim: clk <= not clk after period/2 when endOfSim = false else '0';\n\n"

                gen_process += "-- Instantiate the Unit Under Test (UUT)\n"
                gen_process += "-- Map the component's internal signals to testbench signals\n"
                gen_process += "UUT: " + entity_name + "\n"
                gen_process += "port map\n\t(\n"
                gen_process += io_port_map + "\n\t);\n\n"
                gen_process += "-- Signal stimulus process\n-- Process automatically executes at start of simulation due to empty sensitivity list.\n-- Process halts at the \'wait;\' statement"
                gen_process += "stim_p: process\n"
                gen_process += "begin\n"
                gen_process += "\treport \"%N Simulation start, time = \"& time'image(now);\n\n"
                gen_process += "\t-- Apply default INPUT signal values.\n"
                gen_process += "\t-- Each stimulus signal change occurs 0.2*period after the active low-to-high clk edge\n"
                gen_process += "\t-- if signal type is \'std_logic\', use '0'\n\t-- if signal type is \'std_logic_vector\' use (others => '0')\n\t-- if signal type is \'integer\' use 0\n"
                gen_process += inputsToZero

                if clkrst == 2:
                    gen_process += "\treport \"Assert and toggle rst\";\n\ttestNo <= 0;\n\trst    <= '1';\n"
                    gen_process += "\twait for period*1.2; -- assert rst for 1.2*period, deasserting rst 0.2*period after active clk edge\n"
                    gen_process += "\trst   <= '0';\n\twait for period; -- wait 1 clock period\n\t"
                
                gen_process += "\n\t-- START Testbench stimulus\n"

                gen_process += testbench_code if testbench_code else None

                gen_process += "\n\t-- END Testbench stimulus\n"

                gen_process += "\n\treport \"%N Simulation end, time = \"& time'image(now);\n"
                gen_process += "\t-- Assert \'endOfSim\' flag to stop the clock signal\n\tendOfSim <= TRUE;\n"
                gen_process += "\twait; -- Wait forever\n"

                if len(arch_node) != 0 and arch_node[0].firstChild is not None:
                    arch_syntax = vhdl_root.getElementsByTagName("architecture")[0].firstChild.data

                    gen_arch = arch_syntax.replace("$comp_name", entity_name)
                    gen_arch = gen_arch.replace("$component_declarations",
                                                "-- unit under test (UUT) component declaration. Identical to component entity, with 'entity' replaced with 'component'")
                    gen_arch = gen_arch.replace("$port", gen_signals)
                    gen_arch = gen_arch.replace("$tbSignalDeclaration", tbSignalDeclaration)
                    gen_arch = gen_arch.replace("$arch_elements", gen_process[:-1])

                    tb_code += gen_arch

        return entity_name, tb_code, wcfg, chatgpt_tb

    def create_testbench_file(self, filesNumber):
        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        root = minidom.parse(
            os.path.join(proj_path, "HDLGenPrj", proj_name + ".hdlgen")
        )
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
        testbench_node = hdlDesign[0].getElementsByTagName('testbench')
        if len(testbench_node) != 0 and testbench_node[0].firstChild is not None:
            tb_node = testbench_node[0].getElementsByTagName('TBNote')[0]
            self.note = tb_node.firstChild.nodeValue
            self.note = self.note.replace("&#10;", "\n")
            self.note = self.note.replace("&amp;", "&")
            self.note = self.note.replace("&quot;", "\"")
            self.note = self.note.replace("&apos;", "\'")
            self.note = self.note.replace("&lt;", "<")
            self.note = self.note.replace("&#x9;", "\t")
            self.note = self.note.replace("&gt;", ">")
            self.note = self.note.replace("&#44;", ",")
        else:
            self.note = "--- No Test Plan Created"
        chatgpt = hdlDesign[0].getElementsByTagName('chatgpt')[0]
        VHDLTestbench = "None"
        if chatgpt.hasChildNodes():
            commands_node = chatgpt.getElementsByTagName('commands')[0]
            VHDLTestbench = commands_node.getElementsByTagName('VHDLTestbench')[0].firstChild.data
            VHDLTestbench = VHDLTestbench.replace("&#10;", "\n")
            VHDLTestbench = VHDLTestbench.replace("&amp;", "&")
            VHDLTestbench = VHDLTestbench.replace("&quot;", "\"")
            VHDLTestbench = VHDLTestbench.replace("&apos;", "\'")
            VHDLTestbench = VHDLTestbench.replace("&lt;", "<")
            VHDLTestbench = VHDLTestbench.replace("&#x9;", "\t")
            VHDLTestbench = VHDLTestbench.replace("&gt;", ">")
            VHDLTestbench = VHDLTestbench.replace("&#44;", ",")
            # does not display lines starting with ~
            lines = VHDLTestbench.split('\n')
            filtered_lines = [line for line in lines if not line.startswith('~')]
            VHDLTestbench = '\n'.join(filtered_lines)
        entity_name, vhdl_tb_code, waveform, chatgpt_tb = self.create_vhdl_testbench_code()
        chatgpt_tb = VHDLTestbench + "\n\n" + chatgpt_tb + "\n\n" + self.note
        vhdl_tb_path = os.path.join(proj_path, "VHDL", "testbench", entity_name + "_TB.vhd")
        vhdl_tb_HDLGen_path = os.path.join(proj_path, "VHDL", "testbench", entity_name + "_TB_backup.vhd")
        waveform_path = os.path.join(proj_path, "VHDL", "AMDprj", entity_name + "_TB_behav.wcfg")
        chatgpt_vhdl_file_path = os.path.join(proj_path, "VHDL", "ChatGPT", entity_name + "_VHDL_TB_ChatGPT.txt")
        chatgpt_vhdl_HDLGen_file_path = os.path.join(proj_path, "VHDL", "ChatGPT", "Backups",
                                                     entity_name + "_VHDL_TB_ChatGPT_backup.txt")

        if "3" in filesNumber:
            base_name, extension = os.path.splitext(vhdl_tb_HDLGen_path)
            new_filename = vhdl_tb_HDLGen_path
            if os.path.isfile(new_filename):
                # File already exists, modify the name
                index = 1
                while os.path.isfile(new_filename):
                    index += 1
                    new_filename = f"{base_name}_{index}{extension}"
            try:
                # Writing xml file
                with open(vhdl_tb_path, 'r') as source:
                    with open(new_filename, "w") as f:
                        content = source.read()
                        f.write(content)
                    print("VHDL Testbench Backup file successfully generated at ", new_filename)
            except FileNotFoundError:
                with open(new_filename, "w") as f:
                    f.write(vhdl_tb_code)
                print("VHDL Testbench backup file successfully generated at ", new_filename)
        if "2" in filesNumber:
            # Writing xml file
            with open(vhdl_tb_path, "w") as f:
                f.write(vhdl_tb_code)
            print("VHDL Testbench file successfully generated at ", vhdl_tb_path)

        if "9" in filesNumber:
            base_name, extension = os.path.splitext(chatgpt_vhdl_HDLGen_file_path)
            new_filename = chatgpt_vhdl_HDLGen_file_path
            if os.path.isfile(new_filename):
                # File already exists, modify the name
                index = 1
                while os.path.isfile(new_filename):
                    index += 1
                    new_filename = f"{base_name}_{index}{extension}"
            try:
                with open(chatgpt_vhdl_file_path, 'r') as source:
                    with open(new_filename, "w") as f:
                        content = source.read()
                        f.write(content)
                    print("VHDL Testbench ChatGPT Backup file successfully generated at ", new_filename)
            except FileNotFoundError:
                with open(new_filename, "w") as f:
                    f.write(chatgpt_tb)
                print("VHDL Testbench ChatGPT backup file successfully generated at ", new_filename)

        if "8" in filesNumber:
            with open(chatgpt_vhdl_file_path, "w") as f:
                f.write(chatgpt_tb)
            pyperclip.copy(chatgpt_tb)
            print("VHDL Testbench ChatGPT file successfully generated at ", chatgpt_vhdl_file_path)

        if "10" in filesNumber:
            with open(waveform_path, "w") as f:
                f.write(waveform)
            print("Waveform file successfully generated at ", waveform_path)

    def generate_mainPackage(self):
        gen_arrays = ""
        comp = ""
        vhdl_database_path = "./Generator/HDL_Database/vhdl_database.xml"
        # Parsing the xml file
        vhdl_database = minidom.parse(vhdl_database_path)
        vhdl_root = vhdl_database.documentElement
        mainPackageDir = ProjectManager.get_package_hdlgen()
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
            depth = int(depth) - 1
            width = array_nodes[i].getElementsByTagName('width')[0].firstChild.data
            width = int(width) - 1
            sigType = array_nodes[i].getElementsByTagName('signalType')[0].firstChild.data

            gen_arrayType_syntax = vhdl_root.getElementsByTagName("arrayType")[0].firstChild.data
            gen_arrayType_syntax = gen_arrayType_syntax.replace("$arrayName", name)
            gen_arrayType_syntax = gen_arrayType_syntax.replace("$signalType", sigType)
            gen_arrayType_syntax = gen_arrayType_syntax.replace("$arraySize", str(depth))
            gen_arrayType_syntax = gen_arrayType_syntax.replace("$arrayLength", str(width))
            gen_arrays += gen_arrayType_syntax
        for i in range(0, len(comp_nodes)):
            model = comp_nodes[i].getElementsByTagName('model')[0].firstChild.data
            dir = comp_nodes[i].getElementsByTagName('dir')[0].firstChild.data
            ports = ""
            for port_signal in comp_nodes[i].getElementsByTagName("port"):
                signals = port_signal.firstChild.data.split(",")
                gen_compType_assign_syntax = vhdl_root.getElementsByTagName("signalDeclaration")[0].firstChild.data
                gen_compType_assign_syntax = gen_compType_assign_syntax.replace("$sig_name", signals[0])
                gen_compType_assign_syntax = gen_compType_assign_syntax.replace("$mode", signals[1])
                gen_compType_assign_syntax = gen_compType_assign_syntax.replace("$type", signals[2])
                ports += "\t" + gen_compType_assign_syntax + "\n"
            ports = ports.rstrip()
            ports = ports[0:-1]
            gen_compType_syntax = vhdl_root.getElementsByTagName("component")[0].firstChild.data
            gen_compType_syntax = gen_compType_syntax.replace("$model", model)
            gen_compType_syntax = gen_compType_syntax.replace("$ports", ports)
            comp += gen_compType_syntax + "\n"

        array_vhdl_code = vhdl_root.getElementsByTagName("arrayPackage")[0].firstChild.data
        array_vhdl_code = array_vhdl_code.replace("$arrays", gen_arrays)

        array_vhdl_code = array_vhdl_code.replace("$Component", comp)
        array_vhdl_file_path = ProjectManager.get_package_vhd()
        # Write array code to file
        with open(array_vhdl_file_path, "w") as f:
            f.write(array_vhdl_code)

    def generate_verilog(self):
        gen_verilog = ""
        chatgpt_header = ""
        chatgpt_verilog = ""

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
        arrayList = []
        arrayListIO = []
        arrayInfo = []
        array_assign = ""
        single_bitList = []
        busList = []
        unsignedList = []
        signedList = []
        integerList = []
        # Entity Section
        gen_signals = ""
        port_signals = ""
        output_reg_signals = ""
        entity_signal_description = ""
        io_port_node = hdl_design[0].getElementsByTagName("entityIOPorts")
        gen_entity = ""
        self.includeArrays = False
        portSignals = []
        internalSignals = []
        portNames = []
        internalnames = []
        instances = []
        stateTypeSig = False
        mainPackageDir = ProjectManager.get_package_hdlgen()
        root = minidom.parse(mainPackageDir)
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
        mainPackage = hdlDesign[0].getElementsByTagName("mainPackage")
        array_nodes = mainPackage[0].getElementsByTagName('array')

        if len(io_port_node) != 0 and io_port_node[0].firstChild is not None:

            for signal in io_port_node[0].getElementsByTagName('signal'):
                name = signal.getElementsByTagName('name')[0].firstChild.data
                type = signal.getElementsByTagName('type')[0].firstChild.data
                mode = signal.getElementsByTagName('mode')[0].firstChild.data

                portData = [name, type, mode]
                portSignals.append(portData)
                portNames.append(name)
                if type == "single bit":
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
                else:
                    type = type.split(",")
                    width = 0
                    depth = 0
                    for i in range(0, len(array_nodes)):
                        typeName = array_nodes[i].getElementsByTagName('name')[0].firstChild.data
                        if typeName == type[1]:
                            depth = array_nodes[i].getElementsByTagName('depth')[0].firstChild.data
                            width = array_nodes[i].getElementsByTagName('width')[0].firstChild.data
                    arrayListIO .append(name)
                    arrayInfo.append([name, depth, width])
                    bits = int(width) * int(depth) - 1
                    width = int(width) - 1
                    depth = int(depth) - 1
                    type = "[" + str(bits) + ":0]"
                    bits = bits + 1

                    output_reg_signals += "wire [" + str(width) + ":0] " + name + " [" + str(depth) + ":0];\n"
                    top = bits - 1
                    low = bits - width - 1
                    for j in range(0, depth + 1):
                        array_assign += "assign " + name + "[" + str(j) + "] = " + name + "_" + str(bits) + "[" + str(
                            top) + ":" + str(low) + "];\n"
                        top = low - 1
                        low = low - width - 1

                    self.includeArrays = True
                    name = name+"_"+ str(bits)
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

                signal_declare_syntax = signal_declare_syntax.replace("$sig_name", name)
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
                stateSize = len(stateTypesList) - 1
                binaryStateSize = bin(stateSize)
                binaryStateSize = len(binaryStateSize) - 2
                number = 0
                for stateType in int_sig_node[0].getElementsByTagName("stateTypes"):
                    stateTypesString += stateType.firstChild.data + ", "
                    stateType_syntax = verilog_root.getElementsByTagName("stateNamesDeclarations")[0].firstChild.data
                    stateType_syntax = stateType_syntax.replace("$stateName", stateType.firstChild.data)
                    num = bin(number)[2:]
                    num = num.zfill(binaryStateSize)
                    stateType_syntax = stateType_syntax.replace("$bits", str(binaryStateSize) + "'b" + num)
                    number = number + 1
                    gen_int_sig += "\n" + stateType_syntax
                stateTypesString = stateTypesString[:-2]

                for signal in int_sig_node[0].getElementsByTagName("signal"):
                    name = signal.getElementsByTagName('name')[0].firstChild.data
                    type = signal.getElementsByTagName('type')[0].firstChild.data
                    internalData = [name, type]
                    internalSignals.append(internalData)
                    internalnames.append(name)
                    if type == "Enumerated type state signal pair(NS/CS)":
                        type = ""
                        if name[0:2] == "CS":
                            stateTypeSig = True
                            CSState = name
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
                    elif type[0:7] == "integer":
                        integerList.append(name)
                        type = "integer"
                    else:
                        type = type.split(",")
                        width = 0
                        depth = 0
                        for i in range(0, len(array_nodes)):
                            typeName = array_nodes[i].getElementsByTagName('name')[0].firstChild.data
                            if typeName == type[1]:
                                depth = array_nodes[i].getElementsByTagName('depth')[0].firstChild.data
                                width = array_nodes[i].getElementsByTagName('width')[0].firstChild.data
                        arrayList.append(name)
                        arrayInfo.append([name, depth, width])
                        width = int(width) - 1
                        depth = int(depth) - 1

                        type = "[" + str(width) + ":0] " + name + " [" + str(depth) + ":0]"
                        name = ""
                    int_sig_syntax = verilog_root.getElementsByTagName("intSigDeclaration")[0].firstChild.data
                    int_sig_syntax = int_sig_syntax.replace("$int_sig_name", name)
                    int_sig_syntax = int_sig_syntax.replace("$int_sig_type", type)
                    if type == "integer":
                        int_sig_syntax = int_sig_syntax.replace("reg ", "")
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

                gen_header = "// Title Section Start\n"
                gen_header += "// Generated by HDLGen, Github https://github.com/HDLGen-ChatGPT/HDLGen-ChatGPT, on " + str(
                    datetime.now().strftime("%d-%B-%Y")) + " at " + str(datetime.now().strftime("%H:%M")) + "\n\n"
                gen_header += "// Component Name : " + entity_name + "\n"
                title = header_node[0].getElementsByTagName("title")[0].firstChild.data
                gen_header += "// Title          : " + (title if title != "null" else "") + "\n\n"
                authors = header_node[0].getElementsByTagName("authors")[0].firstChild.data
                gen_header += "// Author(s)      : " + (authors if authors != "null" else "") + "\n"
                company = header_node[0].getElementsByTagName("company")[0].firstChild.data
                gen_header += "// Organisation   : " + (company if company != "null" else "") + "\n"
                email = header_node[0].getElementsByTagName("email")[0].firstChild.data
                gen_header += "// Email          : " + (email if email != "null" else "") + "\n"
                gen_header += "// Date           : " + header_node[0].getElementsByTagName("date")[
                    0].firstChild.data + "\n\n"
                desc = header_node[0].getElementsByTagName("description")[0].firstChild.data
                desc = desc.replace("&#10;", "\n// ")
                gen_header += "// Description\n// "
                gen_header += (desc if desc != "null" else "") + "\n"

                chatgpt_header += gen_header
                gen_verilog += gen_header

                # entity signal dictionary
                gen_entity = gen_entity.replace("$comp_name", entity_name)
                gen_entity_signal = "\n// entity signal dictionary\n"
                gen_entity_signal += entity_signal_description + "\n"
                gen_verilog += gen_entity_signal
                chatgpt_header += gen_entity_signal

                # internal signal dictionary
                gen_internal_signal = "// internal signal dictionary\n"
                gen_internal_signal_result = gen_internal_signal_result + "\n"
                gen_internal_signal += gen_internal_signal_result
                gen_internal_signal += "// Title Section End\n"
                gen_verilog += gen_internal_signal
                chatgpt_header += gen_internal_signal

                # Process
                arch_node = hdl_design[0].getElementsByTagName("architecture")
                gen_archs = ""
                gen_process = ""
                gen_conc = ""
                gen_seq_process = ""
                gen_instance = ""
                if array_assign != "":
                    gen_process = array_assign + "\n"
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
                            ceInSeq = ""
                            caseEmpty = True
                            notes = child.getElementsByTagName("note")[0].firstChild.data
                            notes = re.sub(r'\s+', ' ', notes)
                            notes = notes.replace("&#10;", "\n/// ")
                            notes = notes.replace("&amp;", ",")
                            notes = notes.replace("&quot;", "\"")
                            notes = notes.replace("&apos;", "\'")
                            notes = notes.replace("&lt;", "<")
                            notes = notes.replace("&#x9;", "\t")
                            notes = notes.replace("&gt;", ">")
                            notes = notes.replace("&#44;", ",")
                            notes = notes.replace("(", "[")
                            notes = notes.replace(")", "]")
                            notes = notes.replace("downto", ":")
                            notes = notes.replace("'", "")
                            pattern = r'(?<!:)(?<!\d)([01]+)(?!\d)(?!\s*:)'
                            notes = re.sub(pattern, lambda m: f"1'b{m.group(1)}" if len(
                                m.group(1)) == 1 else f"{len(m.group(1))}'b{m.group(1)}", notes)
                            pattern2 = r"(\[|\w+)([\d]+)'b([\d]+)]"
                            match = re.search(pattern2, notes)
                            while match:
                                notes = notes.replace(match.group(), match.group(1) + match.group(3) + "]")
                                match = re.search(pattern2, notes)
                            #pattern3 = r"(\w+)(\d+'b)(\d+)"
                            pattern3 = r"([a-zA-Z_]+)(\d+'b)(\d+)"
                            match = re.search(pattern3, notes)
                            #This match is for signals that have a 0 or 1 in them
                            while match:
                                notes = notes.replace(match.group(), match.group(1) + match.group(3))
                                match = re.search(pattern3, notes)
                            notes = notes.replace("'", "_")
                            pattern1 = r'\[?(\w+\[[^\]]*\]|\w+)\s*,\s*(\w+\[[^\]]*\]|\w+)\]?'
                            notes = re.sub(pattern1, r'{\1,\2}', notes)
                            notes = notes.replace("{0}","{1b'0}")
                            notes = notes.replace("{1}","{1b'1}")
                            # Define a regular expression pattern to match the desired pattern of finding eg. 16{1'b0} and convert to {16{1'b0}}
                            pattern4 = r'(\w+)\{([^}]+)\}'
                            # Use re.sub to replace the matched pattern with {match}
                            notes = re.sub(pattern4, r'{\1{\2}}', notes)
                            notes = notes.replace("_", "'")
                            signalList = ""
                            for default_out in child.getElementsByTagName("defaultOutput"):
                                arraySignal = False
                                signals = default_out.firstChild.data.split(",")
                                value = signals[1]
                                if value == "rst state":
                                    if stateTypesList != "":
                                        stateNames = stateTypesString.split(",")
                                        value = stateNames[0]
                                elif value == "zero":
                                    if signals[0] in arrayList:
                                        array_syntax = ""
                                        for arr in arrayInfo:
                                            if arr[0] == signals[0]:
                                                depth = int(arr[1])
                                                width = int(arr[2])
                                                array_syntax = "integer i;\n\tfor (i=0; i<" + str(
                                                    depth) + "; i=i+1)\n\t\tbegin\n\t\t\t" + signals[0] + "[i] <= " + str(
                                                    width) + "'b0;\n\t\tend"
                                                arraySignal = True
                                    elif signals[0] in arrayListIO:
                                        array_syntax = ""
                                        for arr in arrayInfo:
                                            if arr[0] == signals[0]:
                                                depth = int(arr[1])
                                                width = int(arr[2])
                                                bits = depth * width
                                                signals[0] = signals[0] + "_" + str(bits)
                                                array_syntax = "integer i;\n\tfor (i=0; i<" + str(
                                                    depth) + "; i=i+1)\n\t\tbegin\n\t\t\t" + signals[0] + "[i] <= " + str(
                                                    width) + "'b0;\n\t\tend\n"
                                                arraySignal = True
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
                                        for signal in internalSignals:
                                            if signals[0] == signal[0]:
                                                match = re.search(r'\((\d+)\sdownto\s(\d+)\)', signal[1])
                                                start = int(match.group(1))
                                                end = int(match.group(2))
                                                size = start - end + 1
                                        value = str(size) + "'b0"
                                    else:
                                        value = str(0)
                                elif value in portNames or value in internalnames:
                                    value = value
                                    if signals[0] in arrayList:
                                        array_syntax = ""
                                        if signals[1] in arrayList:
                                            for arr in arrayInfo:
                                                if arr[0] == signals[0]:
                                                    depth = int(arr[1])
                                                    array_syntax = "integer i;\n\tfor (i=0; i<" + str(
                                                        depth) + "; i=i+1)\n\t\tbegin\n\t\t\t" + signals[0] + "[i] <= " + \
                                                                   signals[1] + "[i];" + "\n\t\tend"
                                                    arraySignal = True

                                elif stateTypeSig == True and value == CSState:
                                    caseEmpty = False
                                    case_syntax = verilog_root.getElementsByTagName("case")[0].firstChild.data
                                    case_syntax = case_syntax.replace("$stateType", value)
                                    stateNames = stateTypesString.split(",")
                                    whenCase = ""
                                    for states in stateNames:
                                        whenCase += "\n\t\t" + states + " :" + "\n\t\t\tbegin\n\n\t\t\tend"
                                else:
                                    value = re.sub(r'\s+', '', value)
                                    value = value.replace("&#10;", "\n/// ")
                                    value = value.replace("&amp;", ",")
                                    value = value.replace("&quot;", "\"")
                                    value = value.replace("&apos;", "\'")
                                    value = value.replace("&lt;", "<")
                                    value = value.replace("&#x9;", "\t")
                                    value = value.replace("&gt;", ">")
                                    value = value.replace("&#44;", ",")
                                    value = value.replace("(", "[")
                                    value = value.replace(")", "]")
                                    value = value.replace("downto", ":")
                                    value = value.replace("'", "")

                                    pattern = r'(?<!:)(?<!\d)([01]+)(?!\d)(?!\s*:)'
                                    value = re.sub(pattern, lambda m: f"1'b{m.group(1)}" if len(
                                        m.group(1)) == 1 else f"{len(m.group(1))}'b{m.group(1)}", value)
                                    pattern2 = r"(\[|\w+)([\d]+)'b([\d]+)]"
                                    match = re.search(pattern2, value)
                                    while match:
                                        value = value.replace(match.group(), match.group(1) + match.group(3) + "]")
                                        match = re.search(pattern2, value)
                                    # pattern3 = r"(\w+)(\d+'b)(\d+)"
                                    pattern3 = r"([a-zA-Z_]+)(\d+'b)(\d+)"
                                    match = re.search(pattern3, value)
                                    # This match is for signals that have a 0 or 1 in them
                                    while match:
                                        value = value.replace(match.group(), match.group(1) + match.group(3))
                                        match = re.search(pattern3, value)
                                    value = value.replace("'", "_")
                                    pattern1 = r'\[?(\w+\[[^\]]*\]|\w+)\s*,\s*(\w+\[[^\]]*\]|\w+)\]?'
                                    value = re.sub(pattern1, r'{\1,\2}', value)
                                    value = value.replace("{0}", "{1b'0}")
                                    value = value.replace("{1}", "{1b'1}")
                                    # Define a regular expression pattern to match the desired pattern of finding eg. 16{1'b0} and convert to {16{1'b0}}
                                    pattern4 = r'(\w+)\{([^}]+)\}'
                                    # Use re.sub to replace the matched pattern with {match}
                                    value = re.sub(pattern4, r'{\1{\2}}', value)
                                    value = value.replace("_", "'")



                                if arraySignal == True:
                                    assign_syntax = array_syntax
                                else:
                                    assign_syntax = verilog_root.getElementsByTagName("processAssign")[
                                        0].firstChild.data
                                    assign_syntax = assign_syntax.replace("$output_signal", signals[0])
                                    assign_syntax = assign_syntax.replace("$value", value)
                                    assign_syntax = assign_syntax
                                if_gen_defaults += "\n\t\t" + assign_syntax
                                gen_defaults += "\n\t" + assign_syntax + " // Default assignment"
                                if len(signals) == 4:
                                    clkAssign_syntax = verilog_root.getElementsByTagName("processAssign")[
                                        0].firstChild.data
                                    clkAssign_syntax = clkAssign_syntax.replace("$output_signal", signals[0])
                                    clkAssign_syntax = clkAssign_syntax.replace("$value", signals[2])
                                    clkgen_defaults += "\n\t\t" + clkAssign_syntax
                                    if signals[3] != "N/A":
                                        ceInSeq = signals[3]
                                else:
                                    signalList += ", " + signals[0]
                            process_syntax = process_syntax.replace("$process_label",
                                                                    child.getElementsByTagName("label")[
                                                                        0].firstChild.data)

                            if gen_defaults != "":
                                if clkgen_defaults != "":
                                    for clkRst in clkAndRst[0].getElementsByTagName("clkAndRst"):
                                        clkEdge = "posedge"
                                        if clkRst.getElementsByTagName('activeClkEdge')[0].firstChild.data == "H-L":
                                            clkEdge = "negedge"
                                        gen_in_sig = clkEdge + " clk"
                                        if clkRst.getElementsByTagName('rst')[0].firstChild.data == "Yes":
                                            if_syntax = verilog_root.getElementsByTagName("ifStatement")[
                                                0].firstChild.data
                                            if_syntax = if_syntax.replace("$assignment", "rst")
                                            lvl = "1"
                                            rstlvl = "posedge"
                                            if clkRst.getElementsByTagName('ActiveRstLvl')[0].firstChild.data == '0':
                                                rstlvl = "negedge"
                                                lvl = "0"
                                            if_syntax = if_syntax.replace("$lvl", lvl)
                                            if_syntax = if_syntax.replace("$default_assignments",
                                                                          if_gen_defaults)
                                            if clkRst.getElementsByTagName('RstType')[0].firstChild.data == "asynch":
                                                gen_in_sig = clkEdge + " clk or " + rstlvl + " rst"
                                                else_syntax = verilog_root.getElementsByTagName("elseStatement")[
                                                    0].firstChild.data
                                                if ceInSeq != "":
                                                    clkgen_defaults = indent(clkgen_defaults, '    ')
                                                    clkgen_defaults = "\n\t\tif ( " + ceInSeq + " ) // enable register\n\t\t\tbegin" + clkgen_defaults + "\n\t\t\tend"
                                                    clkgen_defaults = indent(clkgen_defaults, '    ')
                                                else_syntax = else_syntax.replace("$default_assignments",
                                                                                  clkgen_defaults)
                                                if_syntax = if_syntax.replace("$else", else_syntax)
                                                clkgen_defaults = "\t" + if_syntax + "\n"
                                            else:
                                                gen_in_sig = clkEdge + " clk"
                                                else_syntax = verilog_root.getElementsByTagName("elseStatement")[
                                                    0].firstChild.data
                                                if ceInSeq != "":
                                                    clkgen_defaults = indent(clkgen_defaults, '    ')
                                                    clkgen_defaults = "\n\t\tif ( " + ceInSeq + " ) // enable register\n\t\t\tbegin" + clkgen_defaults + "\n\t\t\tend"
                                                    clkgen_defaults = indent(clkgen_defaults, '    ')
                                                else_syntax = else_syntax.replace("$default_assignments",
                                                                                  clkgen_defaults)
                                                if_syntax = if_syntax.replace("$else", else_syntax)
                                                clkgen_defaults = "\t" + if_syntax + "\n"
                                        else:
                                            clkgen_defaults = textwrap.dedent(clkgen_defaults)
                                            clkgen_defaults = indent(clkgen_defaults, '    ')
                                    clkgen_defaults = clkgen_defaults.rstrip()
                                    process_syntax = process_syntax.replace("$input_signals", gen_in_sig)
                                    process_syntax = process_syntax.replace("$default_assignments", clkgen_defaults)
                                    gen_seq_process += process_syntax + "\n\n"
                                else:
                                    for input_signal in child.getElementsByTagName("inputSignal"):
                                        if input_signal.firstChild.data in arrayList:
                                            for row_idx, row in enumerate(arrayInfo):
                                                for col_idx, element in enumerate(row):
                                                    if input_signal.firstChild.data in element:
                                                        num = int(arrayInfo[row_idx][1])
                                                        for i in range(num):
                                                            gen_in_sig += input_signal.firstChild.data + "[" + str(
                                                                i) + "]" + " or "
                                        elif input_signal.firstChild.data in arrayListIO:
                                            for row_idx, row in enumerate(arrayInfo):
                                                for col_idx, element in enumerate(row):
                                                    if input_signal.firstChild.data in element:
                                                        num = int(arrayInfo[row_idx][1])
                                                        for i in range(num):
                                                            gen_in_sig += input_signal.firstChild.data + "[" + str(i) + "]" + " or "
                                        else:
                                            gen_in_sig += input_signal.firstChild.data + " or "
                                    gen_in_sig = gen_in_sig.strip()
                                    gen_in_sig = gen_in_sig[:-3]
                                    note_syntax = verilog_root.getElementsByTagName("note")[0].firstChild.data
                                    note_syntax = note_syntax.replace("$notes", notes)
                                    if notes == "None":
                                        gen_defaults = gen_defaults.replace("<","")
                                        gen_defaults += ""
                                        if caseEmpty == False:
                                            case_syntax = case_syntax.replace("$whenCase", whenCase)
                                            gen_defaults += "\n" + case_syntax
                                    else:
                                        gen_defaults = gen_defaults.replace("<", "")
                                        gen_defaults += "\n" + note_syntax
                                    gen_defaults = gen_defaults.rstrip()
                                    process_syntax = process_syntax.replace("$input_signals", gen_in_sig)
                                    process_syntax = process_syntax.replace("$default_assignments", gen_defaults)
                                    gen_process += process_syntax + "\n\n"

                        elif (child.nodeType == arch_node[0].ELEMENT_NODE and child.tagName == "concurrentStmt"):

                            for statement in child.getElementsByTagName("statement"):
                                signals = statement.firstChild.data.split(",")
                                notes = child.getElementsByTagName("note")[0].firstChild.data
                                if notes != "None":
                                    notes = re.sub(r'\s+', ' ', notes)
                                    notes = notes.replace("&#10;", "\n/// ")
                                    notes = notes.replace("&amp;", ",")
                                    notes = notes.replace("&quot;", "\"")
                                    notes = notes.replace("&apos;", "\'")
                                    notes = notes.replace("&lt;", "<")
                                    notes = notes.replace("&#x9;", "\t")
                                    notes = notes.replace("&gt;", ">")
                                    notes = notes.replace("&#44;", ",")
                                    notes = notes.replace("(", "[")
                                    notes = notes.replace(")", "]")
                                    notes = notes.replace("downto", ":")
                                    notes = notes.replace("'", "")
                                    pattern = r'(?<!:)(?<!\d)([01]+)(?!\d)(?!\s*:)'
                                    notes = re.sub(pattern, lambda m: f"1'b{m.group(1)}" if len(
                                        m.group(1)) == 1 else f"{len(m.group(1))}'b{m.group(1)}", notes)
                                    pattern2 = r"(\[|\w+)([\d]+)'b([\d]+)]"
                                    match = re.search(pattern2, notes)
                                    while match:
                                        notes = notes.replace(match.group(), match.group(1) + match.group(3) + "]")
                                        match = re.search(pattern2, notes)
                                    # pattern3 = r"(\w+)(\d+'b)(\d+)"
                                    pattern3 = r"([a-zA-Z_]+)(\d+'b)(\d+)"
                                    match = re.search(pattern3, notes)
                                    # This match is for signals that have a 0 or 1 in them
                                    while match:
                                        notes = notes.replace(match.group(), match.group(1) + match.group(3))
                                        match = re.search(pattern3, notes)
                                    notes = notes.replace("'", "_")
                                    pattern1 = r'\[?(\w+\[[^\]]*\]|\w+)\s*,\s*(\w+\[[^\]]*\]|\w+)\]?'
                                    notes = re.sub(pattern1, r'{\1,\2}', notes)
                                    notes = notes.replace("{0}", "{1b'0}")
                                    notes = notes.replace("{1}", "{1b'1}")
                                    # Define a regular expression pattern to match the desired pattern of finding eg. 16{1'b0} and convert to {16{1'b0}}
                                    pattern4 = r'(\w+)\{([^}]+)\}'
                                    # Use re.sub to replace the matched pattern with {match}
                                    notes = re.sub(pattern4, r'{\1{\2}}', notes)
                                    notes = notes.replace("_", "'")
                                    note_syntax = verilog_root.getElementsByTagName("concNote")[0].firstChild.data
                                    note_syntax = note_syntax.replace("$concurrentstmt_label",
                                                                      child.getElementsByTagName("label")[
                                                                          0].firstChild.data)
                                    note_syntax = note_syntax.replace("$output_signal", signals[0])
                                    note_syntax = note_syntax.replace("$notes", notes)
                                    gen_conc += note_syntax + "\n\n"
                                    var_name = signals[0]
                                    pattern = f"(reg)\s*(\[\s*\d+\s*:\s*\d+\s*\])?\s+({var_name})"

                                    # Replace "reg" with "wire" in the matching line
                                    gen_int_sig = re.sub(pattern, r"wire \2 \3", gen_int_sig)
                                else:
                                    gen_stmts = ""
                                    conc_syntax = verilog_root.getElementsByTagName("concurrentstmt")[0].firstChild.data

                                    conc_syntax = conc_syntax.replace("$concurrentstmt_label",
                                                                      child.getElementsByTagName("label")[
                                                                          0].firstChild.data)
                                    arraySignal = False
                                    signals = statement.firstChild.data.split(",")
                                    # find the signal and change it to wire
                                    # Define the regular expression pattern with optional bit width specification
                                    var_name = signals[0]
                                    pattern = f"(reg)\s*(\[\s*\d+\s*:\s*\d+\s*\])?\s+({var_name})"

                                    # Replace "reg" with "wire" in the matching line
                                    gen_int_sig = re.sub(pattern, r"wire \2 \3", gen_int_sig)
                                    value = signals[1]
                                    if value.isdigit():
                                        size = len(value)
                                        value = str(size) + "'b" + value
                                    elif value == "zero":
                                        if signals[0] in arrayList:
                                            array_syntax = ""
                                            for arr in arrayInfo:
                                                if arr[0] == signals[0]:
                                                    depth = int(arr[1]) + 1
                                                    width = int(arr[2])
                                                    for j in range(0, depth):
                                                        array_syntax += "assign " + signals[0] + "[" + str(
                                                            j) + "] = " + str(
                                                            width) + "'b0; // Complete the concurrent statement if required\n"
                                                        arraySignal = True
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
                                            for signal in internalSignals:
                                                if signals[0] == signal[0]:
                                                    match = re.search(r'\((\d+)\sdownto\s(\d+)\)', signal[1])
                                                    start = int(match.group(1))
                                                    end = int(match.group(2))
                                                    size = start - end + 1
                                            value = str(size) + "'b0"
                                        else:
                                            value = str(0)
                                    if arraySignal == True:
                                        conc_syntax = array_syntax
                                    else:
                                        assign_syntax = verilog_root.getElementsByTagName("sigAssign")[
                                            0].firstChild.data
                                        assign_syntax = assign_syntax.replace("$output_signal", signals[0])
                                        assign_syntax = assign_syntax.replace("$value", value)

                                        gen_stmts += assign_syntax

                                        conc_syntax = conc_syntax.replace("$statement", gen_stmts)
                                    gen_conc += conc_syntax
                            gen_conc += "\n"


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
                                var_name = signals[1]
                                pattern = f"(reg)\s*(\[\s*\d+\s*:\s*\d+\s*\])?\s+({var_name})"
                                # Not sure if instance can be a reg
                                # Replace "reg" with "wire" in the matching line
                                #gen_int_sig = re.sub(pattern, r"wire \2 \3", gen_int_sig)

                                gen_stmts += "\t" + assign_syntax + ",\n"
                            gen_stmts = gen_stmts.rstrip()
                            gen_stmts = gen_stmts[0:-1]
                            instance_syntax = instance_syntax.replace("$portAssign", gen_stmts)
                            instance_syntax = instance_syntax.replace("$instance",
                                                                      child.getElementsByTagName("model")[
                                                                          0].firstChild.data)
                            instances.append(child.getElementsByTagName("model")[0].firstChild.data)
                            gen_instance += instance_syntax + "\n"

                        child = next
                    # gen_process = gen_process[:-1]
                    gen_archs += gen_process
                    gen_archs += gen_conc
                    gen_archs += gen_seq_process
                    gen_archs += gen_instance
                    arch_syntax = verilog_root.getElementsByTagName("architecture")[0].firstChild.data

                    gen_arch = arch_syntax.replace("$int_sig_declaration", gen_int_sig)
                    gen_arch = gen_arch.replace("$arch_elements", gen_archs[:-1])
                    gen_entity = gen_entity.replace("$arch", indent(gen_arch, '    '))
                    chatgpt_verilog += gen_entity + "\n\n"
                    # Entity Section placement
                    gen_verilog += gen_entity + "\n\n"
                    gen_verilog = gen_verilog.replace("&#10;", "\n")
                    gen_verilog = gen_verilog.replace("&amp;", "&")
                    gen_verilog = gen_verilog.replace("&amp;", "&")
                    gen_verilog = gen_verilog.replace("&quot;", "\"")
                    gen_verilog = gen_verilog.replace("&apos;", "\'")
                    gen_verilog = gen_verilog.replace("&lt;", "<")
                    gen_verilog = gen_verilog.replace("&#x9;", "\t")
                    gen_verilog = gen_verilog.replace("&gt;", ">")
                    gen_verilog = gen_verilog.replace("&#44;", ",")

                    chatgpt_header = chatgpt_header.replace("&#10;", "\n")
                    chatgpt_header = chatgpt_header.replace("&amp;", "&")
                    chatgpt_header = chatgpt_header.replace("&amp;", "&")
                    chatgpt_header = chatgpt_header.replace("&quot;", "\"")
                    chatgpt_header = chatgpt_header.replace("&apos;", "\'")
                    chatgpt_header = chatgpt_header.replace("&lt;", "<")
                    chatgpt_header = chatgpt_header.replace("&#x9;", "\t")
                    chatgpt_header = chatgpt_header.replace("&gt;", ">")
                    chatgpt_header = chatgpt_header.replace("&#44;", ",")

                    chatgpt_verilog = chatgpt_verilog.replace("&#10;", "\n")
                    chatgpt_verilog = chatgpt_verilog.replace("&amp;", "&")
                    chatgpt_verilog = chatgpt_verilog.replace("&amp;", "&")
                    chatgpt_verilog = chatgpt_verilog.replace("&quot;", "\"")
                    chatgpt_verilog = chatgpt_verilog.replace("&apos;", "\'")
                    chatgpt_verilog = chatgpt_verilog.replace("&lt;", "<")
                    chatgpt_verilog = chatgpt_verilog.replace("&#x9;", "\t")
                    chatgpt_verilog = chatgpt_verilog.replace("&gt;", ">")
                    chatgpt_verilog = chatgpt_verilog.replace("&#44;", ",")

        return entity_name, gen_verilog, instances, chatgpt_header, chatgpt_verilog

    def create_verilog_file(self, filesNumber):

        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        root = minidom.parse(proj_path + "/HDLGenPrj/" + proj_name + ".hdlgen")
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
        VerilogModel = "None"
        VerilogHeader = "None"
        chatgpt = hdlDesign[0].getElementsByTagName('chatgpt')[0]
        if chatgpt.hasChildNodes():
            commands_node = chatgpt.getElementsByTagName('commands')[0]

            VerilogModel = commands_node.getElementsByTagName('VerilogModel')[0].firstChild.data
            VerilogModel = VerilogModel.replace("&#10;", "\n")
            VerilogModel = VerilogModel.replace("&amp;", "&")
            VerilogModel = VerilogModel.replace("&quot;", "\"")
            VerilogModel = VerilogModel.replace("&apos;", "\'")
            VerilogModel = VerilogModel.replace("&lt;", "<")
            VerilogModel = VerilogModel.replace("&#x9;", "\t")
            VerilogModel = VerilogModel.replace("&gt;", ">")
            VerilogModel = VerilogModel.replace("&#44;", ",")
            # does not display lines starting with ~
            lines = VerilogModel.split('\n')
            filtered_lines = [line for line in lines if not line.startswith('~')]
            VerilogModel = '\n'.join(filtered_lines)
        entity_name, verilog_code, instances, chatgpt_header, chatgpt_verilog = self.generate_verilog()
        model = VerilogModel
        chatgpt_verilog = model + "\n\n" + verilog_code
        verilog_file_path = os.path.join(proj_path, "Verilog", "model", entity_name + ".v")
        verilog_file_HDLGen_path = os.path.join(proj_path, "Verilog", "model", entity_name + "_backup.v")
        chatgpt_header_file_path = os.path.join(proj_path, "Verilog", "ChatGPT",
                                                entity_name + "_Verilog_header_ChatGPT.txt")
        chatgpt_verilog_file_path = os.path.join(proj_path, "Verilog", "ChatGPT", entity_name + "_Verilog_ChatGPT.txt")
        chatgpt_header_HDLGen_file_path = os.path.join(proj_path, "Verilog", "ChatGPT", "Backups",
                                                       entity_name + "_Verilog_header_ChatGPT_backup.txt")
        chatgpt_verilog_HDLGen_file_path = os.path.join(proj_path, "Verilog", "ChatGPT", "Backups",
                                                        entity_name + "_Verilog_ChatGPT_backup.txt")

        if "1" in filesNumber:
            base_name, extension = os.path.splitext(verilog_file_HDLGen_path)
            new_filename = verilog_file_HDLGen_path
            if os.path.isfile(new_filename):
                # File already exists, modify the name
                index = 1
                while os.path.isfile(new_filename):
                    index += 1
                    new_filename = f"{base_name}_{index}{extension}"
            try:
                # Writing xml file
                with open(verilog_file_path, 'r') as source:
                    with open(new_filename, "w") as f:
                        content = source.read()
                        f.write(content)
                    print("Verilog Backup Model successfully generated at ", new_filename)
            except FileNotFoundError:
                with open(new_filename, "w") as f:
                    f.write(verilog_code)
                print("Verilog Backup Model successfully generated at ", new_filename)
        if "0" in filesNumber:
            # Writing xml file
            with open(verilog_file_path, "w") as f:
                f.write(verilog_code)
            print("Verilog Model successfully generated at ", verilog_file_path)

        if "5" in filesNumber:
            base_name, extension = os.path.splitext(chatgpt_header_HDLGen_file_path)
            new_filename = chatgpt_header_HDLGen_file_path
            if os.path.isfile(new_filename):
                # File already exists, modify the name
                index = 1
                while os.path.isfile(new_filename):
                    index += 1
                    new_filename = f"{base_name}_{index}{extension}"
            try:
                with open(chatgpt_header_file_path, 'r') as source:
                    with open(new_filename, "w") as f:
                        content = source.read()
                        f.write(content)
                    print("ChatGPT Verilog title Backup successfully generated at ", new_filename)
            except FileNotFoundError:
                with open(new_filename, "w") as f:
                    f.write(chatgpt_header)
                print("ChatGPT Verilog title Backup successfully generated at ", new_filename)
        if "4" in filesNumber:
            # Writing xml file
            with open(chatgpt_header_file_path, "w") as f:
                f.write(chatgpt_header)
            pyperclip.copy(chatgpt_header)
            print("ChatGPT Verilog title successfully generated at ", chatgpt_header_file_path)

        if "7" in filesNumber:
            base_name, extension = os.path.splitext(chatgpt_verilog_HDLGen_file_path)
            new_filename = chatgpt_verilog_HDLGen_file_path
            if os.path.isfile(new_filename):
                # File already exists, modify the name
                index = 1
                while os.path.isfile(new_filename):
                    index += 1
                    new_filename = f"{base_name}_{index}{extension}"
            try:
                with open(chatgpt_verilog_file_path, 'r') as source:
                    with open(new_filename, "w") as f:
                        content = source.read()
                        f.write(content)
                    print("ChatGPT Verilog model Backup successfully generated at ", new_filename)
            except FileNotFoundError:
                with open(new_filename, "w") as f:
                    f.write(chatgpt_verilog)
                print("ChatGPT Verilog model Backup successfully generated at ", new_filename)
        if "6" in filesNumber:
            with open(chatgpt_verilog_file_path, "w") as f:
                f.write(chatgpt_verilog)
            pyperclip.copy(chatgpt_verilog)
            print("ChatGPT Verilog model successfully generated at ", chatgpt_verilog_file_path)

        self.entity_name = entity_name
        return instances

    def create_verilog_testbench_code(self):
        tb_code = ""
        chatgpt_tb = ""
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
        UUTEnt = ""
        header_node = hdl_design[0].getElementsByTagName("header")
        comp_node = header_node[0].getElementsByTagName("compName")[0]
        entity_name = comp_node.firstChild.data
        mainPackageDir = ProjectManager.get_package_hdlgen()
        root = minidom.parse(mainPackageDir)
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
        mainPackage = hdlDesign[0].getElementsByTagName("mainPackage")
        array_nodes = mainPackage[0].getElementsByTagName('array')
        with open(wcfg_database_path, "r") as f:
            xml_string = f.read()

        head_regex = r"<head>(.*?)</head>"
        head_contents = re.search(head_regex, xml_string, re.DOTALL).group(1)

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
        arrayList = []
        if len(io_port_node) != 0 and io_port_node[0].firstChild is not None:

            for signal in io_port_node[0].getElementsByTagName('signal'):
                io_signal_declare_syntax = verilog_root.getElementsByTagName("IOSignalDeclaration")[0].firstChild.data
                io_port_map_syntax = verilog_root.getElementsByTagName("portMap")[0].firstChild.data
                name = signal.getElementsByTagName('name')[0].firstChild.data

                if signal.getElementsByTagName('mode')[0].firstChild.data == "in":
                    regOrwire = "reg"
                else:
                    regOrwire = "wire"
                io_signal_declare_syntax = io_signal_declare_syntax.replace("$regOrwire", regOrwire)
                name = signal.getElementsByTagName('name')[0].firstChild.data
                type = signal.getElementsByTagName('type')[0].firstChild.data
                UUTEnt_content = re.sub(r"\[componentName]", entity_name, UUTEnt_contents)
                UUTEnt_content = re.sub(r"\[signal]", name, UUTEnt_content)

                if type == "single bit":
                    size = ""
                    type = "logic"
                elif type[0:7] == "integer":
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
                elif type[0:7] == "integer":
                    size = ""
                    type = "logic"
                else:
                    depth = 0
                    width = 0
                    type = type.split(",")
                    for i in range(0, len(array_nodes)):
                        typeName = array_nodes[i].getElementsByTagName('name')[0].firstChild.data
                        if typeName == type[1]:
                            depth = array_nodes[i].getElementsByTagName('depth')[0].firstChild.data
                            width = array_nodes[i].getElementsByTagName('width')[0].firstChild.data
                            arrayInfo = [name, depth, width]
                            arrayList.append(arrayInfo)
                    bits = int(width) * int(depth) - 1
                    type = "array"
                    size = "[" + str(bits) + ":0]"
                    bits = int(bits) + 1
                    name = name + "_" + str(bits)
                io_port_map_syntax = io_port_map_syntax.replace("$sig_name", name)
                io_signal_declare_syntax = io_signal_declare_syntax.replace("$sig_name", name)
                io_signal_declare_syntax = io_signal_declare_syntax.replace("$size", size)
                UUTEnt_content = re.sub(r"\[type]", type, UUTEnt_content)
                UUTEnt_content = re.sub(r"\[size]", size, UUTEnt_content)
                UUTEnt += UUTEnt_content

                if signal.getElementsByTagName('mode')[0].firstChild.data == "in":
                    if signal.getElementsByTagName('name')[0].firstChild.data != "clk" and \
                            signal.getElementsByTagName('name')[0].firstChild.data != "rst":
                        if signal.getElementsByTagName('type')[0].firstChild.data == "single bit":
                            inputArray.append(signal.getElementsByTagName('name')[0].firstChild.data)
                            inputsToZero += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " = 1'b0;\n"
                            inputsToOne += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " = '1'b1;\n"
                        elif signal.getElementsByTagName('type')[0].firstChild.data[0:3] == "bus":
                            size = signal.getElementsByTagName('type')[0].firstChild.data
                            digits_list = re.findall(r'\d+', size)
                            size = int(digits_list[0]) + 1
                            inputsToZero += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " = " + str(
                                size) + "'b0;\n"
                            inputsToOne += "\t" + signal.getElementsByTagName('name')[0].firstChild.data + " = " + str(
                                size) + "'b1;\n"
                        else:
                            for i in range(0, len(arrayList)):
                                if signal.getElementsByTagName('name')[0].firstChild.data == arrayList[i][0]:
                                    size = int(arrayList[i][1]) * int(arrayList[i][2])
                                    name = signal.getElementsByTagName('name')[0].firstChild.data + "_" + str(size)
                                    inputsToZero += "\t" + name + " = " + str(size) + "'b0;\n"

                signal_description = signal.getElementsByTagName('description')[
                    0].firstChild.data
                entity_signal_description += "-- " + signal.getElementsByTagName('name')[
                    0].firstChild.data + "\t" + signal_description + "\n"
                # gen_signals += "\t" + signal_declare_syntax + "\n"
                io_port_map += "\t" + io_port_map_syntax + "\n"
                if signal.getElementsByTagName('name')[0].firstChild.data == "clk" or \
                        signal.getElementsByTagName('name')[0].firstChild.data == "rst":
                    clkrst = clkrst + 1
                else:
                    io_signals += io_signal_declare_syntax + "\n"
            wcfg += UUT_contents
            wcfg += UUTEnt
            io_port_map = io_port_map.rstrip()
            io_port_map = io_port_map[0:-1]
            io_signals = io_signals.rstrip()
            chatgpt_tb += "integer testNo;\n"
            chatgpt_tb += "parameter period = 20; // 20 ns\n"
            chatgpt_tb += io_signals
            control_signals = "parameter  period = 20; // 20 ns\n"
            other_signals = ""
            if clkrst > 0:
                other_signals = "reg clk;\n"
                control_signals += "initial clk = 1'b1;\n"
            if clkrst == 2:
                other_signals += "reg rst;\n"
            control_signals += "initial endOfSim = 1'b0;\n"

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
                        size = ""
                    elif type == "single bit":
                        size = ""
                        type = "logic"
                    elif type[0:7] == "integer":
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
                    elif type[0:7] == "integer":
                        size = ""
                        type = "other"
                    else:
                        self.includeArrays = True
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

                gen_header = "// Title Section Start\n"
                gen_header += "// Verilog testbench " + entity_name + "_TB\n"
                gen_header += "// Generated by HDLGen, Github https://github.com/HDLGen-ChatGPT/HDLGen-ChatGPT, on " + str(
                    datetime.now().strftime("%d-%B-%Y")) + " at " + str(datetime.now().strftime("%H:%M")) + "\n\n"
                gen_header += "// Component Name : " + entity_name + "\n"
                title = header_node[0].getElementsByTagName("title")[0].firstChild.data
                gen_header += "// Title          : " + (title if title != "null" else "") + "\n\n"

                authors = header_node[0].getElementsByTagName("authors")[0].firstChild.data
                gen_header += "// Author(s)      : " + (authors if authors != "null" else "") + "\n"
                company = header_node[0].getElementsByTagName("company")[0].firstChild.data
                gen_header += "// Organisation   : " + (company if company != "null" else "") + "\n"
                email = header_node[0].getElementsByTagName("email")[0].firstChild.data
                gen_header += "// Email          : " + (email if email != "null" else "") + "\n"
                gen_header += "// Date           : " + header_node[0].getElementsByTagName("date")[
                    0].firstChild.data + "\n\n"
                gen_header += "// Description    : refer to component hdl model for function description and signal dictionary\n"
                gen_header += "// Title Section End\n"
                tb_code += gen_header

                # Entity declaration
                gen_entity = gen_entity.replace("$comp_name", entity_name)
                tb_code += gen_entity + "\n\n"
                tbSignalDeclaration = sig_decl + "\n" + other_signals + "\n" + io_signals + "\n\n" + control_signals
                # Architecture section

                # Process
                gen_process = ""
                if clkrst > 0:
                    gen_process += "// Generate clk signal, if sequential component, and endOfSim is 0.\n"
                    gen_process += "always # (period/2.0) if (~endOfSim) clk = ~ clk;\n\n"
                gen_process += entity_name + " UUT\n\t(\n"
                gen_process += io_port_map + "\n\t);\n\n"
                gen_process += "initial\nbegin\n"
                gen_process += "$timeformat(-9, 2, \" ns\", 20);\n"
                gen_process += "$display(\"Simulation start :: time is %0t\",$time);\n"
                gen_process += "\t// Apply default INPUT signal values. Do not assign output signals (generated by the UUT) here\n"
                gen_process += "\t// Each stimulus signal change occurs 0.2*period after the active low-to-high clk edge\n"
                gen_process += "\ttestNo = 0;\n"
                gen_process += inputsToZero
                if clkrst == 2:
                    gen_process += "\trst    = 1'b1;\n"
                    gen_process += "\t# (1.2 * period);\n"
                    gen_process += "\trst   = 1'b0;\n"
                    gen_process += "\t# (1 * period);\n"
                if clkrst == 1:
                    gen_process += "\t# (1.2 * period);\n"

                gen_process += "\n\t// Add testbench stimulus here START\n\n\t// === If copying stim_p testbench code, generated by ChatGPT, \n\t// === delete the following lines from the beginning of the pasted code (if they exist)\n\t// === integer testNo;\n\t// === parameter period = 20; // 20 ns\n\t// === reg, wire, declarations  ....\n\t// === initial begin\n\t// === Delete the -- === notes\n\n"
                gen_process += "\t// === If copying a stim_p process generated by ChatGPT, \n\t// === delete the following lines from the end of the pasted code \n\t// === begin end\n\t// === Delete the -- === notes\n\n\t// Add testbench stimulus here END\n\n"
                gen_process += "\t// Print nanosecond (ns) time to simulation transcript\n"
                gen_process += "\t// Use to find time when simulation ends (endOfSim is TRUE)\n"
                gen_process += "\t// Re-run the simulation for this time\n"
                gen_process += "\t// Select timing diagram and use View>Zoom Fit\n"
                gen_process += "\t$display(\"Simulation end :: time is %0t\",$time);\n"
                gen_process += "\tendOfSim = 1'b1; // assert to stop clk signal generation\n\n"

                arch_syntax = verilog_root.getElementsByTagName("architecture")[0].firstChild.data
                gen_arch = arch_syntax.replace("$tbSignalDeclaration", tbSignalDeclaration)
                gen_arch = gen_arch.replace("$arch_elements", gen_process[:-1])

                tb_code += gen_arch
        return entity_name, tb_code, wcfg, chatgpt_tb

    def create_verilog_testbench_file(self, filesNumber):
        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        root = minidom.parse(proj_path + "/HDLGenPrj/" + proj_name + ".hdlgen")
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
        testbench_node = hdlDesign[0].getElementsByTagName('testbench')
        if len(testbench_node) != 0 and testbench_node[0].firstChild is not None:
            tb_node = testbench_node[0].getElementsByTagName('TBNote')[0]
            self.note = tb_node.firstChild.nodeValue
            self.note = self.note.replace("&#10;", "\n")
            self.note = self.note.replace("&amp;", "&")
            self.note = self.note.replace("&quot;", "\"")
            self.note = self.note.replace("&apos;", "\'")
            self.note = self.note.replace("&lt;", "<")
            self.note = self.note.replace("&#x9;", "\t")
            self.note = self.note.replace("&gt;", ">")
            self.note = self.note.replace("&#44;", ",")
        else:
            self.note = "No Test Plan created"
        chatgpt = hdlDesign[0].getElementsByTagName('chatgpt')[0]
        VerilogTestbench = "None"
        if chatgpt.hasChildNodes():
            commands_node = chatgpt.getElementsByTagName('commands')[0]
            VerilogTestbench = commands_node.getElementsByTagName('VerilogTestbench')[0].firstChild.data
            VerilogTestbench = VerilogTestbench.replace("&#10;", "\n")
            VerilogTestbench = VerilogTestbench.replace("&amp;", "&")
            VerilogTestbench = VerilogTestbench.replace("&quot;", "\"")
            VerilogTestbench = VerilogTestbench.replace("&apos;", "\'")
            VerilogTestbench = VerilogTestbench.replace("&lt;", "<")
            VerilogTestbench = VerilogTestbench.replace("&#x9;", "\t")
            VerilogTestbench = VerilogTestbench.replace("&gt;", ">")
            VerilogTestbench = VerilogTestbench.replace("&#44;", ",")
            #does not display lines starting with ~
            lines = VerilogTestbench.split('\n')
            filtered_lines = [line for line in lines if not line.startswith('~')]
            VerilogTestbench = '\n'.join(filtered_lines)
        entity_name, verilog_tb_code, waveform, chatgpt_tb = self.create_verilog_testbench_code()
        chatgpt_tb = VerilogTestbench + "\n\n" + chatgpt_tb + "\n\n" + self.note
        verilog_tb_path = os.path.join(proj_path, "Verilog", "testbench", entity_name + "_TB.v")
        verilog_tb_HDLGen_path = os.path.join(proj_path, "Verilog", "testbench", entity_name + "_TB_backup.v")
        waveform_path = os.path.join(proj_path, "Verilog", "AMDprj", entity_name + "_TB_behav.wcfg")
        chatgpt_verilog_file_path = os.path.join(proj_path, "Verilog", "ChatGPT",
                                                 entity_name + "_Verilog_TB_ChatGPT.txt")
        chatgpt_verilog_HDLGen_file_path = os.path.join(proj_path, "Verilog", "ChatGPT", "Backups",
                                                        entity_name + "_Verilog_TB_ChatGPT_backup.txt")

        if "3" in filesNumber:
            base_name, extension = os.path.splitext(verilog_tb_HDLGen_path)
            new_filename = verilog_tb_HDLGen_path
            if os.path.isfile(new_filename):
                # File already exists, modify the name
                index = 1
                while os.path.isfile(new_filename):
                    index += 1
                    new_filename = f"{base_name}_{index}{extension}"
            try:
                with open(verilog_tb_path, 'r') as source:
                    with open(new_filename, "w") as f:
                        content = source.read()
                        f.write(content)
                    print("Verilog Testbench Backup file successfully generated at ", new_filename)
            except FileNotFoundError:
                with open(new_filename, "w") as f:
                    f.write(verilog_tb_code)
                print("Verilog Testbench backup file successfully generated at ", new_filename)
        if "2" in filesNumber:
            with open(verilog_tb_path, "w") as f:
                f.write(verilog_tb_code)
            print("Verilog Testbench file successfully generated at ", verilog_tb_path)

        if "9" in filesNumber:
            base_name, extension = os.path.splitext(chatgpt_verilog_HDLGen_file_path)
            new_filename = chatgpt_verilog_HDLGen_file_path
            if os.path.isfile(new_filename):
                # File already exists, modify the name
                index = 1
                while os.path.isfile(new_filename):
                    index += 1
                    new_filename = f"{base_name}_{index}{extension}"
            try:
                with open(chatgpt_verilog_file_path, 'r') as source:
                    with open(new_filename, "w") as f:
                        content = source.read()
                        f.write(content)
                    print("Verilog Testbench ChatGPT Backup file successfully generated at ", new_filename)
            except FileNotFoundError:
                with open(new_filename, "w") as f:
                    f.write(chatgpt_tb)
                print("Verilog Testbench ChatGPT backup file successfully generated at ", new_filename)

        if "8" in filesNumber:
            with open(chatgpt_verilog_file_path, "w") as f:
                f.write(chatgpt_tb)
            pyperclip.copy(chatgpt_tb)
            print("Verilog Testbench ChatGPT file successfully generated at ", chatgpt_verilog_file_path)

        if "10" in filesNumber:
            with open(waveform_path, "w") as f:
                f.write(waveform)
            print("Waveform file successfully generated at ", waveform_path)

    def copy_file_contents_to_clipboard(self, file_path):
        try:
            with open(file_path, 'r') as file:
                file_contents = file.read()
                pyperclip.copy(file_contents)
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("File contents copied to clipboard successfully")
                msgBox.exec_()
        except FileNotFoundError:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("File not found. Press Generate button")
            msgBox.exec_()
        except Exception as e:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("An error occurred. Check terminal for details")
            msgBox.exec_()
            print("An error occurred:", str(e))