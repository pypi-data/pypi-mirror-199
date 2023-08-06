from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton

from devoud.browser.page.embedded.view import EmbeddedView
from devoud.browser.widgets.container import ContainerWidget


class NotFoundPage(EmbeddedView):
    def __init__(self, abstract_page, url='devoud://notfound.py', *args):
        super().__init__(abstract_page, url, *args)
        self.main_layout = QVBoxLayout(self)
        self.url = url
        self.title = 'Страница не найдена'
        self.error_widget = ContainerWidget(self, 'Ошибка загрузки')
        self.error_widget.setFixedSize(QSize(600, 200))
        self.error_widget.warning_img = QLabel(self)
        self.error_widget.warning_img.setPixmap(QPixmap("icons:warning.svg"))
        self.error_widget.warning_img.setFixedSize(85, 85)
        self.error_widget.warning_img.setScaledContents(True)
        self.error_widget.content_layout.addWidget(self.error_widget.warning_img, 0, 1)

        self.error_widget.label = QLabel(self, text='Страница не найдена(')
        self.error_widget.label.mousePressEvent = lambda e: self.error_widget.label.setText('Vasily ate cheese')  # Спасибо Егору
        self.error_widget.label.setStyleSheet("font-size: 24px")
        self.error_widget.content_layout.addWidget(self.error_widget.label, 0, 2)

        self.error_widget.reload_select_button = QPushButton(self, text='Перезагрузить')
        self.error_widget.reload_select_button.setFixedSize(120, 22)
        self.error_widget.reload_select_button.setObjectName('page_title_button')
        self.error_widget.reload_select_button.clicked.connect(self.abstract_page.reload)
        self.error_widget.title_layout.addWidget(self.error_widget.reload_select_button)

        self.main_layout.addWidget(self.error_widget, 0, Qt.AlignCenter)
