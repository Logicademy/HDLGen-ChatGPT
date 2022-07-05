from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from Application.ProjectManager.project_manager import ProjectManager

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"

class AddConcurrentStmt(QDialog):

    def __init__(self):
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

        self.conc_name_label = QLabel("Concurrent Statement Name*")
        self.conc_name_label.setStyleSheet(WHITE_COLOR)
        self.conc_name_input = QLineEdit()

        self.out_sig_header_layout = QHBoxLayout()
        self.out_sig_label = QLabel("Output Signals")
        self.out_sig_label.setFont(bold_font)
        self.out_sig_label.setFixedWidth(100)
        self.val_label = QLabel("Value")
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

        self.out_sig_header_layout.addItem(QSpacerItem(40, 1))
        self.out_sig_header_layout.addWidget(self.out_sig_label)
        self.out_sig_header_layout.addWidget(self.val_label)
        self.out_sig_header_layout.addItem(QSpacerItem(80, 1))

        self.out_sig_layout.addLayout(self.out_sig_header_layout)
        self.out_sig_layout.addWidget(self.list_div)
        self.out_sig_table.setFrameStyle(QFrame.NoFrame)
        self.out_sig_table.setColumnCount(3)
        self.out_sig_table.setShowGrid(False)
        self.out_sig_table.setColumnWidth(0, 1)
        self.out_sig_table.setColumnWidth(1, 105)
        self.out_sig_table.setColumnWidth(2, 240)
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
        self.out_sig_frame.setFixedSize(410, 275)

        self.input_layout.addWidget(self.conc_name_label, 0, 0, 1, 1)
        self.input_layout.addWidget(self.conc_name_input, 1, 0, 2, 4)
        self.input_layout.addWidget(self.out_sig_frame, 3, 0, 4, 2)

        self.input_layout.addItem(QSpacerItem(0, 50), 6, 0, 1, 3)
        self.input_layout.addWidget(self.cancel_btn, 7, 2, 1, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 7, 3, 1, 1, alignment=Qt.AlignRight)

        self.conc_name_input.textChanged.connect(self.enable_ok_btn);
        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setFixedSize(450, 400)
        self.input_frame.setLayout(self.input_layout)

        self.ok_btn.clicked.connect(self.get_data)
        self.cancel_btn.clicked.connect(self.cancel_selected)

        self.mainLayout.addWidget(self.input_frame, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)

    def populate_signals(self, proj_dir):

        if (proj_dir != None):
            root = minidom.parse(proj_dir)
            HDLGen = root.documentElement
            hdlDesign = HDLGen.getElementsByTagName("hdlDesign")

            io_ports = hdlDesign[0].getElementsByTagName('entityIOPorts')
            signal_nodes = io_ports[0].getElementsByTagName('signal')

            if len(signal_nodes) != 0:
                for i in range(0, len(signal_nodes)):
                    name = signal_nodes[i].getElementsByTagName('name')[0].firstChild.data
                    mode = signal_nodes[i].getElementsByTagName('mode')[0].firstChild.data

                    if mode == "out":
                        self.output_signals.append(name)


                if len(self.output_signals) != 0:
                    for signal in self.output_signals:
                        checkbox = QCheckBox()
                        checkbox.setFixedWidth(45)

                        out_val_input = QLineEdit()
                        out_val_input.setPlaceholderText("Eg. 1")

                        row_position = self.out_sig_table.rowCount()
                        self.out_sig_table.insertRow(row_position)
                        self.out_sig_table.setRowHeight(row_position, 5)

                        self.out_sig_table.setCellWidget(row_position, 0, checkbox)
                        self.out_sig_table.setItem(row_position, 1, QTableWidgetItem(signal))
                        self.out_sig_table.setCellWidget(row_position, 2, out_val_input)


                    self.out_sig_layout.addWidget(self.out_sig_table)

                else:
                    self.out_sig_layout.addWidget(self.out_sig_empty_info, alignment=Qt.AlignTop)
                return

        self.out_sig_layout.addWidget(self.out_sig_empty_info, alignment=Qt.AlignTop)

    def get_data(self):
        data = []
        out_sigs = []
        data.append(self.conc_name_input.text())

        for i in range(self.out_sig_table.rowCount()):
            if self.out_sig_table.cellWidget(i, 0).checkState() == Qt.Checked:
                output = self.out_sig_table.item(i, 1).text()

                value = self.out_sig_table.cellWidget(i, 2).text()

                out_sigs.append(output + "," + value)

        data.append(out_sigs)
        print(out_sigs)
        self.cancelled = False
        self.close()
        return data

    def cancel_selected(self):
        self.cancelled = True
        self.close()

    def enable_ok_btn(self):
        if self.conc_name_input.text() != "":
            self.ok_btn.setEnabled(True)
        else:
            self.ok_btn.setEnabled(False)