import os
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import qtawesome as qta
import sys
import configparser
sys.path.append("..")
from ProjectManager.project_manager import ProjectManager
from HDLDesigner.Architecture.note_dialog import note_Dialog
from HDLDesigner.testPlan.testplan_help import TestPlanHelpDialog


WHITE_COLOR = "color: white"
BLACK_COLOR = "color: black"

class TestPlan(QWidget):
    save_signal = Signal(bool)
    def __init__(self, proj_dir):
        super().__init__()
        small_text_font = QFont()
        small_text_font.setPointSize(10)
        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        self.proj_dir = proj_dir

        self.mainLayout = QVBoxLayout()

        self.input_layout = QGridLayout()

        self.testbench_btn = QPushButton("Test Plan")
        self.testbench_btn.setFixedSize(160, 25)
        self.testbench_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}")

        self.testplan_label = QLabel("Test Plan")
        self.testplan_label.setFont(title_font)
        self.testplan_label.setStyleSheet(WHITE_COLOR)

        self.testbench_label = QLabel("Preview")
        self.testbench_label.setFont(title_font)
        self.testbench_label.setStyleSheet(BLACK_COLOR)

        self.testplan_input = QTextEdit()
        self.testplan_input.setReadOnly(True)

        self.testPlan_info_btn = QPushButton()
        self.testPlan_info_btn.setIcon(qta.icon("mdi.help"))
        self.testPlan_info_btn.setFixedSize(25, 25)
        self.testPlan_info_btn.clicked.connect(self.testPlan_help_window)

        self.top_layout = QGridLayout()
        self.arch_action_layout = QVBoxLayout()
        self.btn_layout = QHBoxLayout()

        self.vspacer = QSpacerItem(30, 40)
        self.list_layout = QVBoxLayout()
        self.list_frame = QFrame()
        self.main_frame = QFrame()
        self.input_frame = QFrame()
        self.setup_ui()
        if proj_dir != None:
            self.load_data(proj_dir)

    def setup_ui(self):
        bold_font = QFont()
        bold_font.setBold(True)

        self.top_layout.addWidget(self.testplan_label, 0, 0, 1, 1)
        self.top_layout.addWidget(self.testbench_btn, 0, 1, 1, 1)
        self.top_layout.addWidget(self.testPlan_info_btn, 0, 2, 1, 1)

        self.arch_action_layout.addLayout(self.top_layout)

        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        # self.main_frame.setFixedSize(500, 400)

        self.main_frame.setLayout(self.arch_action_layout)
        self.list_layout.addWidget(self.testbench_label)
        self.list_layout.addWidget(self.testplan_input)

        self.list_frame.setFrameShape(QFrame.StyledPanel)
        self.list_frame.setStyleSheet('.QFrame{background-color: white; border-radius: 5px;}')
        # self.list_frame.setFixedSize(420, 300)
        self.list_frame.setLayout(self.list_layout)

        self.arch_action_layout.addItem(QSpacerItem(0, 5))
        self.arch_action_layout.addWidget(self.list_frame)  # , alignment=Qt.AlignCenter)
        self.arch_action_layout.addItem(QSpacerItem(0, 5))
        self.testbench_btn.clicked.connect(self.add_testplan)

        self.mainLayout.addWidget(self.main_frame)  # , alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)

    def add_testplan(self):
        self.note = ""
        if self.proj_dir is not None:
            root = minidom.parse(self.proj_dir[0])
            HDLGen = root.documentElement
            hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
            testbench_node = hdlDesign[0].getElementsByTagName('testbench')
            if len(testbench_node) != 0 and testbench_node[0].firstChild is not None:
                tb_node = testbench_node[0].getElementsByTagName('TBNote')[0]
                self.note = tb_node.firstChild.nodeValue
        button = self.sender()
        if button:
            add_note = note_Dialog("edit", self.note)
            add_note.exec_()

            if not add_note.cancelled:
                note_data = add_note.get_data()
                self.note = note_data
                xml_data_path = ProjectManager.get_xml_data_path()

                root = minidom.parse(xml_data_path)
                HDLGen = root.documentElement
                hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
                testbench_node = root.createElement("testbench")
                tb_node = root.createElement("TBNote")
                tb_node.appendChild(root.createTextNode(self.note))
                testbench_node.appendChild(tb_node)
                hdlDesign[0].replaceChild(testbench_node, hdlDesign[0].getElementsByTagName("testbench")[0])
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

                if note_data!="None":
                    self.testbench_btn.setText("Edit Test Plan")
                else:
                    note_data = "No test plan created"
                    self.testbench_btn.setText("Add Test Plan")
                self.testplan_input.setText(note_data)
                print("Saved test plan")
    def load_data(self, proj_dir):
        self.note = "No test plan created"

        if proj_dir is not None:
            root = minidom.parse(proj_dir[0])
            HDLGen = root.documentElement
            hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
            testbench_node = hdlDesign[0].getElementsByTagName('testbench')
            if len(testbench_node) != 0 and testbench_node[0].firstChild is not None:
                tb_node = testbench_node[0].getElementsByTagName('TBNote')[0]
                self.note = tb_node.firstChild.nodeValue
            note_data = self.note
            note_data = note_data.replace("&#10;", "\n")
            note_data = note_data.replace("&amp;", "&")
            note_data = note_data.replace("&amp;", "&")
            note_data = note_data.replace("&quot;", "\"")
            note_data = note_data.replace("&apos;", "\'")
            note_data = note_data.replace("&lt;", "<")
            note_data = note_data.replace("&#x9;", "\t")
            note_data = note_data.replace("&gt;", ">")
            if note_data != "None":
                self.testbench_btn.setText("Edit Test Plan")
            else:
                note_data="No test plan created"
                self.testbench_btn.setText("Add Test Plan")
            self.testplan_input.setText(note_data)

    def testPlan_help_window(self):
        testPlan_help_dialog = TestPlanHelpDialog()
        testPlan_help_dialog.exec_()

