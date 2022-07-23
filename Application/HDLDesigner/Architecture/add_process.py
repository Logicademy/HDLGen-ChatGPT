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

class AddProcess(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("New Process")
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

        self.proc_name_label = QLabel("Process Name*")
        self.proc_name_label.setStyleSheet(WHITE_COLOR)
        self.proc_name_input = QLineEdit()

        self.in_sig_label = QLabel("Sensitivity List")
        self.in_sig_label.setFont(title_font)


        self.in_sig_layout = QVBoxLayout()
        self.in_sig_frame = QFrame()
        self.in_sig_list = QListWidget()
        self.in_sig_empty_info = QLabel("No Input Signals found!\nPlease add signal in the IO Ports")


        self.out_sig_header_layout = QHBoxLayout()
        self.out_sig_label = QLabel("Output Signals")
        self.out_sig_label.setFont(bold_font)
        self.val_label = QLabel("Default Value")
        self.val_label.setFont(bold_font)
        self.out_sig_empty_info = QLabel("No Output Signals found!\nPlease add signal in the IO Ports")
        self.out_sig_empty_info.setFixedSize(400, 300)
        self.list_div = QFrame()
        self.list_div.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129);}')
        self.list_div.setFixedHeight(1)

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

    def setup_ui(self):

        self.in_sig_layout.addWidget(self.in_sig_label, alignment=Qt.AlignTop)
        self.in_sig_layout.addItem(QSpacerItem(1, 10))
        self.in_sig_list.setFrameStyle(QFrame.NoFrame)
        # self.in_sig_layout.addWidget(self.in_sig_list)
        self.in_sig_frame.setStyleSheet(".QFrame{background-color: white; border-radius: 5px;}")
        self.in_sig_frame.setLayout(self.in_sig_layout)
        self.in_sig_frame.setFixedWidth(175)

        self.out_sig_header_layout.addItem(QSpacerItem(40, 1))
        self.out_sig_header_layout.addWidget(self.out_sig_label)
        self.out_sig_header_layout.addWidget(self.val_label)
        self.out_sig_header_layout.addItem(QSpacerItem(80, 1))

        self.out_sig_layout.addLayout(self.out_sig_header_layout)
        self.out_sig_layout.addWidget(self.list_div)
        self.out_sig_table.setFrameStyle(QFrame.NoFrame)
        self.out_sig_table.setColumnCount(4)
        self.out_sig_table.setShowGrid(False)
        self.out_sig_table.setColumnWidth(0, 1)
        self.out_sig_table.setColumnWidth(1, 100)
        self.out_sig_table.setColumnWidth(2, 100)
        self.out_sig_table.setColumnWidth(3, 60)
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

        self.input_layout.addWidget(self.proc_name_label, 0, 0, 1, 1)
        self.input_layout.addWidget(self.proc_name_input, 1, 0, 2, 1)
        self.input_layout.addWidget(self.in_sig_frame, 0, 2, 7, 2)
        self.input_layout.addWidget(self.out_sig_frame, 3, 0, 4, 2)

        self.input_layout.addItem(QSpacerItem(0, 50), 6, 0, 1, 3)
        self.input_layout.addWidget(self.cancel_btn, 7, 2, 1, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 7, 3, 1, 1, alignment=Qt.AlignRight)

        self.proc_name_input.textChanged.connect(self.enable_ok_btn);
        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setFixedSize(550, 400)
        self.input_frame.setLayout(self.input_layout)

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
                        out_val_options = self.input_signals + self.internal_signals
                        out_val_options.insert(0, "Custom")
                        out_val_combo.addItems(out_val_options)
                        out_val_options.pop(0)

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

                    self.out_sig_layout.addWidget(self.out_sig_table)

                if len(self.internal_signals) != 0:

                    outputList_flag = 1

                    for signal in self.internal_signals:
                        checkbox = QCheckBox()
                        checkbox.setFixedWidth(45)

                        out_val_combo = QComboBox()
                        out_val_options = self.input_signals + self.internal_signals
                        out_val_options.insert(0, "Custom")
                        out_val_combo.addItems(out_val_options)
                        out_val_options.pop(0)

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

                    self.out_sig_layout.addWidget(self.out_sig_table)

                if outputList_flag == 0:

                        self.out_sig_layout.addWidget(self.out_sig_empty_info, alignment=Qt.AlignTop)

                return
        self.in_sig_layout.addWidget(self.in_sig_empty_info, alignment=Qt.AlignTop)
        self.out_sig_layout.addWidget(self.out_sig_empty_info, alignment=Qt.AlignTop)

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
        data.append(self.proc_name_input.text())


        for i in range(self.in_sig_list.count()):
            if self.in_sig_list.item(i).checkState() == Qt.Checked:
                in_sigs.append(self.in_sig_list.item(i).text())


        for i in range(self.out_sig_table.rowCount()):
            if self.out_sig_table.cellWidget(i, 0).checkState() == Qt.Checked:
                output = self.out_sig_table.item(i, 1).text()
                if self.out_sig_table.cellWidget(i, 2).currentText() == "Custom":
                    default_val = self.out_sig_table.cellWidget(i, 3).text()
                else:
                    default_val = self.out_sig_table.cellWidget(i, 2).currentText()

                out_sigs.append(output + "," + default_val)

        data.append(in_sigs)
        data.append(out_sigs)
        print(out_sigs)
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
