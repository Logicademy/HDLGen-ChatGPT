#Dialog box for adding/editing type called in the package.py class.
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import sys

sys.path.append("..")

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"


class PackageDialog(QDialog):

    def __init__(self, add_or_edit, array_data=None):
        super().__init__()
        self.input_layout = QGridLayout()
        if add_or_edit == "add":
            self.setWindowTitle("New Package Signal")
        elif add_or_edit == "edit":
            self.setWindowTitle("Edit Package Signal")

        input_font = QFont()
        input_font.setPointSize(10)
        bold_font = QFont()
        bold_font.setBold(True)

        self.mainLayout = QVBoxLayout()
        self.sig_types = [ "bus", "signed", "unsigned"]
        self.array_name_label = QLabel("Array Name*")
        self.array_name_label.setStyleSheet(WHITE_COLOR)
        self.array_name_label.setFont(input_font)
        self.array_name_input = QLineEdit()
        self.array_name_input.setFont(input_font)

        self.arraySize_label = QLabel("Array Depth")
        self.arraySize_label.setFont(input_font)
        self.arraySize_label.setStyleSheet(WHITE_COLOR)
        self.arraySize_input = QLineEdit()
        self.arraySize_input.setFont(input_font)

        self.arrayLength_label = QLabel("Array Width")
        self.arrayLength_label.setStyleSheet(WHITE_COLOR)
        self.arrayLength_label.setFont(input_font)
        self.arrayLength_input = QLineEdit()
        self.arrayLength_input.setFont(input_font)

        self.sig_type_label = QLabel("Signal Type")
        self.sig_type_label.setFont(input_font)
        self.sig_type_label.setStyleSheet(WHITE_COLOR)
        self.sig_type_combo = QComboBox()
        self.sig_type_combo.setFont(input_font)
        self.sig_type_combo.setStyleSheet("QComboBox {padding: 2px;}")
        pal = self.sig_type_combo.palette()
        pal.setColor(QPalette.Button, QColor(255, 255, 255))
        self.sig_type_combo.setPalette(pal)
        self.sig_type_combo.addItems(self.sig_types)

        self.onlyInt = QIntValidator()
        self.arraySize_input.setValidator(self.onlyInt)
        self.arrayLength_input.setValidator(self.onlyInt)

        self.sig_desc_label = QLabel("Signal Description")
        self.sig_desc_label.setFont(input_font)
        self.sig_desc_label.setStyleSheet(WHITE_COLOR)
        self.sig_desc_input = QLineEdit()
        self.sig_desc_input.setFont(input_font)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFont(input_font)
        self.cancel_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}")

        self.ok_btn = QPushButton("Ok")
        self.ok_btn.setFont(input_font)
        self.ok_btn.setEnabled(False)
        self.ok_btn.setStyleSheet(
            "QPushButton {background-color: rgb(169,169,169);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            "QPushButton:enabled {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px; }")

        self.input_frame = QFrame()

        self.cancelled = True

        self.setup_ui()

        if add_or_edit == "edit" and array_data != None:
            self.load_sig_data(array_data)

    def setup_ui(self):

        self.input_layout.addWidget(self.array_name_label, 0, 0)  # , 1, 3)
        self.input_layout.addWidget(self.array_name_input, 1, 0)  # , 1, 3)

        self.input_layout.addWidget(self.sig_type_label, 0, 1)
        self.input_layout.addWidget(self.sig_type_combo, 1, 1)

        self.input_layout.addWidget(self.arraySize_label, 2, 0, 1, 1)
        self.input_layout.addWidget(self.arraySize_input, 3, 0, 1, 1)

        self.input_layout.addWidget(self.arrayLength_label, 2, 1, 1, 1)
        self.input_layout.addWidget(self.arrayLength_input, 3, 1, 1, 1)

        self.input_layout.addItem(QSpacerItem(0, 20), 4, 0, 1, 2)
        self.input_layout.addWidget(self.cancel_btn, 5, 0, 1, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 5, 1, 1, 1, alignment=Qt.AlignRight)

        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        #self.input_frame.setFixedSize(600, 600)
        self.input_frame.setLayout(self.input_layout)

        self.ok_btn.clicked.connect(self.get_data)
        self.cancel_btn.clicked.connect(self.cancel_selected)

        self.mainLayout.addWidget(self.input_frame, alignment=Qt.AlignCenter)
        self.arraySize_input.textChanged.connect(self.enable_ok_btn)
        self.arrayLength_input.textChanged.connect(self.enable_ok_btn)
        self.setLayout(self.mainLayout)

    def load_sig_data(self, array_data):
        self.array_name_input.setText(array_data[0])
        self.arraySize_input.setText(array_data[1])
        self.arrayLength_input.setText(array_data[2])
        sig_type = array_data[3]
        if sig_type == "std_logic_vector":
            sig_type = "bus"
        self.sig_type_combo.setCurrentText(sig_type)

    def get_data(self):
        sig_type = self.sig_type_combo.currentText()
        if sig_type == "bus":
            sig_type = "std_logic_vector"
        data = [self.array_name_input.text().strip(), self.arraySize_input.text().strip(), self.arrayLength_input.text().strip(), sig_type]

        self.cancelled = False
        self.close()

        return data

    def cancel_selected(self):
        self.cancelled = True
        self.close()

    def enable_ok_btn(self):
        if self.array_name_input.text() != "" and self.arraySize_input.text() != "" and self.arrayLength_input.text() != "":
            self.ok_btn.setEnabled(True)
        else:
            self.ok_btn.setEnabled(False)
    def delete_clicked(self):
        button = self.sender()
        if button:
            print("deleting row")
