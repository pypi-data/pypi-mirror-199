# coding:utf-8
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QPushButton

from ...common.style_sheet import setStyleSheet


class PushButton(QPushButton):
    """ push button """

    def __init__(self, text: str, parent=None):
        super().__init__(text=text, parent=parent)
        setStyleSheet(self, 'button')


class PrimaryPushButton(PushButton):
    """ Primary color push button """


class HyperlinkButton(QPushButton):
    """ Hyperlink button """

    def __init__(self, url: str, text: str, parent=None):
        super().__init__(text, parent)
        self.url = QUrl(url)
        self.clicked.connect(lambda i: QDesktopServices.openUrl(self.url))
        setStyleSheet(self, 'button')
        self.setCursor(Qt.PointingHandCursor)