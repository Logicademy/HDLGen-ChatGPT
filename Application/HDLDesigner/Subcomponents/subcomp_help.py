#Displays the assoicated help markdown file
import markdown as md
from PySide2.QtWidgets import *

COMP_HELP_DOC_FILE_PATH = "./HDLDesigner/Subcomponents/subcomp_help.md"


class SubcompHelpDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("HDLGen Help")

        self.markdown_view = QTextBrowser(readOnly=True)
        self.markdown_view.setOpenExternalLinks(True)

        self.mainLayout = QVBoxLayout()
        self.setFixedSize(800, 300)
        self.setup_ui()

    def setup_ui(self):

        # Writing xml file
        with open(COMP_HELP_DOC_FILE_PATH, "r") as f:
           doc = md.markdown(f.read(),  extensions=['fenced_code', 'codehilite', 'tables', 'attr_list'])
        self.markdown_view.setHtml(doc)
        self.mainLayout.addWidget(self.markdown_view)
        self.setLayout(self.mainLayout)

