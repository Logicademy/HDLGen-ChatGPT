import os
import sys
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys
import configparser
sys.path.append("..")
from ProjectManager.project_manager import ProjectManager


WHITE_COLOR = "color: white"

class CompDetails(QWidget):

    def __init__(self, proj_dir):
        super().__init__()

        self.proj_dir = proj_dir

        self.mainLayout = QVBoxLayout()

        self.input_layout = QGridLayout()

        self.comp_name_label = QLabel("Component Name*")
        self.comp_name_label.setStyleSheet(WHITE_COLOR)
        self.comp_name_input = QLineEdit()

        self.comp_title_label = QLabel("Single Line Title")
        self.comp_title_label.setStyleSheet(WHITE_COLOR)
        self.comp_title_input = QLineEdit()

        self.comp_description_label = QLabel("Component Description")
        self.comp_description_label.setStyleSheet(WHITE_COLOR)
        self.comp_description_input = QPlainTextEdit()
        self.comp_description_input.setLineWrapMode(QPlainTextEdit.WidgetWidth)

        self.comp_author_label = QLabel("Authors")
        self.comp_author_label.setStyleSheet(WHITE_COLOR)
        self.comp_author_input = QLineEdit()

        self.comp_company_label = QLabel("Company")
        self.comp_company_label.setStyleSheet(WHITE_COLOR)
        self.comp_company_input = QLineEdit()

        self.comp_email_label = QLabel("Email")
        self.comp_email_label.setStyleSheet(WHITE_COLOR)
        self.comp_email_input = QLineEdit()

        self.comp_date_label = QLabel("Date")
        self.comp_date_label.setStyleSheet(WHITE_COLOR)

        self.save_btn = QPushButton("Save")
        self.save_btn.setFixedSize(60, 30)
        self.save_btn.setStyleSheet(
            "QPushButton {background-color: rgb(169,169,169);  color: black; border-radius: 8px; border-style: plain;}"
            "QPushButton:enabled {background-color: white; color: black; border-radius: 8px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}")
        self.save_btn.setEnabled(False)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setFixedSize(60, 30)
        self.reset_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}")

        self.btn_layout = QHBoxLayout()

        self.vspacer = QSpacerItem(30, 40)

        self.comp_date_picker = QDateEdit(calendarPopup=True)
        self.comp_date_picker.setDate(QDate.currentDate())
        self.input_frame = QFrame()
        self.setup_ui()
        if proj_dir != None:
            self.load_data(proj_dir)

    def setup_ui(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        author = config.get('user', 'author').strip()
        email = config.get('user', 'email').strip()
        company = config.get('user', 'company').strip()
        self.comp_author_input.setText(author)
        self.comp_email_input.setText(email)
        self.comp_company_input.setText(company)
        self.input_layout.addWidget(self.comp_name_label, 0, 0)
        self.input_layout.addWidget(self.comp_name_input, 1, 0, 1, 2)
        self.comp_name_input.setText(ProjectManager.get_proj_name())
        self.comp_name_input.textChanged.connect(self.enable_save_btn)
        self.comp_title_input.setText("To be Completed")
        self.input_layout.addWidget(self.comp_title_label, 2, 0)
        self.input_layout.addWidget(self.comp_title_input, 3, 0, 1, 2)

        self.comp_description_input.setFixedHeight(50)
        self.comp_description_input.setPlainText("To be Completed")
        self.input_layout.addWidget(self.comp_description_label, 4, 0)
        self.input_layout.addWidget(self.comp_description_input, 5, 0, 2, 2)

        self.input_layout.addWidget(self.comp_author_label, 7, 0)
        self.input_layout.addWidget(self.comp_author_input, 8, 0, 1, 1)

        self.input_layout.addWidget(self.comp_company_label, 7, 1)
        self.input_layout.addWidget(self.comp_company_input, 8, 1, 1, 1)

        self.input_layout.addWidget(self.comp_email_label, 9, 0)
        self.input_layout.addWidget(self.comp_email_input, 10, 0, 1, 1)

        self.input_layout.addWidget(self.comp_date_label, 9, 1)
        self.input_layout.addWidget(self.comp_date_picker, 10, 1, 1, 1)

        self.btn_layout.addWidget(self.reset_btn)
        self.btn_layout.addWidget(self.save_btn)

        self.save_btn.clicked.connect(self.save_comp_details)
        self.reset_btn.clicked.connect(self.reset_comp_details)

        self.input_layout.addItem(self.vspacer, 11, 0, 1, 2)
        self.input_layout.addLayout(self.btn_layout, 12, 1)

        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(30, 30, 30, 25)
        self.input_frame.setFixedSize(500, 400)
        self.input_frame.setLayout(self.input_layout)

        self.mainLayout.addWidget(self.input_frame, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)

    def enable_save_btn(self):
        if self.comp_name_input.text() != "":
            self.save_btn.setEnabled(True)
        else:
            self.save_btn.setEnabled(False)

    def update_comp_name(self):
        self.comp_name_input.setText(ProjectManager.get_proj_name())

    def save_comp_details(self):

        xml_data_path = ProjectManager.get_xml_data_path()

        root = minidom.parse(xml_data_path)
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")

        comp_name = self.comp_name_input.text()
        if comp_name == "":
            comp_name = "null"
        comp_title = self.comp_title_input.text()
        if comp_title == "":
            comp_title = "null"
        cursor = self.comp_description_input.textCursor()
        doc = self.comp_description_input.document()
        lines = ""
        line = ""
        for i in range(doc.blockCount()):
            block = doc.findBlockByNumber(i)
            if block.isVisible():
                print(block.layout().lineCount())
                for j in range(block.layout().lineCount()):
                    lineStart = block.position() + block.layout().lineAt(j).textStart()
                    lineEnd = lineStart + block.layout().lineAt(j).textLength()
                    cursor.setPosition(lineStart)
                    cursor.setPosition(lineEnd, QTextCursor.KeepAnchor)
                    line += cursor.selectedText()
                    print(line)
                    if lineEnd == cursor.position():
                        print(line)
                        lines += line + "\n"
                        line = ""
        lines = lines.strip()
        comp_description = lines#self.comp_description_input.toPlainText()
        if comp_description == "":
            comp_description = "null"
        comp_authors = self.comp_author_input.text().strip()
        if comp_authors == "":
            comp_authors = "null"
        comp_company = self.comp_company_input.text().strip()
        if comp_company == "":
            comp_company = "null"
        comp_email = self.comp_email_input.text().strip()
        if comp_email == "":
            comp_email = "null"
        comp_date = self.comp_date_picker.text()

        header = hdlDesign[0].getElementsByTagName('header')

        header[0].getElementsByTagName('compName')[0].firstChild.data = comp_name
        header[0].getElementsByTagName('title')[0].firstChild.data = comp_title
        comp_description = comp_description.replace("\n", "&#10;")
        header[0].getElementsByTagName('description')[0].firstChild.data = comp_description
        header[0].getElementsByTagName('authors')[0].firstChild.data = comp_authors
        header[0].getElementsByTagName('company')[0].firstChild.data = comp_company
        header[0].getElementsByTagName('email')[0].firstChild.data = comp_email
        header[0].getElementsByTagName('date')[0].firstChild.data = comp_date

        # converting the doc into a string in xml format
        xml_str = root.toprettyxml()
        xml_str = os.linesep.join([s for s in xml_str.splitlines() if s.strip()])

        # Writing xml file
        with open(xml_data_path, "w") as f:
            f.write(xml_str)

        print("Successfully saved!")

    def reset_comp_details(self):

        self.comp_name_input.clear()
        self.comp_title_input.clear()
        self.comp_description_input.clear()
        self.comp_author_input.clear()
        self.comp_company_input.clear()
        self.comp_email_input.clear()
        self.comp_date_picker.setDate(QDate.currentDate())
        print("reset button clicked")

    def load_data(self, proj_dir):

        root = minidom.parse(proj_dir[0])
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")

        header = hdlDesign[0].getElementsByTagName('header')

        comp_name = header[0].getElementsByTagName('compName')[0].firstChild.data
        comp_title = header[0].getElementsByTagName('title')[0].firstChild.data
        comp_description = header[0].getElementsByTagName('description')[0].firstChild.data
        comp_description = comp_description.replace("&#10;", "\n")
        comp_authors = header[0].getElementsByTagName('authors')[0].firstChild.data
        comp_company = header[0].getElementsByTagName('company')[0].firstChild.data
        comp_email = header[0].getElementsByTagName('email')[0].firstChild.data
        comp_date = header[0].getElementsByTagName('date')[0].firstChild.data

        if comp_name != "null":
            self.comp_name_input.setText(comp_name)
            self.enable_save_btn()

        if comp_title != "null":
            self.comp_title_input.setText(comp_title)

        if comp_description != "null":
            self.comp_description_input.setPlainText(comp_description)

        if comp_authors != "null":
            self.comp_author_input.setText(comp_authors)

        if comp_company != "null":
            self.comp_company_input.setText(comp_company)

        if comp_email != "null":
            self.comp_email_input.setText(comp_email)

        if comp_date != "null":
            self.comp_date_picker.setDate(QDate.fromString(comp_date))
