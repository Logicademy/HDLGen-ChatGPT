#Called in generation.py used for editing the ChatGPT Prompt header
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import yaml

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"

class VerilogModelDialog(QDialog):

    def __init__(self, add_or_edit, data=None):
        super().__init__()

        self.setWindowTitle("ChatGPT Verilog Model Command")
        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)
        input_font = QFont()
        input_font.setPointSize(10)
        self.input_layout = QGridLayout()
        self.mainLayout = QVBoxLayout()

        self.ChatGPT_model_label = QLabel("ChatGPT Model Commands")
        self.ChatGPT_model_label.setStyleSheet(WHITE_COLOR)
        self.ChatGPT_model_label.setFont(input_font)
        self.ChatGPT_model_input = QPlainTextEdit()
        self.ChatGPT_model_input.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        self.ChatGPT_model_input.setFont(input_font)


        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setFont(input_font)
        self.reset_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}")

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

        self.setup_ui()

        self.load_data()

    def setup_ui(self):
        self.input_layout.addWidget(self.ChatGPT_model_label, 0, 0, 1, 4)
        self.input_layout.addWidget(self.ChatGPT_model_input, 1, 0, 4, 4)
        self.input_layout.addWidget(self.reset_btn, 5, 1, 1, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.cancel_btn, 5, 2, 1, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 5, 3, 1, 1, alignment=Qt.AlignRight)
        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setFixedSize(900, 800)
        self.input_frame.setLayout(self.input_layout)
        self.cancel_btn.clicked.connect(self.cancel_selected)

        self.mainLayout.addWidget(self.input_frame, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)
        self.ok_btn.clicked.connect(self.get_data)
        self.reset_btn.clicked.connect(self.reset)

    def cancel_selected(self):
        self.cancelled = True
        self.close()

    def load_data(self):
        with open('prompts.yml', 'r') as prompts:
            self.config = yaml.safe_load(prompts)
                
        data = self.config["verilogchatgptmodel"]

        self.ChatGPT_model_input.setPlainText(data)

    def get_data(self):
        data = self.ChatGPT_model_input.toPlainText().strip()
        self.cancelled = False
        self.close()
        return data
    
    def reset(self):
        with open('prompts.yml', 'r') as prompts:
            self.config = yaml.safe_load(prompts)
                
        data = self.config["verilogchatgptmodelreset"]
       
        self.ChatGPT_model_input.setPlainText(data)