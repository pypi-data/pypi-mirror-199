from PySide6.QtCore import QTimer
from PySide6.QtGui import QKeySequence, Qt
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWidgets import QWidget, QCheckBox, QPushButton, QHBoxLayout

from devoud.browser.widgets.line_edit import LineEdit


class FindOnPageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('find_widget')
        self.setFixedHeight(50)
        self.setLayout(QHBoxLayout())

        self.page_view = self.parent().view

        self.line_edit = LineEdit(self)
        self.line_edit.setObjectName('find_widget_edit')
        self.line_edit.setClearButtonEnabled(True)
        self.line_edit.setPlaceholderText("Найти на странице...")
        self.line_edit.focusInEvent = self._line_edit_focus
        self.line_edit.textChanged.connect(self.find_text)
        self.layout().addWidget(self.line_edit)

        self.case_sensitive_checkbox = QCheckBox('Учитывать регистр')
        self.case_sensitive_checkbox.setObjectName('find_widget_checkbox')
        self.case_sensitive_checkbox.stateChanged.connect(self.find_text)
        self.layout().addWidget(self.case_sensitive_checkbox)

        self.previous_button = QPushButton(self)
        self.previous_button.setObjectName('find_widget_back')
        self.previous_button.clicked.connect(lambda: self.find_text(backward=True))
        self.layout().addWidget(self.previous_button)

        self.next_button = QPushButton(self)
        self.next_button.setObjectName('find_widget_forward')
        self.next_button.clicked.connect(self.find_text)
        self.layout().addWidget(self.next_button)

        self.hide_button = QPushButton(self)
        self.hide_button.setObjectName('find_widget_close')
        self.hide_button.setText('Закрыть')
        self.hide_button.setShortcut(QKeySequence(Qt.Key_Escape))
        self.hide_button.clicked.connect(self.hide)
        self.layout().addWidget(self.hide_button)

    def _line_edit_focus(self, event):
        QTimer.singleShot(0, self.line_edit.selectAll)
        super().focusInEvent(event)

    def show(self):
        self.line_edit.setFocus()
        text = self.page_view.selectedText()
        if text != '':
            self.line_edit.setText(text)
        super().show()

    def find_text(self, backward=False):
        text = self.line_edit.text().strip()
        flags = QWebEnginePage.FindFlags()
        if self.case_sensitive_checkbox.isChecked():
            flags |= QWebEnginePage.FindCaseSensitively
        if backward:
            flags |= QWebEnginePage.FindBackward
        self.page_view.findText(text, flags)

    def hide(self):
        self.page_view.findText('')
        super().hide()
