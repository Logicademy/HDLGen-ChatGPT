import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import qtawesome as qta

sys.path.append("..")
from ProjectManager.project_manager import ProjectManager
from HDLDesigner.IOPorts.io_port_dialog import IOPortDialog
from HDLDesigner.IOPorts.sequential_dialog import seqDialog

from HDLDesigner.Architecture.architecture import Architecture

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"
ICONS_DIR = "../../Resources/icons/"

class IOPorts(QWidget):

    def __init__(self, proj_dir):
        super().__init__()

        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)

        self.all_signals = []
        self.all_signals_names = []
        self.clkAndRst = []

        self.port_heading_layout = QHBoxLayout()
        self.port_action_layout = QVBoxLayout()
        self.port_list_layout = QVBoxLayout()
        self.port_list_title_layout = QHBoxLayout()

        self.mainLayout = QVBoxLayout()

        self.io_list_label = QLabel("Ports")
        self.io_list_label.setFont(title_font)
        self.io_list_label.setStyleSheet(WHITE_COLOR)
        self.comb_checkBox = QCheckBox("Combinational")
        self.comb_checkBox.setStyleSheet(WHITE_COLOR)
        self.seqSytle_checkBox = QCheckBox("RTL")
        self.seqSytle_checkBox.setStyleSheet(WHITE_COLOR)
        self.seqSytle_editbtn = QPushButton("Set up clk/rst")
        self.seqSytle_editbtn.setFixedSize(80, 25)
        self.seqSytle_editbtn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}")
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
        self.proj_dir_value = proj_dir
        if proj_dir != None:
            self.load_data(proj_dir)
        else:
            self.comb_checkBox.setChecked(True)

    def setup_ui(self):
        bold_font = QFont()
        bold_font.setBold(True)
        # Port List section
        self.port_heading_layout.addWidget(self.io_list_label, alignment=Qt.AlignLeft)
        self.port_heading_layout.addWidget(self.comb_checkBox, alignment=Qt.AlignLeft)
        self.port_heading_layout.addWidget(self.seqSytle_checkBox, alignment=Qt.AlignCenter)
        self.port_heading_layout.addWidget(self.seqSytle_editbtn)
        self.port_heading_layout.addWidget(self.add_btn, alignment=Qt.AlignRight)
        self.seqSytle_editbtn.setVisible(False)
        self.comb_checkBox.clicked.connect(self.checkBox_clicked)
        self.seqSytle_checkBox.clicked.connect(self.checkBox_clicked)
        self.seqSytle_editbtn.clicked.connect(self.edit_RTL)
        self.add_btn.clicked.connect(self.add_signal)

        #self.port_list_title_layout.addWidget(self.name_label, 2, alignment=Qt.AlignLeft)
        #self.port_list_title_layout.addWidget(self.mode_label, 2, alignment=Qt.AlignLeft)
        #self.port_list_title_layout.addWidget(self.type_label, 2, alignment=Qt.AlignLeft)
        #self.port_list_title_layout.addWidget(self.size_label, 2, alignment=Qt.AlignLeft)
        #self.port_list_title_layout.addSpacerItem(QSpacerItem(40, 1))
        #self.port_list_title_layout.addSpacerItem(QSpacerItem(40, 1))

        self.port_list_layout.setAlignment(Qt.AlignTop)
        #self.port_list_layout.addLayout(self.port_list_title_layout)
        #self.port_list_layout.addWidget(self.list_div)

        self.port_table.setColumnCount(6)
        self.port_table.setShowGrid(False)
        self.port_table.setHorizontalHeaderLabels(['Name', 'Mode', ' Type', 'Size', '', ''])
        header = self.port_table.horizontalHeader()
        header.setSectionsClickable(False)
        header.setSectionsMovable(False)
        self.port_table.horizontalHeader().setFont(bold_font)
        self.port_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.port_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.port_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.port_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        #self.port_table.setColumnWidth(0, 80)
        #self.port_table.setColumnWidth(1, 80)
        #self.port_table.setColumnWidth(2, 80)
        #self.port_table.setColumnWidth(3, 5)
        self.port_table.setColumnWidth(4, 10)
        self.port_table.setColumnWidth(5, 10)
        #self.port_table.horizontalScrollMode()
        self.port_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #self.port_table.horizontalScrollBar().hide()
       # header = self.port_table.horizontalHeader()
        #header.hide()
        vert = self.port_table.verticalHeader()
        vert.hide()
        self.port_table.setFrameStyle(QFrame.NoFrame)
        self.port_list_layout.addWidget(self.port_table)


        self.port_list_frame.setFrameShape(QFrame.StyledPanel)
        self.port_list_frame.setStyleSheet('.QFrame{background-color: white; border-radius: 5px;}')
       # self.port_list_frame.setFixedSize(420, 300)
        self.port_list_frame.setLayout(self.port_list_layout)

        self.port_action_layout.addLayout(self.port_heading_layout)
        self.port_action_layout.addSpacerItem(QSpacerItem(0, 5))
        self.port_action_layout.addWidget(self.port_list_frame)#, alignment=Qt.AlignCenter)
        self.port_action_layout.addSpacerItem(QSpacerItem(0, 5))
        self.port_action_layout.addWidget(self.save_signal_btn, alignment=Qt.AlignRight)

        self.save_signal_btn.clicked.connect(self.save_signals)

        self.port_action_frame.setFrameShape(QFrame.StyledPanel)
        self.port_action_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        #self.port_action_frame.setFixedSize(500, 400)#410
        self.port_action_frame.setLayout(self.port_action_layout)


        self.mainLayout.addWidget(self.port_action_frame)#, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)

    def update_clk_rst_btn(self):
        self.seqSytle_editbtn.setText("Edit clk/rst")
    def edit_RTL(self):
        seq_dialog = seqDialog(self.proj_dir_value)
        seq_dialog.exec_()

        if not seq_dialog.cancelled:
            self.clkAndRst = []
            if "clk" in self.all_signals_names:
                self.port_table.removeRow(self.all_signals_names.index("clk"))
                self.all_signals.pop(self.all_signals_names.index("clk"))
                self.all_signals_names.pop(self.all_signals_names.index("clk"))
            if "rst" in self.all_signals_names:
                self.port_table.removeRow(self.all_signals_names.index("rst"))
                self.all_signals.pop(self.all_signals_names.index("rst"))
                self.all_signals_names.pop(self.all_signals_names.index("rst"))
            clkAndRst_data = seq_dialog.get_clkAndRst()
            self.clkAndRst.append(clkAndRst_data)
            clk_details = ["clk","Input","single bit","1","clk signal"]
            self.all_signals.append(clk_details)
            self.all_signals_names.append(("clk"))
            row_position = self.port_table.rowCount()
            delete_btn = QPushButton()
            delete_btn.setIcon(qta.icon("mdi.delete"))
            delete_btn.setFixedSize(35, 22)
            delete_btn.clicked.connect(self.delete_clicked)

            edit_btn = QPushButton()
            edit_btn.setIcon(qta.icon("mdi.pencil"))
            edit_btn.setFixedSize(35, 22)
            edit_btn.clicked.connect(self.edit_io_port)

            self.port_table.insertRow(row_position)
            self.port_table.setRowHeight(row_position, 5)
            size = QTableWidgetItem("1")
            size.setTextAlignment(Qt.AlignHCenter)
            self.port_table.setItem(row_position, 0, QTableWidgetItem("clk"))
            self.port_table.setItem(row_position, 1, QTableWidgetItem("Input"))
            self.port_table.setItem(row_position, 2, QTableWidgetItem("single bit"))
            self.port_table.setItem(row_position, 3, size)

            if clkAndRst_data[1] == "Yes":
                row_position = self.port_table.rowCount()
                self.port_table.insertRow(row_position)
                self.port_table.setRowHeight(row_position, 5)
                size = QTableWidgetItem("1")
                size.setTextAlignment(Qt.AlignHCenter)
                self.port_table.setItem(row_position, 0, QTableWidgetItem("rst"))
                self.port_table.setItem(row_position, 1, QTableWidgetItem("Input"))
                self.port_table.setItem(row_position, 2, QTableWidgetItem("single bit"))
                self.port_table.setItem(row_position, 3, size)
                rst_details = ["rst", "Input", "single bit", "1", "rst signal"]
                self.all_signals.append(rst_details)
                self.all_signals_names.append(("rst"))
            self.update_clk_rst_btn()


    def add_signal(self):

        io_dialog = IOPortDialog("add")
        io_dialog.exec_()

        if not io_dialog.cancelled:
            signal_data = io_dialog.get_signals()
            self.all_signals.append(signal_data)
            self.all_signals_names.append((signal_data[0]))
            delete_btn = QPushButton()
            delete_btn.setIcon(qta.icon("mdi.delete"))
            delete_btn.setFixedSize(35, 22)
            delete_btn.clicked.connect(self.delete_clicked)

            edit_btn = QPushButton()
            edit_btn.setIcon(qta.icon("mdi.pencil"))
            edit_btn.setFixedSize(35, 22)
            edit_btn.clicked.connect(self.edit_io_port)

            row_position = self.port_table.rowCount()
            self.port_table.insertRow(row_position)
            self.port_table.setRowHeight(row_position, 5)
            size = QTableWidgetItem(signal_data[3] if signal_data[3] != "null" else "1")
            size.setTextAlignment(Qt.AlignHCenter)
            self.port_table.setItem(row_position, 0, QTableWidgetItem(signal_data[0]))
            self.port_table.setItem(row_position, 1, QTableWidgetItem(signal_data[1]))
            self.port_table.setItem(row_position, 2, QTableWidgetItem(signal_data[2]))
            self.port_table.setItem(row_position, 3, size)
            self.port_table.setCellWidget(row_position, 4, edit_btn)
            self.port_table.setCellWidget(row_position, 5, delete_btn)

    def delete_clicked(self):
        button = self.sender()
        if button:
            row = self.port_table.indexAt(button.pos()).row()
            self.port_table.removeRow(row)
            self.all_signals.pop(row)
            self.all_signals_names.pop(row)

    def checkBox_clicked(self):
        button = self.sender()
        if button == self.seqSytle_checkBox:
            if button.isChecked():
                self.clkAndRst = []
                self.seqSytle_editbtn.setVisible(True)
                self.comb_checkBox.setChecked(False)
            else:
                self.comb_checkBox.setChecked(True)
                self.seqSytle_editbtn.setText("Set up clk/rst")
                if "clk" in self.all_signals_names:
                    self.port_table.removeRow(self.all_signals_names.index("clk"))
                    self.all_signals.pop(self.all_signals_names.index("clk"))
                    self.all_signals_names.pop(self.all_signals_names.index("clk"))
                if "rst" in self.all_signals_names:
                    self.port_table.removeRow(self.all_signals_names.index("rst"))
                    self.all_signals.pop(self.all_signals_names.index("rst"))
                    self.all_signals_names.pop(self.all_signals_names.index("rst"))
                self.seqSytle_editbtn.setVisible(False)
                self.clkAndRst = []
        else:
            if button.isChecked():
                self.seqSytle_checkBox.setChecked(False)
                self.seqSytle_editbtn.setText("Set up clk/rst")
                if "clk" in self.all_signals_names:
                    self.port_table.removeRow(self.all_signals_names.index("clk"))
                    self.all_signals.pop(self.all_signals_names.index("clk"))
                    self.all_signals_names.pop(self.all_signals_names.index("clk"))
                if "rst" in self.all_signals_names:
                    self.port_table.removeRow(self.all_signals_names.index("rst"))
                    self.all_signals.pop(self.all_signals_names.index("rst"))
                    self.all_signals_names.pop(self.all_signals_names.index("rst"))
                self.seqSytle_editbtn.setVisible(False)
                self.clkAndRst = []
            else:
                self.clkAndRst = []
                self.seqSytle_editbtn.setVisible(True)
                self.seqSytle_checkBox.setChecked(True)



    def edit_io_port(self):
        button = self.sender()
        if button:
            row = self.port_table.indexAt(button.pos()).row()
            io_dialog = IOPortDialog("edit", self.all_signals[row])
            io_dialog.exec_()

            if not io_dialog.cancelled:
                signal_data = io_dialog.get_signals()
                self.port_table.removeRow(row)
                self.all_signals.pop(row)
                self.all_signals_names.pop(row)

                delete_btn = QPushButton()
                delete_btn.setIcon(qta.icon("mdi.delete"))
                delete_btn.setFixedSize(35, 22)
                delete_btn.clicked.connect(self.delete_clicked)

                edit_btn = QPushButton()
                edit_btn.setIcon(qta.icon("mdi.pencil"))
                edit_btn.setFixedSize(35, 22)
                edit_btn.clicked.connect(self.edit_io_port)

                self.all_signals.insert(row, signal_data)
                self.all_signals_names.insert(row, signal_data[0])
                self.port_table.insertRow(row)
                self.port_table.setRowHeight(row, 5)
                size = QTableWidgetItem(signal_data[3] if signal_data[3] != "null" else "1")
                size.setTextAlignment(Qt.AlignHCenter)
                self.port_table.setItem(row, 0, QTableWidgetItem(signal_data[0]))
                self.port_table.setItem(row, 1, QTableWidgetItem(signal_data[1]))
                self.port_table.setItem(row, 2, QTableWidgetItem(signal_data[2]))
                self.port_table.setItem(row, 3, size)
                self.port_table.setCellWidget(row, 4, edit_btn)
                self.port_table.setCellWidget(row, 5, delete_btn)
            else:
                self.all_signals[row][4]=self.all_signals[row][4].replace("\n", "&#10;")

    def save_signals(self):
        xml_data_path = ProjectManager.get_xml_data_path()

        root = minidom.parse(xml_data_path)
        HDLGen = root.documentElement
        new_Clk_rst = root.createElement('clkAndRst')
        clk_and_rst = root.createElement('clkAndRst')

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
            sig_size = ("(" + str(int(signal[3])-1) + " downto 0)") if signal[2] == "bus" else ""
            sig_type = signal[2] + sig_size
            type_node.appendChild(root.createTextNode(sig_type))
            signal_node.appendChild(type_node)

            desc_node = root.createElement('description')
            desc_node.appendChild(root.createTextNode(signal[4]))
            signal_node.appendChild(desc_node)

            new_io_ports.appendChild(signal_node)

        hdlDesign[0].replaceChild(new_io_ports, hdlDesign[0].getElementsByTagName('entityIOPorts')[0])
        for clkRst in self.clkAndRst:
            activeClkEdge_node = root.createElement('activeClkEdge')
            activeClkEdge_node.appendChild(root.createTextNode(str(clkRst[0])))
            clk_and_rst.appendChild(activeClkEdge_node)

            rst_node = root.createElement('rst')
            rst_node.appendChild(root.createTextNode(str(clkRst[1])))
            clk_and_rst.appendChild(rst_node)

            if len(clkRst) == 4:
                rstType_node = root.createElement('RstType')
                rstType_node.appendChild(root.createTextNode(str(clkRst[2])))
                clk_and_rst.appendChild(rstType_node)

                activeRstLvl_node = root.createElement('ActiveRstLvl')
                activeRstLvl_node.appendChild(root.createTextNode(str(clkRst[3])))
                clk_and_rst.appendChild(activeRstLvl_node)
            new_Clk_rst.appendChild(clk_and_rst)
        hdlDesign[0].replaceChild(new_Clk_rst, hdlDesign[0].getElementsByTagName('clkAndRst')[0])
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
        clkAndRst = hdlDesign[0].getElementsByTagName('clkAndRst')
        self.clkAndRst = []
        if len(clkAndRst) != 1:
            self.update_clk_rst_btn()
            self.seqSytle_checkBox.setCheckState(Qt.Checked)
            self.seqSytle_editbtn.setVisible(True)
            for i in range(0, len(clkAndRst)):
                if clkAndRst[i].getElementsByTagName('rst')[0].firstChild.data == "Yes":
                    clkAndRst_details = [clkAndRst[i].getElementsByTagName('activeClkEdge')[0].firstChild.data,
                                         clkAndRst[i].getElementsByTagName('rst')[0].firstChild.data,
                                         clkAndRst[i].getElementsByTagName('RstType')[0].firstChild.data,
                                         clkAndRst[i].getElementsByTagName('ActiveRstLvl')[0].firstChild.data
                                         ]
                else:
                    clkAndRst_details = [clkAndRst[i].getElementsByTagName('activeClkEdge')[0].firstChild.data,
                                         clkAndRst[i].getElementsByTagName('rst')[0].firstChild.data
                                         ]
            self.clkAndRst.append(clkAndRst_details)
        else:
            self.comb_checkBox.setCheckState(Qt.Checked)
        for i in range(0, len(signal_nodes)):
            name = signal_nodes[i].getElementsByTagName('name')[0].firstChild.data
            mode = signal_nodes[i].getElementsByTagName('mode')[0].firstChild.data
            port = signal_nodes[i].getElementsByTagName('type')[0].firstChild.data
            type = port[0:port.index("(")] if port.endswith(")") else port
            self.all_signals_names.append(name)
            desc = signal_nodes[i].getElementsByTagName('description')[0].firstChild.data
            if desc == "":
                desc = "To be Completed"

            loaded_sig_data = [
                name,
                "Input" if mode == "in" else "Output",
                type,
                "1" if type != "bus" else str(int(port[port.index("(") + 1:port.index(" downto")]) + 1),
                desc
            ]

            delete_btn = QPushButton()
            delete_btn.setIcon(qta.icon("mdi.delete"))
            delete_btn.setFixedSize(35, 22)
            delete_btn.clicked.connect(self.delete_clicked)

            edit_btn = QPushButton()
            edit_btn.setIcon(qta.icon("mdi.pencil"))
            edit_btn.setFixedSize(35, 22)
            edit_btn.clicked.connect(self.edit_io_port)

            self.port_table.insertRow(i)
            self.port_table.setRowHeight(i, 5)
            size = QTableWidgetItem(loaded_sig_data[3])
            size.setTextAlignment(Qt.AlignHCenter)
            self.port_table.setItem(i, 0, QTableWidgetItem(loaded_sig_data[0]))
            self.port_table.setItem(i, 1, QTableWidgetItem(loaded_sig_data[1]))
            self.port_table.setItem(i, 2, QTableWidgetItem(loaded_sig_data[2]))
            self.port_table.setItem(i, 3, size)
            self.port_table.setCellWidget(i, 4, edit_btn)
            self.port_table.setCellWidget(i, 5, delete_btn)
            self.all_signals.append(loaded_sig_data)