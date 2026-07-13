from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class SliderSetting(QWidget):
    """
    Reusable slider widget.

    Features:
    - Label
    - Live value display
    - Optional unit suffix (seconds, pixels, etc.)
    """

    valueChanged = Signal(int)

    def __init__(
        self,
        label: str,
        minimum: int,
        maximum: int,
        value: int,
        unit: str = "",
    ):
        super().__init__()

        self.unit = unit

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # -----------------------
        # Header
        # -----------------------

        header = QHBoxLayout()

        self.label = QLabel(label)

        self.value_label = QLabel()
        self.value_label.setAlignment(
            Qt.AlignmentFlag.AlignRight |
            Qt.AlignmentFlag.AlignVCenter
        )

        header.addWidget(self.label)
        header.addStretch()
        header.addWidget(self.value_label)

        layout.addLayout(header)

        # -----------------------
        # Slider
        # -----------------------

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(minimum, maximum)
        self.slider.setValue(value)

        layout.addWidget(self.slider)

        self.slider.valueChanged.connect(self.on_value_changed)

        # Initialize label
        self.update_value_label(value)

    def update_value_label(self, value: int):
        if self.unit:
            self.value_label.setText(f"{value} {self.unit}")
        else:
            self.value_label.setText(str(value))

    def on_value_changed(self, value: int):
        self.update_value_label(value)
        self.valueChanged.emit(value)

    def value(self):
        return self.slider.value()

    def setValue(self, value: int):
        print(f"{self.label.text()} -> setValue({value})")
        self.slider.setValue(value)