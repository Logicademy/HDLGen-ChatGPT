#Dialog box for note called by concurrenentstmt_dialog.py or process_dialog.py
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import sys

sys.path.append("..")

BLACK_COLOR = "color: black"
WHITE_COLOR = "color: white"


class note_Dialog(QDialog):

    def __init__(self, add_or_edit, noteType, note_data=None):
        super().__init__()

        self.input_layout = QGridLayout()
        self.setWindowTitle(noteType)
        self.noteType = noteType
        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        bold_font = QFont()
        bold_font.setBold(True)
        input_font = QFont()
        input_font.setPointSize(10)
        self.mainLayout = QVBoxLayout()

        self.note_label = QLabel(noteType)
        self.note_label.setFont(input_font)
        self.note_label.setStyleSheet(WHITE_COLOR)
        self.note_input = QPlainTextEdit()
        self.note_input.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.note_input.setFont(input_font)

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
        if add_or_edit == "edit" and note_data is not None:
            self.load_sig_data(note_data)

    def setup_ui(self):

        self.input_layout.addWidget(self.note_label, 0, 0, 1, 1)
        self.input_layout.addWidget(self.note_input, 1, 0, 4, 3)
        self.input_layout.addWidget(self.cancel_btn, 6, 1, 1, 1, alignment=Qt.AlignRight)
        self.input_layout.addWidget(self.ok_btn, 6, 2, 1, 1, alignment=Qt.AlignRight)

        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setStyleSheet('.QFrame{background-color: rgb(97, 107, 129); border-radius: 5px;}')
        self.input_frame.setContentsMargins(10, 10, 10, 10)
        self.input_frame.setLayout(self.input_layout)
        if self.noteType == "Concurrent Statement Custom Value":
            self.input_frame.setFixedSize(700, 350)
        else:
            self.input_frame.setFixedSize(700, 700)

        self.ok_btn.clicked.connect(self.get_data)
        self.cancel_btn.clicked.connect(self.cancel_selected)

        self.mainLayout.addWidget(self.input_frame, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)


    def load_sig_data(self, note_data):
        if note_data == "None":
            note_data=""
        note_data = note_data.replace("&#10;", "\n")
        note_data = note_data.replace("&amp;","&")
        note_data = note_data.replace("&amp;", "&")
        note_data = note_data.replace("&quot;","\"")
        note_data = note_data.replace("&apos;","\'")
        note_data = note_data.replace("&lt;","<")
        note_data = note_data.replace("&#x9;","\t")
        note_data = note_data.replace("&gt;",">")
        note_data = note_data.replace("&#44;",",")
        self.note_input.setPlainText(note_data)

    def get_data(self):
        data = self.note_input.toPlainText().strip()
        cursor = self.note_input.textCursor()
        doc = self.note_input.document()
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
        data = lines
        data=data.replace("&","&amp;")
        data=data.replace("\n", "&#10;")
        data = data.replace("\"", "&quot;")
        data = data.replace("\'", "&apos;")
        data = data.replace("\n", "&#10;")
        data = data.replace("<", "&lt;")
        data = data.replace("\t", "&#x9;")
        data = data.replace(">", "&gt;")
        data=data.replace(",","&#44;")
        if data == "":
            data = "None"
        self.cancelled = False
        self.close()
        return data

    def cancel_selected(self):
        self.cancelled = True
        self.close()
