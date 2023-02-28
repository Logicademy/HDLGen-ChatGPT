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


class InstanceDialog(QDialog):
    def __init__(self, add_or_edit, instance_data = None):
        super().__init__()

        if add_or_edit == "add":
            self.setWindowTitle("New instance")
        elif add_or_edit == "edit":
            self.setWindowTitle("Edit instance")

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

        self.instance_name_label = QLabel("Instance Name*")
        self.instance_name_label.setStyleSheet(WHITE_COLOR)
        self.instance_name_input = QLineEdit()

        self.suffix_label = QLabel("Suffix")
        self.suffix_label.setStyleSheet(WHITE_COLOR)
        self.suffix_input = QLineEdit()
        self.suffix_input.setFixedWidth(40)
        self.suffix_input.setEnabled(False)
        self.suffix_input.setText("_i")

        self.out_sig_header_layout = QHBoxLayout()
        self.out_sig_label = QLabel("Component Signal")
        self.out_sig_label.setFont(bold_font)
        self.val_label = QLabel("Top Level Signal")
        self.val_label.setFont(bold_font)
        self.out_sig_empty_info = QLabel("No Top level Signals found!\nPlease add input and output signals in Ports")
        self.out_sig_empty_info.setFixedSize(400, 300)
        self.list_div = QFrame()
        self.list_div.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129);}')
        self.list_div.setFixedHeight(1)
        self.out_sig_table = QTableWidget()

        self.out_sig_layout = QVBoxLayout()
        self.out_sig_frame = QFrame()

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

        if add_or_edit == "edit" and instance_data != None:
            self.load_instance_data(instance_data)

    def setup_ui(self):

        self.out_sig_header_layout.addWidget(self.out_sig_label)
        self.out_sig_header_layout.addWidget(self.val_label)

        self.out_sig_layout.addLayout(self.out_sig_header_layout)
        self.out_sig_layout.addWidget(self.list_div)
        self.out_sig_table.setFrameStyle(QFrame.NoFrame)
        self.out_sig_table.setColumnCount(2)
        self.out_sig_table.setShowGrid(False)
        self.out_sig_table.setColumnWidth(0, 125)
        self.out_sig_table.setColumnWidth(1, 125)
        self.out_sig_table.horizontalScrollMode()
        self.out_sig_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.out_sig_table.horizontalScrollBar().hide()
        header = self.out_sig_table.horizontalHeader()
        header.hide()
        header = self.out_sig_table.verticalHeader()
        header.hide()
        self.out_sig_layout.addWidget(self.out_sig_table)
        self.out_sig_frame.setFrameStyle(QFrame.NoFrame)
        self.out_sig_frame.setStyleSheet(".QFrame{background-color: white; border-radius: 5px;}")
        self.out_sig_frame.setLayout(self.out_sig_layout)
        self.out_sig_frame.setFixedSize(325, 275)

        self.input_layout.addWidget(self.instance_name_label, 0, 0, 1, 1)
        self.input_layout.addWidget(self.instance_name_input, 1, 0, 1, 1)
        self.input_layout.addWidget(self.suffix_label, 0, 1, 1, 1)
        self.input_layout.addWidget(self.suffix_input, 1, 1, 1, 1)
        self.input_layout.addWidget(self.file_path_label, 2, 0, 1, 2)
        self.input_layout.addWidget(self.file_path_input,3, 0, 1, 1)
        self.input_layout.addWidget(self.browse_btn, 3, 1, 1, 1)
        self.input_layout.addWidget(self.out_sig_frame, 4, 0, 4, 2)


        self.input_layout.addItem(QSpacerItem(0, 50), 6, 0, 1, 3)
        self.input_layout.addWidget(self.cancel_btn, 8, 0, 1, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 8, 1, 1, 1, alignment=Qt.AlignRight)

        self.instance_name_input.textChanged.connect(self.enable_ok_btn);
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
        rows = self.out_sig_table.rowCount()
        for i in range(rows):
            self.out_sig_table.removeRow(0)
       # self.out_sig_table.removeRow(0)
        #self.out_sig_table.removeRow(1)
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
                    for signal in self.comp_signals:
                        out_val_combo = QComboBox()
                        out_val_options = self.input_signals + self.internal_signals + self.output_signals
                        out_val_options.insert(0, "Select Signal")
                        out_val_combo.addItems(out_val_options)
                        out_val_options.pop(0)
                        row_position = self.out_sig_table.rowCount()
                        self.out_sig_table.insertRow(row_position)
                        self.out_sig_table.setRowHeight(row_position, 5)

                        self.out_sig_table.setItem(row_position, 0, QTableWidgetItem(signal))
                        self.out_sig_table.setCellWidget(row_position, 1, out_val_combo)
                   # self.out_sig_layout.addWidget(self.out_sig_table)
                if outputList_flag == 0:
                    self.out_sig_layout.addWidget(self.out_sig_empty_info, alignment=Qt.AlignTop)
                return

        self.out_sig_layout.addWidget(self.out_sig_empty_info, alignment=Qt.AlignTop)

    def set_comp_path(self):
        comp_path = QFileDialog.getOpenFileName(self,"Select model .vhd file","../User_Projects/", filter="VHDL files (*.vhd)")
        comp_path = comp_path[0]
        self.file_path_input.setText(comp_path)
        self.populate_signals(ProjectManager.get_xml_data_path(), self.file_path_input.text())
    def load_instance_data(self, instance_data):
        self.instance_name_input.setText(instance_data[1])
        self.file_path_input.setText(instance_data[4])
        self.populate_signals(ProjectManager.get_xml_data_path(), self.file_path_input.text())
        out_sigs = []
        default_vals = []
        for out_sig in instance_data[2]:
            temp = out_sig.split(',')
            out_sigs.append(temp[0])
            default_vals.append(temp[1])
        for i in range(0, self.out_sig_table.rowCount()):
            if self.out_sig_table.item(i, 0).text() in out_sigs:
                self.out_sig_table.cellWidget(i, 1).setCurrentText(default_vals[i])

    def cancel_selected(self):
        self.cancelled = True
        self.close()

    def enable_ok_btn(self):
        if self.instance_name_input.text() != "":
            self.ok_btn.setEnabled(True)
        else:
            self.ok_btn.setEnabled(False)

    def get_data(self):
        data = []
        out_sigs = []
        instanceName = self.instance_name_input.text().strip().replace(" ", "")
        if instanceName[-2:] != "_i":
            instanceName=instanceName+"_i"
        data.append(instanceName)

        for i in range(self.out_sig_table.rowCount()):
            output = self.out_sig_table.item(i, 0).text()
            if self.out_sig_table.cellWidget(i, 1).currentText() == "Select Signal":
                default_val = self.out_sig_table.cellWidget(i, 1).currentText()
            else:
                default_val = self.out_sig_table.cellWidget(i, 1).currentText()
            sig = self.comp_mode[i].split(" ", 1)
            out_sigs.append(output + "," + default_val + "," + sig[0] + "," + sig[1])#self.comp_mode[i])
        data.append(out_sigs)
        data.append(self.model)
        data.append(self.file_path_input.text())
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

        return signal_names, model, signal_mode
