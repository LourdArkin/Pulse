import os
import logging
logger = logging.getLogger("Pulse")  # DEBUG

from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication, QStyle
from PySide6.QtGui import QIcon, QAction




class TrayManager:
    def __init__(self, app):
        self.app = app

        # -----------------------------
        # SYSTEM TRAY
        # -----------------------------
        self.tray = QSystemTrayIcon()

        # -----------------------------
        # ICON SETUP
        # -----------------------------
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_dir, "assets", "icon.png")

        if os.path.exists(icon_path):
            self.tray.setIcon(QIcon(icon_path))
        else:
            logger.warning("Icon not found, using fallback icon")
            self.tray.setIcon(
                QApplication.style().standardIcon(QStyle.SP_ComputerIcon)
            )

        self.tray.setToolTip("Pulse")

        # -----------------------------
        # MENU
        # -----------------------------
        self.menu = QMenu()

        self.start_action = QAction("Start Simulator")
        self.stop_action = QAction("Stop Simulator")
        self.show_action = QAction("Show Settings")
        self.exit_action = QAction("Exit")

        # -----------------------------
        # ACTIONS
        # -----------------------------
        self.start_action.triggered.connect(self.app.start_simulator)
        self.stop_action.triggered.connect(self.app.stop_simulator)
        self.show_action.triggered.connect(self.app.show_settings)
        self.exit_action.triggered.connect(self.exit_app)

        # -----------------------------
        # BUILD MENU
        # -----------------------------
        self.menu.addAction(self.start_action)
        self.menu.addAction(self.stop_action)
        self.menu.addSeparator()
        self.menu.addAction(self.show_action)
        self.menu.addSeparator()
        self.menu.addAction(self.exit_action)

        self.tray.setContextMenu(self.menu)

        # -----------------------------
        # SIGNALS (DOUBLE CLICK FIX)
        # -----------------------------
        self.tray.activated.connect(self.on_tray_activated)

        # -----------------------------
        # SHOW TRAY
        # -----------------------------
        self.tray.show()
        self.update_state(False)  # Initial state: Stopped

        logger.info("Tray initialized")
        logger.info("System tray available: {}".format(QSystemTrayIcon.isSystemTrayAvailable()))

    # -----------------------------
    # TRAY CLICK HANDLER
    # -----------------------------
    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.app.show_settings()

        elif reason == QSystemTrayIcon.ActivationReason.Trigger:
            # Some systems treat single click as Trigger
            self.app.show_settings()

    # -----------------------------
    # EXIT APP
    # -----------------------------
    def exit_app(self):
        logger.info("Exiting Pulse...")
        
        self.app.stop_simulator()
        self.tray.hide()
        self.app.settings_window.close()

        QApplication.quit()

    def update_state(self, running: bool):
        if running:
            self.tray.setToolTip("Pulse\nStatus: Running")

            self.start_action.setEnabled(False)
            self.stop_action.setEnabled(True)
        else:
            self.tray.setToolTip("Pulse\nStatus: Stopped")

            self.start_action.setEnabled(True)
            self.stop_action.setEnabled(False)