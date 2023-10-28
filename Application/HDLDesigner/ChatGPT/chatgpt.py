import os
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import pyperclip
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
from Generator.generator import Generator


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
        self.proj_path = ""
        self.entity_name = ""
        self.mainLayout = QVBoxLayout()

        self.input_layout = QGridLayout()

        self.testplan_label = QLabel("ChatGPT Message")
        self.testplan_label.setFont(title_font)
        self.testplan_label.setStyleSheet(WHITE_COLOR)

        self.chatgpt_info_btn = QPushButton()
        self.chatgpt_info_btn.setIcon(qta.icon("mdi.help"))
        self.chatgpt_info_btn.setFixedSize(25, 25)
        self.chatgpt_info_btn.clicked.connect(self.chatgpt_help_window)

        self.header_VHDL = QPushButton("VHDL Title Section Command")
        self.header_VHDL.setFixedSize(200,50)
        self.header_VHDL.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.header_VHDL_copy = QPushButton("Copy")
        self.header_VHDL_copy.setFixedSize(200, 50)
        self.header_VHDL_copy.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.model_VHDL = QPushButton("VHDL Model Command")
        self.model_VHDL.setFixedSize(200, 50)
        self.model_VHDL.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.model_VHDL_copy = QPushButton("Copy")
        self.model_VHDL_copy.setFixedSize(200, 50)
        self.model_VHDL_copy.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")

        self.testbench_VHDL = QPushButton("VHDL Testbench Command")
        self.testbench_VHDL.setFixedSize(200, 50)
        self.testbench_VHDL.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.tb_VHDL_copy = QPushButton("Copy")
        self.tb_VHDL_copy.setFixedSize(200, 50)
        self.tb_VHDL_copy.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")

        self.header_Verilog = QPushButton("Verilog Title Section Command")
        self.header_Verilog.setFixedSize(200, 50)
        self.header_Verilog.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.header_Verilog.setVisible(False)

        self.header_Verilog_copy = QPushButton("Copy")
        self.header_Verilog_copy.setFixedSize(200, 50)
        self.header_Verilog_copy.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.header_Verilog_copy.setVisible(False)
        self.model_Verilog = QPushButton("Verilog Model Command")
        self.model_Verilog.setFixedSize(200, 50)
        self.model_Verilog.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.model_Verilog.setVisible(False)

        self.model_Verilog_copy = QPushButton("Copy")
        self.model_Verilog_copy.setFixedSize(200, 50)
        self.model_Verilog_copy.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.model_Verilog_copy.setVisible(False)
        self.testbench_Verilog = QPushButton("Verilog Testbench Command")
        self.testbench_Verilog.setFixedSize(200, 50)
        self.testbench_Verilog.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.testbench_Verilog.setVisible(False)
        self.tb_Verilog_copy = QPushButton("Copy")
        self.tb_Verilog_copy.setFixedSize(200, 50)
        self.tb_Verilog_copy.setStyleSheet(
            "QPushButton {background-color: rgb(97, 107, 129); color: white; border-radius: 10px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(72, 80, 98);  color: white; border-radius: 10px; border-style: plain;}")
        self.tb_Verilog_copy.setVisible(False)
        self.header_check = QRadioButton("Preview")
        # self.vhdl_check.setChecked(True)
        self.header_check.setStyleSheet(BLACK_COLOR)
        self.header_check.setChecked(True)
        self.model_check = QRadioButton("Preview")
        self.model_check.setStyleSheet(BLACK_COLOR)
        self.testbench_check = QRadioButton("Preview")
        self.testbench_check.setStyleSheet(BLACK_COLOR)

        self.top_layout = QGridLayout()
        self.arch_action_layout = QVBoxLayout()
        self.btn_layout = QHBoxLayout()

        self.vspacer = QSpacerItem(30, 40)
        self.list_layout = QVBoxLayout()
        self.list_frame = QFrame()
        self.main_frame = QFrame()
        self.input_frame = QFrame()
        self.generator = Generator()
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
        self.input_layout.addWidget(self.header_VHDL_copy, 0, 1)
        self.input_layout.addWidget(self.model_VHDL, 1, 0)
        self.input_layout.addWidget(self.model_VHDL_copy, 1, 1)
        self.input_layout.addWidget(self.testbench_VHDL, 2, 0)
        self.input_layout.addWidget(self.tb_VHDL_copy, 2, 1)
        self.input_layout.addWidget(self.header_Verilog, 0, 0)
        self.input_layout.addWidget(self.header_Verilog_copy, 0, 1)
        self.input_layout.addWidget(self.model_Verilog, 1, 0)
        self.input_layout.addWidget(self.model_Verilog_copy, 1, 1)
        self.input_layout.addWidget(self.testbench_Verilog, 2, 0)
        self.input_layout.addWidget(self.tb_Verilog_copy, 2, 1)
        self.input_layout.addWidget(self.header_check, 0,2)
        self.input_layout.addWidget(self.model_check, 1, 2)
        self.input_layout.addWidget(self.testbench_check, 2, 2)

        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.header_VHDL.clicked.connect(self.vhdl_header_command)
        self.header_Verilog.clicked.connect(self.verilog_header_command)
        self.model_VHDL.clicked.connect(self.vhdl_model_command)
        self.model_Verilog.clicked.connect(self.verilog_model_command)
        self.testbench_VHDL.clicked.connect(self.vhdl_testbench_command)
        self.testbench_Verilog.clicked.connect(self.verilog_testbench_command)
        self.header_VHDL_copy.clicked.connect(self.header_VHDL_file)
        self.header_Verilog_copy.clicked.connect(self.header_Verilog_file)
        self.model_VHDL_copy.clicked.connect(self.model_VHDL_file)
        self.model_Verilog_copy.clicked.connect(self.model_Verilog_file)
        self.tb_VHDL_copy.clicked.connect(self.tb_VHDL_file)
        self.tb_Verilog_copy.clicked.connect(self.tb_Verilog_file)
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
        xml_str = '\n'.join([line for line in xml_str.splitlines() if line.strip()])
        # Writing xml file
        with open(xml_data_path, "w") as f:
            f.write(xml_str)
        hdl = False
        self.save_signal.emit(hdl)
        print("Saved ChatGPT commands")

    def load_data(self, proj_dir):
        proj_name = ProjectManager.get_proj_name()
        self.proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)


        root = minidom.parse(proj_dir[0])
        HDLGen = root.documentElement
        projectManager = HDLGen.getElementsByTagName("projectManager")
        HDL = projectManager[0].getElementsByTagName("HDL")[0]
        if HDL.hasChildNodes():
            lang_node = HDL.getElementsByTagName('language')[0]
            lang = lang_node.getElementsByTagName('name')[0].firstChild.data
            if lang == "VHDL":
                self.VHDLVisible()
            else:
                self.VerilogVisible()
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
        header_node = hdlDesign[0].getElementsByTagName("header")
        if header_node is not None:
            comp_node = header_node[0].getElementsByTagName("compName")[0]
            if comp_node.firstChild.data != "null":
                self.entity_name = comp_node.firstChild.data
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
    def header_VHDL_file(self):
        self.generator.generate_folders()
        self.generator.create_vhdl_file("4")
        proj_name = ProjectManager.get_proj_name()
        self.proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        self.entity_name=ProjectManager.proj_name
        chatgpt_vhdl_file_path = os.path.join(self.proj_path, "VHDL", "ChatGPT", self.entity_name + "_VHDL_header_ChatGPT.txt")
        self.copy_file_contents_to_clipboard(chatgpt_vhdl_file_path)

    def header_Verilog_file(self):
        self.generator.generate_folders()
        self.generator.create_verilog_file("4")
        proj_name = ProjectManager.get_proj_name()
        self.proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        self.entity_name = ProjectManager.proj_name
        chatgpt_verilog_file_path = os.path.join(self.proj_path, "Verilog", "ChatGPT", self.entity_name + "_Verilog_header_ChatGPT.txt")
        self.copy_file_contents_to_clipboard(chatgpt_verilog_file_path)
    def model_VHDL_file(self):
        self.generator.generate_folders()
        self.generator.create_vhdl_file("6")
        proj_name = ProjectManager.get_proj_name()
        self.proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        self.entity_name = ProjectManager.proj_name
        chatgpt_vhdl_file_path = os.path.join(self.proj_path, "VHDL", "ChatGPT", self.entity_name + "_VHDL_ChatGPT.txt")
        self.copy_file_contents_to_clipboard(chatgpt_vhdl_file_path)

    def model_Verilog_file(self):
        self.generator.generate_folders()
        self.generator.create_verilog_file("6")
        proj_name = ProjectManager.get_proj_name()
        self.proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        self.entity_name = ProjectManager.proj_name
        chatgpt_verilog_file_path = os.path.join(self.proj_path, "Verilog", "ChatGPT", self.entity_name + "_Verilog_ChatGPT.txt")
        self.copy_file_contents_to_clipboard(chatgpt_verilog_file_path)

    def tb_VHDL_file(self):
        self.generator.generate_folders()
        self.generator.create_testbench_file("8")
        proj_name = ProjectManager.get_proj_name()
        self.proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        self.entity_name = ProjectManager.proj_name
        chatgpt_vhdl_file_path = os.path.join(self.proj_path, "VHDL", "ChatGPT", self.entity_name + "_VHDL_TB_ChatGPT.txt")
        self.copy_file_contents_to_clipboard(chatgpt_vhdl_file_path)

    def tb_Verilog_file(self):
        self.generator.generate_folders()
        self.generator.create_verilog_testbench_file("8")
        proj_name = ProjectManager.get_proj_name()
        self.proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        self.entity_name = ProjectManager.proj_name
        chatgpt_verilog_file_path = os.path.join(self.proj_path, "Verilog", "ChatGPT", self.entity_name + "_Verilog_TB_ChatGPT.txt")
        self.copy_file_contents_to_clipboard(chatgpt_verilog_file_path)

    def VHDLVisible(self):
        self.model_VHDL_copy.setVisible(True)
        self.model_VHDL.setVisible(True)
        self.header_VHDL_copy.setVisible(True)
        self.header_VHDL.setVisible(True)
        self.tb_VHDL_copy.setVisible(True)
        self.testbench_VHDL.setVisible(True)

        self.model_Verilog_copy.setVisible(False)
        self.model_Verilog.setVisible(False)
        self.header_Verilog_copy.setVisible(False)
        self.header_Verilog.setVisible(False)
        self.tb_Verilog_copy.setVisible(False)
        self.testbench_Verilog.setVisible(False)
    def VerilogVisible(self):
        self.model_Verilog_copy.setVisible(True)
        self.model_Verilog.setVisible(True)
        self.header_Verilog_copy.setVisible(True)
        self.header_Verilog.setVisible(True)
        self.tb_Verilog_copy.setVisible(True)
        self.testbench_Verilog.setVisible(True)

        self.model_VHDL_copy.setVisible(False)
        self.model_VHDL.setVisible(False)
        self.header_VHDL_copy.setVisible(False)
        self.header_VHDL.setVisible(False)
        self.tb_VHDL_copy.setVisible(False)
        self.testbench_VHDL.setVisible(False)
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
    

