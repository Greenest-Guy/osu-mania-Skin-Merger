# Changelog

All notable changes to this project will be documented in this file. (yyyy-mm-dd)
## [v1.3.1] 2025-08-13

### Added
- Merging osu mania skins into std, taiko, and catch
  
### Changed
  
### Fixed
- Error causing stage images to not be copied over if in skin.ini

### Removed

## [v1.3.0] 2025-08-08

### Added
- Animation support
  
### Changed
- When merging skins both @2x and regular files are copied
  
### Fixed
- Overwritting skins no longer causes message saying "skin sent to downloads folder"

### Removed

## [v1.2.1] 2025-08-03

### Added

### Changed

### Fixed
- bug causing NoteImages to not be assigned

### Removed

## [v1.2.0] 2025-08-03

### Added
- Copying default files and adding _None
- default_assets.py
- key_layouts.py

### Changed
- General process to copying files
- Seperated the classes from main.py into main.py & logic.py

### Fixed
- Default files not being added

### Removed

## [v1.1.0] 2025-07-30

### Added
- Option to overwrite skins

### Changed
- Seperate directory(s) within merge_files for each keycount

### Fixed
- Missing judgement images

### Removed


## [v1.0.1] 2025-07-29

### Added

### Changed
- Improved IniParser.py logic and comments
- PEP8 formatting

### Fixed
- East Asian language support

### Removed


## [v1.0.0] 2025-07-28

### Added
- Support for HD skin files (@2x)
- Merge skin hit judgements are now implemented

### Changed
- Correct error logging & handling regarding missing skins.

### Fixed

### Removed
