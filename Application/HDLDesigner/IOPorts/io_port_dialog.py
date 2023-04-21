import os
import sys
from xml.dom import minidom

from PySide2 import QtWidgets
from PySide2.QtCore import QSizeF
from PySide2.QtWidgets import *
from PySide2.QtGui import *

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"
from ProjectManager.project_manager import ProjectManager
class IOPortDialog(QDialog):

    def __init__(self, add_or_edit, signals_names, signal_data = None):
        super().__init__()

        self.input_layout = QGridLayout()

        if add_or_edit == "add":
            self.setWindowTitle("New IO Port")
        elif add_or_edit == "edit":
            self.setWindowTitle("Edit IO Port")
        self.signalNames = signals_names
        self.signalName=""
        if signal_data != None:
            self.signalName = signal_data[0]
        self.mainLayout = QVBoxLayout()

        self.sig_name_label = QLabel("Signal Name *")
        self.sig_name_label.setStyleSheet(WHITE_COLOR)
        self.sig_name_input = QLineEdit()


        self.sig_mode_label = QLabel("Mode")
        self.sig_mode_label.setStyleSheet(WHITE_COLOR)
        self.sig_mode_input = QComboBox()
        pal = self.sig_mode_input.palette()
        pal.setColor(QPalette.Button, QColor(255, 255, 255))
        self.sig_mode_input.setPalette(pal)
        self.sig_mode_input.addItem("Input")
        self.sig_mode_input.addItem("Output")

        self.sig_type_label = QLabel("Type")
        self.sig_type_label.setStyleSheet(WHITE_COLOR)
        self.sig_type_input = QComboBox()
        pal = self.sig_type_input.palette()
        pal.setColor(QPalette.Button, QColor(255, 255, 255))
        self.sig_type_input.setPalette(pal)
        self.sig_type_input.addItem("single bit")
        self.sig_type_input.addItem("bus")
        self.sig_type_input.addItem(("array"))

        self.sig_size_label = QLabel("Size (eg. 32) * ")
        self.sig_size_label.setStyleSheet(WHITE_COLOR)
        self.sig_size_input = QLineEdit()
        self.sig_size_input.setText("1")
        self.sig_size_input.setEnabled(False)

        self.arrayName_label = QLabel("Arrays")
        self.arrayName_label.setStyleSheet(WHITE_COLOR)
        self.arrayName_input = QComboBox()
        pal = self.arrayName_input.palette()
        pal.setColor(QPalette.Button, QColor(255, 255, 255))
        self.arrayName_input.setPalette(pal)
        self.arrayName_label.setVisible(False)
        self.arrayName_input.setVisible(False)
        self.arrayName_input.setCurrentText("Create in packages")

        self.onlyInt = QIntValidator()
        self.sig_size_input.setValidator(self.onlyInt)

        self.sig_description_label = QLabel("Signal Description")
        self.sig_description_label.setStyleSheet(WHITE_COLOR)
        self.sig_description_input = QPlainTextEdit()#MyPlainTextEdit()#QPlainTextEdit()#QLineEdit()
        self.sig_description_input.setLineWrapMode(QPlainTextEdit.WidgetWidth)


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
        self.arrays=[]
        self.setup_ui()
        mainPackageDir = os.getcwd() + "\HDLDesigner\Package\mainPackage.hdlgen"

        root = minidom.parse(mainPackageDir)
        HDLGen = root.documentElement
        hdlDesign = HDLGen.getElementsByTagName("hdlDesign")
        mainPackage = hdlDesign[0].getElementsByTagName("mainPackage")
        array_nodes = mainPackage[0].getElementsByTagName('array')


        if len(array_nodes) != 0:
            for i in range(0, len(array_nodes)):
                array_name = array_nodes[i].getElementsByTagName('name')[0].firstChild.data
                self.arrays.append(array_name)
        self.arrayName_input.addItems(self.arrays)

        if add_or_edit == "edit" and signal_data != None:
            self.load_signal_data(signal_data)

    def setup_ui(self):
        self.input_layout.addWidget(self.sig_name_label, 0, 0, 1, 1)
        self.input_layout.addWidget(self.sig_name_input, 1, 0, 1, 1)
        self.input_layout.addWidget(self.sig_mode_label, 0, 1, 1, 1)
        self.input_layout.addWidget(self.sig_mode_input, 1, 1, 1, 1)
        self.input_layout.addWidget(self.sig_type_label, 2, 0, 1, 1)
        self.input_layout.addWidget(self.sig_type_input, 3, 0, 1, 1)
        self.input_layout.addWidget(self.sig_size_label, 2, 1, 1, 1)
        self.input_layout.addWidget(self.sig_size_input, 3, 1, 1, 1)
        self.input_layout.addWidget(self.arrayName_label, 2, 1, 1, 1)
        self.input_layout.addWidget(self.arrayName_input, 3, 1, 1, 1)
        self.input_layout.addWidget(self.sig_description_label, 4, 0, 1, 2)
        self.input_layout.addWidget(self.sig_description_input, 5, 0, 1, 2)
        self.input_layout.addItem(QSpacerItem(0, 20), 6, 0, 1, 2)
        self.input_layout.addWidget(self.cancel_btn, 7, 0, 1, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 7, 1, 1, 1, alignment=Qt.AlignRight)

        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setFixedSize(400, 400)
        self.input_frame.setLayout(self.input_layout)

        self.sig_name_input.textChanged.connect(self.enable_ok_btn);
        self.sig_size_input.textChanged.connect(self.enable_ok_btn);
        self.sig_type_input.currentTextChanged.connect(self.enable_size_option)
        self.sig_type_input.currentTextChanged.connect(self.sig_type_options)
        self.ok_btn.clicked.connect(self.get_signals)
        self.cancel_btn.clicked.connect(self.cancel_selected)

        self.mainLayout.addWidget(self.input_frame, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)

    def get_signals(self):
        cursor = self.sig_description_input.textCursor()
        doc = self.sig_description_input.document()
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
                        lines += line+"\n"
                        line = ""
        lines=lines.strip()
        signalDescription=lines
        signalDescription = signalDescription.replace("\n", "&#10;")
        if signalDescription == "":
            signalDescription = "to be completed"
        if self.sig_type_input.currentText() == "array":
            typeValue= "array,"+self.arrayName_input.currentText()
        else:
            typeValue= self.sig_type_input.currentText()
        sig_details = [self.sig_name_input.text().strip().replace(" ", ""),
                       self.sig_mode_input.currentText(),
                       typeValue,
                       self.sig_size_input.text(),
                       signalDescription
                       ]
        self.cancelled = False
        self.close()
        return sig_details

    def load_signal_data(self, signal_data):
        self.sig_name_input.setText(signal_data[0])
        self.sig_mode_input.setCurrentText(signal_data[1])
        sig_type=signal_data[2]
        if sig_type != "bus" and signal_data[2] != "single bit":
            sig_type = "array"
            arrayname = signal_data[2].split(",")
            self.arrayName_input.setCurrentText(arrayname[1])
        self.sig_type_input.setCurrentText(sig_type)
        self.sig_size_input.setText(signal_data[3])
        signal_data[4] = signal_data[4].replace("&#10;", "\n")
        self.sig_description_input.setPlainText(signal_data[4])

    def cancel_selected(self):
        self.cancelled = True
        self.close()

    def enable_ok_btn(self):
        if self.sig_name_input.text() != "" and self.sig_size_input.text() != "" and (self.sig_name_input.text() not in self.signalNames or (self.sig_name_input.text() == self.signalName and self.sig_name_input.text() != "")):
            self.ok_btn.setEnabled(True)
        else:
            if self.sig_name_input.text() != "" and self.sig_type_input.currentText() == "array" and self.arrayName_input.currentText() != "":
                self.ok_btn.setEnabled(True)
            else:
                self.ok_btn.setEnabled(False)

    def enable_size_option(self):
        if self.sig_type_input.currentText() == "bus":
            self.sig_size_input.setEnabled(True)
            self.sig_size_input.clear()
        else:
            self.sig_size_input.setEnabled(False)
            self.sig_size_input.setText("1")
    def sig_type_options(self):
        if self.sig_type_input.currentText() == "array":
            self.arrayName_label.setVisible(True)
            self.arrayName_input.setVisible(True)
            self.sig_size_input.setVisible(False)
            self.sig_size_label.setVisible(False)

        else:
            self.sig_size_input.setVisible(True)
            self.sig_size_label.setVisible(True)
            self.arrayName_label.setVisible(False)
            self.arrayName_input.setVisible(False)
