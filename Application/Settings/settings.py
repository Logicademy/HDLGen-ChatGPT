#settings dialog box when settings is clicked in main.py. Reads/writes from config.ini file default and reusable information
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import sys, yaml, configparser
# make sure to add to requirements.txt
from Settings.VHDLModelDefault import VHDLModelDefaultDialog
from Settings.VerilogModelDefault import VerilogModelDefaultDialog
sys.path.append("..")

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"

class settingsDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.commands = ["None", "None", "None", "None", "None", "None","None", "None", "None", "None"]
        self.setWindowTitle("Settings")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)
        input_font = QFont()
        input_font.setPointSize(10)

        self.input_layout = QGridLayout()
        self.mainLayout = QVBoxLayout()

        self.author_label = QLabel("Author")
        self.author_label.setStyleSheet(WHITE_COLOR)
        self.author_label.setFont(title_font)
        self.author_input = QLineEdit()
        self.author_input.setFont(input_font)

        self.email_label = QLabel("Email")
        self.email_label.setStyleSheet(WHITE_COLOR)
        self.email_input = QLineEdit()

        self.company_label = QLabel("Company")
        self.company_label.setStyleSheet(WHITE_COLOR)
        self.company_input = QLineEdit()

        self.vivado_label = QLabel("Vivado.bat path")
        self.vivado_label.setStyleSheet(WHITE_COLOR)
        self.vivado_input = QLineEdit()

        self.quartus_label = QLabel("Quartus path")
        self.quartus_label.setStyleSheet(WHITE_COLOR)
        self.quartus_input = QLineEdit()

        self.header_VHDL = QPushButton("VHDL Title Section Command")
        #self.header_VHDL.setFixedSize(200, 25)
        self.header_VHDL.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}")
        self.model_VHDL = QPushButton("VHDL Model Command")
        #self.model_VHDL.setFixedSize(250, 25)
        self.model_VHDL.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}")
        self.header_Verilog = QPushButton("Verilog Title Section Command")
        #self.header_Verilog.setFixedSize(200, 25)
        self.header_Verilog.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}")
        self.model_Verilog = QPushButton("Verilog Model Command")
       # self.model_Verilog.setFixedSize(250, 25)
        self.model_Verilog.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}")
        self.browse_btn = QPushButton("Browse")
        #self.browse_btn.setFixedSize(80, 25)
        self.browse_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}")
        self.quartus_browse_btn = QPushButton("Browse")
        #self.quartus_browse_btn.setFixedSize(80, 25)
        self.quartus_browse_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}")

        self.cancel_btn = QPushButton("Cancel")
       # self.cancel_btn.setFixedSize(60, 25)
        self.cancel_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}")


        self.ok_btn = QPushButton("Ok")
        #self.ok_btn.setFixedSize(60, 25)
        self.ok_btn.setStyleSheet(
            "QPushButton {background-color: rgb(169,169,169);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;padding: 10px;}"
            "QPushButton:enabled {background-color: white; color: black; border-radius: 8px; border-style: plain;padding: 10px; }")
        self.input_frame = QFrame()

        self.cancelled = True
        self.config = configparser.ConfigParser()
        self.vivado_label.setFont(title_font)
        self.email_label.setFont(title_font)
        self.company_label.setFont(title_font)
        self.quartus_label.setFont(title_font)
        self.vivado_input.setFont(input_font)
        self.email_input.setFont(input_font)
        self.company_input.setFont(input_font)
        self.quartus_input.setFont(input_font)
        self.browse_btn.setFont(input_font)
        self.quartus_browse_btn.setFont(input_font)
        self.model_VHDL.setFont(input_font)
        self.model_Verilog.setFont(input_font)
        self.ok_btn.setFont(input_font)
        self.cancel_btn.setFont(input_font)
        self.setup_ui()

    def setup_ui(self):
        self.config.read('config.ini')

        with open('prompts.yml', 'r') as prompts:
            self.prompts = yaml.safe_load(prompts)

        vivadoPath= self.config.get('user', 'vivado.bat')
        quartusPath = self.config.get('user','quartus')
        author = self.config.get('user', 'author')
        email = self.config.get('user', 'email')
        company = self.config.get('user', 'company')

        self.commands[0] = self.prompts["vhdlchatgptmodel"]
        self.commands[1] = self.prompts["verilogchatgptmodel"]
        self.commands[2] = self.prompts["vhdlchatgptmodelreset"]
        self.commands[3] = self.prompts["verilogchatgptmodelreset"]

        self.vivado_input.setText(vivadoPath.strip())
        self.quartus_input.setText(quartusPath.strip())
        self.author_input.setText(author.strip())
        self.email_input.setText(email.strip())
        self.company_input.setText(company.strip())
        self.input_layout.addWidget(self.author_label, 0, 0, 1, 1)
        self.input_layout.addWidget(self.author_input, 1, 0, 1, 1)
        self.input_layout.addWidget(self.email_label, 0, 1, 1, 1)
        self.input_layout.addWidget(self.email_input, 1, 1, 1, 1)
        self.input_layout.addWidget(self.company_label, 0, 2, 1, 2)
        self.input_layout.addWidget(self.company_input, 1, 2, 1, 2)
        self.input_layout.addWidget(self.vivado_label, 2, 0, 1, 3)
        self.input_layout.addWidget(self.vivado_input, 3, 0, 1, 3)
        self.input_layout.addWidget(self.browse_btn, 3, 3, 1, 1)
        self.input_layout.addWidget(self.quartus_label, 4, 0, 1, 3)
        self.input_layout.addWidget(self.quartus_input, 5, 0, 1, 3)
        self.input_layout.addWidget(self.quartus_browse_btn, 5, 3, 1, 1)
        self.input_layout.addWidget(self.model_VHDL, 6, 0)
        self.input_layout.addWidget(self.model_Verilog, 6, 1)
        #self.header_VHDL.clicked.connect(self.vhdl_header_command)
        #self.header_Verilog.clicked.connect(self.verilog_header_command)
        self.model_VHDL.clicked.connect(self.vhdl_model_command)
        self.model_Verilog.clicked.connect(self.verilog_model_command)

        self.input_layout.addWidget(self.cancel_btn, 9, 2, 1, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 9, 3, 1, 1, alignment=Qt.AlignRight)
        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setFixedSize(1000, 500)
        self.input_frame.setLayout(self.input_layout)
        self.cancel_btn.clicked.connect(self.cancel)

        self.mainLayout.addWidget(self.input_frame, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)
        self.browse_btn.clicked.connect(self.set_vivado_bat_path)
        self.quartus_browse_btn.clicked.connect(self.set_quartus_exe_path)
        self.ok_btn.clicked.connect(self.save)
    
    def set_vivado_bat_path(self):
        vivado_bat_path = QFileDialog.getOpenFileName(self,"Select Xilinx Vivado Batch file (vivado.bat)","C:/", filter="Batch (*.bat)")
        vivado_bat_path = vivado_bat_path[0]
        self.vivado_input.setText(vivado_bat_path)

    def set_quartus_exe_path(self):
        quartus_exe_path = QFileDialog.getOpenFileName(self,"Select Quartus Exe file (quartus_map.exe)","C:/", filter="Batch (*.exe)")
        quartus_exe_path = quartus_exe_path[0]
        self.quartus_input.setText(quartus_exe_path)

    def cancel(self):
        self.cancelled = True
        self.close()

    def enable_ok_btn(self):
        if self.vivado_input.text() != "" and self.vivado_input.text() != "To be completed":
            self.ok_btn.setEnabled(True)
        else:
            self.ok_btn.setEnabled(False)

    def save(self):
        if self.vivado_input.text().strip() == "":
            self.vivado_input.setText("To be completed")
        if self.quartus_input.text().strip() == "":
            self.quartus_input.setText("To be completed")
        if self.author_input.text().strip() == "":
            self.author_input.setText("To be completed")
        if self.email_input.text().strip() == "":
            self.email_input.setText("To be completed")
        if self.company_input.text().strip() == "":
            self.company_input.setText("To be completed")

        self.config.set("user", "author", self.author_input.text())
        self.config.set("user", "email", self.email_input.text())
        self.config.set("user", "company", self.company_input.text())
        self.config.set("user", "vivado.bat", self.vivado_input.text())
        self.config.set("user", "quartus", self.quartus_input.text())

        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

        with open('prompts.yml', 'r') as prompts:
            self.prompts = yaml.safe_load(prompts)

        self.prompts["vhdlchatgptmodel"] = self.commands[0]
        self.prompts["verilogchatgptmodel"] = self.commands[1]

        with open('prompts.yml', 'w') as prompts:
            yaml.dump(self.prompts, prompts)

        self.cancelled = False
        self.close()

    def vhdl_model_command(self):
        vhdl_model = VHDLModelDefaultDialog("edit", self.commands[0], self.commands[2])
        vhdl_model.exec_()

        if not vhdl_model.cancelled:
            vhdl_model = vhdl_model.get_data()
            self.commands[0] = vhdl_model

    def verilog_model_command(self):
        verilog_model = VerilogModelDefaultDialog("edit", self.commands[1], self.commands[3])
        verilog_model.exec_()

        if not verilog_model.cancelled:
            verilog_model = verilog_model.get_data()
            self.commands[1] = verilog_model