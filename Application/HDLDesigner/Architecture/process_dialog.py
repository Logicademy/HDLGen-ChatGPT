import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import sys
sys.path.append("..")
from ProjectManager.project_manager import ProjectManager

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"

class ProcessDialog(QDialog):

    def __init__(self, add_or_edit, process_data = None):
        super().__init__()

        if add_or_edit == "add":
            self.setWindowTitle("New Process")
        elif add_or_edit == "edit":
            self.setWindowTitle("Edit Process")

        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)

        self.clkState = False
        self.rstState = False
        self.internal_signals = []
        self.input_signals = []
        self.output_signals = []

        self.input_layout = QGridLayout()

        self.mainLayout = QVBoxLayout()

        self.proc_name_label = QLabel("Process Name*")
        self.proc_name_label.setStyleSheet(WHITE_COLOR)
        self.proc_name_input = QLineEdit()

        self.in_sig_label = QLabel("Sensitivity List")
        self.in_sig_label.setFont(title_font)

        self.seq_checkBox = QCheckBox("Sequential")
        #self.seq_label = QLabel("Sequential")
        self.seq_checkBox.setStyleSheet(WHITE_COLOR)

        self.in_sig_layout = QVBoxLayout()
        self.in_sig_frame = QFrame()
        self.in_sig_list = QListWidget()
        self.in_sig_empty_info = QLabel("No Input Signals found!\nPlease add signal in Ports")

        self.suffix_label = QLabel("Suffix")
        self.suffix_label.setStyleSheet(WHITE_COLOR)
        self.suffix_input = QLineEdit()
        self.suffix_input.setFixedWidth(40)
        self.suffix_input.setEnabled(False)
        self.suffix_input.setText("_p")

        self.out_sig_header_layout = QHBoxLayout()
        self.out_sig_label = QLabel("Output Signals")
        self.out_sig_label.setFont(bold_font)
        self.val_label = QLabel("Default Value")
        self.val_label.setFont(bold_font)
        self.Binval_label = QLabel("Binary Value")
        self.Binval_label.setFont(bold_font)
        self.out_sig_empty_info = QLabel("No Output Signals found!\nPlease add signal in Ports")
        self.out_sig_empty_info.setFixedSize(400, 300)
        self.list_div = QFrame()
        self.list_div.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129);}')
        self.list_div.setFixedHeight(1)

        self.CSlist_div = QFrame()
        self.CSlist_div.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129);}')
        self.CSlist_div.setFixedHeight(1)

        self.CSNS_header_layout = QHBoxLayout()
        self.CSNS_label = QLabel("Assign signals")
        self.CSNS_label.setFont(bold_font)
        self.onRst_label = QLabel("on rst")
        self.onRst_label.setFont(bold_font)
        self.onClk_label = QLabel("on clk")
        self.onClk_label.setFont(bold_font)
        self.CSNS_empty_info = QLabel("No CS NS Signals found!\nPlease add signals in Internal Signals")
        self.CSNS_empty_info.setFixedSize(400, 300)
        self.CSNS_table = QTableWidget()
        self.CSNS_layout = QVBoxLayout()
        self.CSNS_frame = QFrame()
        self.out_sig_table = QTableWidget()

        self.out_sig_layout = QVBoxLayout()
        self.out_sig_frame = QFrame()

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

        self.populate_signals(ProjectManager.get_xml_data_path())

        if add_or_edit == "edit" and process_data != None:
            self.load_process_data(process_data)

    def setup_ui(self):

        self.in_sig_layout.addWidget(self.in_sig_label, alignment=Qt.AlignTop)
        self.in_sig_layout.addItem(QSpacerItem(1, 10))
        self.in_sig_list.setFrameStyle(QFrame.NoFrame)
        self.in_sig_frame.setStyleSheet(".QFrame{background-color: white; border-radius: 5px;}")
        self.in_sig_frame.setLayout(self.in_sig_layout)
        self.in_sig_frame.setFixedWidth(175)

        self.out_sig_header_layout.addWidget(self.out_sig_label,alignment=Qt.AlignRight)
        self.out_sig_header_layout.addWidget(self.val_label,alignment=Qt.AlignRight)
        self.out_sig_header_layout.addWidget(self.Binval_label,alignment=Qt.AlignRight)

        self.out_sig_layout.addLayout(self.out_sig_header_layout)
        self.out_sig_layout.addWidget(self.list_div)
        self.out_sig_table.setFrameStyle(QFrame.NoFrame)
        self.out_sig_table.setColumnCount(4)
        self.out_sig_table.setShowGrid(False)
        self.out_sig_table.setColumnWidth(0, 1)
        self.out_sig_table.setColumnWidth(1, 80)
        self.out_sig_table.setColumnWidth(2, 90)
        self.out_sig_table.setColumnWidth(3, 90)
        self.out_sig_table.horizontalScrollMode()
        self.out_sig_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.out_sig_table.horizontalScrollBar().hide()
        header = self.out_sig_table.horizontalHeader()
        header.hide()
        header = self.out_sig_table.verticalHeader()
        header.hide()

        self.out_sig_frame.setFrameStyle(QFrame.NoFrame)
        self.out_sig_frame.setStyleSheet(".QFrame{background-color: white; border-radius: 5px;}")
        self.out_sig_frame.setLayout(self.out_sig_layout)
        self.out_sig_frame.setFixedSize(325, 275)

        self.CSNS_header_layout.addWidget(self.CSNS_label)
        self.CSNS_header_layout.addItem(QSpacerItem(50, 1))
        self.CSNS_header_layout.addWidget(self.onClk_label)
        self.CSNS_header_layout.addWidget(self.onRst_label)

        self.CSNS_layout.addLayout(self.CSNS_header_layout)
        self.CSNS_layout.addWidget(self.CSlist_div)
        self.CSNS_table.setFrameStyle(QFrame.NoFrame)
        self.CSNS_table.setColumnCount(4)
        self.CSNS_table.setShowGrid(False)
        self.CSNS_table.setColumnWidth(0, 1)
        self.CSNS_table.setColumnWidth(1, 80)
        self.CSNS_table.setColumnWidth(2, 80)
        self.CSNS_table.setColumnWidth(3, 80)
        self.CSNS_table.horizontalScrollMode()
        self.CSNS_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.CSNS_table.horizontalScrollBar().hide()
        header = self.CSNS_table.horizontalHeader()
        header.hide()
        header = self.CSNS_table.verticalHeader()
        header.hide()

        self.CSNS_frame.setFrameStyle(QFrame.NoFrame)
        self.CSNS_frame.setStyleSheet(".QFrame{background-color: white; border-radius: 5px;}")
        self.CSNS_frame.setLayout(self.CSNS_layout)
        self.CSNS_frame.setFixedSize(325, 275)
        self.CSNS_frame.hide()

        self.input_layout.addWidget(self.proc_name_label, 0, 0, 1, 1)
        self.input_layout.addWidget(self.proc_name_input, 1, 0, 1, 1)
        self.input_layout.addWidget(self.suffix_label, 0, 1, 1, 1)
        self.input_layout.addWidget(self.suffix_input, 1, 1, 1, 1)
        #self.input_layout.addWidget(self.seq_label, 0, 2, 1, 1)
        self.input_layout.addWidget(self.seq_checkBox, 1, 2, 1, 1, Qt.AlignCenter)
        self.input_layout.addWidget(self.in_sig_frame, 0, 3, 7, 2)
        self.input_layout.addWidget(self.out_sig_frame, 3, 0, 4, 2)
        self.input_layout.addWidget(self.CSNS_frame, 3, 0, 4, 2)

        self.input_layout.addItem(QSpacerItem(0, 50), 6, 0, 1, 3)
        self.input_layout.addWidget(self.cancel_btn, 7, 3, 1, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 7, 4, 1, 1, alignment=Qt.AlignRight)

        self.proc_name_input.textChanged.connect(self.enable_ok_btn);
        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setFixedSize(550, 400)
        self.input_frame.setLayout(self.input_layout)
        self.seq_checkBox.clicked.connect(self.seq_checked)
        self.ok_btn.clicked.connect(self.get_data)
        self.cancel_btn.clicked.connect(self.cancel_selected)

        self.mainLayout.addWidget(self.input_frame, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)

    def populate_signals(self, proj_dir):

        sensitivityList_flag = 0
        outputList_flag = 0

        if (proj_dir != None):
            root = minidom.parse(proj_dir)
            HDLGen = root.documentElement
            hdlDesign = HDLGen.getElementsByTagName("hdlDesign")

            io_ports = hdlDesign[0].getElementsByTagName('entityIOPorts')
            signal_nodes = io_ports[0].getElementsByTagName('signal')

            intSignals = hdlDesign[0].getElementsByTagName('internalSignals')
            intSignal_nodes = intSignals[0].getElementsByTagName('signal')

            clkAndRst = hdlDesign[0].getElementsByTagName('clkAndRst')
            if len(clkAndRst) != 1:
                self.clkState = True
                if clkAndRst[0].getElementsByTagName('rst')[0].firstChild.data == "Yes":
                    self.rstState = True

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

                if len(self.input_signals) != 0:

                    sensitivityList_flag = 1

                    for signal in self.input_signals:
                        item = QListWidgetItem(signal)
                        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                        item.setCheckState(Qt.Unchecked)
                        self.in_sig_list.addItem(item)

                        self.in_sig_layout.addWidget(self.in_sig_list)
                        self.seq_checkBox.setVisible(False)
                    if self.clkState == True:
                        self.seq_checkBox.setVisible(True)
                        self.in_sig_list.item(self.input_signals.index("clk")).setHidden(True)
                        if self.rstState == True:
                            self.in_sig_list.item(self.input_signals.index("rst")).setHidden(True)

                if len(self.internal_signals) != 0:

                    sensitivityList_flag = 1

                    for signal in self.internal_signals:
                        item = QListWidgetItem(signal)
                        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                        item.setCheckState(Qt.Unchecked)
                        self.in_sig_list.addItem(item)

                        self.in_sig_layout.addWidget(self.in_sig_list)

                if sensitivityList_flag == 0:

                    self.in_sig_layout.addWidget(self.in_sig_empty_info, alignment=Qt.AlignTop)


                if len(self.output_signals) != 0:

                    outputList_flag = 1

                    for signal in self.output_signals:
                        checkbox = QCheckBox()
                        checkbox.setFixedWidth(45)

                        out_val_combo = QComboBox()
                        out_val_options = self.input_signals + self.internal_signals #+ "select"
                        out_val_options.append("zero")
                        #out_val_options.append("Custom")
                        out_val_options.insert(0, "Custom")
                        #out_val_options.insert(1, "zero")
                        #out_val_options.insert(2, "one")
                        out_val_combo.addItems(out_val_options)
                        #out_val_options.pop(0)

                        out_val_combo.currentTextChanged.connect(self.disable_custom_input)
                        out_val_input = QLineEdit()
                        out_val_input.setFixedWidth(60)
                        out_val_input.setPlaceholderText("Eg. 1")

                        row_position = self.out_sig_table.rowCount()
                        self.out_sig_table.insertRow(row_position)
                        self.out_sig_table.setRowHeight(row_position, 5)

                        self.out_sig_table.setCellWidget(row_position, 0, checkbox)
                        self.out_sig_table.setItem(row_position, 1, QTableWidgetItem(signal))
                        self.out_sig_table.setCellWidget(row_position, 2, out_val_combo)
                        self.out_sig_table.setCellWidget(row_position, 3, out_val_input)

                        CScheckbox = QCheckBox()
                        CScheckbox.setFixedWidth(45)

                        CSout_val_combo = QComboBox()
                        CSout_val_options = self.input_signals + self.internal_signals #+ "select"
                        CSout_val_options.append("zero")
                        #CSout_val_options.append("Select")
                        CSout_val_options.insert(0, "Select")
                        CSout_val_combo.addItems(CSout_val_options)
                        #CSout_val_options.pop(0)

                        CSout_val_combo.currentTextChanged.connect(self.disable_custom_input)

                        onRst_val_combo = QComboBox()
                        onRst_val_options = self.input_signals + self.internal_signals #+ "select" + "zero"
                        onRst_val_options.append("zero")
                        #onRst_val_options.append("Select")
                        onRst_val_options.insert(0, "Select")
                        #onRst_val_options.insert(0, "zero")
                        onRst_val_combo.addItems(onRst_val_options)
                        #onRst_val_options.pop(0)

                        #onRst_val_combo.currentTextChanged.connect(self.disable_custom_input)
                        row_positionCSNS = self.CSNS_table.rowCount()
                        self.CSNS_table.insertRow(row_positionCSNS)
                        self.CSNS_table.setRowHeight(row_positionCSNS, 5)

                        self.CSNS_table.setCellWidget(row_positionCSNS, 0, CScheckbox)
                        self.CSNS_table.setItem(row_positionCSNS, 1, QTableWidgetItem(signal))
                        self.CSNS_table.setCellWidget(row_position, 2, CSout_val_combo)
                        self.CSNS_table.setCellWidget(row_position, 3, onRst_val_combo)

                    self.CSNS_layout.addWidget(self.CSNS_table)
                    self.out_sig_layout.addWidget(self.out_sig_table)
                if len(self.internal_signals) != 0:

                    outputList_flag = 1
                    for signal in self.internal_signals:

                        checkbox = QCheckBox()
                        checkbox.setFixedWidth(45)

                        out_val_combo = QComboBox()
                        out_val_options = self.input_signals + self.internal_signals
                        out_val_options.append("zero")
                        #out_val_options.append("Custom")
                        #out_val_options.insert(0, "zero")
                       # out_val_options.insert(0, "one")
                        out_val_options.insert(0, "Custom")
                        out_val_combo.addItems(out_val_options)
                        #out_val_options.pop(0)

                        out_val_combo.currentTextChanged.connect(self.disable_custom_input)
                        out_val_input = QLineEdit()
                        out_val_input.setFixedWidth(60)
                        out_val_input.setPlaceholderText("Eg. 1")

                        row_position = self.out_sig_table.rowCount()
                        self.out_sig_table.insertRow(row_position)
                        self.out_sig_table.setRowHeight(row_position, 5)

                        self.out_sig_table.setCellWidget(row_position, 0, checkbox)
                        self.out_sig_table.setItem(row_position, 1, QTableWidgetItem(signal))
                        self.out_sig_table.setCellWidget(row_position, 2, out_val_combo)
                        self.out_sig_table.setCellWidget(row_position, 3, out_val_input)
                        if signal[0:2] != "NS":
                            CScheckbox = QCheckBox()
                            CScheckbox.setFixedWidth(45)

                            CSout_val_combo = QComboBox()
                            CSout_val_options = self.input_signals + self.internal_signals
                            CSout_val_options.append("zero")
                            #CSout_val_options.append("Custom")
                            CSout_val_options.insert(0, "Select")
                            CSout_val_combo.addItems(CSout_val_options)
                            #CSout_val_options.pop(0)

                            CSout_val_combo.currentTextChanged.connect(self.disable_custom_input)

                            onRst_val_combo = QComboBox()
                            onRst_val_options = self.input_signals + self.internal_signals
                            onRst_val_options.append("zero")
                            #onRst_val_options.append("Custom")
                            #onRst_val_options.insert(0, "rst state")
                            #onRst_val_options.insert(0, "zero")
                            #onRst_val_options.insert(0, "one")
                            onRst_val_options.insert(0, "Select")
                            onRst_val_combo.addItems(onRst_val_options)
                            #onRst_val_options.pop(0)

                            onRst_val_combo.currentTextChanged.connect(self.disable_custom_input)
                            row_positionCSNS = self.CSNS_table.rowCount()
                            self.CSNS_table.insertRow(row_positionCSNS)
                            self.CSNS_table.setRowHeight(row_positionCSNS, 5)

                            self.CSNS_table.setCellWidget(row_positionCSNS, 0, CScheckbox)
                            self.CSNS_table.setItem(row_positionCSNS, 1, QTableWidgetItem(signal))
                            self.CSNS_table.setCellWidget(row_positionCSNS, 2, CSout_val_combo)
                            self.CSNS_table.setCellWidget(row_positionCSNS, 3, onRst_val_combo)
                        self.CSNS_layout.addWidget(self.CSNS_table)
                    self.out_sig_layout.addWidget(self.out_sig_table)
                if outputList_flag == 0:
                        self.out_sig_layout.addWidget(self.out_sig_empty_info, alignment=Qt.AlignTop)
                return

        self.in_sig_layout.addWidget(self.in_sig_empty_info, alignment=Qt.AlignTop)
        self.CSNS_layout.addWidget(self.CSNS_empty_info, alignment=Qt.AlignTop)
        self.out_sig_layout.addWidget(self.out_sig_empty_info, alignment=Qt.AlignTop)

    def seq_checked(self):
        if self.seq_checkBox.isChecked():
            self.CSNS_frame.show()
            self.out_sig_frame.hide()
            if self.clkState == True:
                for i in range(self.in_sig_list.count()):
                    self.in_sig_list.item(i).setHidden(True)
                self.in_sig_list.item(self.input_signals.index("clk")).setHidden(False)
                self.in_sig_list.item(self.input_signals.index("clk")).setCheckState(Qt.Checked)
                if self.rstState == True:
                    self.CSNS_table.showColumn(3)
                    self.in_sig_list.item(self.input_signals.index("rst")).setHidden(False)
                    self.in_sig_list.item(self.input_signals.index("rst")).setCheckState(Qt.Checked)
                else:
                    self.CSNS_table.hideColumn(3)
        else:
            self.CSNS_frame.hide()
            self.out_sig_frame.show()
            for i in range(self.in_sig_list.count()):
                self.in_sig_list.item(i).setHidden(False)
            if self.clkState == True:
                self.in_sig_list.item(self.input_signals.index("clk")).setHidden(True)
                if self.rstState == True:
                    self.in_sig_list.item(self.input_signals.index("rst")).setHidden(True)

    def load_process_data(self, process_data):

        self.proc_name_input.setText(process_data[1])
        for i in range(0, self.in_sig_list.count()):
            if self.in_sig_list.item(i).text() in process_data[2]:
                self.in_sig_list.item(i).setCheckState(Qt.Checked)
        out_sigs = []
        default_vals = []
        clk_default_vals = []
        for out_sig in process_data[3]:
            temp = out_sig.split(',')

            out_sigs.append(temp[0])
            default_vals.append(temp[1])
            if len(temp) == 3:
                clk_default_vals.append(temp[2])


        for i in range(0, self.out_sig_table.rowCount()):

            if self.out_sig_table.item(i, 1).text() in out_sigs:
                if not clk_default_vals:
                    self.out_sig_table.cellWidget(i, 0).setCheckState(Qt.Checked)
                    self.out_sig_table.cellWidget(i, 2).setCurrentText(default_vals[out_sigs.index(self.out_sig_table.item(i, 1).text())])
                    if self.out_sig_table.cellWidget(i, 2).currentText() == "Custom":
                        self.out_sig_table.cellWidget(i, 3).setText(default_vals[out_sigs.index(self.out_sig_table.item(i, 1).text())])

        for i in range(self.CSNS_table.rowCount()):
            if self.CSNS_table.item(i, 1).text() in out_sigs:
                if clk_default_vals:
                    self.seq_checkBox.setCheckState(Qt.Checked)
                    self.seq_checked()
                    self.CSNS_table.cellWidget(i, 0).setCheckState(Qt.Checked)
                    self.CSNS_table.cellWidget(i, 2).setCurrentText(clk_default_vals[out_sigs.index(self.CSNS_table.item(i, 1).text())])
                    self.CSNS_table.cellWidget(i, 3).setCurrentText(default_vals[out_sigs.index(self.CSNS_table.item(i, 1).text())])


    def cancel_selected(self):
        self.cancelled = True
        self.close()

    def enable_ok_btn(self):
        if self.proc_name_input.text() != "":
            self.ok_btn.setEnabled(True)
        else:
            self.ok_btn.setEnabled(False)

    def get_data(self):

        data = []
        in_sigs = []
        out_sigs = []
        CSNS_sigs = []
        processName = self.proc_name_input.text().strip().replace(" ", "")
        if processName[-2:] != "_p":
            processName=processName+"_p"
        data.append(processName)#self.proc_name_input.text())
        rstBoolean = False

        for i in range(self.in_sig_list.count()):
            if self.in_sig_list.item(i).checkState() == Qt.Checked:
                in_sigs.append(self.in_sig_list.item(i).text())
                if self.in_sig_list.item(i).text() == "rst":
                    rstBoolean = True


        for i in range(self.out_sig_table.rowCount()):
            if self.out_sig_table.cellWidget(i, 0).checkState() == Qt.Checked:
                output = self.out_sig_table.item(i, 1).text()
                if self.out_sig_table.cellWidget(i, 2).currentText() == "Custom":
                    default_val = self.out_sig_table.cellWidget(i, 3).text()
                else:
                    default_val = self.out_sig_table.cellWidget(i, 2).currentText()

                out_sigs.append(output + "," + default_val)

        for i in range(self.CSNS_table.rowCount()):
            if self.CSNS_table.cellWidget(i, 0).checkState() == Qt.Checked:
                output = self.CSNS_table.item(i, 1).text()
                rst_default_val = self.CSNS_table.cellWidget(i, 3).currentText()
                if rstBoolean == False:
                    rst_default_val = "N/A"
                clk_default_val = self.CSNS_table.cellWidget(i, 2).currentText()
                out_sigs.append(output + "," + rst_default_val + "," + clk_default_val)

        data.append(in_sigs)
        data.append(out_sigs)
        self.cancelled = False
        self.close()
        return data

    def disable_custom_input(self):
        combo = self.sender()

        if combo:
            row = self.out_sig_table.indexAt(combo.pos()).row()
            if combo.currentText() == "Custom":
                self.out_sig_table.cellWidget(row, 3).setEnabled(True)
                self.out_sig_table.cellWidget(row, 3).setPlaceholderText("Eg. 1")
            else:
                self.out_sig_table.cellWidget(row, 3).clear()
                self.out_sig_table.cellWidget(row, 3).setPlaceholderText("")
                self.out_sig_table.cellWidget(row, 3).setEnabled(False)