import os
import sys
import webbrowser
from xml.dom import minidom
import markdown as md

from PySide2.QtCore import QUrl
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtWebEngineWidgets import *

HELP_DOC_FILE_PATH = "E:\BE_Project\Project\Project_files\HDLGen_files\HDLGen\Docs\help.md"

class Help(QWidget):

    def __init__(self):
        super().__init__()

        self.webEngineView = QWebEngineView()

        self.mainLayout = QHBoxLayout()

        self.setup_ui()

    def setup_ui(self):



        # Writing xml file
        with open(HELP_DOC_FILE_PATH, "r") as f:
           doc = md.markdown(f.read(),  extensions=['fenced_code', 'codehilite', 'tables', 'attr_list'])

        webview = HtmlView()
        webview.setHtml(doc)

        self.mainLayout.addWidget(webview)
        self.setLayout(self.mainLayout)


class WebEnginePage(QWebEnginePage):
    def acceptNavigationRequest(self, url,  _type, isMainFrame):
        if _type == QWebEnginePage.NavigationTypeLinkClicked:
            QDesktopServices.openUrl(url);
            return False
        return True

class HtmlView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        QWebEngineView.__init__(self, *args, **kwargs)
        self.setPage(WebEnginePage(self))
