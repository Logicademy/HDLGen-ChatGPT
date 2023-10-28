#Component section in HDL Designer. This class will only call comp_help.md if help button is clicked
#This class will save all entered data to the .hdlgen. The save happens when there is a change.
import os
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys
import configparser
import qtawesome as qta
sys.path.append("..")
from ProjectManager.project_manager import ProjectManager
from HDLDesigner.comp.comp_help import CompHelpDialog


WHITE_COLOR = "color: white"

class CompDetails(QWidget):
    save_signal = Signal(bool)
    def __init__(self, proj_dir):
        super().__init__()
        small_text_font = QFont()
        small_text_font.setPointSize(10)
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        self.proj_dir = proj_dir

        self.mainLayout = QVBoxLayout()

        self.input_layout = QGridLayout()
        self.comp_label = QLabel("Component")
        self.comp_label.setFont(title_font)
        self.comp_label.setStyleSheet(WHITE_COLOR)

        self.comp_name_label = QLabel("Component Name*")
        self.comp_name_label.setStyleSheet(WHITE_COLOR)
        self.comp_name_label.setFont(small_text_font)
        self.comp_name_input = QLineEdit()
        self.comp_name_input.setFont(small_text_font)

        self.comp_info_btn = QPushButton()
        self.comp_info_btn.setIcon(qta.icon("mdi.help"))
        self.comp_info_btn.setFixedSize(25, 25)
        self.comp_info_btn.clicked.connect(self.comp_help_window)

        self.comp_title_label = QLabel("Single Line Title")
        self.comp_title_label.setStyleSheet(WHITE_COLOR)
        self.comp_title_label.setFont(small_text_font)
        self.comp_title_input = QLineEdit()
        self.comp_title_input.setFont(small_text_font)

        self.comp_description_label = QLabel("Component Description")
        self.comp_description_label.setStyleSheet(WHITE_COLOR)
        self.comp_description_label.setFont(small_text_font)
        self.comp_description_input = QPlainTextEdit()
        self.comp_description_input.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        self.comp_description_input.setFont(small_text_font)

        self.comp_author_label = QLabel("Authors")
        self.comp_author_label.setStyleSheet(WHITE_COLOR)
        self.comp_author_label.setFont(small_text_font)
        self.comp_author_input = QLineEdit()
        self.comp_author_input.setFont(small_text_font)

        self.comp_company_label = QLabel("Company")
        self.comp_company_label.setStyleSheet(WHITE_COLOR)
        self.comp_company_label.setFont(small_text_font)
        self.comp_company_input = QLineEdit()
        self.comp_company_input.setFont(small_text_font)

        self.comp_email_label = QLabel("Email")
        self.comp_email_label.setStyleSheet(WHITE_COLOR)
        self.comp_email_label.setFont(small_text_font)
        self.comp_email_input = QLineEdit()
        self.comp_email_input.setFont(small_text_font)

        self.comp_date_label = QLabel("Date")
        self.comp_date_label.setStyleSheet(WHITE_COLOR)
        self.comp_date_label.setFont(small_text_font)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setFixedSize(60, 30)
        self.reset_btn.setStyleSheet(
            "QPushButton {background-color: white; color: black; border-radius: 8px; border-style: plain; }"
            " QPushButton:pressed { background-color: rgb(250, 250, 250);  color: black; border-radius: 8px; border-style: plain;}")

        self.btn_layout = QHBoxLayout()

        self.vspacer = QSpacerItem(30, 40)

        self.comp_date_picker = QDateEdit(calendarPopup=True)
        self.comp_date_picker.setDate(QDate.currentDate())
        self.comp_date_picker.setFont(small_text_font)
        self.comp_date_picker.setDisplayFormat("dd/MM/yyyy")
        
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
        self.input_layout.addWidget(self.comp_label, 0, 0,1,1)
        self.input_layout.addWidget(self.comp_info_btn,0,1,alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.comp_name_label, 1, 0)
        self.input_layout.addWidget(self.comp_name_input, 2, 0, 1, 2)
        self.comp_name_input.setText(ProjectManager.get_proj_name())
        self.comp_title_input.setText("To be Completed")
        self.input_layout.addWidget(self.comp_title_label, 3, 0)
        self.input_layout.addWidget(self.comp_title_input, 4, 0, 1, 2)
        self.comp_description_input.setPlainText("To be Completed")
        self.input_layout.addWidget(self.comp_description_label, 5, 0)
        self.input_layout.addWidget(self.comp_description_input, 6, 0, 4, 2)

        self.input_layout.addWidget(self.comp_author_label, 10, 0)
        self.input_layout.addWidget(self.comp_author_input, 11, 0, 1, 1)

        self.input_layout.addWidget(self.comp_company_label, 10, 1)
        self.input_layout.addWidget(self.comp_company_input, 11, 1, 1, 1)

        self.input_layout.addWidget(self.comp_email_label, 12, 0)
        self.input_layout.addWidget(self.comp_email_input, 13, 0, 1, 1)

        self.input_layout.addWidget(self.comp_date_label, 12, 1)
        self.input_layout.addWidget(self.comp_date_picker, 13, 1, 1, 1)

        self.comp_description_input.textChanged.connect(self.save_data)
        self.comp_author_input.textChanged.connect(self.save_data)
        self.comp_name_input.textChanged.connect(self.save_data)
        self.comp_email_input.textChanged.connect(self.save_data)
        self.comp_title_input.textChanged.connect(self.save_data)
        self.comp_company_input.textChanged.connect(self.save_data)
        self.comp_date_picker.dateChanged.connect(self.save_data)

        self.input_layout.addItem(self.vspacer, 14, 0, 1, 2)
        self.input_layout.addLayout(self.btn_layout, 15, 1)

        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(30, 30, 30, 25)
        self.input_frame.setLayout(self.input_layout)

        self.mainLayout.addWidget(self.input_frame)

        self.setLayout(self.mainLayout)

    def update_comp_name(self):
        self.comp_name_input.setText(ProjectManager.get_proj_name())

    def save_data(self):

        xml_data_path = ProjectManager.get_xml_data_path()

        root = minidom.parse(xml_data_path)
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")

        comp_name = self.comp_name_input.text()
        if comp_name == "":
            comp_name = "To be completed"
        comp_title = self.comp_title_input.text()
        if comp_title == "":
            comp_title = "To be completed"
        cursor = self.comp_description_input.textCursor()
        doc = self.comp_description_input.document()
        lines = ""
        line = ""
        for i in range(doc.blockCount()):
            block = doc.findBlockByNumber(i)
            if block.isVisible():
                for j in range(block.layout().lineCount()):
                    lineStart = block.position() + block.layout().lineAt(j).textStart()
                    lineEnd = lineStart + block.layout().lineAt(j).textLength()
                    cursor.setPosition(lineStart)
                    cursor.setPosition(lineEnd, QTextCursor.KeepAnchor)
                    line += cursor.selectedText()
                    if lineEnd == cursor.position():
                        lines += line + "\n"
                        line = ""
        lines = lines.strip()
        comp_description = lines
        comp_authors = self.comp_author_input.text().strip()
        if comp_authors == "":
            comp_authors = "To be completed"
        comp_company = self.comp_company_input.text().strip()
        if comp_company == "":
            comp_company = "To be completed"
        comp_email = self.comp_email_input.text().strip()
        if comp_email == "":
            comp_email = "To be completed"
        comp_date = self.comp_date_picker.text()

        header = hdlDesign[0].getElementsByTagName('header')

        header[0].getElementsByTagName('compName')[0].firstChild.data = comp_name
        header[0].getElementsByTagName('title')[0].firstChild.data = comp_title

        if comp_description.count('\n') == 0:
            comp_description=self.comp_description_input.toPlainText()
        comp_description = comp_description.replace("&", "&amp;")
        comp_description = comp_description.replace("\n", "&#10;")
        comp_description = comp_description.replace("\"", "&quot;")
        comp_description = comp_description.replace("\'", "&apos;")
        comp_description = comp_description.replace("\n", "&#10;")
        comp_description = comp_description.replace("<", "&lt;")
        comp_description = comp_description.replace("\t", "&#x9;")
        comp_description = comp_description.replace(">", "&gt;")
        comp_description = comp_description.replace(",", "&#44;")

        if comp_description == "":
            comp_description = "To be completed"
        header[0].getElementsByTagName('description')[0].firstChild.data = comp_description
        header[0].getElementsByTagName('authors')[0].firstChild.data = comp_authors
        header[0].getElementsByTagName('company')[0].firstChild.data = comp_company
        header[0].getElementsByTagName('email')[0].firstChild.data = comp_email
        header[0].getElementsByTagName('date')[0].firstChild.data = comp_date

        # converting the doc into a string in xml format
        xml_str = root.toprettyxml()
        xml_str = '\n'.join([line for line in xml_str.splitlines() if line.strip()])

        # Writing xml file
        with open(xml_data_path, "w") as f:
            f.write(xml_str)
        hdl = False
        self.save_signal.emit(hdl)
        print("Saved Component details")

    def comp_help_window(self):
        comp_help_dialog = CompHelpDialog()
        comp_help_dialog.exec_()

    def reset_comp_details(self):

        self.comp_name_input.clear()
        self.comp_title_input.clear()
        self.comp_description_input.clear()
        self.comp_author_input.clear()
        self.comp_company_input.clear()
        self.comp_email_input.clear()
        self.comp_date_picker.setDate(QDate.currentDate())

    def load_data(self, proj_dir):
        root = minidom.parse(proj_dir[0])
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")

        header = hdlDesign[0].getElementsByTagName('header')

        comp_name = header[0].getElementsByTagName('compName')[0].firstChild.data
        comp_title = header[0].getElementsByTagName('title')[0].firstChild.data
        comp_description = header[0].getElementsByTagName('description')[0].firstChild.data

        comp_authors = header[0].getElementsByTagName('authors')[0].firstChild.data
        comp_company = header[0].getElementsByTagName('company')[0].firstChild.data
        comp_email = header[0].getElementsByTagName('email')[0].firstChild.data
        comp_date = header[0].getElementsByTagName('date')[0].firstChild.data

        if comp_description != "null":
            comp_description = comp_description.replace("&#10;", "\n")
            comp_description = comp_description.replace("&amp;", "&")
            comp_description = comp_description.replace("&amp;", "&")
            comp_description = comp_description.replace("&quot;", "\"")
            comp_description = comp_description.replace("&apos;", "\'")
            comp_description = comp_description.replace("&lt;", "<")
            comp_description = comp_description.replace("&#x9;", "\t")
            comp_description = comp_description.replace("&gt;", ">")
            comp_description = comp_description.replace("&#44;", ",")
            self.comp_description_input.setPlainText(comp_description)

        if comp_name != "null":
            self.comp_name_input.setText(comp_name)

        if comp_title != "null":
            self.comp_title_input.setText(comp_title)

        if comp_authors != "null":
            self.comp_author_input.setText(comp_authors)

        if comp_company != "null":
            self.comp_company_input.setText(comp_company)

        if comp_email != "null":
            self.comp_email_input.setText(comp_email)

        if comp_date != "null":
            self.comp_date_picker.setDate(QDate.fromString(comp_date))