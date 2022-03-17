import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from projectManager import ProjectManager
from add_process import AddProcess

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"
ICONS_DIR = "./resources/icons/"

class Architecture(QWidget):

    def __init__(self, proj_dir):
        super().__init__()

        self.proj_dir = proj_dir
        self.all_data = []
        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)

        self.mainLayout = QVBoxLayout()

        self.top_layout = QGridLayout()
        self.arch_action_layout = QVBoxLayout()

        self.arch_name_input = QLineEdit()
        self.arch_name_label = QLabel("Architecture Name")
        self.arch_name_label.setStyleSheet(WHITE_COLOR)

        self.new_proc_btn = QPushButton("New process")
        self.new_proc_btn.setFixedSize(100, 25)
        self.new_proc_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 5px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 5px; border-style: plain;}")

        self.new_conc_btn = QPushButton("New Concurrent statement")
        self.new_conc_btn.setFixedSize(175, 25)
        self.new_conc_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 5px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 5px; border-style: plain;}")

        self.new_strg_btn = QPushButton("New StateReg")
        self.new_strg_btn.setFixedSize(100, 25)
        self.new_strg_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 5px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 5px; border-style: plain;}")

        self.save_btn = QPushButton("Save")
        self.save_btn.setFixedSize(100, 25)
        self.save_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 5px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 5px; border-style: plain;}")

        self.name_label = QLabel("Name")
        self.name_label.setFont(bold_font)
        self.type_label = QLabel("Type")
        self.type_label.setFont(bold_font)
        self.in_sig_label = QLabel("Input Signals")
        self.in_sig_label.setFont(bold_font)

        self.list_div = QFrame()
        self.list_div.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129);}')
        self.list_div.setFixedHeight(1)

        self.proc_table = QTableWidget()


        self.list_header_layout = QHBoxLayout()
        self.list_layout = QVBoxLayout()

        self.list_frame = QFrame()
        self.main_frame = QFrame()

        self.setup_ui()



    def setup_ui(self):

        self.top_layout.addWidget(self.arch_name_label, 0, 0, alignment=Qt.AlignLeft)
        self.top_layout.addWidget(self.arch_name_input, 1, 0)
        self.top_layout.addWidget(self.new_proc_btn, 1, 1)
        self.new_proc_btn.clicked.connect(self.add_proc)
        # self.top_layout.addWidget(self.new_conc_btn, 2, 0)
        # self.top_layout.addWidget(self.new_strg_btn, 2, 1)

        self.arch_action_layout.addLayout(self.top_layout)

        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.main_frame.setContentsMargins(5, 5, 5, 5)
        self.main_frame.setFixedSize(400, 400)
        self.main_frame.setLayout(self.arch_action_layout)

        self.name_label.setFixedWidth(100)
        self.list_header_layout.addWidget(self.name_label, alignment=Qt.AlignLeft)
        self.type_label.setFixedWidth(50)
        self.list_header_layout.addWidget(self.type_label, alignment=Qt.AlignLeft)
        self.list_header_layout.addWidget(self.in_sig_label, alignment=Qt.AlignLeft)
        self.list_header_layout.addItem(QSpacerItem(103, 1))
        self.list_layout.addLayout(self.list_header_layout)
        self.list_layout.addWidget(self.list_div)

        self.proc_table.setColumnCount(4)
        self.proc_table.setShowGrid(False)
        self.proc_table.setColumnWidth(0, 100)
        self.proc_table.setColumnWidth(1, 70)
        self.proc_table.setColumnWidth(2, 130)
        self.proc_table.setColumnWidth(3, 5)
        self.proc_table.horizontalScrollMode()
        self.proc_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.proc_table.horizontalScrollBar().hide()
        header = self.proc_table.horizontalHeader()
        header.hide()
        header = self.proc_table.verticalHeader()
        header.hide()
        self.proc_table.setFrameStyle(QFrame.NoFrame)
        self.list_layout.addWidget(self.proc_table)


        self.list_frame.setFrameShape(QFrame.StyledPanel)
        self.list_frame.setStyleSheet('.QFrame{background-color: white; border-radius: 5px;}')
        self.list_frame.setFixedSize(370, 275)
        self.list_frame.setLayout(self.list_layout)

        self.arch_action_layout.addItem(QSpacerItem(10, 5))
        self.arch_action_layout.addWidget(self.list_frame)
        self.arch_action_layout.addItem(QSpacerItem(10, 15))
        self.arch_action_layout.addWidget(self.save_btn, alignment=Qt.AlignRight)
        self.save_btn.clicked.connect(self.save_data)

        self.mainLayout.addWidget(self.main_frame)

        self.setLayout(self.mainLayout)

    def add_proc(self):
        add_proc = AddProcess(self.proj_dir)
        add_proc.exec_()

        if not add_proc.cancelled:
            data = add_proc.get_data()
            self.all_data.append(data)
            print(data)

            delete_btn = QPushButton()
            # delete_btn.setIcon(QIcon(ICONS_DIR + "delete.svg"))
            delete_btn.setIcon(self.style().standardIcon(QStyle.SP_TitleBarCloseButton))
            delete_btn.setFixedSize(45, 25)
            delete_btn.clicked.connect(self.delete_clicked)

            row_position = self.proc_table.rowCount()
            self.proc_table.insertRow(row_position)
            self.proc_table.setRowHeight(row_position, 5)

            self.proc_table.setItem(row_position, 0, QTableWidgetItem(data[0]))


            self.proc_table.setItem(row_position, 1, QTableWidgetItem("Process"))
            input_signals = ""
            for in_sig in data[1]:
                input_signals = input_signals + ", " + in_sig

            input_signals = input_signals[1:]

            self.proc_table.setItem(row_position, 2, QTableWidgetItem(input_signals))
            self.proc_table.setCellWidget(row_position, 3, delete_btn)

    def delete_clicked(self):
        button = self.sender()
        if button:
            row = self.proc_table.indexAt(button.pos()).row()
            self.proc_table.removeRow(row)
            self.all_data.pop(row)

    def save_data(self):

        xml_data_path = ProjectManager.get_xml_data_path()

        root = minidom.parse(xml_data_path)
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
        new_arch_node = root.createElement("architecture")

        arch_name = root.createElement("archName")
        arch_name.appendChild(root.createTextNode(self.arch_name_input.text()))
        new_arch_node.appendChild(arch_name)


        for data in self.all_data:
            process_node = root.createElement("process")
            label_node = root.createElement("label")
            label_node.appendChild(root.createTextNode(data[0]))
            process_node.appendChild(label_node)

            for input_signal in data[1]:
                in_sig_node = root.createElement("inputSignal")
                in_sig_node.appendChild(root.createTextNode(input_signal))
                process_node.appendChild(in_sig_node)

            for output_signal in data[2]:
                out_sig_node = root.createElement("defaultOutput")
                out_sig_node.appendChild(root.createTextNode(output_signal))
                process_node.appendChild(out_sig_node)

            new_arch_node.appendChild(process_node)


        hdlDesign[0].replaceChild(new_arch_node, hdlDesign[0].getElementsByTagName("architecture")[0])
        # converting the doc into a string in xml format
        xml_str = root.toprettyxml()
        xml_str = os.linesep.join([s for s in xml_str.splitlines() if s.strip()])
        # Writing xml file
        with open(xml_data_path, "w") as f:
            f.write(xml_str)

        print("Successfully saved all the signals!")