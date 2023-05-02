import os
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys
import qtawesome as qta
sys.path.append("..")
from HDLDesigner.ChatGPT.chatgpt_help import ChatGPTHelpDialog


WHITE_COLOR = "color: white"
BLACK_COLOR = "color: black"

class ChatGPT(QWidget):
    save_signal = Signal(bool)

    def __init__(self, proj_dir):
        super().__init__()
        small_text_font = QFont()
        small_text_font.setPointSize(10)
        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        self.proj_dir = proj_dir

        self.mainLayout = QVBoxLayout()

        self.input_layout = QGridLayout()

        self.testplan_label = QLabel("Test Plan")
        self.testplan_label.setFont(title_font)
        self.testplan_label.setStyleSheet(WHITE_COLOR)

        self.chatgpt_info_btn = QPushButton()
        self.chatgpt_info_btn.setIcon(qta.icon("mdi.help"))
        self.chatgpt_info_btn.setFixedSize(25, 25)
        self.chatgpt_info_btn.clicked.connect(self.chatgpt_help_window)

        self.top_layout = QGridLayout()
        self.arch_action_layout = QVBoxLayout()
        self.btn_layout = QHBoxLayout()

        self.vspacer = QSpacerItem(30, 40)
        self.list_layout = QVBoxLayout()
        self.list_frame = QFrame()
        self.main_frame = QFrame()
        self.input_frame = QFrame()
        self.setup_ui()
        #if proj_dir != None:
            #self.load_data(proj_dir)

    def setup_ui(self):
        bold_font = QFont()
        bold_font.setBold(True)

        self.top_layout.addWidget(self.testplan_label, 0, 0, 1, 1)
        self.top_layout.addWidget(self.chatgpt_info_btn, 0, 1, 1, 1)
        self.arch_action_layout.addLayout(self.top_layout)

        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        # self.main_frame.setFixedSize(500, 400)

        self.main_frame.setLayout(self.arch_action_layout)

        self.list_frame.setFrameShape(QFrame.StyledPanel)
        self.list_frame.setStyleSheet('.QFrame{background-color: white; border-radius: 5px;}')
        # self.list_frame.setFixedSize(420, 300)
        self.list_frame.setLayout(self.list_layout)

        self.arch_action_layout.addItem(QSpacerItem(0, 5))
        self.arch_action_layout.addWidget(self.list_frame)  # , alignment=Qt.AlignCenter)
        self.arch_action_layout.addItem(QSpacerItem(0, 5))

        self.mainLayout.addWidget(self.main_frame)  # , alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)

    def chatgpt_help_window(self):
        chatgpt_help_dialog = ChatGPTHelpDialog()
        chatgpt_help_dialog.exec_()


