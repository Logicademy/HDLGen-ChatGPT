#Test Plan section in HDL Designer. This class will call note_dialog.py when adding/editing test plan and testplan_help.md if help button is clicked
#This class will save all entered data to the .hdlgen. The save happens when there is a change.

import os
import sys
import configparser
from xml.dom import minidom
import qtawesome as qta
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from ProjectManager.project_manager import ProjectManager
from HDLDesigner.Architecture.note_dialog import note_Dialog
from HDLDesigner.testPlan.testplan_help import TestPlanHelpDialog

sys.path.append("..")

WHITE_COLOR = "color: white"
BLACK_COLOR = "color: black"

class TestPlan(QWidget):
    save_signal = Signal(bool)

    # Defines UI components and their visual characteristics, as well as class variables needed for the Test Plan tab
    def __init__(self, proj_dir):
        super().__init__()

        small_text_font = QFont().setPointSize(10)
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)

        self.proj_dir = proj_dir
        self.note = "None"

        self.main_layout = QVBoxLayout()
        self.input_layout = QGridLayout()

        self.testbench_btn = QPushButton("Test Plan")
        self.testbench_btn.setFont(small_text_font)
        self.testbench_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px; }"
            "QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
        )

        self.testplan_label = QLabel("Test Plan")
        self.testplan_label.setFont(title_font)
        self.testplan_label.setStyleSheet(WHITE_COLOR)

        self.testbench_label = QLabel("Preview")
        self.testbench_label.setFont(title_font)
        self.testbench_label.setStyleSheet(BLACK_COLOR)

        self.testplan_input = QTextEdit()
        self.testplan_input.setReadOnly(True)

        # The (?) button in the Test Plab tab
        self.testplan_info_btn = QPushButton()
        self.testplan_info_btn.setIcon(qta.icon("mdi.help"))
        self.testplan_info_btn.setFixedSize(25, 25)
        self.testplan_info_btn.clicked.connect(self.testplan_help_window)

        self.top_layout = QHBoxLayout()
        self.arch_action_layout = QVBoxLayout()
        self.btn_layout = QHBoxLayout()

        self.vspacer = QSpacerItem(30, 40)
        self.list_layout = QVBoxLayout()
        self.list_frame = QFrame()
        self.main_frame = QFrame()
        self.input_frame = QFrame()

        self.setup_ui()
        self.load_data()

    # Sets up key UI components defined in __init__(), by adding their callback functions
    # Adds UI components into their respective layouts and sets the interface layout for the Test Plan tab
    def setup_ui(self):
        bold_font = QFont()
        bold_font.setBold(True)

        self.top_layout.addWidget(self.testplan_label)
        self.top_layout.addWidget(self.testbench_btn, alignment=Qt.AlignRight)
        self.top_layout.addWidget(self.testplan_info_btn)

        self.arch_action_layout.addLayout(self.top_layout)

        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')

        self.main_frame.setLayout(self.arch_action_layout)
        self.list_layout.addWidget(self.testbench_label)
        self.list_layout.addWidget(self.testplan_input)

        self.list_frame.setFrameShape(QFrame.StyledPanel)
        self.list_frame.setStyleSheet('.QFrame{background-color: white; border-radius: 5px;}')
        self.list_frame.setLayout(self.list_layout)

        self.arch_action_layout.addItem(QSpacerItem(0, 5))
        self.arch_action_layout.addWidget(self.list_frame)
        self.arch_action_layout.addItem(QSpacerItem(0, 5))
        self.testbench_btn.clicked.connect(self.add_testplan)

        self.main_layout.addWidget(self.main_frame)

        self.setLayout(self.main_layout)

    def add_testplan(self):
        if self.proj_dir is not None:
            root = minidom.parse(self.proj_dir[0])
            HDLGen = root.documentElement
            hdl_design = HDLGen.getElementsByTagName("hdlDesign")
            testbench_node = hdl_design[0].getElementsByTagName('testbench')
            
            if len(testbench_node) != 0 and testbench_node[0].firstChild is not None:
                tb_note = testbench_node[0].getElementsByTagName('TBNote')[0]
                self.note = tb_note.firstChild.nodeValue

        button = self.sender()
        if button:
            add_note = note_Dialog("edit","Test Plan",self.note)
            add_note.exec_()

            if not add_note.cancelled:
                note_data = add_note.get_data()
                self.note = note_data
                self.save_data()

    def save_data(self):
        xml_data_path = ProjectManager.get_xml_data_path()

        root = minidom.parse(xml_data_path)
        HDLGen = root.documentElement
        hdl_design = HDLGen.getElementsByTagName("hdlDesign")
        testbench_node = root.createElement("testbench")
        tb_note = root.createElement("TBNote")
        tb_note.appendChild(root.createTextNode(self.note))
        testbench_node.appendChild(tb_note)
        hdl_design[0].replaceChild(testbench_node, hdl_design[0].getElementsByTagName("testbench")[0])
        # converting the doc into a string in xml format
        xml_str = root.toprettyxml()
        xml_str = os.linesep.join([s for s in xml_str.splitlines() if s.strip()])
        # Writing xml file
        with open(xml_data_path, "w") as f:
            f.write(xml_str)
        note_data = self.note
        note_data = note_data.replace("&#10;", "\n")
        note_data = note_data.replace("&amp;", "&")
        note_data = note_data.replace("&amp;", "&")
        note_data = note_data.replace("&quot;", "\"")
        note_data = note_data.replace("&apos;", "\'")
        note_data = note_data.replace("&lt;", "<")
        note_data = note_data.replace("&#x9;", "\t")
        note_data = note_data.replace("&gt;", ">")
        note_data = note_data.replace("&#44;", ",")

        # if note_data != "None":
        #     self.testbench_btn.setText("Edit Test Plan")
        # else:
        #     note_data = "No test plan created"
        #     self.testbench_btn.setText("Add Test Plan")
        self.testbench_btn.setText("Edit Test Plan")

        self.testplan_input.setText(note_data)
        self.note = note_data
        print("Saved test plan")

    def load_data(self):
        self.note = self.generate_testplan_template()

        if self.proj_dir is not None:
            root = minidom.parse(self.proj_dir[0])
            HDLGen = root.documentElement
            hdl_design = HDLGen.getElementsByTagName("hdlDesign")
            testbench_node = hdl_design[0].getElementsByTagName('testbench')
            if len(testbench_node) != 0 and testbench_node[0].firstChild is not None:
                tb_note = testbench_node[0].getElementsByTagName('TBNote')[0]
                self.note = tb_note.firstChild.nodeValue
            note_data = self.note
            note_data = note_data.replace("&#10;", "\n")
            note_data = note_data.replace("&amp;", "&")
            note_data = note_data.replace("&amp;", "&")
            note_data = note_data.replace("&quot;", "\"")
            note_data = note_data.replace("&apos;", "\'")
            note_data = note_data.replace("&lt;", "<")
            note_data = note_data.replace("&#x9;", "\t")
            note_data = note_data.replace("&gt;", ">")
            note_data = note_data.replace(",","&#44;")
            self.testbench_btn.setText("Edit Test Plan")
            self.testplan_input.setText(note_data)
            self.note = note_data

    def generate_testplan_template(self):
        template = [
            ("Signals", "Signal Radix")
        ]

        for name, mode, _, width in self.HDLDesigner.ioPorts.all_signals:
            template.append(
                (f"{name} ({mode})", width)
            )

        template.append(
            ("TestNo", "1'd"), ("Delay", "1'd"), ("Note", "String")
        )

        output = ""
        for row in template:
            output += ("\t".join(row) + "\n")

        return output

    # Defines the (?) button on the Test Plan tab
    def testplan_help_window(self):
        testplan_help_dialog = TestPlanHelpDialog()
        testplan_help_dialog.exec_()
