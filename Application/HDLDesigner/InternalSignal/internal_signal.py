import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import qtawesome as qta

sys.path.append("../..")
from ProjectManager.project_manager import ProjectManager
from HDLDesigner.InternalSignal.int_sig_dialog import IntSignalDialog
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
        self.stateTypes_names = []

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
        self.size_label = QLabel("Size")
        self.size_label.setFont(bold_font)

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

        self.name_label.setFixedWidth(115)
        self.type_label.setFixedWidth(105)
        self.size_label.setFixedWidth(145)

        self.instSig_list_title_layout.addWidget(self.name_label, alignment=Qt.AlignLeft)
        self.instSig_list_title_layout.addWidget(self.type_label, alignment=Qt.AlignLeft)
        self.instSig_list_title_layout.addWidget(self.size_label, alignment=Qt.AlignLeft)

        self.intSig_list_layout.setAlignment(Qt.AlignTop)
        self.intSig_list_layout.addLayout(self.instSig_list_title_layout)
        self.intSig_list_layout.addWidget(self.list_div)

        self.intSig_table.setColumnCount(5)
        self.intSig_table.setShowGrid(False)
        self.intSig_table.setColumnWidth(0, 100)
        self.intSig_table.setColumnWidth(1, 110)
        self.intSig_table.setColumnWidth(2, 50)
        self.intSig_table.setColumnWidth(3, 1)
        self.intSig_table.setColumnWidth(4, 1)
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
        self.intSig_list_frame.setFixedSize(420, 300)#380, 295)
        self.intSig_list_frame.setLayout(self.intSig_list_layout)

        self.intSig_action_layout.addLayout(self.port_heading_layout)
        self.intSig_action_layout.addSpacerItem(QSpacerItem(0, 5))
        self.intSig_action_layout.addWidget(self.intSig_list_frame, alignment=Qt.AlignCenter)
        self.intSig_action_layout.addSpacerItem(QSpacerItem(0, 5))
        self.intSig_action_layout.addWidget(self.save_signal_btn, alignment=Qt.AlignRight)

        self.save_signal_btn.clicked.connect(self.save_signals)

        self.intSig_action_frame.setFrameShape(QFrame.StyledPanel)
        self.intSig_action_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.intSig_action_frame.setFixedSize(500, 400)#400, 400
        self.intSig_action_frame.setLayout(self.intSig_action_layout)


        self.mainLayout.addWidget(self.intSig_action_frame, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)

    def add_intSignal(self):
        add_intSig = IntSignalDialog("add")
        add_intSig.exec_()

        if not add_intSig.cancelled:
            intSignal_data = add_intSig.get_data()
            CSIntSignal_data = add_intSig.get_data()
            CSIntSignal_data[0] = "CS" + CSIntSignal_data[0]

            if intSignal_data[1] == "std_logic_vector state signals" or intSignal_data[1] == "Enumerated type state signals":
                i = 2
            else:
                i = 1
            print("Entering while loop " + str(self.all_intSignals))
            while i > 0:
                delete_btn = QPushButton()
                delete_btn.setIcon(qta.icon("mdi.delete"))
                delete_btn.setFixedSize(35, 22)
                delete_btn.clicked.connect(self.delete_clicked)

                edit_btn = QPushButton()
                edit_btn.setIcon(qta.icon("mdi.pencil"))
                edit_btn.setFixedSize(35, 22)
                edit_btn.clicked.connect(self.edit_intSign)

                row_position = self.intSig_table.rowCount()
                self.intSig_table.insertRow(row_position)
                self.intSig_table.setRowHeight(row_position, 5)

                self.intSig_table.setItem(row_position, 1, QTableWidgetItem(intSignal_data[1]))
                if type(intSignal_data[2]) is list:
                    print("test3")
                    print(type(intSignal_data[2]))
                    intSignal_data[2] = str(intSignal_data[2])
                    #intSignal_data[2] = ""
                    #for state in intSignal_data[2]:
                    #    print("test2")
                    #    intSignal_data[2] = state
                print(intSignal_data[2])
                self.intSig_table.setItem(row_position, 2, QTableWidgetItem(intSignal_data[2]))
                self.intSig_table.setCellWidget(row_position, 3, edit_btn)
                self.intSig_table.setCellWidget(row_position, 4, delete_btn)
                if intSignal_data[1] == "std_logic_vector state signals" or intSignal_data[1] == "Enumerated type state signals":
                    if (i == 2) :
                        self.intSig_table.removeCellWidget(row_position, 3)
                        self.intSig_table.removeCellWidget(row_position, 4)
                        intSignal_data[0] = "NS" + intSignal_data[0]
                        add_intSig.makeIdeal()
                        if intSignal_data[1] == "Enumerated type state signals":
                            self.stateTypes_names = add_intSig.get_stateTypes()
                        self.all_intSignals.append(intSignal_data)
                        self.intSig_table.setItem(row_position, 0, QTableWidgetItem(intSignal_data[0]))
                    else:
                        self.all_intSignals.append(CSIntSignal_data)
                        self.intSig_table.setItem(row_position, 0, QTableWidgetItem(CSIntSignal_data[0]))
                else:
                    self.all_intSignals.append(intSignal_data)
                    self.intSig_table.setItem(row_position, 0, QTableWidgetItem(intSignal_data[0]))
                i=i-1
    def edit_intSign(self):
        button = self.sender()
        if button:
            row = self.intSig_table.indexAt(button.pos()).row()
            rowBefore = row - 1
            add_intSig = IntSignalDialog("edit", self.all_intSignals[row])
            add_intSig.exec_()
        if not add_intSig.cancelled:
            intSignal_data = add_intSig.get_data()
            CSIntSignal_data = add_intSig.get_data()
            self.intSig_table.removeRow(row)
            self.all_intSignals.pop(row)
            CSIntSignal_data[0] = "CS" + CSIntSignal_data[0]

            if intSignal_data[1] == "std_logic_vector state signals" or intSignal_data[1] == "Enumerated type state signals":
                i = 2
                print("NS row removed")
                self.intSig_table.removeRow(rowBefore)
                self.all_intSignals.pop(rowBefore)
            else:
                i = 1
            print("Entering while loop " + str(self.all_intSignals))
            while i > 0:
                delete_btn = QPushButton()
                delete_btn.setIcon(qta.icon("mdi.delete"))
                delete_btn.setFixedSize(35, 22)
                delete_btn.clicked.connect(self.delete_clicked)

                edit_btn = QPushButton()
                edit_btn.setIcon(qta.icon("mdi.pencil"))
                edit_btn.setFixedSize(35, 22)
                edit_btn.clicked.connect(self.edit_intSign)

                row_position = self.intSig_table.rowCount()
                self.intSig_table.insertRow(row_position)
                self.intSig_table.setRowHeight(row_position, 5)

                self.intSig_table.setItem(row_position, 1, QTableWidgetItem(intSignal_data[1]))
                if type(intSignal_data[2]) is list:
                    print("test3")
                    print(type(intSignal_data[2]))
                    intSignal_data[2] = str(intSignal_data[2])
                print(intSignal_data[2])
                self.intSig_table.setItem(row_position, 2, QTableWidgetItem(intSignal_data[2]))
                self.intSig_table.setCellWidget(row_position, 3, edit_btn)
                self.intSig_table.setCellWidget(row_position, 4, delete_btn)
                if intSignal_data[1] == "std_logic_vector state signals" or intSignal_data[1] == "Enumerated type state signals":
                    if (i == 2) :
                        self.intSig_table.removeCellWidget(row_position, 3)
                        self.intSig_table.removeCellWidget(row_position, 4)
                        intSignal_data[0] = "NS" + intSignal_data[0]
                        add_intSig.makeIdeal()
                        if intSignal_data[1] == "Enumerated type state signals":
                            self.stateTypes_names = add_intSig.get_stateTypes()
                        self.all_intSignals.append(intSignal_data)
                        self.intSig_table.setItem(row_position, 0, QTableWidgetItem(intSignal_data[0]))
                    else:
                        self.all_intSignals.append(CSIntSignal_data)
                        self.intSig_table.setItem(row_position, 0, QTableWidgetItem(CSIntSignal_data[0]))
                else:
                    self.all_intSignals.append(intSignal_data)
                    self.intSig_table.setItem(row_position, 0, QTableWidgetItem(intSignal_data[0]))
                i=i-1




    def delete_clicked(self):
        button = self.sender()
        if button:
            row = self.intSig_table.indexAt(button.pos()).row()
            rowBefore = row -1
            print("deleting")
            if str(self.all_intSignals[row][1]) == "Enumerated type state signals":
                self.stateTypes_names = []
            if str(self.all_intSignals[row][1]) == "Enumerated type state signals" or str(self.all_intSignals[row][1]) == "std_logic_vector state signals":
                print("deleting row before")
                self.intSig_table.removeRow(row)
                self.all_intSignals.pop(row)
                self.all_intSignals.pop(rowBefore)
                self.intSig_table.removeRow(rowBefore)

            else:
                print("deleting row")
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
            if signal[1] == "std_logic":
                sig_type = "std_logic"
            elif signal[1] == "Enumerated type state signals":
                sig_type = "Enumerated type state signals"
            elif signal[1] == "array":
                sig_type = signal[2]
            else:
                sig_size = ("(" + str(int(signal[2]) - 1) + " downto 0)")
                sig_type = "std_logic_vector" + sig_size
            type_node.appendChild(root.createTextNode(sig_type))
            signal_node.appendChild(type_node)

            desc_node = root.createElement('description')
            desc_node.appendChild(root.createTextNode(signal[3]))
            signal_node.appendChild(desc_node)

            new_intSigs.appendChild(signal_node)

        for states in self.stateTypes_names:
            stateTypes_nodes = root.createElement('stateTypes')
            stateTypes_nodes.appendChild(root.createTextNode(states))
            new_intSigs.appendChild(stateTypes_nodes)
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
            self.intSig_table.insertRow(i)
            self.intSig_table.setRowHeight(i, 5)
            delete_btn = QPushButton()
            delete_btn.setIcon(qta.icon("mdi.delete"))
            delete_btn.setFixedSize(35, 22)
            delete_btn.clicked.connect(self.delete_clicked)

            edit_btn = QPushButton()
            edit_btn.setIcon(qta.icon("mdi.pencil"))
            edit_btn.setFixedSize(35, 22)
            edit_btn.clicked.connect(self.edit_intSign)

            self.intSig_table.setCellWidget(i, 3, edit_btn)
            self.intSig_table.setCellWidget(i, 4, delete_btn)
            name = signal_nodes[i].getElementsByTagName('name')[0].firstChild.data
            signal = signal_nodes[i].getElementsByTagName('type')[0].firstChild.data
            value = "1"
            if signal == "Enumerated type state signals":
                type = signal
                if name[:2] == "NS":
                    self.intSig_table.removeCellWidget(i, 3)
                    self.intSig_table.removeCellWidget(i, 4)
            elif signal[0:5] == "array":
                type=signal.split(",")
                print(type)
                value = type[0]+","+type[1] + "," + type[2]
                type=type[0]
            else:
                type = signal[0:signal.index("(")] if signal.endswith(")") else signal
            desc = signal_nodes[i].getElementsByTagName('description')[0].firstChild.data
            if type == "std_logic_vector":
                value = str(int(signal[signal.index("(") + 1:signal.index(" downto")]) + 1)
            #elif type == "array":
            #    value = type[1]+","+type[2]
            #    print("this is array value")
             #   print(value)
            elif type == "Enumerated type state signals":
                stateTypesList = []
                for stateType in io_ports[0].getElementsByTagName("stateTypes"):
                    stateTypesList.append(stateType.firstChild.data)
                self.stateTypes_names = stateTypesList
                value = ' '.join(stateTypesList)

            loaded_sig_data = [
                name,
                type,
                value,
                #"1" if type != "std_logic_vector" else str(int(signal[signal.index("(") + 1:signal.index(" downto")]) + 1),
                desc
            ]

            self.all_intSignals.append(loaded_sig_data)





            self.intSig_table.setItem(i, 0, QTableWidgetItem(loaded_sig_data[0]))
            self.intSig_table.setItem(i, 1, QTableWidgetItem(loaded_sig_data[1]))
            self.intSig_table.setItem(i, 2, QTableWidgetItem(str(loaded_sig_data[2])))

            #self.intSig_table.setCellWidget(i, 3, edit_btn)
            #self.intSig_table.setCellWidget(i, 4, delete_btn)