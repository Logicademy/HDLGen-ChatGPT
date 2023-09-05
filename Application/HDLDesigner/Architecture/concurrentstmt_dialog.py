#Dialog box for concurrent statement called by the architecture.py when adding or editing concurrent statement
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import sys
import re
sys.path.append("..")
from ProjectManager.project_manager import ProjectManager
from HDLDesigner.Architecture.note_dialog import note_Dialog

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"

class ConcurrentStmtDialog(QDialog):

    def __init__(self, add_or_edit, concNames ,conc_data = None):
        super().__init__()

        if add_or_edit == "add":
            self.setWindowTitle("New Concurrent Statement")
        elif add_or_edit == "edit":
            self.setWindowTitle("Edit Concurrent Statement")
        self.conc_names = concNames
        self.conc_name = ""
        if conc_data != None:
            self.conc_name = conc_data[1]
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
        self.conc_notes = "None"
        self.input_layout = QGridLayout()

        self.mainLayout = QVBoxLayout()

        self.conc_name_label = QLabel("Concurrent Statement Name*")
        self.conc_name_label.setStyleSheet(WHITE_COLOR)
        self.conc_name_label.setFont(input_font)
        self.conc_name_input = QLineEdit()
        self.conc_name_input.setFont(input_font)
        self.noteBox = QCheckBox("Custom Value")
        self.noteBox.setStyleSheet(WHITE_COLOR)
        self.noteBox.setFont(input_font)
        self.note_label = QLabel("Custom Value")
        self.note_label.setStyleSheet(WHITE_COLOR)
        self.note_label.setFont(input_font)
        self.note_label.setVisible(False)
        self.note_input = QLineEdit()
        self.note_input.setVisible(False)
        self.note_input.setFont(input_font)
        self.add_note_btn = QPushButton("Add Custom Value")
        self.add_note_btn.setFont(input_font)
        self.add_note_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}")
        self.add_note_btn.setVisible(False)

        self.out_sig_header_layout = QHBoxLayout()
        self.out_sig_label = QLabel("Assign Signal")
        self.out_sig_label.setFont(input_font)
        self.out_sig_label.setStyleSheet(WHITE_COLOR)
        self.options_sig_label = QLabel("Default Value")
        self.options_sig_label.setFont(input_font)
        self.options_sig_label.setStyleSheet(WHITE_COLOR)
        self.val_label = QLabel("Binary Value")
        self.val_label.setFont(input_font)
        self.val_label.setStyleSheet(WHITE_COLOR)
        self.out_sig_empty_info = QLabel("No Output Signals found!\nPlease add signal in the IO Ports")
        self.out_sig_empty_info.setFont(input_font)
        self.out_sig_empty_info.setFixedSize(400, 300)

        self.out_signals_combo = QComboBox()
        self.out_signals_combo.setFont(input_font)
        self.out_signals_combo.setStyleSheet("QComboBox {padding: 2px;}")
        self.options_signals_combo = QComboBox()
        self.options_signals_combo.setFont(input_font)
        self.options_signals_combo.setStyleSheet("QComboBox {padding: 2px;}")
        self.out_val_input = QLineEdit()
        self.out_val_input.setFont(input_font)
        validator = QIntValidator()
        self.out_val_input.setValidator(validator)

        self.out_sig_layout = QHBoxLayout()

        self.suffix_label = QLabel("Suffix")
        self.suffix_label.setStyleSheet(WHITE_COLOR)
        self.suffix_label.setFont(input_font)
        self.suffix_input = QLineEdit()
        self.suffix_input.setFont(input_font)
        self.suffix_input.setEnabled(False)
        self.suffix_input.setText("_c")

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

        if add_or_edit == "edit" and conc_data != None:
            self.load_conc_data(conc_data)

    def setup_ui(self):

        self.input_layout.addWidget(self.conc_name_label, 0, 0, 1, 1)
        self.input_layout.addWidget(self.conc_name_input, 1, 0, 1, 1)
        self.input_layout.addWidget(self.suffix_label, 0, 1, 1, 1)
        self.input_layout.addWidget(self.suffix_input, 1, 1, 1, 1)
        self.input_layout.addWidget(self.noteBox, 1, 2, 1, 1)
        self.input_layout.addWidget(self.out_sig_label, 3, 0, 1, 1)
        self.input_layout.addWidget(self.out_signals_combo, 4, 0, 1, 1)
        self.input_layout.addWidget(self.add_note_btn, 4, 1, 1, 1)
        self.input_layout.addWidget(self.options_sig_label,3,1,1,1)
        self.input_layout.addWidget(self.options_signals_combo, 4, 1, 1, 1)
        self.input_layout.addItem(QSpacerItem(0, 10), 5, 0, 1, 3)
        self.input_layout.addWidget(self.cancel_btn, 6, 1, 1, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 6, 2, 1, 1, alignment=Qt.AlignRight)

        self.conc_name_input.textChanged.connect(self.enable_ok_btn);
        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setFixedSize(600, 300)
        self.input_frame.setLayout(self.input_layout)
        self.add_note_btn.clicked.connect(self.add_conc_note)
        self.ok_btn.clicked.connect(self.get_data)
        self.cancel_btn.clicked.connect(self.cancel_selected)
        self.noteBox.clicked.connect(self.note_checked)
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

                    self.output_signals.insert(0, "Select signal")
                    self.out_signals_combo.addItems(self.output_signals + self.internal_signals )
                    self.output_signals.pop(0)
                    self.options_signals_combo.addItem("zero")
                    self.options_signals_combo.addItems(self.internal_signals + self.input_signals)

                else:
                    self.out_sig_layout.addWidget(self.out_sig_empty_info, alignment=Qt.AlignTop)
                return

        self.out_sig_layout.addWidget(self.out_sig_empty_info, alignment=Qt.AlignTop)

    def load_conc_data(self, conc_data):

        self.conc_name_input.setText(conc_data[1])
        self.conc_notes = conc_data[3]
        if self.conc_notes != "None":
            self.noteBox.setChecked(True)
            self.add_note_btn.setVisible(True)
            self.options_sig_label.setVisible(False)
            self.options_signals_combo.setVisible(False)
            self.add_note_btn.setText("Edit Custom Value")
        if len(conc_data[2]) != 0:
            temp = conc_data[2][0].split(",")
            out_sig = temp[0]
            out_val = temp[1]
            self.out_signals_combo.setCurrentText(out_sig)
            self.options_signals_combo.setCurrentText(out_val)
            self.out_val_input.setEnabled(False)


    def get_data(self):
        data = []
        out_sig = []
        concurrentName = self.conc_name_input.text().strip().replace(" ", "")
        if concurrentName[-2:] != "_c":
            concurrentName=concurrentName+"_c"
        data.append(concurrentName)
        output = self.out_signals_combo.currentText()
        if self.noteBox.isChecked():
            out_sig.append(output+",zero")
        else:
            self.conc_notes = "None"
            value = self.options_signals_combo.currentText()
            out_sig.append(output + "," + value)
        data.append(out_sig)
        data.append(self.conc_notes)

        self.cancelled = False
        self.close()
        return data

    def cancel_selected(self):
        self.cancelled = True
        self.close()
    def enable_ok_btn(self):
        if self.conc_name_input.text() != ""and (self.conc_name_input.text()+"_c" not in self.conc_names or self.conc_name_input.text() == self.conc_name[:-2] ) and (self.conc_name_input.text() not in self.conc_names or self.conc_name_input.text() == self.conc_name):
            self.ok_btn.setEnabled(True)
        else:
            self.ok_btn.setEnabled(False)

    def add_conc_note(self):
        button = self.sender()
        if button:
            if button.text() == "Edit Custom Value":
                add_note = note_Dialog("edit", "Concurrent Statement Custom Value",self.conc_notes)
            else:
                add_note = note_Dialog("add", "Concurrent Statement Custom Value",self.conc_notes)
            add_note.exec_()

            if not add_note.cancelled:
                note_data = add_note.get_data()
                note_data = re.sub(r'\s+', ' ', note_data)
                if note_data == "None":
                    self.add_note_btn.setText("Add Custom Value")
                else:
                    self.add_note_btn.setText("Edit Custom Value")
                self.conc_notes = note_data

    def note_checked(self):
        if self.noteBox.isChecked():
            self.add_note_btn.setVisible(True)
            self.options_sig_label.setVisible(False)
            self.options_signals_combo.setVisible(False)
        else:
            self.add_note_btn.setVisible(False)
            self.options_sig_label.setVisible(True)
            self.options_signals_combo.setVisible(True)
    def disable_Binary_input(self):
        combo = self.sender()
        if combo:
            if combo.currentText() == "Binary":
                self.out_val_input.setEnabled(True)
                self.out_val_input.setPlaceholderText("Eg. 1")
            else:
                self.out_val_input.clear()
                self.out_val_input.setPlaceholderText("")
                self.out_val_input.setEnabled(False)
