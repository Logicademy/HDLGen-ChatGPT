import os
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import sys
sys.path.append("..")
from HDLDesigner.comp_details import CompDetails
from HDLDesigner.IOPorts.io_ports import IOPorts
from HDLDesigner.Architecture.architecture import Architecture
from HDLDesigner.InternalSignal.internal_signal import InternalSignal
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

        # Creating a container
        self.container = QWidget()
        self.compDetails = CompDetails(self.proj_dir)
        self.setup_ui()

        if load_data:
            self.update_preview()

    def setup_ui(self):
        print("in set up")
        self.compDetails = CompDetails(self.proj_dir)
        ioPorts = IOPorts(self.proj_dir)
        self.architecture = Architecture(self.proj_dir)
        internalSignal = InternalSignal(self.proj_dir)

        self.preview_window.setReadOnly(True)
        self.preview_pane_layout.addWidget(self.preview_label)
        self.preview_pane_layout.addWidget(self.preview_window)

        self.tabs.addTab(self.compDetails, "Component")
        # self.tabs.addTab(ClkRst(self.proj_dir), "Clock and Reset")
        self.tabs.addTab(ioPorts, "Ports")
        self.tabs.addTab(internalSignal, "Internal Signals")
        self.tabs.addTab(self.architecture, "Architecture")

        self.mainLayout.addWidget(self.tabs)
        self.mainLayout.addLayout(self.preview_pane_layout)
        self.setLayout(self.mainLayout)

        self.compDetails.save_btn.clicked.connect(self.update_preview)
        ioPorts.save_signal_btn.clicked.connect(self.update_preview)
        ioPorts.save_signal_btn.clicked.connect(self.update_arch)
        self.architecture.save_btn.clicked.connect(self.update_preview)
        internalSignal.save_signal_btn.clicked.connect(self.update_preview)

    def update_preview(self):
        entity_name, vhdl = Generator.generate_vhdl()
        self.preview_window.setText(vhdl)
    def update_arch(self):
        xml_data_path = ProjectManager.get_xml_data_path()
        print(xml_data_path)
        #print(self.proj_dir)
        self.architecture.updateProcessName(xml_data_path)
        #self.architecture.updateProcessName(self.proj_dir)#load_data(self.proj_dir)

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

