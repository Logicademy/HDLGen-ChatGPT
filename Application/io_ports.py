import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from projectManager import ProjectManager
from add_io_port import AddIO

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"
ICONS_DIR = "./resources/icons/"

class IOPorts(QWidget):

    def __init__(self, proj_dir):
        super().__init__()

        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)

        self.all_signals = []

        self.port_heading_layout = QHBoxLayout()
        self.port_action_layout = QVBoxLayout()
        self.port_list_layout = QVBoxLayout()
        self.port_list_title_layout = QHBoxLayout()

        self.mainLayout = QVBoxLayout()

        self.io_list_label = QLabel("Input/Output Ports")
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
        self.mode_label = QLabel("Mode")
        self.mode_label.setFont(bold_font)
        self.type_label = QLabel("Type")
        self.type_label.setFont(bold_font)
        self.size_label = QLabel("Size")
        self.size_label.setFont(bold_font)

        self.list_div = QFrame()
        self.list_div.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129);}')
        self.list_div.setFixedHeight(1)

        self.port_table = QTableWidget()


        self.port_list_frame = QFrame()
        self.port_action_frame = QFrame()


        self.setup_ui()

        if proj_dir != None:
            self.load_data(proj_dir)

    def setup_ui(self):

        # Port List section
        self.port_heading_layout.addWidget(self.io_list_label, alignment=Qt.AlignLeft)
        self.port_heading_layout.addWidget(self.add_btn, alignment=Qt.AlignRight)
        self.add_btn.clicked.connect(self.add_signal)

        self.name_label.setFixedWidth(102)
        self.mode_label.setFixedWidth(36)
        self.type_label.setFixedWidth(50)
        self.size_label.setFixedWidth(85)

        self.port_list_title_layout.addWidget(self.name_label, alignment=Qt.AlignLeft)
        self.port_list_title_layout.addWidget(self.mode_label, alignment=Qt.AlignLeft)
        self.port_list_title_layout.addWidget(self.type_label, alignment=Qt.AlignLeft)
        self.port_list_title_layout.addWidget(self.size_label, alignment=Qt.AlignLeft)

        self.port_list_layout.setAlignment(Qt.AlignTop)
        self.port_list_layout.addLayout(self.port_list_title_layout)
        self.port_list_layout.addWidget(self.list_div)

        self.port_table.setColumnCount(5)
        self.port_table.setShowGrid(False)
        self.port_table.setColumnWidth(0, 102)
        self.port_table.setColumnWidth(1, 55)
        self.port_table.setColumnWidth(2, 105)
        self.port_table.setColumnWidth(3, 1)
        self.port_table.setColumnWidth(4, 5)
        self.port_table.horizontalScrollMode()
        self.port_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.port_table.horizontalScrollBar().hide()
        header = self.port_table.horizontalHeader()
        header.hide()
        header = self.port_table.verticalHeader()
        header.hide()
        self.port_table.setFrameStyle(QFrame.NoFrame)
        self.port_list_layout.addWidget(self.port_table)


        self.port_list_frame.setFrameShape(QFrame.StyledPanel)
        self.port_list_frame.setStyleSheet('.QFrame{background-color: white; border-radius: 5px;}')
        self.port_list_frame.setFixedSize(370, 295)
        self.port_list_frame.setLayout(self.port_list_layout)

        self.port_action_layout.addLayout(self.port_heading_layout)
        self.port_action_layout.addSpacerItem(QSpacerItem(0, 5))
        self.port_action_layout.addWidget(self.port_list_frame, alignment=Qt.AlignCenter)
        self.port_action_layout.addSpacerItem(QSpacerItem(0, 5))
        self.port_action_layout.addWidget(self.save_signal_btn, alignment=Qt.AlignRight)

        self.save_signal_btn.clicked.connect(self.save_signals)

        self.port_action_frame.setFrameShape(QFrame.StyledPanel)
        self.port_action_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.port_action_frame.setContentsMargins(5, 5, 5, 5)
        self.port_action_frame.setFixedSize(400, 400)
        self.port_action_frame.setLayout(self.port_action_layout)


        self.mainLayout.addWidget(self.port_action_frame, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)


    def add_signal(self):

        add_io = AddIO()
        add_io.exec_()


        if not add_io.cancelled:
            signal_data = add_io.get_signals()
            self.all_signals.append(signal_data)

            print(signal_data)
            delete_btn = QPushButton()
            delete_btn.setIcon(QIcon(ICONS_DIR + "delete.svg"))
            delete_btn.setFixedSize(45, 25)
            delete_btn.clicked.connect(self.delete_clicked)

            row_position = self.port_table.rowCount()
            self.port_table.insertRow(row_position)
            self.port_table.setRowHeight(row_position, 5)

            self.port_table.setItem(row_position, 0, QTableWidgetItem(signal_data[0]))
            self.port_table.setItem(row_position, 1, QTableWidgetItem(signal_data[1]))
            self.port_table.setItem(row_position, 2, QTableWidgetItem(signal_data[2]))
            self.port_table.setItem(row_position, 3, QTableWidgetItem(signal_data[3] if signal_data[3] != "null" else "1"))
            self.port_table.setCellWidget(row_position, 4, delete_btn)

    def delete_clicked(self):
        button = self.sender()
        if button:
            row = self.port_table.indexAt(button.pos()).row()
            self.port_table.removeRow(row)
            self.all_signals.pop(row)

    def save_signals(self):

        proj_name = ProjectManager.get_proj_name()
        proj_path = os.path.join(ProjectManager.get_proj_dir(), proj_name)
        xml_data_path = os.path.join(proj_path, 'HDLGenPrj', proj_name + '.hdlgen')

        root = minidom.parse(xml_data_path)
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")

        new_io_ports = root.createElement('entityIOPorts')
        for signal in self.all_signals:
            signal_node = root.createElement('signal')

            name_node = root.createElement('name')
            name_node.appendChild(root.createTextNode(signal[0]))
            signal_node.appendChild(name_node)

            mode_node = root.createElement('mode')
            sig_mode = "in" if signal[1] == "Input" else "out"
            mode_node.appendChild(root.createTextNode(sig_mode))
            signal_node.appendChild(mode_node)

            type_node = root.createElement('type')
            sig_size = ("(" + signal[3] + " downto 0)") if signal[2] == "std_logic_vector" else ""
            sig_type = signal[2] + sig_size
            type_node.appendChild(root.createTextNode(sig_type))
            signal_node.appendChild(type_node)

            desc_node = root.createElement('description')
            desc_node.appendChild(root.createTextNode(signal[4]))
            signal_node.appendChild(desc_node)

            new_io_ports.appendChild(signal_node)

        hdlDesign[0].replaceChild(new_io_ports, hdlDesign[0].getElementsByTagName('entityIOPorts')[0])

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

        io_ports = hdlDesign[0].getElementsByTagName('entityIOPorts')
        signal_nodes = io_ports[0].getElementsByTagName('signal')

        for i in range(0, len(signal_nodes)):
            name = signal_nodes[i].getElementsByTagName('name')[0].firstChild.data
            mode = signal_nodes[i].getElementsByTagName('mode')[0].firstChild.data
            port = signal_nodes[i].getElementsByTagName('type')[0].firstChild.data
            type = port[0:port.index("(")] if port.endswith(")") else port
            if len(signal_nodes[i].getElementsByTagName('description')) != 1:
                desc = signal_nodes[i].getElementsByTagName('description')[0].firstChild.data
            else:
                desc = ""

            loaded_sig_data = [
                name,
                "Input" if mode == "in" else "Output",
                type,
                "1" if type != "std_logic_vector" else port[port.index("(") + 1:port.index(" downto")],
                desc
            ]

            delete_btn = QPushButton()
            delete_btn.setIcon(QIcon(ICONS_DIR + "delete.svg"))
            # delete_btn.setStyleSheet("background-color: white; border-style: plain;")
            delete_btn.setFixedSize(45, 25)
            delete_btn.clicked.connect(self.delete_clicked)

            self.port_table.insertRow(i)
            self.port_table.setRowHeight(i, 5)

            self.port_table.setItem(i, 0, QTableWidgetItem(loaded_sig_data[0]))
            self.port_table.setItem(i, 1, QTableWidgetItem(loaded_sig_data[1]))
            self.port_table.setItem(i, 2, QTableWidgetItem(loaded_sig_data[2]))
            self.port_table.setItem(i, 3, QTableWidgetItem(loaded_sig_data[3]))
            self.port_table.setCellWidget(i, 4, delete_btn)
            self.all_signals.append(loaded_sig_data)
