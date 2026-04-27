# Soho DMG Packaging Plan

## Goal

Create a repeatable macOS DMG packaging path for Soho that produces a user-installable disk image without making global installs point back to a mounted, read-only DMG volume.

## Architecture Summary

The DMG contains:

- a bundled `Soho/` source snapshot
- an executable `Install Soho.command`
- a short `README.txt`

The installer command copies the bundled source snapshot into a durable local install directory, then runs `scripts/install-global.sh` from that copied location.

## Files To Create Or Modify

- Create `scripts/build-dmg.sh`
- Create `docs/packaging.md`
- Modify `Makefile`
- Modify `README.md`
- Modify `docs/install.md`
- Modify `scripts/validate.py`
- Modify `tests/test_repo.py`

## Implementation Steps

1. Add `scripts/build-dmg.sh` with dry-run support for tests and a real `hdiutil create` path for macOS.
2. Stage the DMG contents from the repo while excluding `.git`, `build`, `dist`, caches, and editor junk.
3. Generate `Install Soho.command` into the staged DMG root.
4. Ensure `Install Soho.command` backs up any existing install path before copying the bundled source.
5. Add docs that explain the DMG is unsigned and local, not notarized.
6. Add a Makefile target so `make dmg` is the canonical source-build command.
7. Add tests and validation so packaging files cannot drift out of the repo contract.

## Test Steps

1. Run `python3 scripts/validate.py`.
2. Run `python3 -m unittest discover -s tests -p 'test_*.py'`.
3. Run `make check`.
4. Run `SOHO_DMG_DRY_RUN=1 scripts/build-dmg.sh` through the unit test.
5. Run `scripts/build-dmg.sh` locally on macOS to produce `dist/Soho-<version>.dmg`.

## Verification Steps

1. Verify the DMG file exists.
2. Verify the DMG can be attached with `hdiutil attach`.
3. Verify the mounted volume contains `Install Soho.command`, `README.txt`, and `Soho/`.
4. Verify the DMG can be detached cleanly.
