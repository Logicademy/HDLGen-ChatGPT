import os
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import sys
sys.path.append("..")
from HDLDesigner.comp.comp_details import CompDetails
from HDLDesigner.IOPorts.io_ports import IOPorts
from HDLDesigner.Architecture.architecture import Architecture
from HDLDesigner.testPlan.testplan import TestPlan
from HDLDesigner.ChatGPT.chatgpt import ChatGPT
from HDLDesigner.InternalSignal.internal_signal import InternalSignal
from HDLDesigner.Package.package import Package
from HDLDesigner.Subcomponents.subcomponents import Subcomponents
from Generator.generator import Generator
from ProjectManager.project_manager import ProjectManager


class HDLDesigner(QWidget):

    def __init__(self, proj_dir, load_data):
        super().__init__()

        self.proj_dir = proj_dir
        self.code = "No Model Code"
        self.chatgpt_header = "No Header Command Entered"
        self.chatgpt_model = "No Model Command Entered"
        self.chatgpt_tb = "No Testbench"
        self.tb_code = "No Testbench"
        self.ModelCmd = "No Command Entered"
        self.HeaderCmd = "No Command Entered"
        self.TBCmd = "No Command Entered"
        self.hdl = "VHDL"
        self.mainLayout = QHBoxLayout()
        self.preview_pane_layout = QVBoxLayout()

        self.preview_label = QLabel("Preview")
        self.preview_window = QTextEdit()

        self.tabs = VerticalTabWidget()
        self.tabs.other_class = self
        # Creating a container
        self.container = QWidget()
        #self.compDetails = CompDetails(self.proj_dir)
        self.project_manager = ProjectManager(self.proj_dir, self)
        self.setup_ui()
        self.hdl = "VHDL"
        if load_data:
            if self.project_manager.vhdl_check.isChecked():
                self.hdl = "VHDL"
                self.update_preview("VHDL")
            else:
                self.hdl = "Verilog"
                self.update_preview("Verilog")
        else:
            self.hdl = "VHDL"
    def setup_ui(self):
        self.compDetails = CompDetails(self.proj_dir)
        #compDetails = CompDetails(self.proj_dir)
        ioPorts = IOPorts(self.proj_dir)
        self.architecture = Architecture(self.proj_dir)
        testplan = TestPlan(self.proj_dir)
        self.chatGPT = ChatGPT(self.proj_dir)
        internalSignal = InternalSignal(self.proj_dir)
        package = Package()
        subcomponents = Subcomponents()

        self.preview_window.setReadOnly(True)
        self.preview_pane_layout.addWidget(self.preview_label)
        self.preview_pane_layout.addWidget(self.preview_window)

        self.tabs.addTab(self.compDetails, "Component")
        #self.tabs.addTab(compDetails, "Component")
        self.tabs.addTab(package, "VHDL types")
        self.tabs.addTab(subcomponents, "Sub-components")
        self.tabs.addTab(ioPorts, "Ports")
        self.tabs.addTab(internalSignal, "Internal Signals")
        self.tabs.addTab(self.architecture, "Architecture")
        self.tabs.addTab(testplan, "Test Plan")
        self.tabs.addTab(self.chatGPT,"ChatGPT")
        font = self.tabs.font()
        font.setPointSize(10)
        self.tabs.setFont(font)
        self.mainLayout.addWidget(self.tabs)
        self.mainLayout.addLayout(self.preview_pane_layout)
        self.setLayout(self.mainLayout)

        #self.compDetails.save_btn.clicked.connect(self.update_preview)
        self.compDetails.save_signal.connect(self.update_preview)
        #compDetails.save_signal.connect(self.update_preview)
        #ioPorts.save_signal_btn.clicked.connect(self.update_preview)
        ioPorts.save_signal.connect(self.update_preview)
        ioPorts.save_signal.connect(self.update_arch)
        #ioPorts.save_signal_btn.clicked.connect(self.update_arch)
        #internalSignal.save_signal_btn.clicked.connect(self.update_preview)
        internalSignal.save_signal.connect(self.update_preview)
        #self.architecture.save_btn.clicked.connect(self.update_preview)
        self.architecture.save_signal.connect(self.update_preview)
        self.chatGPT.save_signal.connect(self.update_preview)
        self.chatGPT.header_check.clicked.connect(self.update_preview)
        self.chatGPT.model_check.clicked.connect(self.update_preview)
        self.chatGPT.testbench_check.clicked.connect(self.update_preview)

    def update_preview(self, hdl):
        print(hdl)
        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        root = minidom.parse(proj_path + "/HDLGenPrj/" + proj_name + ".hdlgen")
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
        testbench_node = hdlDesign[0].getElementsByTagName('testbench')
        if len(testbench_node) != 0 and testbench_node[0].firstChild is not None:
            tb_node = testbench_node[0].getElementsByTagName('TBNote')[0]
            self.tbnote = tb_node.firstChild.nodeValue
            self.tbnote = self.tbnote.replace("&#10;", "\n")
            self.tbnote = self.tbnote.replace("&amp;", "&")
            self.tbnote = self.tbnote.replace("&quot;", "\"")
            self.tbnote = self.tbnote.replace("&apos;", "\'")
            self.tbnote = self.tbnote.replace("&lt;", "<")
            self.tbnote = self.tbnote.replace("&#x9;", "\t")
            self.tbnote = self.tbnote.replace("&gt;", ">")
            self.tbnote = self.tbnote.replace("&#44;", ",")
            if self.tbnote == "None":
                self.tbnote = "No Test Plan Created"
        else:
            self.tbnote = "No Test Plan Created"

        if hdl != False and hdl != True:
            self.hdl = hdl
        if self.hdl == "VHDL":
            print("VHDL")
            entity_name, self.code, instances, self.chatgpt_header, self.chatgpt_model = Generator.generate_vhdl(self)
            entity_name, self.tb_code, wcfg, self.chatgpt_tb = Generator.create_vhdl_testbench_code(self)
            chatgpt = hdlDesign[0].getElementsByTagName('chatgpt')[0]
            if chatgpt.hasChildNodes():
                commands_node = chatgpt.getElementsByTagName('commands')[0]
                VHDLHeader = commands_node.getElementsByTagName('VHDLHeader')[0].firstChild.data
                VHDLHeader = VHDLHeader.replace("&#10;", "\n")
                VHDLHeader = VHDLHeader.replace("&amp;", "&")
                VHDLHeader = VHDLHeader.replace("&quot;", "\"")
                VHDLHeader = VHDLHeader.replace("&apos;", "\'")
                VHDLHeader = VHDLHeader.replace("&lt;", "<")
                VHDLHeader = VHDLHeader.replace("&#x9;", "\t")
                VHDLHeader = VHDLHeader.replace("&gt;", ">")
                VHDLHeader = VHDLHeader.replace("&#44;", ",")
                self.HeaderCmd = VHDLHeader
                VHDLModel = commands_node.getElementsByTagName('VHDLModel')[0].firstChild.data
                VHDLModel = VHDLModel.replace("&#10;", "\n")
                VHDLModel = VHDLModel.replace("&amp;", "&")
                VHDLModel = VHDLModel.replace("&quot;", "\"")
                VHDLModel = VHDLModel.replace("&apos;", "\'")
                VHDLModel = VHDLModel.replace("&lt;", "<")
                VHDLModel = VHDLModel.replace("&#x9;", "\t")
                VHDLModel = VHDLModel.replace("&gt;", ">")
                VHDLModel = VHDLModel.replace("&#44;", ",")
                self.ModelCmd = VHDLModel
                VHDLTestbench = commands_node.getElementsByTagName('VHDLTestbench')[0].firstChild.data
                VHDLTestbench = VHDLTestbench.replace("&#10;", "\n")
                VHDLTestbench = VHDLTestbench.replace("&amp;", "&")
                VHDLTestbench = VHDLTestbench.replace("&quot;", "\"")
                VHDLTestbench = VHDLTestbench.replace("&apos;", "\'")
                VHDLTestbench = VHDLTestbench.replace("&lt;", "<")
                VHDLTestbench = VHDLTestbench.replace("&#x9;", "\t")
                VHDLTestbench = VHDLTestbench.replace("&gt;", ">")
                VHDLTestbench = VHDLTestbench.replace("&#44;", ",")
                self.TBCmd = VHDLTestbench
        elif self.hdl == "Verilog":
            print("verilog")
            entity_name,self.code, instances, self.chatgpt_header, self.chatgpt_model = Generator.generate_verilog(self)
            entity_name, self.tb_code, wcfg, self.chatgpt_tb = Generator.create_verilog_testbench_code(self)
            chatgpt = hdlDesign[0].getElementsByTagName('chatgpt')[0]
            if chatgpt.hasChildNodes():
                commands_node = chatgpt.getElementsByTagName('commands')[0]
                VerilogHeader = commands_node.getElementsByTagName('VerilogHeader')[0].firstChild.data
                VerilogHeader = VerilogHeader.replace("&#10;", "\n")
                VerilogHeader = VerilogHeader.replace("&amp;", "&")
                VerilogHeader = VerilogHeader.replace("&quot;", "\"")
                VerilogHeader = VerilogHeader.replace("&apos;", "\'")
                VerilogHeader = VerilogHeader.replace("&lt;", "<")
                VerilogHeader = VerilogHeader.replace("&#x9;", "\t")
                VerilogHeader = VerilogHeader.replace("&gt;", ">")
                VerilogHeader = VerilogHeader.replace("&#44;", ",")
                self.HeaderCmd = VerilogHeader
                VerilogModel = commands_node.getElementsByTagName('VerilogModel')[0].firstChild.data
                VerilogModel = VerilogModel.replace("&#10;", "\n")
                VerilogModel = VerilogModel.replace("&amp;", "&")
                VerilogModel = VerilogModel.replace("&quot;", "\"")
                VerilogModel = VerilogModel.replace("&apos;", "\'")
                VerilogModel = VerilogModel.replace("&lt;", "<")
                VerilogModel = VerilogModel.replace("&#x9;", "\t")
                VerilogModel = VerilogModel.replace("&gt;", ">")
                VerilogModel = VerilogModel.replace("&#44;", ",")
                self.ModelCmd=VerilogModel
                VerilogTestbench = commands_node.getElementsByTagName('VerilogTestbench')[0].firstChild.data
                VerilogTestbench = VerilogTestbench.replace("&#10;", "\n")
                VerilogTestbench = VerilogTestbench.replace("&amp;", "&")
                VerilogTestbench = VerilogTestbench.replace("&quot;", "\"")
                VerilogTestbench = VerilogTestbench.replace("&apos;", "\'")
                VerilogTestbench = VerilogTestbench.replace("&lt;", "<")
                VerilogTestbench = VerilogTestbench.replace("&#x9;", "\t")
                VerilogTestbench = VerilogTestbench.replace("&gt;", ">")
                VerilogTestbench = VerilogTestbench.replace("&#44;", ",")
                self.TBCmd = VerilogTestbench
        if self.tabs.currentIndex() == 6:
            self.preview_window.setText(self.tb_code)
        elif self.tabs.currentIndex() == 7:
            if self.chatGPT.header_check.isChecked():
                self.preview_window.setText(self.HeaderCmd + "\n\n" +self.chatgpt_header)
                print("header")
            elif self.chatGPT.model_check.isChecked():
                self.preview_window.setText(self.ModelCmd + "\n\n" +self.chatgpt_model)
                print("model")
            elif self.chatGPT.testbench_check.isChecked():
                self.chatgpt_tb = self.TBCmd + "\n\n"+self.chatgpt_tb + "\n\n" + self.tbnote
                self.preview_window.setText(self.chatgpt_tb)
                print("testbench")
        else:
            self.preview_window.setText(self.code)
    def update_arch(self):
        xml_data_path = ProjectManager.get_xml_data_path()
        self.architecture.updateProcessName(xml_data_path)

    def get_hdl(self):
        return self.hdl

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
    def __init__(self, other_class=None, *args, **kwargs):
        QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBar())
        self.setTabPosition(QTabWidget.West)
        self.currentChanged.connect(self.tab_changed)
        self.previous_index = self.currentIndex()
        self.other_class = other_class
    def tab_changed(self, index):
        # save state of previous tab
        prev_tab = self.widget(self.previous_index)
        if index == 6 or index == 7:
            if self.other_class:
                lang = self.other_class.get_hdl()
                self.other_class.update_preview(lang)
        if self.previous_index == 6 or self.previous_index == 7:
            if self.other_class:
                lang = self.other_class.get_hdl()
                self.other_class.update_preview(lang)
        self.previous_index = index


