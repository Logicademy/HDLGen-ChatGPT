from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import sys
sys.path.append("..")
from ProjectManager.project_manager import ProjectManager

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"

class ConcurrentStmtDialog(QDialog):

    def __init__(self, add_or_edit, conc_data = None):
        super().__init__()

        if add_or_edit == "add":
            self.setWindowTitle("New Concurrent Statement")
        elif add_or_edit == "edit":
            self.setWindowTitle("Edit Concurrent Statement")
        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)

        self.internal_signals = []
        self.input_signals = []
        self.output_signals = []

        self.input_layout = QGridLayout()

        self.mainLayout = QVBoxLayout()

        self.conc_name_label = QLabel("Concurrent Statement Name*")
        self.conc_name_label.setStyleSheet(WHITE_COLOR)
        self.conc_name_input = QLineEdit()

        self.out_sig_header_layout = QHBoxLayout()
        self.out_sig_label = QLabel("Assign Signal")
        self.out_sig_label.setStyleSheet(WHITE_COLOR)
        self.out_sig_label.setFixedWidth(100)
        self.options_sig_label = QLabel("Default Value")
        self.options_sig_label.setStyleSheet(WHITE_COLOR)
        self.options_sig_label.setFixedWidth(100)
        self.val_label = QLabel("Binary Value")
        self.val_label.setStyleSheet(WHITE_COLOR)
        self.out_sig_empty_info = QLabel("No Output Signals found!\nPlease add signal in the IO Ports")
        self.out_sig_empty_info.setFixedSize(400, 300)

        self.out_signals_combo = QComboBox()
        self.options_signals_combo = QComboBox()
        self.out_val_input = QLineEdit()

        self.out_sig_layout = QHBoxLayout()

        self.suffix_label = QLabel("Suffix")
        self.suffix_label.setStyleSheet(WHITE_COLOR)
        self.suffix_input = QLineEdit()
        #self.suffix_input.setFixedWidth(20)
        self.suffix_input.setEnabled(False)
        self.suffix_input.setText("_c")

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

        if add_or_edit == "edit" and conc_data != None:
            self.load_conc_data(conc_data)

    def setup_ui(self):

        self.input_layout.addWidget(self.conc_name_label, 0, 0, 1, 3)
        self.input_layout.addWidget(self.conc_name_input, 1, 0, 1, 3)
        self.input_layout.addWidget(self.suffix_label, 0, 3, 1, 1)
        self.input_layout.addWidget(self.suffix_input, 1, 3, 1, 1)
        self.input_layout.addWidget(self.out_sig_label, 3, 0, 1, 1)
        self.input_layout.addWidget(self.out_signals_combo, 4, 0, 1, 1)
        self.input_layout.addWidget(self.options_sig_label,3,1,1,1)
        self.input_layout.addWidget(self.options_signals_combo, 4, 1, 1, 1)
        self.input_layout.addWidget(self.val_label, 3, 2, 1, 2)
        self.input_layout.addWidget(self.out_val_input, 4, 2, 1, 2)
        self.input_layout.addItem(QSpacerItem(0, 10), 5, 0, 1, 3)
        self.input_layout.addWidget(self.cancel_btn, 6, 2, 1, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 6, 3, 1, 1, alignment=Qt.AlignRight)

        self.conc_name_input.textChanged.connect(self.enable_ok_btn);
        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setFixedSize(400, 175)
        self.input_frame.setLayout(self.input_layout)
        #self.out_signals_combo.currentIndexChanged.connect(self.setName)
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

                    if mode == "out":
                        self.output_signals.append(name)
                    else:
                        if name != "clk" and name != "rst":
                            self.input_signals.append(name)

                for i in range(0, len(intSignal_nodes)):
                    internal_signal = intSignal_nodes[i].getElementsByTagName('name')[0].firstChild.data
                    self.internal_signals.append(internal_signal)

                if len(self.output_signals) != 0 or len(self.internal_signals) != 0:

                    self.output_signals.insert(0, "Please select")
                    self.out_signals_combo.addItems(self.output_signals + self.internal_signals )
                    self.output_signals.pop(0)

                    self.options_signals_combo.addItem("Custom")
                    self.options_signals_combo.addItem("zero")
                    self.options_signals_combo.addItems(self.internal_signals + self.input_signals)
                    self.options_signals_combo.currentTextChanged.connect(self.disable_custom_input)

                else:
                    self.out_sig_layout.addWidget(self.out_sig_empty_info, alignment=Qt.AlignTop)
                return

        self.out_sig_layout.addWidget(self.out_sig_empty_info, alignment=Qt.AlignTop)

    def load_conc_data(self, conc_data):

        self.conc_name_input.setText(conc_data[1])

        if len(conc_data[2]) != 0:
            temp = conc_data[2][0].split(",")
            out_sig = temp[0]
            out_val = temp[1]
            self.out_signals_combo.setCurrentText(out_sig)
            if out_val not in self.input_signals and out_val not in self.internal_signals and out_val != "zero":
                self.out_val_input.setText(out_val)
                self.options_signals_combo.setCurrentText("Custom")
            else:
                self.options_signals_combo.setCurrentText(out_val)
                self.out_val_input.setEnabled(False)


    def get_data(self):
        data = []
        out_sig = []
        concurrentName = self.conc_name_input.text().strip().replace(" ", "")
        if concurrentName[-2:] != "_c":
            concurrentName=concurrentName+"_c"
        data.append(concurrentName)

        if (self.out_signals_combo.currentText() != "Please select"):
            output = self.out_signals_combo.currentText()
            if self.options_signals_combo.currentText() == "Custom":
                value = self.out_val_input.text()
            else:
                value = self.options_signals_combo.currentText()
            out_sig.append(output + "," + value)

        data.append(out_sig)

        self.cancelled = False
        self.close()
        return data

    def cancel_selected(self):
        self.cancelled = True
        self.close()
    def setName(self):
        self.conc_name_input.setText("asgn_")
        if self.out_signals_combo.currentText() != "Please select":
            self.conc_name_input.setText("asgn_"+self.out_signals_combo.currentText())
    def enable_ok_btn(self):
        if self.conc_name_input.text() != "":
            self.ok_btn.setEnabled(True)
        else:
            self.ok_btn.setEnabled(False)

    def disable_custom_input(self):
        combo = self.sender()
        if combo:
            if combo.currentText() == "Custom":
                self.out_val_input.setEnabled(True)
                self.out_val_input.setPlaceholderText("Eg. 1")
            else:
                self.out_val_input.clear()
                self.out_val_input.setPlaceholderText("")
                self.out_val_input.setEnabled(False)
