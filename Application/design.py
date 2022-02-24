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


class Design(QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QHBoxLayout()
        self.preview_pane_layout = QVBoxLayout()

        self.preview_label = QLabel("Preview")
        self.preview_window = QTextEdit()

        self.tabs = VerticalTabWidget()

        # Creating a container
        self.container = QWidget()

        self.setup_ui()

    def setup_ui(self):

        self.preview_pane_layout.addWidget(self.preview_label)
        self.preview_pane_layout.addWidget(self.preview_window)

        self.tabs.addTab(CompDetails(), "Component Details")
        self.tabs.addTab(ClkRst(), "Clock and Reset")
        self.tabs.addTab(IOPorts(), "Component I/O Ports")
        self.tabs.addTab(Architecture(), "Architecture")

        self.mainLayout.addWidget(self.tabs)
        self.mainLayout.addLayout(self.preview_pane_layout)
        self.setLayout(self.mainLayout)


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