import os
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys
import qtawesome as qta
sys.path.append("..")
from HDLDesigner.ChatGPT.chatgpt_help import ChatGPTHelpDialog
from HDLDesigner.ChatGPT.VHDLHeader import VHDLHeaderDialog
from HDLDesigner.ChatGPT.VerilogHeader import VerilogHeaderDialog
from HDLDesigner.ChatGPT.VHDLModel import VHDLModelDialog
from HDLDesigner.ChatGPT.VerilogModel import VerilogModelDialog
from HDLDesigner.ChatGPT.VHDLTestbench import VHDLTestbenchDialog
from HDLDesigner.ChatGPT.VerilogTestbench import VerilogTestbenchDialog
from ProjectManager.project_manager import ProjectManager


WHITE_COLOR = "color: white"
BLACK_COLOR = "color: black"

class ChatGPT(QWidget):
    save_signal = Signal(bool)

    def __init__(self, proj_dir):
        super().__init__()
        small_text_font = QFont()
        small_text_font.setPointSize(10)
        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        self.proj_dir = proj_dir
        self.commands = ["None","None","None","None","None","None"]

        self.mainLayout = QVBoxLayout()

        self.input_layout = QGridLayout()

        self.testplan_label = QLabel("Test Plan")
        self.testplan_label.setFont(title_font)
        self.testplan_label.setStyleSheet(WHITE_COLOR)

        self.chatgpt_info_btn = QPushButton()
        self.chatgpt_info_btn.setIcon(qta.icon("mdi.help"))
        self.chatgpt_info_btn.setFixedSize(25, 25)
        self.chatgpt_info_btn.clicked.connect(self.chatgpt_help_window)

        self.header_VHDL = QPushButton("VHDL Header Command")
        self.header_VHDL.setFixedSize(200,50)
        self.header_VHDL.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.model_VHDL = QPushButton("VHDL Model Command")
        self.model_VHDL.setFixedSize(200, 50)
        self.model_VHDL.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.testbench_VHDL = QPushButton("VHDL Testbench Command")
        self.testbench_VHDL.setFixedSize(200, 50)
        self.testbench_VHDL.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.header_Verilog = QPushButton("Verilog Header Command")
        self.header_Verilog.setFixedSize(200, 50)
        self.header_Verilog.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.model_Verilog = QPushButton("Verilog Model Command")
        self.model_Verilog.setFixedSize(200, 50)
        self.model_Verilog.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.testbench_Verilog = QPushButton("Verilog Testbench Command")
        self.testbench_Verilog.setFixedSize(200, 50)
        self.testbench_Verilog.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")

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
        self.top_layout.addWidget(self.chatgpt_info_btn, 0, 1, 1, 1)
        self.arch_action_layout.addLayout(self.top_layout)
        self.input_layout.addWidget(self.header_VHDL,0,0)
        self.input_layout.addWidget(self.model_VHDL, 1, 0)
        self.input_layout.addWidget(self.testbench_VHDL, 2, 0)
        self.input_layout.addWidget(self.header_Verilog, 0, 1)
        self.input_layout.addWidget(self.model_Verilog, 1, 1)
        self.input_layout.addWidget(self.testbench_Verilog, 2, 1)

        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.header_VHDL.clicked.connect(self.vhdl_header_command)
        self.header_Verilog.clicked.connect(self.verilog_header_command)
        self.model_VHDL.clicked.connect(self.vhdl_model_command)
        self.model_Verilog.clicked.connect(self.verilog_model_command)
        self.testbench_VHDL.clicked.connect(self.vhdl_testbench_command)
        self.testbench_Verilog.clicked.connect(self.verilog_testbench_command)
        self.main_frame.setLayout(self.arch_action_layout)

        self.list_frame.setFrameShape(QFrame.StyledPanel)
        self.list_frame.setStyleSheet('.QFrame{background-color: white; border-radius: 5px;}')
        self.list_frame.setLayout(self.input_layout)

        self.arch_action_layout.addItem(QSpacerItem(0, 5))
        self.arch_action_layout.addWidget(self.list_frame)
        self.arch_action_layout.addItem(QSpacerItem(0, 5))

        self.mainLayout.addWidget(self.main_frame)

        self.setLayout(self.mainLayout)

    def save_data(self):

        xml_data_path = ProjectManager.get_xml_data_path()

        root = minidom.parse(xml_data_path)
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")

        new_chatgpt = root.createElement('chatgpt')
        commands_node = root.createElement('commands')

        VHDLHeader_node = root.createElement('VHDLHeader')
        VHDLHeader_node.appendChild(root.createTextNode(self.commands[0]))
        commands_node.appendChild(VHDLHeader_node)

        VerilogHeader_node = root.createElement('VerilogHeader')
        VerilogHeader_node.appendChild(root.createTextNode(self.commands[1]))
        commands_node.appendChild(VerilogHeader_node)

        VHDLModel_node = root.createElement('VHDLModel')
        VHDLModel_node.appendChild(root.createTextNode(self.commands[2]))
        commands_node.appendChild(VHDLModel_node)

        VerilogModel_node = root.createElement('VerilogModel')
        VerilogModel_node.appendChild(root.createTextNode(self.commands[3]))
        commands_node.appendChild(VerilogModel_node)

        VHDLTestbench_node = root.createElement('VHDLTestbench')
        VHDLTestbench_node.appendChild(root.createTextNode(self.commands[4]))
        commands_node.appendChild(VHDLTestbench_node)

        VerilogTestbench_node = root.createElement('VerilogTestbench')
        VerilogTestbench_node.appendChild(root.createTextNode(self.commands[5]))
        commands_node.appendChild(VerilogTestbench_node)

        new_chatgpt.appendChild(commands_node)
        hdlDesign[0].replaceChild(new_chatgpt, hdlDesign[0].getElementsByTagName('chatgpt')[0])

        # converting the doc into a string in xml format
        xml_str = root.toprettyxml()
        xml_str = os.linesep.join([s for s in xml_str.splitlines() if s.strip()])
        # Writing xml file
        with open(xml_data_path, "w") as f:
            f.write(xml_str)
        hdl = False
        self.save_signal.emit(hdl)
        print("Saved ChatGPT commands")

    def load_data(self, proj_dir):
        root = minidom.parse(proj_dir[0])
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")

        chatgpt = hdlDesign[0].getElementsByTagName('chatgpt')[0]
        if chatgpt.hasChildNodes():
            commands_node = chatgpt.getElementsByTagName('commands')[0]

            VHDLHeader = commands_node.getElementsByTagName('VHDLHeader')[0].firstChild.data
            VerilogHeader = commands_node.getElementsByTagName('VerilogHeader')[0].firstChild.data
            VHDLModel = commands_node.getElementsByTagName('VHDLModel')[0].firstChild.data
            VerilogModel = commands_node.getElementsByTagName('VerilogModel')[0].firstChild.data
            VHDLTestbench = commands_node.getElementsByTagName('VHDLTestbench')[0].firstChild.data
            VerilogTestbench = commands_node.getElementsByTagName('VerilogTestbench')[0].firstChild.data

            self.commands=[VHDLHeader,VerilogHeader,VHDLModel,VerilogModel,VHDLTestbench,VerilogTestbench]

    def chatgpt_help_window(self):
        chatgpt_help_dialog = ChatGPTHelpDialog()
        chatgpt_help_dialog.exec_()

    def vhdl_header_command(self):
        vhdl_header = VHDLHeaderDialog("edit", self.commands[0])
        vhdl_header.exec_()

        if not vhdl_header.cancelled:
            vhdl_header = vhdl_header.get_data()
            self.commands[0]=vhdl_header
        self.save_data()
    
    def verilog_header_command(self):
        verilog_header = VerilogHeaderDialog("edit", self.commands[1])
        verilog_header.exec_()

        if not verilog_header.cancelled:
            verilog_header = verilog_header.get_data()
            self.commands[1]=verilog_header
        self.save_data()
    
    def vhdl_model_command(self):
        vhdl_model = VHDLModelDialog("edit", self.commands[2])
        vhdl_model.exec_()

        if not vhdl_model.cancelled:
            vhdl_model = vhdl_model.get_data()
            self.commands[2]=vhdl_model
        self.save_data()
        
    def verilog_model_command(self):
        verilog_model = VerilogModelDialog("edit", self.commands[3])
        verilog_model.exec_()

        if not verilog_model.cancelled:
            verilog_model = verilog_model.get_data()
            self.commands[3]=verilog_model
        self.save_data()
    
    def vhdl_testbench_command(self):
        vhdl_testbench = VHDLTestbenchDialog("edit", self.commands[4])
        vhdl_testbench.exec_()

        if not vhdl_testbench.cancelled:
            vhdl_testbench = vhdl_testbench.get_data()
            self.commands[4]=vhdl_testbench
        self.save_data()
        
    def verilog_testbench_command(self):
        verilog_testbench = VerilogTestbenchDialog("edit", self.commands[5])
        verilog_testbench.exec_()

        if not verilog_testbench.cancelled:
            verilog_testbench = verilog_testbench.get_data()
            self.commands[5]=verilog_testbench
        self.save_data()
    

