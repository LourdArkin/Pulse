from PySide6.QtWidgets import (
    QFrame,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class CollapsibleSection(QFrame):
    def __init__(self, title: str):
        super().__init__()

        self.title = title

        self.setFrameShape(QFrame.Shape.StyledPanel)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.main_layout.setSpacing(6)

        self.toggle_button = QPushButton(f"▶ {self.title}")
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(False)
        self.toggle_button.clicked.connect(self.toggle_content)

        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)

        # Start collapsed
        self.content.hide()

        self.main_layout.addWidget(self.toggle_button)
        self.main_layout.addWidget(self.content)

    def toggle_content(self):
        expanded = self.toggle_button.isChecked()

        self.content.setVisible(expanded)

        arrow = "▼" if expanded else "▶"
        self.toggle_button.setText(f"{arrow} {self.title}")