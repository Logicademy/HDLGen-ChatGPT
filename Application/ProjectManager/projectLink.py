from PySide2.QtWidgets import *
from PySide2.QtGui import *
import configparser

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"

class LinkDialog(QDialog):

    def __init__(self, add_or_edit, data=None):
        super().__init__()

        self.setWindowTitle("Project Information Link")
        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)
        input_font = QFont()
        input_font.setPointSize(10)

        self.input_layout = QGridLayout()
        self.mainLayout = QVBoxLayout()

        self.link_label = QLabel("Project Information Link")
        self.link_label.setFont(input_font)
        self.link_label.setStyleSheet(WHITE_COLOR)
        self.link_input = QLineEdit()
        self.link_input.setFont(input_font)


        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFont(input_font)
        self.cancel_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}")


        self.ok_btn = QPushButton("Ok")
        self.ok_btn.setFont(input_font)
        self.ok_btn.setStyleSheet(
            "QPushButton {background-color: rgb(169,169,169);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            "QPushButton:enabled {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px; }")
        self.input_frame = QFrame()

        self.cancelled = True
        self.config = configparser.ConfigParser()

        self.setup_ui()
        if add_or_edit == "edit" and data != None:
            self.load_data(data)
    def setup_ui(self):

        self.input_layout.addWidget(self.link_label, 0, 0, 1, 4)
        self.input_layout.addWidget(self.link_input, 1, 0, 1, 4)

        self.input_layout.addWidget(self.cancel_btn, 2, 2, 1, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 2, 3, 1, 1, alignment=Qt.AlignRight)
        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setFixedSize(500, 200)
        self.input_frame.setLayout(self.input_layout)
        self.cancel_btn.clicked.connect(self.cancel_selected)

        self.mainLayout.addWidget(self.input_frame, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)
        self.ok_btn.clicked.connect(self.get_data)

    def cancel_selected(self):
        self.cancelled = True
        self.close()

    def load_data(self, data):
        if data == "None":
            data=""
        data = data.replace("&#10;", "\n")
        data = data.replace("&amp;","&")
        data = data.replace("&amp;", "&")
        data = data.replace("&quot;","\"")
        data = data.replace("&apos;","\'")
        data = data.replace("&lt;","<")
        data = data.replace("&#x9;","\t")
        data = data.replace("&gt;",">")
        self.link_input.setText(data)
    def get_data(self):
        data = self.link_input.text().strip()
        data = data.replace("&", "&amp;")
        data = data.replace("\n", "&#10;")
        data = data.replace("\"", "&quot;")
        data = data.replace("\'", "&apos;")
        data = data.replace("\n", "&#10;")
        data = data.replace("<", "&lt;")
        data = data.replace("\t", "&#x9;")
        data = data.replace(">", "&gt;")
        data = data.replace(",", " ")
        if data == "":
            data = "None"
        self.cancelled = False
        self.close()
        return data