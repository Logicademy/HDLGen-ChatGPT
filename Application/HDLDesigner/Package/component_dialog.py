import re
import os
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import sys

sys.path.append("..")
from ProjectManager.project_manager import ProjectManager
from Generator.generator import Generator
BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"


class ComponentDialog(QDialog):
    def __init__(self, add_or_edit, component_data = None):
        super().__init__()

        if add_or_edit == "add":
            self.setWindowTitle("New component")
        elif add_or_edit == "edit":
            self.setWindowTitle("Edit component")

        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)

        self.internal_signals = []
        self.input_signals = []
        self.output_signals = []

        self.input_layout = QGridLayout()

        self.mainLayout = QVBoxLayout()

        self.component_name_label = QLabel("Component Name")
        self.component_name_label.setStyleSheet(WHITE_COLOR)
        self.component_name_input = QLabel("Browse to selct VHDL Model")
        self.component_name_input.setStyleSheet(WHITE_COLOR)

        self.signal_empty_info = QLabel("No Top level Signals found!\nPlease add input and output signals in Ports")
        self.signal_empty_info.setFixedSize(400, 300)
        self.signal_table = QTableWidget()

        self.signal_layout = QVBoxLayout()
        self.signal_frame = QFrame()

        self.file_path_label = QLabel("Component model file path")
        self.file_path_label.setStyleSheet(WHITE_COLOR)
        self.file_path_input = QLineEdit()

        self.browse_btn = QPushButton("Browse")
        self.browse_btn.setFixedSize(60, 25)
        self.browse_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}")

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFixedSize(60, 25)
        self.cancel_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}")


        self.ok_btn = QPushButton("Ok")
        #self.ok_btn.setEnabled(False)
        self.ok_btn.setFixedSize(60, 25)
        self.ok_btn.setStyleSheet(
            "QPushButton {background-color: rgb(169,169,169);  color: black; border-radius: 8px; border-style: plain;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}"
            "QPushButton:enabled {background-color: white; color: black; border-radius: 8px; border-style: plain; }")

        self.input_frame = QFrame()

        self.cancelled = True
        self.generator = Generator()
        self.setup_ui()

        #self.populate_signals(ProjectManager.get_xml_data_path())

        if add_or_edit == "edit" and component_data != None:
            self.load_component_data(component_data)

    def setup_ui(self):
        bold_font = QFont()
        bold_font.setBold(True)
        
        self.signal_table.setFrameStyle(QFrame.NoFrame)
        self.signal_table.setColumnCount(3)
        self.signal_table.setShowGrid(False)
        self.signal_table.setHorizontalHeaderLabels(['Name', 'Mode', ' Type'])
        header = self.signal_table.horizontalHeader()
        header.setSectionsClickable(False)
        header.setSectionsMovable(False)
        self.signal_table.horizontalHeader().setFont(bold_font)
        self.signal_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.signal_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.signal_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        
        self.signal_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        vert = self.signal_table.verticalHeader()
        vert.hide()
        self.signal_layout.addWidget(self.signal_table)
        self.signal_frame.setFrameStyle(QFrame.NoFrame)
        self.signal_frame.setStyleSheet(".QFrame{background-color: white; border-radius: 5px;}")
        self.signal_frame.setLayout(self.signal_layout)
        self.signal_frame.setFixedSize(325, 275)

        self.input_layout.addWidget(self.component_name_label, 0, 0, 1, 1)
        self.input_layout.addWidget(self.component_name_input, 1, 0, 1, 1)
        self.input_layout.addWidget(self.file_path_label, 2, 0, 1, 2)
        self.input_layout.addWidget(self.file_path_input,3, 0, 1, 1)
        self.input_layout.addWidget(self.browse_btn, 3, 1, 1, 1)
        self.input_layout.addWidget(self.signal_frame, 4, 0, 4, 2)


        self.input_layout.addItem(QSpacerItem(0, 50), 6, 0, 1, 3)
        self.input_layout.addWidget(self.cancel_btn, 8, 0, 1, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 8, 1, 1, 1, alignment=Qt.AlignRight)

        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setLayout(self.input_layout)
        self.ok_btn.clicked.connect(self.get_data)
        self.cancel_btn.clicked.connect(self.cancel_selected)
        self.browse_btn.clicked.connect(self.set_comp_path)

        self.mainLayout.addWidget(self.input_frame, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)

    def populate_signals(self, proj_dir, comp_dir):
        self.input_signals=[]
        self.output_signals=[]
        self.internal_signals=[]
        rows = self.signal_table.rowCount()
        for i in range(rows):
            self.signal_table.removeRow(0)
        outputList_flag = 0
        if (proj_dir != None):
            root = minidom.parse(proj_dir)
            HDLGen = root.documentElement
            hdlDesign = HDLGen.getElementsByTagName("hdlDesign")

            io_ports = hdlDesign[0].getElementsByTagName('entityIOPorts')
            signal_nodes = io_ports[0].getElementsByTagName('signal')

            intSignals = hdlDesign[0].getElementsByTagName('internalSignals')
            intSignal_nodes = intSignals[0].getElementsByTagName('signal')


            if len(signal_nodes) != 0 or len(intSignal_nodes) != 0:
                for i in range(0, len(signal_nodes)):
                    port_name = signal_nodes[i].getElementsByTagName('name')[0].firstChild.data
                    port_mode = signal_nodes[i].getElementsByTagName('mode')[0].firstChild.data

                    if port_mode == "in":
                        self.input_signals.append(port_name)
                    elif port_mode == "out":
                        self.output_signals.append(port_name)

                for i in range(0, len(intSignal_nodes)):
                    internal_signal = intSignal_nodes[i].getElementsByTagName('name')[0].firstChild.data
                    self.internal_signals.append(internal_signal)

                if len(self.output_signals) != 0 and len(self.input_signals) != 0:
                    outputList_flag = 1
                    self.comp_signals, self.model, self.comp_mode = self.loadComponent(comp_dir)
                    i = 0
                    for signal in self.comp_signals:
                        temp = self.comp_mode[i].split(' ')
                        row_position = self.signal_table.rowCount()
                        self.signal_table.insertRow(row_position)
                        self.signal_table.setRowHeight(row_position, 5)

                        self.signal_table.setItem(row_position, 0, QTableWidgetItem(signal))
                        self.signal_table.setItem(row_position, 1, QTableWidgetItem(temp[0]))
                        self.signal_table.setItem(row_position, 2, QTableWidgetItem(temp[1]))
                        i = i + 1
                   # self.signal_layout.addWidget(self.signal_table)
                if outputList_flag == 0:
                    self.signal_layout.addWidget(self.signal_empty_info, alignment=Qt.AlignTop)
                return

        self.signal_layout.addWidget(self.signal_empty_info, alignment=Qt.AlignTop)

    def set_comp_path(self):
        comp_path = QFileDialog.getOpenFileName(self,"Select model .vhd file","../User_Projects/", filter="VHDL files (*.vhd)")
        comp_path = comp_path[0]
        self.file_path_input.setText(comp_path)
        self.populate_signals(ProjectManager.get_xml_data_path(), self.file_path_input.text())
    def load_component_data(self, component_data):
        self.component_name_input.setText(component_data[0])
        self.file_path_input.setText(component_data[1])
        signals = []
        mode = []
        type = []
        rows = self.signal_table.rowCount()
        for i in range(rows):
            self.signal_table.removeRow(0)
        for signal in component_data[2]:
            temp = signal.split(',')
            signals.append(temp[0])
            mode.append(temp[1])
            if temp[2][0:16] == "std_logic_vector":
                temp[2] = temp[2] + " downto 0)"
            type.append(temp[2])
        i = 0
        for sig in signals:
            row_position = self.signal_table.rowCount()
            self.signal_table.insertRow(row_position)
            self.signal_table.setRowHeight(row_position, 5)
            self.signal_table.setItem(row_position, 0, QTableWidgetItem(sig))
            self.signal_table.setItem(row_position, 1, QTableWidgetItem(mode[i]))
            self.signal_table.setItem(row_position, 2, QTableWidgetItem(type[i]))
            i = i+1
        self.signal_layout.addWidget(self.signal_table)

    def cancel_selected(self):
        self.cancelled = True
        self.close()

    def enable_ok_btn(self):
        if self.component_name_input.text() != "":
            self.ok_btn.setEnabled(True)
        else:
            self.ok_btn.setEnabled(False)

    def get_data(self):
        data = []
        signals = []
        componentName = self.component_name_input.text().strip().replace(" ", "")
        if componentName[-2:] != "_i":
            componentName=componentName+"_i"
        #data.append(componentName)

        for i in range(self.signal_table.rowCount()):
            signal = self.signal_table.item(i, 0).text()
            mode = self.signal_table.item(i, 1).text()
            type = self.signal_table.item(i, 2).text()
            if type[0:16] == "std_logic_vector":
                type = type + " downto 0)"
            signals.append(signal + "," + mode + "," + type)

        data.append(self.component_name_input.text())
        data.append(self.file_path_input.text())
        data.append(signals)
        self.cancelled = False
        self.close()
        return data

    def loadComponent(self, comp_dir):
        # Open the VHDL file and read its contents
        with open(comp_dir, 'r') as file:
            vhdl_code = file.read()
        # Use a regular expression to match the port declarations
        model = os.path.splitext(os.path.basename(comp_dir))[0]
        start_port_pattern = re.compile(r'entity\s*' + model + '\s*is\s*Port\s*\(', re.IGNORECASE | re.DOTALL)
        matchStart = start_port_pattern.search(vhdl_code)
        startEnd = matchStart.end()
        startStart = matchStart.start()
        end_port_pattern = re.compile(r'\);\s*end\s*Entity\s*' + model, re.IGNORECASE | re.DOTALL)
        matchEnd = end_port_pattern.search(vhdl_code)
        endStart = matchEnd.start()
        endEnd = matchEnd.end()

        asign = vhdl_code[startEnd:endStart]
        mainPackage = vhdl_code[startStart:endEnd].lower()
        mainPackage = mainPackage.replace("entity", "component")
        asign = "\n".join([line for line in asign.splitlines() if line.strip()])
        signal_names = [line.split(":")[0].strip() for line in asign.splitlines()]
        signal_mode = [line.split(":")[1].strip().replace(";","") for line in asign.splitlines()]
        #signal_mode = signal_mode.replace("\t","")
        #signal_mode = signal_mode.replace("\n","")
        self.component_name_input.setText(model)
        return signal_names, model, signal_mode