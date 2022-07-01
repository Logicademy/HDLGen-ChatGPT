import os
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from Application.HDLDesigner.comp_details import CompDetails
from Application.HDLDesigner.IOPorts.io_ports import IOPorts
from Application.HDLDesigner.Architecture.architecture import Architecture
from Application.Generator.generator import Generator
from Application.ProjectManager.projectManager import ProjectManager


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

        self.setup_ui()

        if load_data:
            self.update_preview()

    def setup_ui(self):

        compDetails = CompDetails(self.proj_dir)
        ioPorts = IOPorts(self.proj_dir)
        architecture = Architecture(self.proj_dir)

        self.preview_window.setReadOnly(True)
        self.preview_pane_layout.addWidget(self.preview_label)
        self.preview_pane_layout.addWidget(self.preview_window)

        self.tabs.addTab(compDetails, "Component Details")
        # self.tabs.addTab(ClkRst(self.proj_dir), "Clock and Reset")
        self.tabs.addTab(ioPorts, "Component I/O Ports")
        self.tabs.addTab(architecture, "Architecture")

        self.mainLayout.addWidget(self.tabs)
        self.mainLayout.addLayout(self.preview_pane_layout)
        self.setLayout(self.mainLayout)

        compDetails.save_btn.clicked.connect(self.update_preview)
        ioPorts.save_signal_btn.clicked.connect(self.update_preview)
        architecture.save_btn.clicked.connect(self.update_preview)

    def update_preview(self):
        entity_name, vhdl = Generator.generate_vhdl()
        self.preview_window.setText(vhdl)

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