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
        chatGPT = ChatGPT(self.proj_dir)
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
        self.tabs.addTab(chatGPT,"ChatGPT")
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
        chatGPT.save_signal.connect(self.update_preview)

    def update_preview(self, hdl):
        if hdl != False:
            self.hdl = hdl

        if self.hdl == "VHDL":
            entity_name, code, instances, chatgpt_header, chatgpt_vhdl = Generator.generate_vhdl(self)
        elif self.hdl == "Verilog":
            entity_name,code, instances, chatgpt_header, chatgpt_vhdl = Generator.generate_verilog(self)
        self.preview_window.setText(code)
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
        #self.currentChanged.connect(self.tab_changed)
        self.previous_index = self.currentIndex()
        self.other_class = other_class
    def tab_changed(self, index):
        # save state of previous tab
        prev_tab = self.widget(self.previous_index)
        if prev_tab:
            prev_tab.save_data()
            if self.other_class:
                lang = self.other_class.get_hdl()
                self.other_class.update_preview(lang)
        self.previous_index = index


