from PySide6.QtWidgets import QLabel, QVBoxLayout, QFrame


class StatusCard(QFrame):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("STATUS")
        self.status = QLabel("🔴 Stopped")

        layout.addWidget(title)
        layout.addWidget(self.status)

    def set_status(self, text: str):
        self.status.setText(text)