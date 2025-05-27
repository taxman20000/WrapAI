# CHANGELOG.md

## SECTIONS (if applicable)
Added: New features or enhancements.
Changed: Backward-compatible changes (e.g., refactoring, config updates).
Deprecated: Features marked for future removal.
Removed: Backward-incompatible removals.
Fixed: Bug fixes.
Security: Security patches (critical to highlight). 

## [0.2.4] - 2025-05-27
### Changed
- Miscellaneous change for initial release including account_info changes to return values instead of print them

## [0.2.3] - 2025-05-20
### Changed
- Updated the README.md file for api_key instructions

## [0.2.2] - 2025-05-19
### Added
- added support for new venice_parameters in the prompt_attributes
  - strip_thinking_response
  - disable_thinking
  - enable_web_citations
- added placeholders for additional OpenAIPromptAttributes not yet fully implemented

## [0.2.1] - 2025-05-19
### Added
- example_account_info.py file to show examples of using account_info.py module
- added def get_full_model_detail_dict method to VeniceModels class

### Removed
- removed application specific methods to show VeniceModel info in specific format.  Those should be in programs.
    - get_model_detail_dict
    - get_model_detail


## [0.2.0] - 2025-05-16
- Initial stable release with CHANGELOG
