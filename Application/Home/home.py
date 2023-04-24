from PySide2.QtGui import QFont
from PySide2.QtWidgets import *
import os
import sys
sys.path.append("..")
from ProjectManager.project_manager import ProjectManager
from Generator.generator import Generator
from Help.help import Help
from HDLDesigner.hdl_designer import HDLDesigner
from HDLDesigner.Architecture.note_dialog import note_Dialog
from xml.dom import minidom


class Home(QMainWindow):

    def __init__(self, proj_dir=None):

        super().__init__()
        small_text_font = QFont()
        small_text_font.setPointSize(10)
        self.setWindowTitle("HDLGen V2022.0.1")

        self.cornerWidget = QWidget()
        self.generate_btn = QPushButton("Generate model and TB HDL")
        self.generate_btn.setFont(small_text_font)
        self.testbench_btn = QPushButton("Testbench ChatGPT")
        self.testbench_btn.setFont(small_text_font)
        #self.generate_btn.setFixedHeight(20)
        self.start_vivado_btn = QPushButton("Generate/Open Vivado")
        self.start_vivado_btn.setFont(small_text_font)
        #self.start_vivado_btn.setFixedHeight(20)
        self.cornerWidgetLayout = QHBoxLayout()
        self.cornerWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.cornerWidgetLayout.addWidget(self.testbench_btn)
        self.cornerWidgetLayout.addWidget(self.generate_btn)
        self.cornerWidgetLayout.addWidget(self.start_vivado_btn)
        self.cornerWidget.setLayout(self.cornerWidgetLayout)

        # Initializing UI Elements
        self.mainLayout = QVBoxLayout()

        self.tabs = QTabWidget()

        # Creating a container
        self.container = QWidget()

        self.proj_dir = proj_dir
        self.generator = Generator()
        self.project_manager = ProjectManager(self.proj_dir, self)

        self.setup_ui()


    def setup_ui(self):

        load_data = False

        if self.proj_dir is not None:
            load_data = True
        else:
            self.project_manager.vhdl_check.setChecked(True)
        self.hdl_designer = HDLDesigner(self.proj_dir, load_data)

        self.tabs.addTab(self.project_manager, "Project Manager")
        self.tabs.addTab(self.hdl_designer, "HDL Designer")
        self.tabs.addTab(Help(), "Help")
        font = self.tabs.font()
        font.setPointSize(10)
        self.tabs.setFont(font)
        self.generate_btn.clicked.connect(self.generate_btn_clicked)
        self.testbench_btn.clicked.connect(self.testbench_btn_clicked)
        self.tabs.setCornerWidget(self.cornerWidget)
        self.start_vivado_btn.clicked.connect(self.start_vivado_btn_clicked)

        self.project_manager.vhdl_check.clicked.connect(lambda: self.hdl_designer.update_preview("VHDL"))
        self.project_manager.verilog_check.clicked.connect(lambda: self.hdl_designer.update_preview("Verilog"))
        self.tabs.currentChanged.connect(self.hdl_designer.compDetails.update_comp_name)

        self.mainLayout.addWidget(self.tabs)
        self.setLayout(self.mainLayout)

        self.container.setLayout(self.mainLayout)

        self.setCentralWidget(self.container)

    def testbench_btn_clicked(self):
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


    def generate_btn_clicked(self):
        if self.project_manager.vhdl_check.isChecked():
            self.generator.generate_folders()
            overwrite, instances = self.generator.create_vhdl_file()
            self.generator.create_tcl_file("VHDL", instances)
            self.generator.create_testbench_file(overwrite)
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("VHDL and Testbench Generated")
            msgBox.exec_()
        elif self.project_manager.verilog_check.isChecked():
            self.generator.generate_folders()
            overwrite, instances = self.generator.create_verilog_file()
            self.generator.create_tcl_file("Verilog", instances)
            self.generator.create_verilog_testbench_file(overwrite)
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Alert")
            msgBox.setText("Verilog and Testbench Generated")
            msgBox.exec_()
    def start_vivado_btn_clicked(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Alert")
        if self.project_manager.vivado_dir_input.text()[-10:] == "vivado.bat":
            if self.project_manager.vhdl_check.isChecked():
                msgBox.setText("Starting EDA tool")
                msgBox.exec_()
                #self.generator.create_tcl_file()
                self.generator.run_tcl_file("VHDL")
            else:
                msgBox.setText("Starting EDA tool")
                msgBox.exec_()
                # self.generator.create_tcl_file()
                self.generator.run_tcl_file("Verilog")
        else:
            msgBox.setText("No vivado.bat path set")


