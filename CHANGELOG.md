# Changelog

## [Unreleased]

### Added

- Hardware settings are configurable from the UI in a basic fashion (#141).
- Microlab 0.5 simulation configuration (#140).

### Changed

- Configuration is now stored in /etc/microlab instead of backend/config.py (#141).
- Recipe data was moved from /backend/recipes/files to being stored by default at /var/lib/microlab/recipes. Recipes in the repository are kept at backend/data/recipes and copied to their proper storage location at launch. (#141).
- Hardware configuration files were moved from backend/hardware to being stored by default at /var/lib/microlab/controllerhardware and /var/lib/microlab/labhardware. Hardware configurations in the repository are kept at backend/data/hardware and copied to their proper storage location at launch. (#141).
- The API endpoints `/start/<name>`, `/stop`, `/select/option/<name>`, `/controllerHardware/<name>`, `/labHardware/<name>` are now POST rather than GET. (#144).

### Fixed

- Bug when multiple gpiod instances were being used (#141).
- Syringe pump configuration was not being used (#118).
- Error responses no longer return status code 200. (#144).

### Removed

- Celery and redis (#139).

## [0.5.1]

## [0.5.0]
