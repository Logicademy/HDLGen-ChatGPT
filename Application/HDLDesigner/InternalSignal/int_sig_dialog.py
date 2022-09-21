from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import sys
sys.path.append("..")
from ProjectManager.project_manager import ProjectManager

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"

class IntSignalDialog(QDialog):

    def __init__(self, add_or_edit, intSig_data=None):
        super().__init__()

        self.input_layout = QGridLayout()
        
        if add_or_edit == "add":
            self.setWindowTitle("New Internal Signal")
        elif add_or_edit == "edit":
            self.setWindowTitle("Edit Internal Signal")

        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)

        self.sig_types = ["std_logic", "std_logic_vector"]


        self.mainLayout = QVBoxLayout()

        self.intSig_name_label = QLabel("Internal Signal Name*")
        self.intSig_name_label.setStyleSheet(WHITE_COLOR)
        self.intSig_name_input = QLineEdit()
        #self.intSig_name_input.setFixedWidth(120)

        self.sig_type_label = QLabel("Signal Type")
        self.sig_type_label.setStyleSheet(WHITE_COLOR)
        self.sig_type_combo = QComboBox()
        pal = self.sig_type_combo.palette()
        pal.setColor(QPalette.Button, QColor(255, 255, 255))
        self.sig_type_combo.setPalette(pal)
        #self.sig_type_combo.setFixedWidth(110)
        self.sig_type_combo.addItems(self.sig_types)

        self.sig_size_label = QLabel("Size (eg. 32) * ")
        self.sig_size_label.setStyleSheet(WHITE_COLOR)
        self.sig_size_input = QLineEdit()
        self.sig_size_input.setText("1")
        #self.sig_size_input.setFixedWidth(100)
        self.sig_size_input.setEnabled(False)

        self.onlyInt = QIntValidator()
        self.sig_size_input.setValidator(self.onlyInt)

        self.sig_desc_label = QLabel("Signal Description")
        self.sig_desc_label.setStyleSheet(WHITE_COLOR)
        #self.sig_desc_label.setFixedWidth(120)
        self.sig_desc_input = QLineEdit()

        #self.sig_layout = QHBoxLayout()


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

        if add_or_edit == "edit" and intSig_data != None:
            self.load_sig_data(intSig_data)

    def setup_ui(self):

        self.input_layout.addWidget(self.intSig_name_label, 0, 0, 1, 1)
        self.input_layout.addWidget(self.intSig_name_input, 1, 0, 1, 3)
        self.input_layout.addWidget(self.sig_type_label, 2, 0, 1, 1)
        self.input_layout.addWidget(self.sig_type_combo, 3, 0, 1, 2)
        self.input_layout.addWidget(self.sig_size_label, 2, 2, 1, 1)
        self.input_layout.addWidget(self.sig_size_input, 3, 2, 1, 1)
        self.input_layout.addWidget(self.sig_desc_label, 4, 0, 1, 1)
        self.input_layout.addWidget(self.sig_desc_input, 5, 0, 1, 3)
        self.input_layout.addItem(QSpacerItem(0, 20), 6, 0, 1, 3)
        self.input_layout.addWidget(self.cancel_btn, 7, 1, 1, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 7, 2, 1, 1, alignment=Qt.AlignRight)

        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setFixedSize(400, 250)
        self.input_frame.setLayout(self.input_layout)
        
        self.intSig_name_input.textChanged.connect(self.enable_ok_btn);
        self.sig_type_combo.currentTextChanged.connect(self.enable_size_option)

        self.ok_btn.clicked.connect(self.get_data)
        self.cancel_btn.clicked.connect(self.cancel_selected)

        self.mainLayout.addWidget(self.input_frame, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)

    def load_sig_data(self, intSig_data):

        self.intSig_name_input.setText(intSig_data[0])
        self.sig_type_combo.setCurrentText(intSig_data[1])
        self.sig_size_input.setText(intSig_data[2])
        self.sig_desc_input.setText(intSig_data[3])

    def get_data(self):
        data = []
        intSignalDescription = self.sig_desc_input.text()
        if intSignalDescription == "":
            intSignalDescription = "to be completed"
        data.append(self.intSig_name_input.text())
        data.append(self.sig_type_combo.currentText())
        data.append(self.sig_size_input.text())
        data.append(intSignalDescription)
        self.cancelled = False
        self.close()
        return data

    def cancel_selected(self):
        self.cancelled = True
        self.close()

    def enable_ok_btn(self):
        if self.intSig_name_input.text() != "" and self.sig_size_input.text() != "":
            self.ok_btn.setEnabled(True)
        else:
            self.ok_btn.setEnabled(False)

    def enable_size_option(self):
        if self.sig_type_combo.currentText() == "std_logic_vector":
            self.sig_size_input.setEnabled(True)
            self.sig_size_input.clear()
        else:
            self.sig_size_input.setEnabled(False)
            self.sig_size_input.setText("1")