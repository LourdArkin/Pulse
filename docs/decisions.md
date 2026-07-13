# Decisions

## 2026-06-28

### Use PySide6

Reason:
Modern UI, excellent tray support, and room to grow.

---

### Hide window on close

Reason:
Pulse is intended to run in the background.

## Use QSystemTrayIcon instead of pystray

Reason:

Since the application already uses PySide6, Qt's built-in tray support
reduces dependencies and integrates better with the event loop.
