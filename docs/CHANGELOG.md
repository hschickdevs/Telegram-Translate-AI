# Changelog

All notable changes to this project will be documented in this file.

## [v2.2.0] - 2024-12-01

### Added
- New `/models` command to view and select available AI models
- New `/quit` command to explicitly end translation sessions
- Support for per-user model configuration via chat configs
- Translation limit system with configurable limits per chat
- Chat configuration system for storing user preferences
- New chat_configs/ directory for storing user settings

### Changed
- Renamed MODEL env var to DEFAULT_MODEL in .env
- Moved model selection from constructor to per-request basis in Translator class
- Updated help documentation to include new commands
- Improved command organization in README.md
- Added pyyaml to requirements.txt for model config support

### Fixed
- Improved session management with dedicated config storage
- Better error handling for model selection
- More consistent command documentation

### Internal
- Added new utility functions for config management
- Restructured bot initialization to support new features
- Added translation counting system
- Improved code organization and documentation
