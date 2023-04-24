import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import qtawesome as qta

import sys
sys.path.append("..")
from ProjectManager.project_manager import ProjectManager
from HDLDesigner.Architecture.process_dialog import ProcessDialog
from HDLDesigner.Architecture.concurrentstmt_dialog import ConcurrentStmtDialog
from HDLDesigner.Architecture.instance_dialog import InstanceDialog
from Generator.generator import Generator
from PySide2.QtCore import QObject, Signal

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"
ICONS_DIR = "../../Resources/icons/"

class Architecture(QWidget):
    save_signal = Signal(bool)
    def __init__(self, proj_dir):
        super().__init__()

        self.proj_dir = proj_dir
        self.all_data = []
        self.comps = []
        self.processNames = []
        self.concNames = []
        self.instanceNames = []
        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        btn_font = QFont()
        btn_font.setPointSize(10)
        bold_font = QFont()
        bold_font.setBold(True)
        self.process = ""
        self.mainLayout = QVBoxLayout()

        self.top_layout = QGridLayout()
        self.arch_action_layout = QVBoxLayout()

        self.arch_types = ["RTL", "Combinational"]
        self.arch_name_input = QLabel("Combinational")
        self.arch_name_input.setFont(title_font)
        self.arch_name_input.setStyleSheet(WHITE_COLOR)

        self.new_proc_btn = QPushButton("New Process")
        self.new_proc_btn.setFixedSize(80, 25)
        self.new_proc_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 5px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 5px; border-style: plain;}")
        #self.new_proc_btn.setFont(btn_font)
        self.new_conc_btn = QPushButton("New Concurrent statement")
        self.new_conc_btn.setFixedSize(175, 25)
        self.new_conc_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 5px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 5px; border-style: plain;}")
        #self.new_conc_btn.setFont(btn_font)
        self.new_instance_btn = QPushButton("New Instance")
        self.new_instance_btn.setFixedSize(80, 25)
        self.new_instance_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 5px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 5px; border-style: plain;}")
        #self.new_instance_btn.setFont(btn_font)

        #self.save_btn = QPushButton("Save")
       # self.save_btn.setEnabled(False)
        #self.save_btn.setFixedSize(60, 30)
        #self.save_btn.setStyleSheet(
         #   "QPushButton {background-color: rgb(169,169,169);  color: black; border-radius: 8px; border-style: plain;}"
         #   " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}"
         #   "QPushButton:enabled {background-color: white; color: black; border-radius: 8px; border-style: plain; }")

        self.name_label = QLabel("Name")
        self.name_label.setFont(bold_font)
        self.type_label = QLabel("Type")
        self.type_label.setFont(bold_font)
        self.in_sig_label = QLabel("Sensitivity List")
        self.in_sig_label.setFont(bold_font)

        self.list_div = QFrame()
        self.list_div.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129);}')
        self.list_div.setFixedHeight(1)

        self.proc_table = QTableWidget()


        self.list_header_layout = QHBoxLayout()
        self.list_layout = QVBoxLayout()

        self.list_frame = QFrame()
        self.main_frame = QFrame()
        self.generator = Generator()
        self.setup_ui()
        if proj_dir != None:
            self.load_data(proj_dir)
    def setup_ui(self):
        bold_font = QFont()
        bold_font.setBold(True)

        #self.enable_save_btn()
        self.top_layout.addWidget(self.arch_name_input, 0, 0, 1, 1)
        self.top_layout.addWidget(self.new_proc_btn, 0, 1, 1, 1)
        self.new_proc_btn.clicked.connect(self.add_proc)
        self.top_layout.addWidget(self.new_conc_btn, 0, 2, 1, 1)
        self.new_conc_btn.clicked.connect(self.add_concurrentstmt)
        self.top_layout.addWidget(self.new_instance_btn, 0, 3, 1, 1)
        self.new_instance_btn.clicked.connect(self.add_instance)

        self.arch_action_layout.addLayout(self.top_layout)

        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        #self.main_frame.setFixedSize(500, 400)

        self.main_frame.setLayout(self.arch_action_layout)

        self.name_label.setFixedWidth(97)
        self.list_header_layout.addWidget(self.name_label, alignment=Qt.AlignLeft)
        self.type_label.setFixedWidth(60)
        self.list_header_layout.addWidget(self.type_label, alignment=Qt.AlignLeft)
        self.list_header_layout.addWidget(self.in_sig_label, alignment=Qt.AlignLeft)
        self.list_header_layout.addItem(QSpacerItem(140, 1))
        #self.list_layout.addLayout(self.list_header_layout)
        #self.list_layout.addWidget(self.list_div)

        self.proc_table.setColumnCount(5)
        self.proc_table.setShowGrid(False)
        self.proc_table.setHorizontalHeaderLabels(['Name', ' Type', 'Sensitivity List', '', ''])
        header = self.proc_table.horizontalHeader()
        header.setSectionsClickable(False)
        header.setSectionsMovable(False)
        self.proc_table.horizontalHeader().setFont(bold_font)
        self.proc_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.proc_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.proc_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        #self.proc_table.setColumnWidth(0, 100)
        #self.proc_table.setColumnWidth(1, 75)
        #self.proc_table.setColumnWidth(2, 100)
        self.proc_table.setColumnWidth(3, 10)
        self.proc_table.setColumnWidth(4, 10)
        #self.proc_table.horizontalScrollMode()
        self.proc_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #self.proc_table.horizontalScrollBar().hide()
        #header = self.proc_table.horizontalHeader()
        #header.hide()
        vert = self.proc_table.verticalHeader()
        vert.hide()
        self.proc_table.setFrameStyle(QFrame.NoFrame)
        self.list_layout.addWidget(self.proc_table)

        self.list_frame.setFrameShape(QFrame.StyledPanel)
        self.list_frame.setStyleSheet('.QFrame{background-color: white; border-radius: 5px;}')
        #self.list_frame.setFixedSize(420, 300)
        self.list_frame.setLayout(self.list_layout)

        self.arch_action_layout.addItem(QSpacerItem(0, 5))
        self.arch_action_layout.addWidget(self.list_frame)#, alignment=Qt.AlignCenter)
        self.arch_action_layout.addItem(QSpacerItem(0, 5))
        #self.arch_action_layout.addWidget(self.save_btn, alignment=Qt.AlignRight)
        #self.save_btn.clicked.connect(self.save_data)

        self.mainLayout.addWidget(self.main_frame)#, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)

    def add_proc(self):
        add_proc = ProcessDialog("add", self.processNames)
        add_proc.exec_()

        if not add_proc.cancelled:
            data = add_proc.get_data()
            data.insert(0, "process")
            self.all_data.append(data)
            self.processNames.append((data[1]))
            self.instanceNames.append("")
            self.concNames.append("")

            delete_btn = QPushButton()
            delete_btn.setIcon(qta.icon("mdi.delete"))
            delete_btn.setFixedSize(35, 22)
            delete_btn.clicked.connect(self.delete_clicked)

            edit_btn = QPushButton()
            edit_btn.setIcon(qta.icon("mdi.pencil"))
            edit_btn.setFixedSize(35, 22)
            edit_btn.clicked.connect(self.edit_proc)

            row_position = self.proc_table.rowCount()
            self.proc_table.insertRow(row_position)
            self.proc_table.setRowHeight(row_position, 5)

            self.proc_table.setItem(row_position, 0, QTableWidgetItem(data[1]))

            self.proc_table.setItem(row_position, 1, QTableWidgetItem("Process"))
            input_signals = ""
            for in_sig in data[2]:
                input_signals = input_signals + ", " + in_sig

            input_signals = input_signals[1:]

            self.proc_table.setItem(row_position, 2, QTableWidgetItem(input_signals))
            self.proc_table.setCellWidget(row_position, 3, edit_btn)
            self.proc_table.setCellWidget(row_position, 4, delete_btn)
            self.save_data()

    def edit_proc(self):
        button = self.sender()
        if button:
            row = self.proc_table.indexAt(button.pos()).row()

            proc_dialog = ProcessDialog("edit", self.processNames, self.all_data[row])
            proc_dialog.exec_()

            if not proc_dialog.cancelled:
                data = proc_dialog.get_data()
                data.insert(0, "process")
                self.proc_table.removeRow(row)
                dataProcess = self.all_data[row]
                #if dataProcess[0] == "process":
                self.processNames.pop(row)
                self.instanceNames.pop(row)
                self.concNames.pop(row)
                self.all_data.pop(row)

                delete_btn = QPushButton()
                delete_btn.setIcon(qta.icon("mdi.delete"))
                delete_btn.setFixedSize(35, 22)
                delete_btn.clicked.connect(self.delete_clicked)

                edit_btn = QPushButton()
                edit_btn.setIcon(qta.icon("mdi.pencil"))
                edit_btn.setFixedSize(35, 22)
                edit_btn.clicked.connect(self.edit_proc)

                self.all_data.insert(row, data)
                self.concNames.insert(row, "")
                self.instanceNames.insert(row, "")
                self.processNames.insert(row, data[1])

                self.proc_table.insertRow(row)
                self.proc_table.setRowHeight(row, 5)

                self.proc_table.setItem(row, 0, QTableWidgetItem(data[1]))

                self.proc_table.setItem(row, 1, QTableWidgetItem("Process"))
                input_signals = ""
                for in_sig in data[2]:
                    input_signals = input_signals + ", " + in_sig

                input_signals = input_signals[1:]

                self.proc_table.setItem(row, 2, QTableWidgetItem(input_signals))
                self.proc_table.setCellWidget(row, 3, edit_btn)
                self.proc_table.setCellWidget(row, 4, delete_btn)
                self.save_data()

    def add_concurrentstmt(self):
        add_concurrentstmt = ConcurrentStmtDialog("add", self.concNames)
        add_concurrentstmt.exec_()

        if not add_concurrentstmt.cancelled:
            data = add_concurrentstmt.get_data()
            data.insert(0, "concurrentStmt")
            self.concNames.append((data[1]))
            self.processNames.append("")
            self.instanceNames.append("")
            self.all_data.append(data)

            delete_btn = QPushButton()
            delete_btn.setIcon(qta.icon("mdi.delete"))
            delete_btn.setFixedSize(35, 22)
            delete_btn.clicked.connect(self.delete_clicked)

            edit_btn = QPushButton()
            edit_btn.setIcon(qta.icon("mdi.pencil"))
            edit_btn.setFixedSize(35, 22)
            edit_btn.clicked.connect(self.edit_concurrentstmt)

            row_position = self.proc_table.rowCount()
            self.proc_table.insertRow(row_position)
            self.proc_table.setRowHeight(row_position, 5)

            self.proc_table.setItem(row_position, 0, QTableWidgetItem(data[1]))


            self.proc_table.setItem(row_position, 1, QTableWidgetItem("Concurrent Statement"))
            self.proc_table.setItem(row_position, 2, QTableWidgetItem("-"))
            self.proc_table.setCellWidget(row_position, 3, edit_btn)
            self.proc_table.setCellWidget(row_position, 4, delete_btn)
            self.save_data()

    def edit_concurrentstmt(self):
        button = self.sender()
        if button:
            row = self.proc_table.indexAt(button.pos()).row()

            edit_concurrentstmt = ConcurrentStmtDialog("edit", self.concNames, self.all_data[row])
            edit_concurrentstmt.exec_()

            if not edit_concurrentstmt.cancelled:
                data = edit_concurrentstmt.get_data()
                data.insert(0, "concurrentStmt")
                self.proc_table.removeRow(row)

                self.concNames.pop(row)
                self.instanceNames.pop(row)
                self.processNames.pop(row)
                self.all_data.pop(row)

                delete_btn = QPushButton()
                delete_btn.setIcon(qta.icon("mdi.delete"))
                delete_btn.setFixedSize(35, 22)
                delete_btn.clicked.connect(self.delete_clicked)
                edit_btn = QPushButton()
                edit_btn.setIcon(qta.icon("mdi.pencil"))
                edit_btn.setFixedSize(35, 22)
                edit_btn.clicked.connect(self.edit_concurrentstmt)

                self.all_data.insert(row, data)
                self.concNames.insert(row, data[1])
                self.instanceNames.insert(row, "")
                self.processNames.insert(row, "")
                self.proc_table.insertRow(row)
                self.proc_table.setRowHeight(row, 5)
                self.proc_table.setItem(row, 0, QTableWidgetItem(data[1]))
                self.proc_table.setItem(row, 1, QTableWidgetItem("Concurrent Statement"))
                self.proc_table.setItem(row, 2, QTableWidgetItem("-"))
                self.proc_table.setCellWidget(row, 3, edit_btn)
                self.proc_table.setCellWidget(row, 4, delete_btn)
                self.save_data()
    def add_instance(self):
        add_instance= InstanceDialog("add", self.instanceNames)
        add_instance.exec_()

        if not add_instance.cancelled:
            data = add_instance.get_data()
            data.insert(0, "instance")
            self.all_data.append(data)
            self.instanceNames.append((data[1]))
            self.concNames.append("")
            self.processNames.append("")

            delete_btn = QPushButton()
            delete_btn.setIcon(qta.icon("mdi.delete"))
            delete_btn.setFixedSize(35, 22)
            delete_btn.clicked.connect(self.delete_clicked)

            edit_btn = QPushButton()
            edit_btn.setIcon(qta.icon("mdi.pencil"))
            edit_btn.setFixedSize(35, 22)
            edit_btn.clicked.connect(self.edit_instance)

            row_position = self.proc_table.rowCount()
            self.proc_table.insertRow(row_position)
            self.proc_table.setRowHeight(row_position, 5)

            self.proc_table.setItem(row_position, 0, QTableWidgetItem(data[1]))


            self.proc_table.setItem(row_position, 1, QTableWidgetItem("Instance"))
            self.proc_table.setItem(row_position, 2, QTableWidgetItem("-"))
            self.proc_table.setCellWidget(row_position, 3, edit_btn)
            self.proc_table.setCellWidget(row_position, 4, delete_btn)
            self.save_data()

    def edit_instance(self):
        button = self.sender()
        if button:
            row = self.proc_table.indexAt(button.pos()).row()

            edit_instance = InstanceDialog("edit", self.instanceNames, self.all_data[row])
            edit_instance.exec_()

            if not edit_instance.cancelled:
                data = edit_instance.get_data()
                data.insert(0, "instance")
                dataInst = self.all_data[row]
                #print(self.instanceNames)
                #if dataInst[0] == "instance":
                self.instanceNames.pop(row)
                self.processNames.pop(row)
                self.concNames.pop(row)

                self.proc_table.removeRow(row)
                self.all_data.pop(row)

                delete_btn = QPushButton()
                delete_btn.setIcon(qta.icon("mdi.delete"))
                delete_btn.setFixedSize(35, 22)
                delete_btn.clicked.connect(self.delete_clicked)
                edit_btn = QPushButton()
                edit_btn.setIcon(qta.icon("mdi.pencil"))
                edit_btn.setFixedSize(35, 22)
                edit_btn.clicked.connect(self.edit_instance)

                self.all_data.insert(row, data)
                self.concNames.insert(row, "")
                self.instanceNames.insert(row, data[1])
                self.processNames.insert(row, "")
                self.proc_table.insertRow(row)
                self.proc_table.setRowHeight(row, 5)
                self.proc_table.setItem(row, 0, QTableWidgetItem(data[1]))
                self.proc_table.setItem(row, 1, QTableWidgetItem("Instance"))
                self.proc_table.setItem(row, 2, QTableWidgetItem("-"))
                self.proc_table.setCellWidget(row, 3, edit_btn)
                self.proc_table.setCellWidget(row, 4, delete_btn)
                self.save_data()

    def delete_clicked(self):
        button = self.sender()
        if button:
            row = self.proc_table.indexAt(button.pos()).row()
            self.proc_table.removeRow(row)
            data=self.all_data[row]
            self.processNames.pop(row)
            self.concNames.pop(row)
            self.instanceNames.pop(row)
            self.all_data.pop(row)
            self.save_data()


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

            if data[0] == "process":
                process_node = root.createElement("process")
                label_node = root.createElement("label")
                label_node.appendChild(root.createTextNode(data[1]))
                process_node.appendChild(label_node)

                for input_signal in data[2]:
                    in_sig_node = root.createElement("inputSignal")
                    in_sig_node.appendChild(root.createTextNode(input_signal))
                    process_node.appendChild(in_sig_node)

                for output_signal in data[3]:
                    out_sig_node = root.createElement("defaultOutput")
                    out_sig_node.appendChild(root.createTextNode(output_signal))
                    process_node.appendChild(out_sig_node)
                note_node = root.createElement("note")
                note_node.appendChild(root.createTextNode(data[4]))
                process_node.appendChild(note_node)
                new_arch_node.appendChild(process_node)

            elif data[0] == "concurrentStmt":
                conc_node = root.createElement("concurrentStmt")
                label_node = root.createElement("label")
                label_node.appendChild(root.createTextNode(data[1]))
                conc_node.appendChild(label_node)

                for output_signal in data[2]:
                    out_sig_node = root.createElement("statement")
                    out_sig_node.appendChild(root.createTextNode(output_signal))
                    conc_node.appendChild(out_sig_node)

                new_arch_node.appendChild(conc_node)

            elif data[0] == "instance":
                instance_node = root.createElement("instance")
                label_node = root.createElement("label")
                label_node.appendChild(root.createTextNode(data[1]))
                instance_node.appendChild(label_node)
                model_node = root.createElement("model")
                model_node.appendChild(root.createTextNode(data[2]))
                instance_node.appendChild(model_node)
                for output_signal in data[3]:
                    out_sig_node = root.createElement("port")
                    out_sig_node.appendChild(root.createTextNode(output_signal))
                    instance_node.appendChild(out_sig_node)
                    #temp = output_signal.split(",")
                    #ports = temp[0] + "," + temp[2] + "," + temp[3]

                new_arch_node.appendChild(instance_node)
        hdlDesign[0].replaceChild(new_arch_node, hdlDesign[0].getElementsByTagName("architecture")[0])
        # converting the doc into a string in xml format
        xml_str = root.toprettyxml()
        xml_str = os.linesep.join([s for s in xml_str.splitlines() if s.strip()])
        # Writing xml file
        with open(xml_data_path, "w") as f:
            f.write(xml_str)
        self.generator.generate_mainPackage()
        hdl=False
        self.save_signal.emit(hdl)
        print("Saved process, concurrent or instance")


    def load_data(self, proj_dir):
        xml_data_path = ProjectManager.get_xml_data_path()
        self.updateProcessName(xml_data_path)
        root = minidom.parse(proj_dir[0])
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")

        arch_node = hdlDesign[0].getElementsByTagName('architecture')
        arch_name_node = hdlDesign[0].getElementsByTagName("archName")
        #self.arch_name_input.setText(arch_name_node[0].firstChild.data)

        if len(arch_node) != 0 and arch_node[0].firstChild is not None:

            child = arch_node[0].firstChild

            while child is not None:

                next = child.nextSibling

                if (child.nodeType == arch_node[0].ELEMENT_NODE and child.tagName == "process"):
                    temp_data = []
                    label_val = child.getElementsByTagName("label")[0].firstChild.data
                    self.processNames.append(label_val)
                    self.concNames.append("")
                    self.instanceNames.append("")
                    temp_data.append(label_val)

                    input_signal_nodes = child.getElementsByTagName("inputSignal")

                    input_signals = []
                    for input_signal_node in input_signal_nodes:
                        input_signals.append(input_signal_node.firstChild.data)

                    temp_data.append(input_signals)

                    output_signal_nodes = child.getElementsByTagName("defaultOutput")

                    output_signals = []
                    for output_signal_node in output_signal_nodes:
                        output_signals.append(output_signal_node.firstChild.data)

                    temp_data.append(output_signals)
                    note = child.getElementsByTagName("note")[0].firstChild.nodeValue
                    temp_data.append(note)
                    temp_data.insert(0, "process")
                    self.all_data.append(temp_data)



                    delete_btn = QPushButton()
                    delete_btn.setIcon(qta.icon("mdi.delete"))
                    delete_btn.setFixedSize(35, 22)
                    delete_btn.clicked.connect(self.delete_clicked)

                    edit_btn = QPushButton()
                    edit_btn.setIcon(qta.icon("mdi.pencil"))
                    edit_btn.setFixedSize(35, 22)
                    edit_btn.clicked.connect(self.edit_proc)

                    row_position = self.proc_table.rowCount()
                    self.proc_table.insertRow(row_position)
                    self.proc_table.setRowHeight(row_position, 5)

                    self.proc_table.setItem(row_position, 0, QTableWidgetItem(label_val))

                    self.proc_table.setItem(row_position, 1, QTableWidgetItem("Process"))
                    temp_in_sig = ""
                    for in_sig in input_signals:
                        temp_in_sig = temp_in_sig + ", " + in_sig

                    temp_in_sig = temp_in_sig[1:]

                    self.proc_table.setItem(row_position, 2, QTableWidgetItem(temp_in_sig))
                    self.proc_table.setCellWidget(row_position, 3, edit_btn)
                    self.proc_table.setCellWidget(row_position, 4, delete_btn)

                elif (child.nodeType == arch_node[0].ELEMENT_NODE and child.tagName == "concurrentStmt"):

                    temp_data = []
                    label_val = child.getElementsByTagName("label")[0].firstChild.data
                    self.concNames.append(label_val)
                    self.instanceNames.append("")
                    self.processNames.append("")

                    temp_data.append(label_val)

                    output_signal_nodes = child.getElementsByTagName("statement")

                    output_signals = []
                    for output_signal_node in output_signal_nodes:
                        output_signals.append(output_signal_node.firstChild.data)

                    temp_data.append(output_signals)
                    temp_data.insert(0, "concurrentStmt")
                    self.all_data.append(temp_data)

                    delete_btn = QPushButton()
                    # delete_btn.setIcon(QIcon(ICONS_DIR + "delete.svg"))
                    delete_btn.setIcon(qta.icon("mdi.delete"))
                    delete_btn.setFixedSize(35, 22)
                    delete_btn.clicked.connect(self.delete_clicked)

                    edit_btn = QPushButton()
                    edit_btn.setIcon(qta.icon("mdi.pencil"))
                    edit_btn.setFixedSize(35, 22)
                    edit_btn.clicked.connect(self.edit_concurrentstmt)

                    row_position = self.proc_table.rowCount()
                    self.proc_table.insertRow(row_position)
                    self.proc_table.setRowHeight(row_position, 5)

                    self.proc_table.setItem(row_position, 0, QTableWidgetItem(label_val))

                    self.proc_table.setItem(row_position, 1, QTableWidgetItem("Concurrent Statement"))

                    self.proc_table.setItem(row_position, 2, QTableWidgetItem("-"))
                    self.proc_table.setCellWidget(row_position, 3, edit_btn)
                    self.proc_table.setCellWidget(row_position, 4, delete_btn)

                elif (child.nodeType == arch_node[0].ELEMENT_NODE and child.tagName == "instance"):

                    temp_data = []


                    output_signal_nodes = child.getElementsByTagName("port")

                    output_signals = []
                    for output_signal_node in output_signal_nodes:
                        output_signals.append(output_signal_node.firstChild.data)


                    temp_data.insert(0, "instance")
                    label_val = child.getElementsByTagName("label")[0].firstChild.data
                    self.instanceNames.append(label_val)
                    self.concNames.append("")
                    self.processNames.append("")

                    temp_data.append(label_val)
                    temp_data.append(child.getElementsByTagName("model")[0].firstChild.data)
                    temp_data.append(output_signals)
                    self.all_data.append(temp_data)

                    delete_btn = QPushButton()
                    # delete_btn.setIcon(QIcon(ICONS_DIR + "delete.svg"))
                    delete_btn.setIcon(qta.icon("mdi.delete"))
                    delete_btn.setFixedSize(35, 22)
                    delete_btn.clicked.connect(self.delete_clicked)

                    edit_btn = QPushButton()
                    edit_btn.setIcon(qta.icon("mdi.pencil"))
                    edit_btn.setFixedSize(35, 22)
                    edit_btn.clicked.connect(self.edit_instance)

                    row_position = self.proc_table.rowCount()
                    self.proc_table.insertRow(row_position)
                    self.proc_table.setRowHeight(row_position, 5)

                    self.proc_table.setItem(row_position, 0, QTableWidgetItem(label_val))

                    self.proc_table.setItem(row_position, 1, QTableWidgetItem("Instance"))

                    self.proc_table.setItem(row_position, 2, QTableWidgetItem("-"))
                    self.proc_table.setCellWidget(row_position, 3, edit_btn)
                    self.proc_table.setCellWidget(row_position, 4, delete_btn)
                child = next
    def updateProcessName(self, proj_dir):

        root = minidom.parse(proj_dir)
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
        clkAndRst = hdlDesign[0].getElementsByTagName('clkAndRst')
        if len(clkAndRst) != 1:
            self.process = "RTL"
            self.arch_name_input.setText('RTL')
        else:
            self.process = "Combin"
            self.arch_name_input.setText('Combinational')
    #def enable_save_btn(self):
        #if self.arch_name_input.text() != "":
        #if self.arch_name_input.text() != "":
        #    self.save_btn.setEnabled(True)
        #else:
           # self.save_btn.setEnabled(False)