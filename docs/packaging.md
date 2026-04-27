# Packaging Soho

Soho can be distributed as a macOS DMG for people who prefer a double-clickable local installer over cloning the repository manually.

## Build

From the repo root:

```bash
make dmg
```

or:

```bash
scripts/build-dmg.sh
```

The output is written to:

```text
dist/Soho-<version>.dmg
```

The version comes from `.claude-plugin/plugin.json`.

## What The DMG Contains

The DMG contains:

- `Soho/`: a source snapshot of this repository
- `Install Soho.command`: a Terminal installer
- `README.txt`: short install notes

The installer does not wire global tools to the mounted DMG. It copies `Soho/` into a durable install path first, then runs the normal installer from there.

Default install path:

```text
~/agent-plugins/soho
```

Override path:

```bash
SOHO_INSTALL_DIR=~/tools/soho /Volumes/Soho*/Install\ Soho.command
```

## Installer Behavior

`Install Soho.command`:

1. copies the bundled source into `SOHO_INSTALL_DIR`
2. backs up any existing install directory before replacing it
3. runs `scripts/install-global.sh`
4. attempts Claude Code plugin install through the `claude plugin` CLI if Claude Code is available
5. prints the Goose command: `goose recipe open soho`

## Signing And Notarization

The local DMG produced by `scripts/build-dmg.sh` is unsigned and not notarized. That is acceptable for local testing and private distribution, but a public release DMG should be signed and notarized before broad distribution.

## Verification

Build and inspect locally:

```bash
scripts/build-dmg.sh
hdiutil attach dist/Soho-*.dmg
ls /Volumes/Soho*
hdiutil detach /Volumes/Soho*
```
