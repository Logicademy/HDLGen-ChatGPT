import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *

sys.path.append("../..")
from ProjectManager.project_manager import ProjectManager
from HDLDesigner.InternalSignal.add_int_sig import AddIntSignal

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"
ICONS_DIR = "../../Resources/icons/"

class InternalSignal(QWidget):
    def __init__(self, proj_dir):
        super().__init__()

        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)

        self.all_intSignals = []

        self.port_heading_layout = QHBoxLayout()
        self.intSig_action_layout = QVBoxLayout()
        self.intSig_list_layout = QVBoxLayout()
        self.instSig_list_title_layout = QHBoxLayout()

        self.mainLayout = QVBoxLayout()

        self.io_list_label = QLabel("Internal Signals")
        self.io_list_label.setFont(title_font)
        self.io_list_label.setStyleSheet(WHITE_COLOR)

        self.add_btn = QPushButton("Add Signal")
        self.add_btn.setFixedSize(80, 25)
        self.add_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}")


        self.save_signal_btn = QPushButton("Save")
        self.save_signal_btn.setFixedSize(60, 30)
        self.save_signal_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}")


        # Port list layout widgets
        self.name_label = QLabel("Name")
        self.name_label.setFont(bold_font)
        self.type_label = QLabel("Type")
        self.type_label.setFont(bold_font)
        self.description_label = QLabel("Description")
        self.description_label.setFont(bold_font)

        self.list_div = QFrame()
        self.list_div.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129);}')
        self.list_div.setFixedHeight(1)

        self.intSig_table = QTableWidget()


        self.intSig_list_frame = QFrame()
        self.intSig_action_frame = QFrame()


        self.setup_ui()

        if proj_dir != None:
            self.load_data(proj_dir)

    def setup_ui(self):

        # Port List section
        self.port_heading_layout.addWidget(self.io_list_label, alignment=Qt.AlignLeft)
        self.port_heading_layout.addWidget(self.add_btn, alignment=Qt.AlignRight)
        self.add_btn.clicked.connect(self.add_intSignal)

        self.name_label.setFixedWidth(90)
        self.type_label.setFixedWidth(50)
        self.description_label.setFixedWidth(155)

        self.instSig_list_title_layout.addWidget(self.name_label, alignment=Qt.AlignLeft)
        self.instSig_list_title_layout.addWidget(self.type_label, alignment=Qt.AlignLeft)
        self.instSig_list_title_layout.addWidget(self.description_label, alignment=Qt.AlignLeft)

        self.intSig_list_layout.setAlignment(Qt.AlignTop)
        self.intSig_list_layout.addLayout(self.instSig_list_title_layout)
        self.intSig_list_layout.addWidget(self.list_div)

        self.intSig_table.setColumnCount(4)
        self.intSig_table.setShowGrid(False)
        self.intSig_table.setColumnWidth(0, 95)
        self.intSig_table.setColumnWidth(1, 100)
        self.intSig_table.setColumnWidth(2, 105)
        self.intSig_table.setColumnWidth(3, 5)
        self.intSig_table.horizontalScrollMode()
        self.intSig_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.intSig_table.horizontalScrollBar().hide()
        header = self.intSig_table.horizontalHeader()
        header.hide()
        header = self.intSig_table.verticalHeader()
        header.hide()
        self.intSig_table.setFrameStyle(QFrame.NoFrame)
        self.intSig_list_layout.addWidget(self.intSig_table)


        self.intSig_list_frame.setFrameShape(QFrame.StyledPanel)
        self.intSig_list_frame.setStyleSheet('.QFrame{background-color: white; border-radius: 5px;}')
        self.intSig_list_frame.setFixedSize(380, 295)
        self.intSig_list_frame.setLayout(self.intSig_list_layout)

        self.intSig_action_layout.addLayout(self.port_heading_layout)
        self.intSig_action_layout.addSpacerItem(QSpacerItem(0, 5))
        self.intSig_action_layout.addWidget(self.intSig_list_frame, alignment=Qt.AlignCenter)
        self.intSig_action_layout.addSpacerItem(QSpacerItem(0, 5))
        self.intSig_action_layout.addWidget(self.save_signal_btn, alignment=Qt.AlignRight)

        self.save_signal_btn.clicked.connect(self.save_signals)

        self.intSig_action_frame.setFrameShape(QFrame.StyledPanel)
        self.intSig_action_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.intSig_action_frame.setFixedSize(400, 400)
        self.intSig_action_frame.setLayout(self.intSig_action_layout)


        self.mainLayout.addWidget(self.intSig_action_frame, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)

    def add_intSignal(self):
        add_intSig = AddIntSignal()
        add_intSig.exec_()

        if not add_intSig.cancelled:
            intSignal_data = add_intSig.get_data()
            self.all_intSignals.append(intSignal_data)

            print(intSignal_data)
            delete_btn = QPushButton()
            #delete_btn.setIcon(QIcon(ICONS_DIR + "delete.svg"))
            delete_btn.setIcon(self.style().standardIcon(QStyle.SP_TitleBarCloseButton))
            delete_btn.setFixedSize(45, 25)
            delete_btn.clicked.connect(self.delete_clicked)

            row_position = self.intSig_table.rowCount()
            self.intSig_table.insertRow(row_position)
            self.intSig_table.setRowHeight(row_position, 5)

            self.intSig_table.setItem(row_position, 0, QTableWidgetItem(intSignal_data[0]))
            self.intSig_table.setItem(row_position, 1, QTableWidgetItem(intSignal_data[1]))
            self.intSig_table.setItem(row_position, 2, QTableWidgetItem(intSignal_data[2]))
            self.intSig_table.setCellWidget(row_position, 3, delete_btn)

    def delete_clicked(self):
        button = self.sender()
        if button:
            row = self.intSig_table.indexAt(button.pos()).row()
            self.intSig_table.removeRow(row)
            self.all_intSignals.pop(row)

    def save_signals(self):

        xml_data_path = ProjectManager.get_xml_data_path()

        root = minidom.parse(xml_data_path)
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")

        new_intSigs = root.createElement('internalSignals')

        for signal in self.all_intSignals:
            signal_node = root.createElement('signal')

            name_node = root.createElement('name')
            name_node.appendChild(root.createTextNode(signal[0]))
            signal_node.appendChild(name_node)

            type_node = root.createElement('type')
            sig_type = signal[1]
            type_node.appendChild(root.createTextNode(sig_type))
            signal_node.appendChild(type_node)

            desc_node = root.createElement('description')
            desc_node.appendChild(root.createTextNode(signal[2]))
            signal_node.appendChild(desc_node)

            new_intSigs.appendChild(signal_node)

        hdlDesign[0].replaceChild(new_intSigs, hdlDesign[0].getElementsByTagName('internalSignals')[0])

        # converting the doc into a string in xml format
        xml_str = root.toprettyxml()
        xml_str = os.linesep.join([s for s in xml_str.splitlines() if s.strip()])
        # Writing xml file
        with open(xml_data_path, "w") as f:
            f.write(xml_str)

        print("Successfully saved all the signals!")


    def load_data(self, proj_dir):

        root = minidom.parse(proj_dir[0])
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")

        io_ports = hdlDesign[0].getElementsByTagName('internalSignals')
        signal_nodes = io_ports[0].getElementsByTagName('signal')

        for i in range(0, len(signal_nodes)):
            name = signal_nodes[i].getElementsByTagName('name')[0].firstChild.data
            type = signal_nodes[i].getElementsByTagName('type')[0].firstChild.data
            if len(signal_nodes[i].getElementsByTagName('description')) != 1:
                desc = signal_nodes[i].getElementsByTagName('description')[0].firstChild.data
            else:
                desc = ""

            loaded_sig_data = [
                name,
                type,
                desc
            ]

            delete_btn = QPushButton()
            delete_btn.setIcon(self.style().standardIcon(QStyle.SP_TitleBarCloseButton))
            # delete_btn.setStyleSheet("background-color: white; border-style: plain;")
            delete_btn.setFixedSize(45, 25)
            delete_btn.clicked.connect(self.delete_clicked)

            self.intSig_table.insertRow(i)
            self.intSig_table.setRowHeight(i, 5)

            self.intSig_table.setItem(i, 0, QTableWidgetItem(loaded_sig_data[0]))
            self.intSig_table.setItem(i, 1, QTableWidgetItem(loaded_sig_data[1]))
            self.intSig_table.setItem(i, 2, QTableWidgetItem(loaded_sig_data[2]))
            self.intSig_table.setCellWidget(i, 3, delete_btn)
            self.all_intSignals.append(loaded_sig_data)