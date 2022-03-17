import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from projectManager import ProjectManager

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"

class AddProcess(QDialog):

    def __init__(self, proj_dir):
        super().__init__()

        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)

        self.input_signals = []
        self.output_signals = []

        self.input_layout = QGridLayout()

        self.mainLayout = QVBoxLayout()

        self.proc_name_label = QLabel("Process Name*")
        self.proc_name_label.setStyleSheet(WHITE_COLOR)
        self.proc_name_input = QLineEdit()

        self.in_sig_label = QLabel("Input Signals")
        self.in_sig_label.setFont(title_font)
        self.out_sig_label = QLabel("Output Signals")
        self.out_sig_label.setFont(title_font)

        self.in_sig_layout = QVBoxLayout()
        self.in_sig_frame = QFrame()
        self.in_sig_list = QListWidget()
        self.in_sig_empty_info = QLabel("No Input Signals found!\nPlease add signal in the IO Ports")

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

        self.populate_input_signals(proj_dir)

    def setup_ui(self):

        self.in_sig_layout.addWidget(self.in_sig_label, alignment=Qt.AlignTop)
        self.in_sig_layout.addItem(QSpacerItem(1, 10))
        self.in_sig_list.setFrameStyle(QFrame.NoFrame)
        # self.in_sig_layout.addWidget(self.in_sig_list)
        self.in_sig_frame.setStyleSheet(".QFrame{background-color: white; border-radius: 5px;}")
        self.in_sig_frame.setLayout(self.in_sig_layout)
        self.in_sig_frame.setFixedWidth(175)


        self.out_sig_frame.setFrameStyle(QFrame.NoFrame)
        self.out_sig_frame.setStyleSheet(".QFrame{background-color: white; border-radius: 5px;}")
        self.out_sig_frame.setLayout(self.out_sig_layout)
        self.out_sig_frame.setFixedSize(275, 275)

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
        self.input_frame.setFixedSize(500, 400)
        self.input_frame.setLayout(self.input_layout)


        self.ok_btn.clicked.connect(self.get_data)
        self.cancel_btn.clicked.connect(self.cancel_selected)

        self.mainLayout.addWidget(self.input_frame, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)

    def populate_input_signals(self, proj_dir):

        if (proj_dir != None):
            root = minidom.parse(proj_dir[0])
            HDLGen = root.documentElement
            hdlDesign = HDLGen.getElementsByTagName("hdlDesign")

            io_ports = hdlDesign[0].getElementsByTagName('entityIOPorts')
            signal_nodes = io_ports[0].getElementsByTagName('signal')

            if len(signal_nodes) != 0:
                for i in range(0, len(signal_nodes)):
                    name = signal_nodes[i].getElementsByTagName('name')[0].firstChild.data
                    mode = signal_nodes[i].getElementsByTagName('mode')[0].firstChild.data

                    if mode == "in":
                        self.input_signals.append(name)
                    elif mode == "out":
                        self.output_signals.append(name)

                for signal in self.input_signals:
                    item = QListWidgetItem(signal)
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    item.setCheckState(Qt.Unchecked)
                    self.in_sig_list.addItem(item)

                    self.in_sig_layout.addWidget(self.in_sig_list)
                return
        self.in_sig_layout.addWidget(self.in_sig_empty_info, alignment=Qt.AlignTop)

    def cancel_selected(self):
        self.cancelled = True
        self.close()

    def enable_ok_btn(self):
        if self.proc_name_input.text() != "" and self.proc_name_input.text() != "":
            self.ok_btn.setEnabled(True)
        else:
            self.ok_btn.setEnabled(False)

    def get_data(self):

        data = []
        in_sigs = []
        data.append(self.proc_name_input.text())


        for i in range(self.in_sig_list.count()):
            if self.in_sig_list.item(i).checkState() == Qt.Checked:
                in_sigs.append(self.in_sig_list.item(i).text())

        data.append(in_sigs)

        self.cancelled = False
        self.close()
        return data
