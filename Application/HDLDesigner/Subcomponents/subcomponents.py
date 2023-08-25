import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import qtawesome as qta

sys.path.append("../..")
from ProjectManager.project_manager import ProjectManager
from HDLDesigner.Subcomponents.component_dialog import ComponentDialog
from Generator.generator import Generator
from HDLDesigner.Subcomponents.subcomp_help import SubcompHelpDialog

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"
ICONS_DIR = "../../Resources/icons/"
class Subcomponents(QWidget):

    def __init__(self):
        super().__init__()
        small_text_font = QFont()
        small_text_font.setPointSize(10)
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)

        self.all_signals = []
        self.all_signals_names = []
        self.arrays = []
        self.arrays_names = []
        self.comps = []
        self.comps_names = []

        self.package_heading_layout = QHBoxLayout()#QGridLayout()
        self.package_action_layout = QVBoxLayout()
        self.component_list_layout = QVBoxLayout()
        self.mainLayout = QVBoxLayout()

        self.package_label = QLabel("Sub-components")
        self.package_label.setFont(title_font)
        self.package_label.setStyleSheet(WHITE_COLOR)

        self.add_component_btn = QPushButton("Add component")
        #self.add_component_btn.setFixedSize(120, 25)
        self.add_component_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain; padding: 10px;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}")

        self.subcomp_info_btn = QPushButton()
        self.subcomp_info_btn.setIcon(qta.icon("mdi.help"))
        self.subcomp_info_btn.setFixedSize(25, 25)
        self.subcomp_info_btn.clicked.connect(self.subcomp_help_window)
        self.list_div = QFrame()
        self.list_div.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129);}')
        self.list_div.setFixedHeight(1)

        self.component_table = QTableWidget()

        self.package_list_frame = QFrame()
        self.component_list_frame = QFrame()
        self.package_action_frame = QFrame()
        self.generator = Generator()
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        bold_font = QFont()
        bold_font.setBold(True)

        self.package_heading_layout.addWidget(self.package_label)#, 0, 0, 1, 1)
        self.package_heading_layout.addWidget(self.add_component_btn, alignment=Qt.AlignRight)#, 0, 1, 1, 1)
        self.package_heading_layout.addWidget(self.subcomp_info_btn)#, 0, 2, 1, 1)
        #self.port_heading_layout.addWidget(self.add_btn, alignment=Qt.AlignRight)
        self.add_component_btn.clicked.connect(self.add_component)

        self.component_list_layout.setAlignment(Qt.AlignTop)

        self.component_table.setColumnCount(3)
        self.component_table.setShowGrid(False)
        self.component_table.setHorizontalHeaderLabels(['Component Name', '', ''])
        header = self.component_table.horizontalHeader()
        header.setSectionsClickable(False)
        header.setSectionsMovable(False)
        self.component_table.horizontalHeader().setFont(bold_font)
        self.component_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.component_table.setColumnWidth(1, 10)
        self.component_table.setColumnWidth(2, 10)
        self.component_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        vert = self.component_table.verticalHeader()
        vert.hide()
        self.component_table.setFrameStyle(QFrame.NoFrame)
        self.component_list_layout.addWidget(self.component_table)

        self.component_list_frame.setFrameShape(QFrame.StyledPanel)
        self.component_list_frame.setStyleSheet('.QFrame{background-color: white; border-radius: 5px;}')
        self.component_list_frame.setLayout(self.component_list_layout)

        self.package_action_layout.addLayout(self.package_heading_layout)
        self.package_action_layout.addSpacerItem(QSpacerItem(0, 5))
        self.package_action_layout.addWidget(self.component_list_frame)
        self.package_action_layout.addSpacerItem(QSpacerItem(0, 5))
        self.package_action_frame.setFrameShape(QFrame.StyledPanel)
        self.package_action_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.package_action_frame.setLayout(self.package_action_layout)

        self.mainLayout.addWidget(self.package_action_frame)

        self.setLayout(self.mainLayout)

    def add_component(self):
        add_comp = ComponentDialog("add")
        add_comp.exec_()
        if not add_comp.cancelled:
            comp_data = add_comp.get_data()
            self.comps.append(comp_data)
            self.comps_names.append((comp_data[0]))
            delete_btn = QPushButton()
            delete_btn.setIcon(qta.icon("mdi.delete"))
            delete_btn.setFixedSize(35, 22)
            delete_btn.clicked.connect(self.delete_component)

            edit_btn = QPushButton()
            edit_btn.setIcon(qta.icon("mdi.pencil"))
            edit_btn.setFixedSize(35, 22)
            edit_btn.clicked.connect(self.edit_component)

            row_position = self.component_table.rowCount()
            self.component_table.insertRow(row_position)
            self.component_table.setRowHeight(row_position, 5)
            self.component_table.setItem(row_position, 0, QTableWidgetItem(comp_data[0]))
            self.component_table.setCellWidget(row_position, 1, edit_btn)
            self.component_table.setCellWidget(row_position, 2, delete_btn)
            self.save_data()

    def edit_component(self):
        button = self.sender()
        if button:
            row = self.component_table.indexAt(button.pos()).row()
            add_comp = ComponentDialog("edit", self.comps[row])
            add_comp.exec_()

            if not add_comp.cancelled:
                comp_data = add_comp.get_data()
                self.component_table.removeRow(row)
                self.comps.pop(row)
                self.comps_names.pop(row)

                delete_btn = QPushButton()
                delete_btn.setIcon(qta.icon("mdi.delete"))
                delete_btn.setFixedSize(35, 22)
                delete_btn.clicked.connect(self.delete_component)

                edit_btn = QPushButton()
                edit_btn.setIcon(qta.icon("mdi.pencil"))
                edit_btn.setFixedSize(35, 22)
                edit_btn.clicked.connect(self.edit_component)

                self.comps.insert(row, comp_data)
                self.comps_names.insert(row, comp_data[0])
                self.component_table.insertRow(row)
                self.component_table.setRowHeight(row, 5)
                self.component_table.setItem(row, 0, QTableWidgetItem(comp_data[0]))
                self.component_table.setCellWidget(row, 1, edit_btn)
                self.component_table.setCellWidget(row, 2, delete_btn)
                self.save_data()

    def subcomp_help_window(self):
        subcomp_help_dialog = SubcompHelpDialog()
        subcomp_help_dialog.exec_()

    def delete_component(self):
        button = self.sender()
        if button:
            row = self.component_table.indexAt(button.pos()).row()
            self.component_table.removeRow(row)
            self.comps.pop(row)
            self.comps_names.pop(row)
            self.save_data()
    def save_data(self):
        mainPackageDir = ProjectManager.get_proj_environment() + "\Package\mainPackage.hdlgen"

        root = minidom.parse(mainPackageDir)
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
        new_comp_node = root.createElement("components")

        for component in self.comps:
            comp_node = root.createElement("component")
            package_model_node = root.createElement("model")
            package_model_node.appendChild(root.createTextNode(component[0]))
            comp_node.appendChild(package_model_node)
            package_dir_node = root.createElement("dir")
            package_dir_node.appendChild(root.createTextNode(component[1]))
            comp_node.appendChild(package_dir_node)

            for output_signal in component[2]:
                port_node = root.createElement("port")
                temp = output_signal.split(",")
                if temp[2][-1].isdigit():
                    temp[2] = temp[2]+" downto 0)"
                ports = temp[0] + "," + temp[1] + "," + temp[2]
                port_node.appendChild(root.createTextNode(ports))
                comp_node.appendChild(port_node)
            new_comp_node.appendChild(comp_node)
        hdlDesign[0].replaceChild(new_comp_node, hdlDesign[0].getElementsByTagName("components")[0])
        # converting the doc into a string in xml format
        xml_str = root.toprettyxml()
        xml_str = os.linesep.join([s for s in xml_str.splitlines() if s.strip()])
        # Writing xml file
        with open(mainPackageDir, "w") as f:
            f.write(xml_str)
        self.generator.generate_mainPackage()
        print("Saved sub component")

    def load_data(self):
        if self.comps:
            for row in range(0, self.component_table.rowCount()):
                self.component_table.removeRow(0)
                self.comps.pop(0)
                self.comps_names.pop(0)
        mainPackageDir = ProjectManager.get_proj_environment() + "\Package\mainPackage.hdlgen"
        try:
            root = minidom.parse(mainPackageDir)
            HDLGen = root.documentElement
            hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
            compPackage = hdlDesign[0].getElementsByTagName("components")
            comp_nodes = compPackage[0].getElementsByTagName('component')

            for i in range(0, len(comp_nodes)):
                model = comp_nodes[i].getElementsByTagName('model')[0].firstChild.data
                directory = comp_nodes[i].getElementsByTagName('dir')[0].firstChild.data
                self.comps_names.append(model)
                output_signal_nodes = comp_nodes[i].getElementsByTagName("port")

                output_signals = []
                for output_signal_node in output_signal_nodes:
                    output_signals.append(output_signal_node.firstChild.data)

                comp_data = [
                    model,
                    directory,
                    output_signals
                ]
                delete_btn = QPushButton()
                delete_btn.setIcon(qta.icon("mdi.delete"))
                delete_btn.setFixedSize(35, 22)
                delete_btn.clicked.connect(self.delete_component)

                edit_btn = QPushButton()
                edit_btn.setIcon(qta.icon("mdi.pencil"))
                edit_btn.setFixedSize(35, 22)
                edit_btn.clicked.connect(self.edit_component)

                self.component_table.insertRow(i)
                self.component_table.setRowHeight(i, 5)
                self.component_table.setItem(i, 0, QTableWidgetItem(comp_data[0]))
                self.component_table.setCellWidget(i, 1, edit_btn)
                self.component_table.setCellWidget(i, 2, delete_btn)
                self.comps.append(comp_data)
        except:
            print("")