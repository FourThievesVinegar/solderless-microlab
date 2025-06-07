# Changelog

## [Unreleased]

### Added

- Support for controlling gpio pins on the arduino when using custom grbl firmware. (#282)
- Ability to delete recipes from the microlab on the recipe details page. (#288)

### Changed

- Added alphabetical navigation of the recipe list. (#273)
- Extra validation for hardware config files. Hardware components are now automatically sorted by dependencies to prevent them from loading out of order. (#269)
- Syringe pump and peristaltic pump implementations no longer directly open a serial connection to grbl, and config instead now references a grbl device. (#282)
- Upgraded `gpiod` library and corresponding `gpiod_chip` client to v2.3.0 (#298)
- Refactored code for Pythonic compliance: added type hints, enhanced readability, and fixed minor type-checking bugs. 
- Performance improvements, such as caching for `localization.load_translation` function or replacing `time.sleep` with synchronization primitives.
- Improved multiprocess queues lifecycle management.
- Expanded UnitTests
- Expanded usage of Pydantic models

## [0.6.0]

### Added

- Slowly dispense reagents over time.
- Many pre-release tweaks and bug fixes.
- Massive docs update.
- New printable cases, stands, and reactor parts.
- Ability to manually reload hardware from the settings menu. (#197)
- Hardware settings are configurable from the UI in a basic fashion (#141).
- v0.6 hardware config supports PID temperature control
- MicroLab 0.5 simulation configuration (#140).
- Configurable hardware limits for supported temperatures. Recipes that require values outside of the configured range will no longer run. (#146).
- Sounds that play on recipe completion, errors, and user input steps (#149).
- Page for viewing logs on the frontend (#158).
- Uses the 4TV color palette (#157)
- Dark mode! (#81)

### Changed

- Performance and logging tuning
- Configuration is now stored in /etc/microlab instead of backend/config.py (#141).
- Recipe data was moved from /backend/recipes/files to being stored by default at /var/lib/microlab/recipes. Recipes in the repository are kept at backend/data/recipes and copied to their proper storage location at launch. (#141).
- Hardware configuration files were moved from backend/hardware to being stored by default at /var/lib/microlab/controllerhardware and /var/lib/microlab/labhardware. Hardware configurations in the repository are kept at backend/data/hardware and copied to their proper storage location at launch. (#141).
- The API endpoints `/start/<name>`, `/stop`, `/select/option/<name>`, `/controllerHardware/<name>`, `/labHardware/<name>` are now POST rather than GET. (#144).
- Hardware upgrades including but not limited to #74 and #83

### Fixed

- Bug when multiple gpiod instances were being used (#141).
- Syringe pump configuration was not being used (#118).
- Error responses no longer return status code 200. (#144).
- Kiosk mode now properly launches and restore dialog not shown (#133)
- Uploading recipes now immediately shows the uploaded recipe in the recipe list (#236)

### Removed

- Celery and redis (#139).

## [0.5.1]

## [0.5.0]
