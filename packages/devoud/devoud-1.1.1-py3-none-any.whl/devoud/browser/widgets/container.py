from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QLabel


class ContainerWidget(QWidget):
    def __init__(self, parent=None, title: str = ''):
        super().__init__(parent)
        self.title = title
        self.setObjectName('container')
        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(12, 0, 12, 0)

        self.title_widget = QWidget(self)
        self.title_widget.setObjectName('container_title')
        self.title_widget.setFixedHeight(32)
        self.title_layout = QHBoxLayout(self.title_widget)
        self.title_layout.setContentsMargins(6, 0, 10, 0)
        self.title_label = QLabel(self, text=self.title)
        self.title_label.setObjectName('container_title_text')
        self.title_layout.addWidget(self.title_label)
        self.layout.addWidget(self.title_widget)

        self.content = QWidget(self)
        self.content.setObjectName('container_content')
        self.content_layout = QGridLayout(self.content)
        self.layout.addWidget(self.content)
