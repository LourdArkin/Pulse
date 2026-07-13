# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by **Keep a Changelog**, and this project follows its own versioning while under active development.

---

## [Unreleased]

### Planned

- Status-aware UI updates
- Tray status indicators
- Global hotkeys
- Startup with Windows
- Full settings presets
- Human-like mouse movement
- Human-like keyboard timing
- Notifications

---

## [0.2.0] - Core Infrastructure Complete

### Added

- Configuration management system using `config.json`
- Automatic loading and saving of application settings
- Keyboard simulation engine
- Keyboard presets and custom key selection
- Simulator running in a dedicated background thread
- System tray integration
- Tray menu actions (Start, Stop, Show Settings, Exit)
- Logging system with console and file output
- Centralized application state management (`PulseApp.is_running`)

### Improved

- Simulator lifecycle management
- Cleaner project architecture
- Improved separation between configuration, simulation, UI, and tray components
- Absolute path handling for tray icon
- More reliable application startup and shutdown

### Fixed

- System tray initialization issues
- Window visibility issues after refactoring
- Tray exit correctly terminates the application
- Keyboard configuration loading
- Simulator start/stop reliability

---

## [0.1.0] - Initial Prototype

### Added

- Initial PySide6 desktop application
- Settings window
- Mouse simulation
- Keyboard simulation
- Mouse configuration section
- Keyboard configuration section
- Status card
- Collapsible settings sections
- Save settings button
- Basic project structure
