import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from comp_details import CompDetails
from io_ports import IOPorts
from architecture import Architecture
from clk_rst import ClkRst

from projectManager import ProjectManager

class Design(QWidget):

    def __init__(self, proj_dir, load_data):
        super().__init__()

        self.proj_dir = proj_dir

        self.mainLayout = QHBoxLayout()
        self.preview_pane_layout = QVBoxLayout()

        self.preview_label = QLabel("Preview")
        self.preview_window = QTextEdit()

        self.tabs = VerticalTabWidget()

        # Creating a container
        self.container = QWidget()

        self.setup_ui()

        if load_data:
            self.update_preview()

    def setup_ui(self):

        compDetails = CompDetails(self.proj_dir)

        self.preview_window.setReadOnly(True)
        self.preview_pane_layout.addWidget(self.preview_label)
        self.preview_pane_layout.addWidget(self.preview_window)

        self.tabs.addTab(compDetails, "Component Details")
        self.tabs.addTab(ClkRst(self.proj_dir), "Clock and Reset")
        self.tabs.addTab(IOPorts(self.proj_dir), "Component I/O Ports")
        self.tabs.addTab(Architecture(self.proj_dir), "Architecture")

        self.mainLayout.addWidget(self.tabs)
        self.mainLayout.addLayout(self.preview_pane_layout)
        self.setLayout(self.mainLayout)

        compDetails.save_btn.clicked.connect(self.update_preview)


    def update_preview(self):
        vhdl = self.generate_vhdl()
        self.preview_window.setText(vhdl)

    def generate_vhdl(self):

        self.gen_vhdl = ""

        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        xml_data_path = os.path.join(proj_path, 'HDLGenPrj', proj_name + '.hdlgen')

        test_xml = os.path.join("resources", "SampleProject.xml")

        vhdl_database_path = os.path.join("resources", "HDL_Database", "vhdl_database.xml")

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

                if io_port_node is not None:
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
                if int_sig_node is not None:
                    for signal in int_sig_node[0].getElementsByTagName("signal"):
                        int_sig_syntax = vhdl_root.getElementsByTagName("intSigDeclaration")[0].firstChild.data
                        int_sig_syntax = int_sig_syntax.replace("$int_sig_name", signal.getElementsByTagName('name')[0].firstChild.data)
                        int_sig_syntax = int_sig_syntax.replace("$int_sig_type", signal.getElementsByTagName('type')[0].firstChild.data)

                        gen_int_sig += int_sig_syntax

                    gen_int_sig.rstrip()

                # Process
                arch_node = hdl_design[0].getElementsByTagName("architecture")

                gen_process = ""

                if arch_node is not None:
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
                    arch_name_node = arch_node[0].getElementsByTagName("archName")

                    arch_name = "comb"

                    if len(arch_name_node) != 0:
                        arch_name = arch_name_node[0].firstChild.data

                    gen_arch = arch_syntax.replace("$arch_name", arch_name)
                    gen_arch = gen_arch.replace("$comp_name", entity_name)
                    gen_arch = gen_arch.replace("$int_sig_declaration", gen_int_sig)
                    gen_arch = gen_arch.replace("$arch_elements", gen_process[:-1])

                    self.gen_vhdl += gen_arch

        return self.gen_vhdl

class TabBar(QTabBar):
    def tabSizeHint(self, index):
        s = QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QStylePainter(self)
        opt = QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size() * 100
            s.transpose()
            r = QRect(QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QStyle.CE_TabBarTabLabel, opt)
            painter.restore()

class VerticalTabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBar())
        self.setTabPosition(QTabWidget.West)