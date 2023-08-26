from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import sys
sys.path.append("..")
from ProjectManager.project_manager import ProjectManager

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"

class ChipEnabledDialog(QDialog):

    def __init__(self, add_or_edit, ce_data = None):
        super().__init__()

        if add_or_edit == "add":
            self.setWindowTitle("Set Chip Enabled Signal")
        elif add_or_edit == "edit":
            self.setWindowTitle("Edit Chip Enabled Signal")
        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)
        input_font = QFont()
        input_font.setPointSize(10)
        self.internal_signals = []
        self.input_signals = []
        self.output_signals = []

        self.input_layout = QGridLayout()

        self.mainLayout = QVBoxLayout()

        self.chipEnabled_name_label = QLabel("Chip Enabled Signal")
        self.chipEnabled_name_label.setFont(input_font)
        self.chipEnabled_name_label.setStyleSheet(WHITE_COLOR)

        self.chipEnabled_signals_combo = QComboBox()
        self.chipEnabled_signals_combo.setFont(input_font)
        self.chipEnabled_signals_combo.setStyleSheet("QComboBox {padding: 2px;}")

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFont(input_font)
        self.cancel_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}")


        self.ok_btn = QPushButton("Ok")
        self.ok_btn.setEnabled(False)
        self.ok_btn.setFont(input_font)
        self.ok_btn.setStyleSheet(
            "QPushButton {background-color: rgb(169,169,169);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            "QPushButton:enabled {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px; }")

        self.input_frame = QFrame()

        self.cancelled = True

        self.setup_ui()

        self.populate_signals(ProjectManager.get_xml_data_path())

        if add_or_edit == "edit" and ce_data != None:
            self.load_ce_data(ce_data)

    def setup_ui(self):

        self.input_layout.addWidget(self.chipEnabled_name_label, 0, 0, 1, 2)
        self.input_layout.addWidget(self.chipEnabled_signals_combo, 1, 0, 1, 2)
        self.input_layout.addItem(QSpacerItem(0, 10), 2, 0, 1, 2)
        self.input_layout.addWidget(self.cancel_btn, 3, 0, 2, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 3, 1, 2, 1, alignment=Qt.AlignRight)

        self.chipEnabled_signals_combo.currentTextChanged.connect(self.enable_ok_btn);
        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setFixedSize(400, 175)
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

            intSignals = hdlDesign[0].getElementsByTagName('internalSignals')
            intSignal_nodes = intSignals[0].getElementsByTagName('signal')

            if len(signal_nodes) != 0 or len(intSignal_nodes) != 0:

                for i in range(0, len(signal_nodes)):
                    name = signal_nodes[i].getElementsByTagName('name')[0].firstChild.data
                    mode = signal_nodes[i].getElementsByTagName('mode')[0].firstChild.data

                    if mode != "out":
                        if name != "clk" and name != "rst":
                            self.input_signals.append(name)

                for i in range(0, len(intSignal_nodes)):
                    internal_signal = intSignal_nodes[i].getElementsByTagName('name')[0].firstChild.data
                    self.internal_signals.append(internal_signal)

                if len(self.input_signals) != 0 or len(self.internal_signals) != 0:
                    self.chipEnabled_signals_combo.addItem("Please select")
                    self.chipEnabled_signals_combo.addItems(self.input_signals + self.internal_signals)


    def load_ce_data(self, ce_data):
        if ce_data in self.internal_signals or ce_data in self.input_signals:
            self.chipEnabled_signals_combo.setCurrentText(ce_data)
        else:
            self.chipEnabled_signals_combo.setCurrentText("Please select")
    def get_data(self):
        data = self.chipEnabled_signals_combo.currentText()
        self.cancelled = False
        self.close()
        return data

    def cancel_selected(self):
        self.cancelled = True
        self.close()
    def enable_ok_btn(self):
        if self.chipEnabled_signals_combo.currentText() != "Please select":
            self.ok_btn.setEnabled(True)
        else:
            self.ok_btn.setEnabled(False)
