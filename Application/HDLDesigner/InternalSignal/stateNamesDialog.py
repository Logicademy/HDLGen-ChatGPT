from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import qtawesome as qta
import sys

sys.path.append("..")
from ProjectManager.project_manager import ProjectManager

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"


class state_Name_Dialog(QDialog):

    def __init__(self, add_or_edit, stateName_data=None):
        super().__init__()

        self.input_layout = QGridLayout()
        self.setWindowTitle("New State Name")

        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)

        self.mainLayout = QVBoxLayout()

        self.state_name_label = QLabel("State Name")
        self.state_name_label.setStyleSheet(WHITE_COLOR)
        self.state_name_input = QLineEdit()

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
        if add_or_edit == "edit" and stateName_data != None:
            self.load_sig_data(stateName_data)

    def setup_ui(self):

        self.input_layout.addWidget(self.state_name_label, 0, 0, 1, 1)
        self.input_layout.addWidget(self.state_name_input, 1, 0, 1, 3)


        self.input_layout.addItem(QSpacerItem(0, 20), 2, 0, 1, 3)
        self.input_layout.addWidget(self.cancel_btn, 3, 1, 1, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 3, 2, 1, 1, alignment=Qt.AlignRight)

        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setLayout(self.input_layout)

        self.state_name_input.textChanged.connect(self.enable_ok_btn);

        self.ok_btn.clicked.connect(self.get_data)
        self.cancel_btn.clicked.connect(self.cancel_selected)

        self.mainLayout.addWidget(self.input_frame, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)


    def load_sig_data(self, stateName_data):
        self.state_name_input.setText(stateName_data)

    def get_data(self):
        state_name = self.state_name_input.text().strip().replace(" ", "")
        data = state_name
        self.cancelled = False
        self.close()
        return data

    def cancel_selected(self):
        self.cancelled = True
        self.close()

    def enable_ok_btn(self):
        if self.state_name_input.text() != "" :
            self.ok_btn.setEnabled(True)
        else:
            self.ok_btn.setEnabled(False)

