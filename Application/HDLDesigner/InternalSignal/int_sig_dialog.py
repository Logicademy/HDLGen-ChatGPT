#Dialog box for adding/editing internal signals called in the internal_signal.py class. Will also call stateNamesDialog.py when states are added/edited
import os
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import qtawesome as qta
import sys
sys.path.append("..")
from HDLDesigner.InternalSignal.stateNamesDialog import state_Name_Dialog
from ProjectManager.project_manager import ProjectManager
from xml.dom import minidom

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"

class IntSignalDialog(QDialog):

    def __init__(self, add_or_edit, signals_names, intSig_data=None):
        super().__init__()
        input_font = QFont()
        input_font.setPointSize(10)
        self.signalNames = signals_names
        self.signalName = ""
        if intSig_data != None:
            self.signalName = intSig_data[0]
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

        self.sig_types = ["standard", "state signal pair(NS/CS)","array"]

        self.state_sig_types = ["bus", "Enumerated type", "integer"]
        self.standard_signal_types = ["single bit", "bus", "signed", "unsigned", "integer"]
        self.mainLayout = QVBoxLayout()

        self.intSig_name_label = QLabel("Internal Signal Name*")
        self.intSig_name_label.setStyleSheet(WHITE_COLOR)
        self.intSig_name_label.setFont(input_font)
        self.intSig_name_input = QLineEdit()
        self.intSig_name_input.setFont(input_font)

        self.state_signal_Type_label = QLabel("State Signal Type")
        self.state_signal_Type_label.setStyleSheet(WHITE_COLOR)
        self.state_signal_Type_label.setFont(input_font)
        self.state_signal_Type_input = QComboBox()
        self.state_signal_Type_input.setFont(input_font)
        self.state_signal_Type_input.setStyleSheet("QComboBox {padding: 2px;}")
        pal = self.state_signal_Type_input.palette()
        pal.setColor(QPalette.Button, QColor(255, 255, 255))
        self.state_signal_Type_input.setPalette(pal)
        self.state_signal_Type_input.addItems(self.state_sig_types)
        self.state_signal_Type_input.setVisible(False)
        self.state_signal_Type_label.setVisible(False)

        self.standard_signal_Type_label = QLabel("Standard Signal Type")
        self.standard_signal_Type_label.setStyleSheet(WHITE_COLOR)
        self.standard_signal_Type_label.setFont(input_font)
        self.standard_signal_Type_input = QComboBox()
        self.standard_signal_Type_input.setFont(input_font)
        self.standard_signal_Type_input.setStyleSheet("QComboBox {padding: 2px;}")
        pal = self.standard_signal_Type_input.palette()
        pal.setColor(QPalette.Button, QColor(255, 255, 255))
        self.standard_signal_Type_input.setPalette(pal)
        self.standard_signal_Type_input.addItems(self.standard_signal_types)
        #self.standard_signal_Type_input.setVisible(True)
        #self.standard_signal_Type_label.setVisible(True)

        self.CS_name_label = QLabel("CS name")
        self.CS_name_label.setStyleSheet(WHITE_COLOR)
        self.CS_name_label.setFont(input_font)
        self.CS_name_input = QLineEdit()
        self.CS_name_input.setFont(input_font)
        self.CS_name_label.setVisible(False)
        self.CS_name_input.setVisible(False)
        self.CS_name_input.setEnabled(False)
        self.NS_name_label = QLabel("NS name")
        self.NS_name_label.setStyleSheet(WHITE_COLOR)
        self.NS_name_label.setFont(input_font)
        self.NS_name_input = QLineEdit()
        self.NS_name_input.setFont(input_font)
        self.NS_name_label.setVisible(False)
        self.NS_name_input.setVisible(False)
        self.NS_name_input.setEnabled(False)
        self.NS_name_input.setText("NS")
        self.CS_name_input.setText("CS")

        self.sig_type_label = QLabel("Signal Type")
        self.sig_type_label.setStyleSheet(WHITE_COLOR)
        self.sig_type_label.setFont(input_font)
        self.sig_type_combo = QComboBox()
        self.sig_type_combo.setFont(input_font)
        self.sig_type_combo.setStyleSheet("QComboBox {padding: 2px;}")
        pal = self.sig_type_combo.palette()
        pal.setColor(QPalette.Button, QColor(255, 255, 255))
        self.sig_type_combo.setPalette(pal)
        self.sig_type_combo.addItems(self.sig_types)

        self.sig_size_label = QLabel("Size (eg. 32) * ")
        self.sig_size_label.setStyleSheet(WHITE_COLOR)
        self.sig_size_label.setFont(input_font)
        self.sig_size_input = QLineEdit()
        self.sig_size_input.setFont(input_font)
        self.sig_size_input.setText("1")
        self.sig_size_input.setEnabled(False)

        self.onlyInt = QIntValidator()
        self.sig_size_input.setValidator(self.onlyInt)
        self.binaryBitSize_label = QLabel("Bits")
        self.binaryBitSize_label.setFont(input_font)
        self.binaryBitSize_label.setStyleSheet(WHITE_COLOR)
        self.binaryBitSize_input = QLineEdit()
        self.binaryBitSize_input.setFont(input_font)
        self.binaryBitSize_input.setText("1")
        self.binaryBitSize_input.setValidator(self.onlyInt)
        self.binaryBitSize_input.setVisible(False)
        self.binaryBitSize_label.setVisible(False)

        self.sig_desc_label = QLabel("Signal Description")
        self.sig_desc_label.setFont(input_font)
        self.sig_desc_label.setStyleSheet(WHITE_COLOR)
        self.sig_desc_input = QPlainTextEdit()
        self.sig_desc_input.setFont(input_font)
        self.sig_desc_input.setLineWrapMode(QPlainTextEdit.WidgetWidth)

        self.stateNames_table = QTableWidget()
        self.stateNames_table.setFont(input_font)
        self.stateNames_table.setColumnCount(4)
        self.stateNames_table.setShowGrid(False)
        #self.stateNames_table.setColumnWidth(0, 150)
        #self.stateNames_table.setColumnWidth(1, 25)
        #self.stateNames_table.setColumnWidth(2, 25)
        #self.stateNames_table.setColumnWidth(3, 100)
        self.stateNames_table.setVisible(False)
        self.stateNames_table.horizontalScrollBar().hide()
        self.header0_label = QLabel("state name")
        self.header0_label.setFont(input_font)
        header = self.stateNames_table.horizontalHeader()
        header.hide()
        header = self.stateNames_table.verticalHeader()
        header.hide()

        self.add_btn = QPushButton("Add state")
        self.add_btn.setFont(input_font)
        #self.add_btn.setFixedSize(80, 25)
        self.add_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}")
        self.add_btn.setVisible(False)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFont(input_font)
        self.cancel_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}")

        self.ok_btn = QPushButton("Ok")
        self.ok_btn.setEnabled(False)
        self.ok_btn.setFont(input_font)
        self.ok_btn.setStyleSheet(
            "QPushButton {background-color: rgb(169,169,169);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            "QPushButton:enabled {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px; }")

        self.arrayName_label = QLabel("Arrays")
        self.arrayName_label.setStyleSheet(WHITE_COLOR)
        self.arrayName_label.setFont(input_font)
        self.arrayName_input = QComboBox()
        self.arrayName_input.setFont(input_font)
        self.arrayName_input.setStyleSheet("QComboBox {padding: 2px;}")
        pal = self.arrayName_input.palette()
        pal.setColor(QPalette.Button, QColor(255, 255, 255))
        self.arrayName_input.setPalette(pal)
        self.arrayName_label.setVisible(False)
        self.arrayName_input.setVisible(False)
        self.arrayName_input.setCurrentText("Create in packages")
        self.stateNames_table.setVisible(False)
        self.input_frame = QFrame()

        self.cancelled = True
        self.arrays = []
        self.setup_ui()
        mainPackageDir = ProjectManager.get_main_hdlgen()

        root = minidom.parse(mainPackageDir)
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
        mainPackage = hdlDesign[0].getElementsByTagName("mainPackage")
        array_nodes = mainPackage[0].getElementsByTagName('array')

        if len(array_nodes) != 0:
            for i in range(0, len(array_nodes)):
                array_name = array_nodes[i].getElementsByTagName('name')[0].firstChild.data
                self.arrays.append(array_name)
        self.arrayName_input.addItems(self.arrays)

        if add_or_edit == "edit" and intSig_data != None:
            self.load_sig_data(intSig_data)

    def setup_ui(self):

        self.input_layout.addWidget(self.intSig_name_label, 0, 0)
        self.input_layout.addWidget(self.intSig_name_input, 1, 0)

        self.input_layout.addWidget(self.CS_name_label, 0, 0)
        self.input_layout.addWidget(self.CS_name_input, 1, 0)

        self.input_layout.addWidget(self.NS_name_label, 0, 1)
        self.input_layout.addWidget(self.NS_name_input, 1, 1)

        self.input_layout.addWidget(self.sig_type_label, 2, 0, 1, 1)
        self.input_layout.addWidget(self.sig_type_combo, 3, 0, 1, 1)

        self.input_layout.addWidget(self.sig_size_label, 2, 2, 1, 1)
        self.input_layout.addWidget(self.sig_size_input, 3, 2, 1, 1)

        self.input_layout.addWidget(self.arrayName_label, 2, 1, 1, 2)
        self.input_layout.addWidget(self.arrayName_input, 3, 1, 1, 2)

        self.input_layout.addWidget(self.sig_desc_label, 6, 0, 1, 3)
        self.input_layout.addWidget(self.sig_desc_input, 7, 0, 1, 3)

        self.input_layout.addWidget(self.stateNames_table, 4, 0, 2, 3)


        self.input_layout.addWidget(self.add_btn, 3, 2, 1, 1)
        self.input_layout.addWidget(self.state_signal_Type_label, 2, 1, 1, 1)
        self.input_layout.addWidget(self.state_signal_Type_input, 3, 1, 1, 1)
        self.input_layout.addWidget(self.standard_signal_Type_label, 2, 1, 1, 1)
        self.input_layout.addWidget(self.standard_signal_Type_input, 3, 1, 1, 1)
        self.input_layout.addWidget(self.cancel_btn, 8, 1, 1, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 8, 2, 1, 1, alignment=Qt.AlignRight)

        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setFixedSize(600, 600)
        self.input_frame.setLayout(self.input_layout)

        self.sig_type_combo.currentTextChanged.connect(self.sig_type_options)
        self.state_signal_Type_input.currentTextChanged.connect(self.state_sig_type_options)
        self.standard_signal_Type_input.currentTextChanged.connect(self.standard_sig_type_options)

        self.sig_type_combo.currentTextChanged.connect(self.enable_ok_btn)
        self.state_signal_Type_input.currentTextChanged.connect(self.enable_ok_btn)
        self.standard_signal_Type_input.currentTextChanged.connect(self.enable_ok_btn)
        self.intSig_name_input.textChanged.connect(self.updateCSAndNS)



        self.add_btn.clicked.connect(self.add_stateName)
        self.ok_btn.clicked.connect(self.get_data)
        self.cancel_btn.clicked.connect(self.cancel_selected)

        self.mainLayout.addWidget(self.input_frame, alignment=Qt.AlignCenter)
        self.sig_size_input.textChanged.connect(self.enable_ok_btn)
        self.intSig_name_input.textChanged.connect(self.enable_ok_btn)
        self.setLayout(self.mainLayout)

    def load_sig_data(self, intSig_data):
        if intSig_data[1][-24:] == "state signal pair(NS/CS)":
            self.sig_type_combo.setCurrentText(intSig_data[1][-24:])
            self.state_signal_Type_input.setCurrentText(intSig_data[1][:-25])
        else:
            self.sig_type_combo.setCurrentText(intSig_data[1])
        if intSig_data[1][:15] != "Enumerated type":
            if intSig_data[1] == "bus state signal pair(NS/CS)" or intSig_data[1] == "integer state signal pair(NS/CS)":
                self.intSig_name_input.setText(intSig_data[0][2:])
                self.sig_size_input.setText(intSig_data[2])
            else:
                if intSig_data[1] == "single bit":
                    self.standard_signal_Type_input.setCurrentText(intSig_data[1])
                    self.sig_type_combo.setCurrentText("standard")
                    self.intSig_name_input.setText(intSig_data[0])
                    self.sig_size_input.setText(intSig_data[2])
                elif intSig_data[1][:3] == "bus":
                    self.standard_signal_Type_input.setCurrentText(intSig_data[1][:3])
                    self.sig_type_combo.setCurrentText("standard")
                    self.intSig_name_input.setText(intSig_data[0])
                    self.sig_size_input.setText(intSig_data[2])
                elif intSig_data[1][:7] == "integer":
                    self.standard_signal_Type_input.setCurrentText(intSig_data[1][:7])
                    self.sig_type_combo.setCurrentText("standard")
                    self.intSig_name_input.setText(intSig_data[0])
                    self.sig_size_input.setText(intSig_data[2])
                elif intSig_data[1][:6] == "signed":
                    self.standard_signal_Type_input.setCurrentText(intSig_data[1][:6])
                    self.sig_type_combo.setCurrentText("standard")
                    self.intSig_name_input.setText(intSig_data[0])
                    self.sig_size_input.setText(intSig_data[2])
                elif intSig_data[1][:8] == "unsigned":
                    self.standard_signal_Type_input.setCurrentText(intSig_data[1][:8])
                    self.sig_type_combo.setCurrentText("standard")
                    self.intSig_name_input.setText(intSig_data[0])
                    self.sig_size_input.setText(intSig_data[2])
                else:
                    self.intSig_name_input.setText(intSig_data[0])
                    self.sig_type_combo.setCurrentText("array")
                    arrayname = intSig_data[1].split(",")
                    self.arrayName_input.setCurrentText(arrayname[1])

        elif intSig_data[1][:15] == "Enumerated type":
            self.intSig_name_input.setText(intSig_data[0][2:])
            self.all_stateNames.append(intSig_data[2])
            intSig_data[2] = str(intSig_data[2]).replace('\'', '')
            intSig_data[2] = str(intSig_data[2]).replace('[', '')
            intSig_data[2] = str(intSig_data[2]).replace(']', '')
            intSig_data[2] = str(intSig_data[2]).replace(',', '')
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
                input_font = QFont()
                input_font.setPointSize(10)
                rst_state_tickbox.setFont(input_font)
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
        intSig_data[3] = intSig_data[3].replace("&amp;", "&")
        intSig_data[3] = intSig_data[3].replace("&amp;", "&")
        intSig_data[3] = intSig_data[3].replace("&quot;", "\"")
        intSig_data[3] = intSig_data[3].replace("&apos;", "\'")
        intSig_data[3] = intSig_data[3].replace("&lt;", "<")
        intSig_data[3] = intSig_data[3].replace("&#x9;", "\t")
        intSig_data[3] = intSig_data[3].replace("&gt;", ">")
        intSig_data[3] = intSig_data[3].replace("&#44;", ",")

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
        cursor = self.sig_desc_input.textCursor()
        doc = self.sig_desc_input.document()
        lines = ""
        line = ""
        for i in range(doc.blockCount()):
            block = doc.findBlockByNumber(i)
            if block.isVisible():
                for j in range(block.layout().lineCount()):
                    lineStart = block.position() + block.layout().lineAt(j).textStart()
                    lineEnd = lineStart + block.layout().lineAt(j).textLength()
                    cursor.setPosition(lineStart)
                    cursor.setPosition(lineEnd, QTextCursor.KeepAnchor)
                    line += cursor.selectedText()
                    if lineEnd == cursor.position():
                        lines += line + "\n"
                        line = ""
        lines = lines.strip()
        intSignalDescription = lines
        intSignalDescription = intSignalDescription.replace("&", "&amp;")
        intSignalDescription = intSignalDescription.replace("\n", "&#10;")
        intSignalDescription = intSignalDescription.replace("\"", "&quot;")
        intSignalDescription = intSignalDescription.replace("\'", "&apos;")
        intSignalDescription = intSignalDescription.replace("\n", "&#10;")
        intSignalDescription = intSignalDescription.replace("<", "&lt;")
        intSignalDescription = intSignalDescription.replace("\t", "&#x9;")
        intSignalDescription = intSignalDescription.replace(">", "&gt;")
        intSignalDescription = intSignalDescription.replace(",", "&#44;")


        intSignalDescription = os.linesep.join([
            line for line in intSignalDescription.splitlines()
            if line.strip() != ''
        ])
        if intSignalDescription == "":
            intSignalDescription = "to be completed"
        data.append(self.intSig_name_input.text().strip().replace(" ", ""))

        if self.sig_type_combo.currentText() == "state signal pair(NS/CS)":
            data.append(str(self.state_signal_Type_input.currentText())+" state signal pair(NS/CS)")
        elif self.sig_type_combo.currentText() == "array":
            data.append("array," + self.arrayName_input.currentText())
        elif self.sig_type_combo.currentText() == "standard":
            data.append(self.standard_signal_Type_input.currentText())
        if data[1] != "Enumerated type state signal pair(NS/CS)":
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

        if self.sig_type_combo.currentText() == "standard" and (self.standard_signal_Type_input.currentText() == "bus" or self.standard_signal_Type_input.currentText() == "integer" or self.standard_signal_Type_input.currentText() == "signed" or self.standard_signal_Type_input.currentText() == "unsigned"):
            if self.sig_size_input.text() != "" and self.intSig_name_input.text() != "":
                self.ok_btn.setEnabled(True)
            else:
                self.ok_btn.setEnabled(False)
        elif self.sig_type_combo.currentText() == "array":
            if self.intSig_name_input.text() != "":
                if self.arrayName_input.currentText() != "Create in packages":
                    self.ok_btn.setEnabled(True)
            else:
                self.ok_btn.setEnabled(False)
        elif self.sig_type_combo.currentText() == "state signal pair(NS/CS)" and (self.state_signal_Type_input.currentText() == "bus" or self.state_signal_Type_input.currentText() == "integer"):
            if self.sig_size_input.text() != "":
                self.ok_btn.setEnabled(True)
            else:
                self.ok_btn.setEnabled(False)
        elif self.sig_type_combo.currentText() == "state signal pair(NS/CS)" and self.state_signal_Type_input.currentText() == "Enumerated type":
            self.ok_btn.setEnabled(True)
        elif self.sig_type_combo.currentText() == "standard" and self.standard_signal_Type_input.currentText() == "single bit":
            if self.intSig_name_input.text() != "":
                self.ok_btn.setEnabled(True)
            else:
                self.ok_btn.setEnabled(False)
        else:
            self.ok_btn.setEnabled(False)



    def add_stateName(self):
        add_stateName = state_Name_Dialog("add")
        add_stateName.exec_()

        if not add_stateName.cancelled:
            stateName_data = add_stateName.get_data()
            self.all_stateNames.append(stateName_data)
            delete_btn = QPushButton()
            delete_btn.setIcon(qta.icon("mdi.delete"))
            delete_btn.setFixedSize(35, 22)
            delete_btn.clicked.connect(self.delete_clicked)

            edit_btn = QPushButton()
            edit_btn.setIcon(qta.icon("mdi.pencil"))
            edit_btn.setFixedSize(35, 22)
            edit_btn.clicked.connect(self.edit_stateName)

            rst_state_tickbox = QCheckBox("Make rst state")
            input_font = QFont()
            input_font.setPointSize(10)
            rst_state_tickbox.setFont(input_font)
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
                input_font = QFont()
                input_font.setPointSize(10)
                rst_state_tickbox.setFont(input_font)
                rst_state_tickbox.setStyleSheet(BLACK_COLOR)

                self.all_stateNames.insert(row, stateName_data)
                row_position = self.stateNames_table.rowCount()
                self.stateNames_table.insertRow(row_position)
                self.stateNames_table.setRowHeight(row_position, 1)

                self.stateNames_table.setItem(row_position, 0, QTableWidgetItem(stateName_data))#[0]))
                self.stateNames_table.setCellWidget(row_position, 1, edit_btn)
                self.stateNames_table.setCellWidget(row_position, 2, delete_btn)
                self.stateNames_table.setCellWidget(row_position, 3, rst_state_tickbox)

    def standard_sig_type_options(self):
        if self.standard_signal_Type_input.currentText() != "single bit":
            self.sig_size_input.setEnabled(True)
            self.sig_size_input.clear()
            if self.standard_signal_Type_input.currentText() == "integer":
                self.sig_size_label.setText("Number of values")
            else:
                self.sig_size_label.setText("Size (eg. 32)*")
        else:
            self.sig_size_input.setText("1")
            self.sig_size_input.setEnabled(False)


    def state_sig_type_options(self):
        if self.state_signal_Type_input.currentText() != "Enumerated type":
            self.add_btn.setVisible(False)
            self.stateNames_table.setVisible(False)
            self.add_btn.setVisible(False)
            self.sig_size_label.setVisible(True)
            self.sig_size_input.setVisible(True)
            self.sig_size_input.setEnabled(True)
            if self.state_signal_Type_input.currentText() == "integer":
                self.sig_size_label.setText("Number of values")
            else:
                self.sig_size_label.setText("Size (eg. 32)*")
        else:
            self.stateNames_table.setVisible(True)
            self.add_btn.setVisible(True)
            self.sig_size_label.setVisible(False)
            self.sig_size_input.setVisible(False)
            self.sig_size_input.setEnabled(False)


    def sig_type_options(self):
        if self.sig_type_combo.currentText() == "standard":
            self.intSig_name_label.setText("Internal Signal Name*")
            self.input_layout.addWidget(self.intSig_name_label, 0, 0)
            self.input_layout.addWidget(self.intSig_name_input, 1, 0)
            self.standard_signal_Type_input.setVisible(True)
            self.standard_signal_Type_label.setVisible(True)
            self.ok_btn.setEnabled(False)
            self.sig_desc_label.setVisible(True)
            self.state_signal_Type_input.setVisible(False)
            self.state_signal_Type_label.setVisible(False)
            self.sig_desc_input.setVisible(True)
            self.CS_name_label.setVisible(False)
            self.CS_name_input.setVisible(False)
            self.NS_name_label.setVisible(False)
            self.NS_name_input.setVisible(False)
            self.sig_size_label.setVisible(True)
            self.sig_size_input.setVisible(True)
            self.standard_signal_Type_input.setCurrentText("single bit")
            self.sig_size_input.setText("1")
            self.sig_size_input.setEnabled(False)
            self.stateNames_table.setVisible(False)
            self.add_btn.setVisible(False)
            self.arrayName_label.setVisible(False)
            self.arrayName_input.setVisible(False)

        elif self.sig_type_combo.currentText() == "array":
            self.intSig_name_label.setText("Internal Signal Name*")
            self.input_layout.addWidget(self.intSig_name_label, 0, 0)
            self.input_layout.addWidget(self.intSig_name_input, 1, 0)
            self.ok_btn.setEnabled(False)
            self.sig_desc_label.setVisible(True)
            self.standard_signal_Type_input.setVisible(False)
            self.standard_signal_Type_label.setVisible(False)
            self.state_signal_Type_input.setVisible(False)
            self.state_signal_Type_label.setVisible(False)
            self.sig_desc_input.setVisible(True)
            self.CS_name_label.setVisible(False)
            self.CS_name_input.setVisible(False)
            self.NS_name_label.setVisible(False)
            self.NS_name_input.setVisible(False)
            self.sig_size_label.setVisible(False)
            self.sig_size_input.setVisible(False)
            self.sig_size_input.setEnabled(False)
            self.sig_size_input.clear()
            self.stateNames_table.setVisible(False)
            self.add_btn.setVisible(False)
            self.arrayName_label.setVisible(True)
            self.arrayName_input.setVisible(True)

        elif self.sig_type_combo.currentText() == "state signal pair(NS/CS)":
            self.intSig_name_label.setText("Suffix eg_abc")
            self.input_layout.addWidget(self.intSig_name_label, 0, 2)
            self.input_layout.addWidget(self.intSig_name_input, 1, 2)
            self.ok_btn.setEnabled(False)
            self.sig_desc_label.setVisible(True)
            self.sig_desc_input.setVisible(True)
            self.CS_name_label.setVisible(True)
            self.CS_name_input.setVisible(True)
            self.NS_name_label.setVisible(True)
            self.NS_name_input.setVisible(True)
            self.state_signal_Type_input.setVisible(True)
            self.state_signal_Type_label.setVisible(True)
            self.standard_signal_Type_input.setVisible(False)
            self.standard_signal_Type_label.setVisible(False)
            self.add_btn.setVisible(False)
            self.stateNames_table.setVisible(False)
            self.add_btn.setVisible(False)
            self.sig_size_label.setVisible(True)
            self.sig_size_input.setVisible(True)
            self.sig_size_input.setEnabled(True)
            self.sig_size_input.clear()
            self.arrayName_label.setVisible(False)
            self.arrayName_input.setVisible(False)

    def delete_clicked(self):
        button = self.sender()
        if button:
            row = self.stateNames_table.indexAt(button.pos()).row()
            self.stateNames_table.removeRow(row)
            self.all_stateNames.pop(row)

    def updateCSAndNS(self):
        self.NS_name_input.setText("NS"+self.intSig_name_input.text())
        self.CS_name_input.setText("CS"+self.intSig_name_input.text())