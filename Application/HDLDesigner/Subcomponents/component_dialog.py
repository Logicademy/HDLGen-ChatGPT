#Dialog box for adding/editing sub-component called in the subcomponents.py class.
import re
import os
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import sys

sys.path.append("..")
import configparser
from ProjectManager.project_manager import ProjectManager
from Generator.generator import Generator

WHITE_COLOR = "color: white"

class ComponentDialog(QDialog):
    def __init__(self, add_or_edit, component_data = None):
        super().__init__()

        if add_or_edit == "add":
            self.setWindowTitle("New component")
        elif add_or_edit == "edit":
            self.setWindowTitle("Edit component")

        input_font = QFont()
        input_font.setPointSize(10)
        bold_font = QFont()
        bold_font.setBold(True)

        self.internal_signals = []
        self.input_signals = []
        self.output_signals = []

        self.input_layout = QGridLayout()

        self.mainLayout = QVBoxLayout()

        self.component_name_label = QLabel("Component Name")
        self.component_name_label.setStyleSheet(WHITE_COLOR)
        self.component_name_label.setFont(input_font)
        self.component_name_input = QLabel("Browse to select VHDL Model")
        self.component_name_input.setStyleSheet(WHITE_COLOR)
        self.component_name_input.setEnabled(False)
        self.component_name_input.setFont(input_font)

        self.signal_empty_info = QLabel("No Top level Signals found!\nPlease add input and output signals in Ports")
        self.signal_empty_info.setFont(input_font)
        self.signal_empty_info.setFixedSize(400, 300)
        self.signal_table = QTableWidget()

        self.signal_layout = QVBoxLayout()
        self.signal_frame = QFrame()

        self.file_path_label = QLabel("Component model file path")
        self.file_path_label.setFont(input_font)
        self.file_path_label.setStyleSheet(WHITE_COLOR)
        self.file_path_input = QLineEdit()
        self.file_path_input.setFont(input_font)

        self.browse_btn = QPushButton("Browse")
        self.browse_btn.setFont(input_font)
        self.browse_btn.setStyleSheet(
             "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}")

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFont(input_font)
        self.cancel_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}")

        self.ok_btn = QPushButton("Ok")
        self.ok_btn.setFont(input_font)
        self.ok_btn.setStyleSheet(
            "QPushButton {background-color: rgb(169,169,169);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            "QPushButton:enabled {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px; }")

        self.input_frame = QFrame()

        self.cancelled = True
        self.generator = Generator()
        self.config = configparser.ConfigParser()
        self.setup_ui()


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
        self.signal_frame.setFixedSize(600, 600)

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
        rows = self.signal_table.rowCount()
        for i in range(rows):
            self.signal_table.removeRow(0)
        self.comp_signals, self.model, self.comp_mode = self.loadComponent(comp_dir)
        i = 0
        for signal in self.comp_signals:
            temp = self.comp_mode[i].split(' ')
            row_position = self.signal_table.rowCount()
            self.signal_table.insertRow(row_position)
            self.signal_table.setRowHeight(row_position, 5)

            self.signal_table.setItem(row_position, 0, QTableWidgetItem(signal))
            if temp[1] == "std_logic":
                temp[1] = "single bit"
            elif temp[1][0:16] == "std_logic_vector":
                temp[1] = "bus "+ "["+temp[1][17:]+":0]"
            self.signal_table.setItem(row_position, 1, QTableWidgetItem(temp[0]))
            self.signal_table.setItem(row_position, 2, QTableWidgetItem(temp[1]))
            i = i + 1

    def is_subdirectory(self, directory, potential_parent):
        # Normalize the paths to use forward slashes
        directory = os.path.normpath(directory).replace("\\", "/")
        potential_parent = os.path.normpath(potential_parent).replace("\\", "/")
        # Get the common prefix of the two paths
        common_prefix = os.path.commonprefix([directory, potential_parent])

        # Check if the common prefix is the same as the potential parent
        return os.path.normpath(common_prefix) == os.path.normpath(potential_parent)

    def set_comp_path(self):
        self.config.read('config.ini')
        lastDir = self.config.get('user', 'recentEnviro')
        if not os.path.exists(lastDir):
            lastDir = "../User_Projects/"
        comp_path = QFileDialog.getOpenFileName(self,"Select model .vhd file",lastDir, filter="VHDL files (*.vhd)")
        comp_path = comp_path[0]
        if self.is_subdirectory(comp_path, lastDir):
            if comp_path != "":
                self.file_path_input.setText(comp_path)
                self.populate_signals(ProjectManager.get_xml_data_path(), self.file_path_input.text())
                print("The directory is within the potential parent directory.")
        else:
            if comp_path != "":
                print("The directory is not within the potential parent directory.")
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Alert")
                msgBox.setText("Component cannot be added!\nThe component is not part of the project environment.")
                msgBox.exec_()
       # if comp_path != "":
           # self.file_path_input.setText(comp_path)
           # self.populate_signals(ProjectManager.get_xml_data_path(), self.file_path_input.text())
    def load_component_data(self, component_data):
        self.component_name_input.setText(component_data[0])
        self.file_path_input.setText(ProjectManager.get_proj_environment()+component_data[1])
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
            type.append(temp[2])
        i = 0
        for sig in signals:
            row_position = self.signal_table.rowCount()
            self.signal_table.insertRow(row_position)
            self.signal_table.setRowHeight(row_position, 5)
            self.signal_table.setItem(row_position, 0, QTableWidgetItem(sig))
            self.signal_table.setItem(row_position, 1, QTableWidgetItem(mode[i]))
            if type[i] == "std_logic":
                type[i] = "single bit"
            elif type[i][0:16] == "std_logic_vector":
                type[i] = "bus "+ "["+type[i][17:]
                type[i] = type[i].replace(" downto ",":")
                type[i] = type[i].replace(")","]")
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

        for i in range(self.signal_table.rowCount()):
            signal = self.signal_table.item(i, 0).text()
            mode = self.signal_table.item(i, 1).text()
            type = self.signal_table.item(i, 2).text()
            if type == "single bit":
                type = "std_logic"
            elif type[0:3] == "bus":
                type = "std_logic_vector("+type[5:]+" downto 0)"
                type = type.replace(":0]","")
            signals.append(signal + "," + mode + "," + type)

        data.append(self.component_name_input.text())
        dir = self.file_path_input.text()
        dir = dir.replace(ProjectManager.get_proj_environment(),"")
        data.append(dir)
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
        asign = "\n".join([line for line in asign.splitlines() if line.strip()])
        signal_names = [line.split(":")[0].strip() for line in asign.splitlines()]
        signal_mode = [line.split(":")[1].strip().replace(";","") for line in asign.splitlines()]
        self.component_name_input.setText(model)
        return signal_names, model, signal_mode