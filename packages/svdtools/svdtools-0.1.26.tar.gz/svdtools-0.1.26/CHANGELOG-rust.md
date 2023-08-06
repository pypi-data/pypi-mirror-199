# Changelog

This changelog tracks the Rust `svdtools` project. See
[CHANGELOG-python.md](CHANGELOG-python.md) for the Python `svdtools` project.

## [Unreleased]

## [v0.3.0] 2023-03-27

* cluster add/modify
* use `normpath` instead of std::fs::canonicalize

## [v0.2.8] 2023-01-28

* patch: added possibility to modify dim elements (arrays)
* mmap: replace %s in field array

## [v0.2.7] 2022-09-18

* Print svdtools version on error, update dependencies
* Check `_delete`, `_strip`, etc. on array of strings

## [v0.2.6] 2022-08-21

**Breaking changes**:

* Move `_strip`, `_strip_end` before `_modify` (#89)
    * Existing patch files may need updating to refer to the stripped
      versions of names being modified
* Allow `_derive` to rename derived peripherals, optionally specify a new base
    address and description (#118)
    * If registers were being copied and modified, use `_copy` instead of
      `_derive` for those peripherals.

Other changes:

* Improve error messages on missing files (#117)
* Fix help documentation for `svdtools patch` command (#119)

## [v0.2.5] 2022-07-23

* update `svd-rs` crates to 0.14
* `convert`: Add `format_config` option

## [v0.2.4] 2022-05-15

* Added action to build binaries and release for every version tag and latest commit
* Use `svd-parser` 0.13.4, add `expand_properties` option in `convert`
* `patch`: check enum `usage`, don't add it if unneeded

## [v0.2.3] 2022-05-01

* Add support for `modifiedWriteValues` & `readAction` for fields

## [v0.2.2] 2022-04-23

* Use `svd-encoder` 0.13.2
* Support `expand` when processing SVD files (#104)
* Sanitize enumeratedValues (#103)

## [v0.2.1] 2022-02-12

* Use `svd-encoder` 0.13.1
* Remove register `access` if empty

## [v0.2.0] 2022-01-15

* Use `svd-parser` 0.13.1
* Add `_clear_fields` in `Device` and `Peripheral` (#90)
* Add new `convert` command to convert between SVD (XML), JSON, and YAML (#92)
* Provide option to opt out of regex replace of 0's in description when
  creating arrays by using a custom `description` attribute (#95)

## [v0.1.0] 2021-12-09

* Initial release with feature-parity with the Python project.

[Unreleased]: https://github.com/stm32-rs/svdtools/compare/v0.3.0...HEAD
[v0.3.0]: https://github.com/stm32-rs/svdtools/compare/v0.2.8...v0.3.0
[v0.2.8]: https://github.com/stm32-rs/svdtools/compare/v0.2.7...v0.2.8
[v0.2.7]: https://github.com/stm32-rs/svdtools/compare/v0.2.6...v0.2.7
[v0.2.6]: https://github.com/stm32-rs/svdtools/compare/v0.2.5...v0.2.6
[v0.2.5]: https://github.com/stm32-rs/svdtools/compare/v0.2.4...v0.2.5
[v0.2.4]: https://github.com/stm32-rs/svdtools/compare/v0.2.3...v0.2.4
[v0.2.3]: https://github.com/stm32-rs/svdtools/compare/v0.2.2...v0.2.3
[v0.2.2]: https://github.com/stm32-rs/svdtools/compare/v0.2.1...v0.2.2
[v0.2.1]: https://github.com/stm32-rs/svdtools/compare/v0.2.0...v0.2.1
[v0.2.0]: https://github.com/stm32-rs/svdtools/compare/35c3a79...v0.2.0
[v0.1.0]: https://github.com/stm32-rs/svdtools/pull/84
