import os

from PySide2.QtWidgets import *
from PySide2.QtGui import *
import qtawesome as qta
import sys
sys.path.append("..")
from HDLDesigner.InternalSignal.stateNamesDialog import state_Name_Dialog
from ProjectManager.project_manager import ProjectManager

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"

class IntSignalDialog(QDialog):

    def __init__(self, add_or_edit, intSig_data=None):
        super().__init__()

        self.input_layout = QGridLayout()
        self.all_stateNames = []
        if add_or_edit == "add":
            self.setWindowTitle("New Internal Signal")
        elif add_or_edit == "edit":
            self.setWindowTitle("Edit Internal Signal")

        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)

        self.sig_types = ["std_logic", "std_logic_vector", "signed", "unsigned", "std_logic_vector state signals", "Enumerated type state signals", "integer"]
        self.FSM_types = ["Enumerated", "Binary"]
        self.rst_types = ["0", "1"]

        self.mainLayout = QVBoxLayout()

        self.intSig_name_label = QLabel("Internal Signal Name*")
        self.intSig_name_label.setStyleSheet(WHITE_COLOR)
        self.intSig_name_input = QLineEdit()
        self.CS_name_label = QLabel("CS name")
        self.CS_name_label.setStyleSheet(WHITE_COLOR)
        self.CS_name_input = QLineEdit()
        self.CS_name_label.setVisible(False)
        self.CS_name_input.setVisible(False)
        self.CS_name_input.setEnabled(False)
        self.NS_name_label = QLabel("NS name")
        self.NS_name_label.setStyleSheet(WHITE_COLOR)
        self.NS_name_input = QLineEdit()
        self.NS_name_label.setVisible(False)
        self.NS_name_input.setVisible(False)
        self.NS_name_input.setEnabled(False)
        self.NS_name_input.setText("NS")
        self.CS_name_input.setText("CS")

        self.sig_type_label = QLabel("Signal Type")
        self.sig_type_label.setStyleSheet(WHITE_COLOR)
        self.sig_type_combo = QComboBox()
        pal = self.sig_type_combo.palette()
        pal.setColor(QPalette.Button, QColor(255, 255, 255))
        self.sig_type_combo.setPalette(pal)
        self.sig_type_combo.addItems(self.sig_types)

        self.sig_size_label = QLabel("Size (eg. 32) * ")
        self.sig_size_label.setStyleSheet(WHITE_COLOR)
        self.sig_size_input = QLineEdit()
        self.sig_size_input.setText("1")
        self.sig_size_input.setEnabled(False)

        self.onlyInt = QIntValidator()
        self.sig_size_input.setValidator(self.onlyInt)
        self.binaryBitSize_label = QLabel("Bits")
        self.binaryBitSize_label.setStyleSheet(WHITE_COLOR)
        self.binaryBitSize_input = QLineEdit()
        self.binaryBitSize_input.setText("1")
        self.binaryBitSize_input.setValidator(self.onlyInt)
        self.binaryBitSize_input.setVisible(False)
        self.binaryBitSize_label.setVisible(False)

        self.sig_desc_label = QLabel("Signal Description")
        self.sig_desc_label.setStyleSheet(WHITE_COLOR)
        self.sig_desc_input = QPlainTextEdit()

        self.stateNames_table = QTableWidget()
        self.stateNames_table.setColumnCount(4)
        self.stateNames_table.setShowGrid(False)
        self.stateNames_table.setColumnWidth(0, 150)
        self.stateNames_table.setColumnWidth(1, 25)
        self.stateNames_table.setColumnWidth(2, 25)
        self.stateNames_table.setColumnWidth(3, 100)
        self.stateNames_table.setVisible(False)
        self.stateNames_table.horizontalScrollBar().hide()
        self.header0_label = QLabel("state name")
        header = self.stateNames_table.horizontalHeader()
        header.hide()
        header = self.stateNames_table.verticalHeader()
        header.hide()

        self.add_btn = QPushButton("Add state")
        self.add_btn.setFixedSize(80, 25)
        self.add_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}")
        self.add_btn.setVisible(False)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFixedSize(60, 25)
        self.cancel_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}")


        self.ok_btn = QPushButton("Ok")
        self.ok_btn.setEnabled(False)
        self.ok_btn.setFixedSize(60, 25)
        self.ok_btn.setStyleSheet(
            "QPushButton {background-color: rgb(169,169,169);  color: black; border-radius: 8px; border-style: plain;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}"
            "QPushButton:enabled {background-color: white; color: black; border-radius: 8px; border-style: plain; }")

        self.input_frame = QFrame()

        self.cancelled = True

        self.setup_ui()

        if add_or_edit == "edit" and intSig_data != None:
            print("editing")
            self.load_sig_data(intSig_data)

    def setup_ui(self):

        self.input_layout.addWidget(self.intSig_name_label, 0, 0)#, 1, 3)
        self.input_layout.addWidget(self.intSig_name_input, 1, 0)#, 1, 3)

        self.input_layout.addWidget(self.CS_name_label, 0, 1)
        self.input_layout.addWidget(self.CS_name_input, 1, 1)

        self.input_layout.addWidget(self.NS_name_label, 0, 2)
        self.input_layout.addWidget(self.NS_name_input, 1, 2)

        self.input_layout.addWidget(self.sig_desc_label, 2, 0, 1, 3)
        self.input_layout.addWidget(self.sig_desc_input, 3, 0, 1, 3)

        self.input_layout.addWidget(self.sig_type_label, 4, 0, 1, 2)
        self.input_layout.addWidget(self.sig_type_combo, 5, 0, 1, 2)

        self.input_layout.addWidget(self.sig_size_label, 4, 2, 1, 1)
        self.input_layout.addWidget(self.sig_size_input, 5, 2, 1, 1)

        self.input_layout.addWidget(self.stateNames_table, 6, 0, 2, 3)


        self.input_layout.addWidget(self.add_btn, 5, 2, 1, 1)

        self.input_layout.addItem(QSpacerItem(0, 20), 7, 0, 1, 3)
        self.input_layout.addWidget(self.cancel_btn, 8, 1, 1, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 8, 2, 1, 1, alignment=Qt.AlignRight)

        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setFixedSize(400, 400)
        self.input_frame.setLayout(self.input_layout)

        self.sig_type_combo.currentTextChanged.connect(self.sig_type_options)
        self.intSig_name_input.textChanged.connect(self.updateCSAndNS)
        self.sig_desc_input.setVisible(True)
        self.sig_desc_label.setVisible(True)
        self.stateNames_table.setVisible(False)

        self.add_btn.clicked.connect(self.add_stateName)
        self.ok_btn.clicked.connect(self.get_data)
        self.cancel_btn.clicked.connect(self.cancel_selected)

        self.mainLayout.addWidget(self.input_frame, alignment=Qt.AlignCenter)
        self.sig_size_input.textChanged.connect(self.enable_ok_btn)
        self.intSig_name_input.textChanged.connect(self.enable_ok_btn)
        self.setLayout(self.mainLayout)

    def load_sig_data(self, intSig_data):
        self.sig_type_combo.setCurrentText(intSig_data[1])
        if intSig_data[1] != "Enumerated type state signals":
            self.sig_size_input.setText(intSig_data[2])
            if intSig_data[1] == "std_logic_vector state signals":
                self.intSig_name_input.setText(intSig_data[0][2:])
            else:
                self.intSig_name_input.setText(intSig_data[0])
        else:
            self.intSig_name_input.setText(intSig_data[0][2:])
            self.all_stateNames.append(intSig_data[2])
            intSig_data[2] = str(intSig_data[2]).replace('\'', '')
            intSig_data[2] = str(intSig_data[2]).replace('[', '')
            intSig_data[2] = str(intSig_data[2]).replace(']', '')
            intSig_data[2] = str(intSig_data[2]).replace(',', '')
            print(intSig_data[2])
            stateNames = intSig_data[2].split(" ")
            self.all_stateNames=stateNames
            i = 0
            for state in stateNames:

                delete_btn = QPushButton()
                delete_btn.setIcon(qta.icon("mdi.delete"))
                delete_btn.setFixedSize(35, 22)
                delete_btn.clicked.connect(self.delete_clicked)

                edit_btn = QPushButton()
                edit_btn.setIcon(qta.icon("mdi.pencil"))
                edit_btn.setFixedSize(35, 22)
                edit_btn.clicked.connect(self.edit_stateName)

                rst_state_tickbox = QCheckBox("Make rst state")
                rst_state_tickbox.setStyleSheet(BLACK_COLOR)
                if i==0:
                    rst_state_tickbox.setCheckState(Qt.Checked)
                row_position = self.stateNames_table.rowCount()
                self.stateNames_table.insertRow(row_position)
                self.stateNames_table.setRowHeight(row_position, 1)

                self.stateNames_table.setItem(row_position, 0, QTableWidgetItem(state))
                self.stateNames_table.setCellWidget(row_position, 1, edit_btn)
                self.stateNames_table.setCellWidget(row_position, 2, delete_btn)
                self.stateNames_table.setCellWidget(row_position, 3, rst_state_tickbox)
                i=i+1
        intSig_data[3] = intSig_data[3].replace("&#10;", "\n")
        intSig_data[3] = os.linesep.join([
            line for line in intSig_data[3].splitlines()
            if line.strip() != ''
        ])
        self.sig_desc_input.setPlainText(intSig_data[3])

    def makeIdeal(self):
        for i in range(self.stateNames_table.rowCount()):
            if self.stateNames_table.cellWidget(i, 3).checkState() == Qt.Checked:
                self.all_stateNames.insert(0, self.all_stateNames[i])
                self.all_stateNames.pop(i+1)
    def get_stateTypes(self):
        data = self.all_stateNames
        return data
    def get_data(self):
        data = []

        intSignalDescription = self.sig_desc_input.toPlainText()#text()
        intSignalDescription = intSignalDescription.replace("\n", "&#10;")
        intSignalDescription = os.linesep.join([
            line for line in intSignalDescription.splitlines()
            if line.strip() != ''
        ])
        if intSignalDescription == "":
            intSignalDescription = "to be completed"
        data.append(self.intSig_name_input.text())
        data.append(self.sig_type_combo.currentText())
        if self.sig_type_combo.currentText() != "Enumerated type state signals":
            data.append(self.sig_size_input.text())
        else:
            data.append(self.all_stateNames)
        data.append(intSignalDescription)

        self.cancelled = False
        self.close()
        return data

    def cancel_selected(self):
        self.cancelled = True
        self.close()

    def enable_ok_btn(self):
        if self.sig_type_combo.currentText() == "std_logic_vector state signals" or self.sig_type_combo.currentText() == "Enumerated type state signals":
            if self.sig_size_input.text() != "":
                self.ok_btn.setEnabled(True)
            else:
                self.ok_btn.setEnabled(False)
        else:
            if self.intSig_name_input.text() != "" and self.sig_size_input.text() != "" :
                self.ok_btn.setEnabled(True)
            else:
                self.ok_btn.setEnabled(False)

    def add_stateName(self):
        add_stateName = state_Name_Dialog("add")
        add_stateName.exec_()

        if not add_stateName.cancelled:
            stateName_data = add_stateName.get_data()
            self.all_stateNames.append(stateName_data)
            print(self.all_stateNames)
            delete_btn = QPushButton()
            delete_btn.setIcon(qta.icon("mdi.delete"))
            delete_btn.setFixedSize(35, 22)
            delete_btn.clicked.connect(self.delete_clicked)

            edit_btn = QPushButton()
            edit_btn.setIcon(qta.icon("mdi.pencil"))
            edit_btn.setFixedSize(35, 22)
            edit_btn.clicked.connect(self.edit_stateName)

            rst_state_tickbox = QCheckBox("Make rst state")
            rst_state_tickbox.setStyleSheet(BLACK_COLOR)

            row_position = self.stateNames_table.rowCount()
            self.stateNames_table.insertRow(row_position)
            self.stateNames_table.setRowHeight(row_position, 1)

            self.stateNames_table.setItem(row_position, 0, QTableWidgetItem(stateName_data))
            self.stateNames_table.setCellWidget(row_position, 1, edit_btn)
            self.stateNames_table.setCellWidget(row_position, 2, delete_btn)
            self.stateNames_table.setCellWidget(row_position, 3, rst_state_tickbox)



    def edit_stateName(self):
        button = self.sender()
        if button:
            row = self.stateNames_table.indexAt(button.pos()).row()
            add_stateName = state_Name_Dialog("edit", self.all_stateNames[row])
            add_stateName.exec_()

            if not add_stateName.cancelled:
                stateName_data = add_stateName.get_data()
                self.stateNames_table.removeRow(row)
                self.all_stateNames.pop(row)

                delete_btn = QPushButton()
                delete_btn.setIcon(qta.icon("mdi.delete"))
                delete_btn.setFixedSize(35, 22)
                delete_btn.clicked.connect(self.delete_clicked)

                edit_btn = QPushButton()
                edit_btn.setIcon(qta.icon("mdi.pencil"))
                edit_btn.setFixedSize(35, 22)
                edit_btn.clicked.connect(self.edit_stateName)

                rst_state_tickbox = QCheckBox("Make rst state")
                rst_state_tickbox.setStyleSheet(BLACK_COLOR)

                self.all_stateNames.insert(row, stateName_data)
                row_position = self.stateNames_table.rowCount()
                self.stateNames_table.insertRow(row_position)
                self.stateNames_table.setRowHeight(row_position, 1)

                self.stateNames_table.setItem(row_position, 0, QTableWidgetItem(stateName_data))#[0]))
                self.stateNames_table.setCellWidget(row_position, 1, edit_btn)
                self.stateNames_table.setCellWidget(row_position, 2, delete_btn)
                self.stateNames_table.setCellWidget(row_position, 3, rst_state_tickbox)


    def sig_type_options(self):
        if self.sig_type_combo.currentText() == "std_logic_vector":
            self.intSig_name_label.setText("Internal Signal Name*")
            self.ok_btn.setEnabled(False)
            self.sig_desc_label.setVisible(True)
            self.sig_desc_input.setVisible(True)
            self.CS_name_label.setVisible(False)
            self.CS_name_input.setVisible(False)
            self.NS_name_label.setVisible(False)
            self.NS_name_input.setVisible(False)
            self.sig_size_label.setVisible(True)
            self.sig_size_input.setVisible(True)
            self.sig_size_input.setEnabled(True)
            self.sig_size_input.clear()
            self.stateNames_table.setVisible(False)
            self.add_btn.setVisible(False)

        elif self.sig_type_combo.currentText() == "std_logic" :
            self.intSig_name_label.setText("Internal Signal Name*")
            self.ok_btn.setEnabled(False)
            self.sig_desc_label.setVisible(True)
            self.sig_desc_input.setVisible(True)
            self.CS_name_label.setVisible(False)
            self.CS_name_input.setVisible(False)
            self.NS_name_label.setVisible(False)
            self.NS_name_input.setVisible(False)
            self.stateNames_table.setVisible(False)
            self.add_btn.setVisible(False)
            self.sig_size_label.setVisible(True)
            self.sig_size_input.setVisible(True)
            self.sig_size_input.setEnabled(False)
            self.sig_size_input.setText("1")
        elif self.sig_type_combo.currentText() == "Enumerated type state signals":
            self.intSig_name_label.setText("Suffix eg_abc")
            self.ok_btn.setEnabled(True)
            self.sig_desc_label.setVisible(True)
            self.sig_desc_input.setVisible(True)
            self.CS_name_label.setVisible(True)
            self.CS_name_input.setVisible(True)
            self.NS_name_label.setVisible(True)
            self.NS_name_input.setVisible(True)
            self.stateNames_table.setVisible(True)
            self.add_btn.setVisible(True)
            self.sig_size_label.setVisible(False)
            self.sig_size_input.setVisible(False)
            self.sig_size_input.setEnabled(False)

        elif self.sig_type_combo.currentText() == "std_logic_vector state signals":
            self.intSig_name_label.setText("Suffix eg_abc")
            self.ok_btn.setEnabled(False)
            self.sig_desc_label.setVisible(True)
            self.sig_desc_input.setVisible(True)
            self.CS_name_label.setVisible(True)
            self.CS_name_input.setVisible(True)
            self.NS_name_label.setVisible(True)
            self.NS_name_input.setVisible(True)
            self.add_btn.setVisible(False)
            self.stateNames_table.setVisible(False)
            self.add_btn.setVisible(False)
            self.sig_size_label.setVisible(True)
            self.sig_size_input.setVisible(True)
            self.sig_size_input.setEnabled(True)
            self.sig_size_input.clear()

        elif self.sig_type_combo.currentText() == "signed":
            self.intSig_name_label.setText("Internal Signal Name*")
            self.ok_btn.setEnabled(False)
            self.sig_desc_label.setVisible(True)
            self.sig_desc_input.setVisible(True)
            self.CS_name_label.setVisible(False)
            self.CS_name_input.setVisible(False)
            self.NS_name_label.setVisible(False)
            self.NS_name_input.setVisible(False)
            self.sig_size_label.setVisible(True)
            self.sig_size_input.setVisible(True)
            self.sig_size_input.setEnabled(True)
            self.sig_size_input.clear()
            self.stateNames_table.setVisible(False)
            self.add_btn.setVisible(False)

        elif self.sig_type_combo.currentText() == "unsigned":
            self.ok_btn.setEnabled(False)
            self.sig_desc_label.setVisible(True)
            self.sig_desc_input.setVisible(True)
            self.CS_name_label.setVisible(False)
            self.CS_name_input.setVisible(False)
            self.NS_name_label.setVisible(False)
            self.NS_name_input.setVisible(False)
            self.sig_size_label.setVisible(True)
            self.sig_size_input.setVisible(True)
            self.sig_size_input.setEnabled(True)
            self.sig_size_input.clear()
            self.stateNames_table.setVisible(False)
            self.add_btn.setVisible(False)

        elif self.sig_type_combo.currentText() == "integer":
            self.intSig_name_label.setText("Internal Signal Name*")
            self.ok_btn.setEnabled(False)
            self.sig_desc_label.setVisible(True)
            self.sig_desc_input.setVisible(True)
            self.CS_name_label.setVisible(False)
            self.CS_name_input.setVisible(False)
            self.NS_name_label.setVisible(False)
            self.NS_name_input.setVisible(False)
            self.sig_size_label.setVisible(True)
            self.sig_size_input.setVisible(True)
            self.sig_size_input.setEnabled(True)
            self.sig_size_input.clear()
            self.stateNames_table.setVisible(False)
            self.add_btn.setVisible(False)

    def delete_clicked(self):
        button = self.sender()
        if button:
            row = self.stateNames_table.indexAt(button.pos()).row()
            self.stateNames_table.removeRow(row)
            self.all_stateNames.pop(row)

    def updateCSAndNS(self):
        self.NS_name_input.setText("NS"+self.intSig_name_input.text())
        self.CS_name_input.setText("CS"+self.intSig_name_input.text())