from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QLabel, QPushButton


class TreeWidget(QTreeWidget):
    def __init__(self, container, headers: list = None):
        super().__init__(container)
        if headers:
            self.setHeaderItem(QTreeWidgetItem(headers))
        self.header().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)

        self.count = 0
        self.empty_info_label = QLabel()
        self.empty_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container.content_layout.addWidget(self.empty_info_label, 0, 0)

        self.remove_all_button = QPushButton(self.parent(), icon=QIcon('custom:clean(container_title_btn).svg'),
                                             text='Очистить всё')
        self.remove_all_button.setFixedSize(120, 22)
        self.remove_all_button.setObjectName('container_title_button')
        self.remove_all_button.clicked.connect(self.remove_all)
        container.title_layout.addWidget(self.remove_all_button)

        self.hide()

    def context_menu(self, event):
        ...

    def show_empty_message(self):
        self.empty_info_label.setHidden(self.count)
        self.setHidden(not self.count)

    def add(self):
        ...

    def remove(self):
        ...

    def remove_all(self):
        ...
