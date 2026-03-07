# SWL Schedule Tool Developer Guide

## Project Structure

```
SWLScheduleTool/
├── swl.py                  # Interactive TUI dashboard (Textual)
├── checksked.py            # CLI frequency query tool (Rich)
├── updatesked.py           # Schedule downloader & converter
├── swlconfig.conf          # User QTH configuration (git-ignored)
├── .gitignore              # Ignores __pycache__/, swlconfig.conf
├── countrycode.dat         # ITU country codes (latin-1)
├── targetcode              # Target area code definitions
├── transmittersite         # Transmitter site locations (text)
├── CLAUDE.md               # Claude Code instructions
├── README.md               # Project overview
├── USER-GUIDE.md           # End-user documentation
├── DEV-GUIDE.md            # This file
└── swl-schedules-data/     # Schedule data directory
    ├── sked-current.csv    # Active schedule (semicolon CSV)
    ├── freq-current.dat    # Frequency-sorted list
    ├── bc-current.dat      # Time-sorted list
    ├── README-current.TXT  # EiBi documentation
    ├── transmitter-sites.json  # Extracted sites with coordinates
    └── sked-{a|b}##.csv   # Archived seasonal files
```

## Architecture

### swl.py — TUI Dashboard

The main application built with [Textual](https://textual.textualize.io/).

**Theme & Styling:**
- Tokyo Night theme (`theme = "tokyo-night"`) with black backgrounds
- Starship-style powerline input prompts using Nerd Font glyphs
- Color palette from user's Starship config: `#769ff0`, `#a3aed2`, `#394260`; all backgrounds black
- ON AIR rows: bold green; inactive rows: `#aaaaaa` (light grey); zoom rows: bold `#769ff0` (blue)
- Detail modal: round `#769ff0` border, `#a9b1d6` text

**Key Classes:**
- `SWLApp(App)` — Main application; handles compose, search, update, tick
- `DetailScreen(ModalScreen)` — Station detail popup

**Data Loading (on startup):**
- `load_config()` — QTH from `swlconfig.conf` via `configparser`
- `load_sites()` — Transmitter sites from `transmitter-sites.json`
- `load_schedule()` — Schedule rows from `sked-current.csv` (latin-1, semicolon-delimited)
- `load_country_names()` — ITU codes from `countrycode.dat`
- `load_target_names()` — Target areas from `targetcode` with compound code expansion
- `load_language_names()` — Language codes parsed from `README-current.TXT` Section I

**Core Functions:**
- `compute_on_air(time_range, current_time)` — Returns `(duration, is_active, status_str)`. Active → `◄ ON AIR HHhMM`, inactive → `→ NEXT HHhMM`, unparseable → `"—"`
- `resolve_site_info(row, sites_index)` — Resolves transmitter site by `(country, site_code)` with fallback to default site
- `haversine(lat1, lon1, lat2, lon2)` — Great-circle distance in km
- `bearing(lat1, lon1, lat2, lon2)` — Initial bearing in degrees
- `compass_label(deg)` — 8-point compass label (N, NE, E, etc.)

**Event Flow:**
1. `on_input_submitted` — Dispatches to `_do_search()` or `_run_update()` based on input ID
2. `_do_search()` — Filters schedule by frequency, computes ON AIR/NEXT status, populates DataTable via `_build_result()` and `_populate_table()` helpers
3. `_run_update()` — Validates period (`^[ab]\d{2}$`), runs `updatesked.py` as subprocess in worker thread
4. `_apply_reload(sites, schedule)` — Thread-safe callback to update data on main thread after successful download
5. `on_data_table_row_selected` — Opens `DetailScreen` with resolved station details
6. `action_zoom()` — Finds nearest on-air stations below/above selected frequency, inserts them into displayed_rows as blue-highlighted zoom rows via `_rebuild_table_rows()`
7. `_tick()` — Updates UTC clock every second

### checksked.py — CLI Query Tool

Standalone Rich-based CLI tool. Reads the same `sked-current.csv` and displays a formatted table for a given frequency. Active broadcasts shown in bold green with `◄ ON AIR` indicator.

### updatesked.py — Schedule Updater

Downloads EiBi schedule files from `http://eibispace.de/dx`:
- `sked-{period}.csv` → `sked-current.csv`
- `freq-{period}.txt` → `freq-current.dat`
- `bc-{period}.txt` → `bc-current.dat`
- `README.TXT` → `README-current.TXT`

Converts all files from ISO-8859-1 to UTF-8. Extracts transmitter sites from README Section IV into `transmitter-sites.json`.

**Site Extraction:**
- `parse_dms_coord()` — Converts DMS coordinates (e.g. `34N32`, `26S07'40"`) to decimal degrees
- `extract_transmitter_sites()` — Parses country codes, site codes, names, coordinates
- `_parse_site_entry()` / `_parse_multi_site()` — Handle single and multi-site entries

## CSV Schedule Format

`sked-current.csv` — semicolon-delimited, 11 columns:

| # | Column | Example |
|---|--------|---------|
| 0 | kHz | `6070` |
| 1 | Time(UTC) | `0000-0400` |
| 2 | Days | `Sa,Su` |
| 3 | ITU | `CAN` |
| 4 | Station | `CFRX` |
| 5 | Lng | `E` |
| 6 | Target | `NAm` |
| 7 | Remarks/Site | `k` |
| 8 | P | `50` |
| 9 | Start | `0901` |
| 10 | Stop | `1004` |

## Time Handling

All times are UTC, stored as HHMM integers (e.g. `1430` = 14:30 UTC).

**Midnight-crossing broadcasts:** When `end_time < start_time`, duration adds 2400. Active check: `current >= start OR current < end`.

**NEXT calculation:** For inactive stations, compute minutes from current time to start time. If start is earlier than current, add 24 hours (next day).

## Site Resolution

The `site_code` field in the CSV can be:
- A simple code (e.g. `k`) — lookup as `(country, "k")`
- A `/COUNTRY` reference (e.g. `/USA`) — lookup as `("USA", "")`
- A `/COUNTRY-code` reference (e.g. `/USA-g`) — lookup as `("USA", "g")`

Fallback: if exact `(country, site_code)` not found, try `(country, "")`.

## Target Code Resolution

Target codes can be:
- Direct (e.g. `FE`, `Eu`) — simple lookup
- Compound (e.g. `CAf` = Central Africa, `NAm` = North America) — prefix expansion using `_prefixes` + `_regions` dicts
- Country codes — fallback to `countrycode.dat`

## Dependencies

**Standard library:** `argparse`, `os`, `sys`, `csv`, `json`, `re`, `configparser`, `socket`, `subprocess`, `math`, `datetime`, `urllib.request`, `shutil`

**External packages:**
- `rich` — Terminal formatting (checksked.py, swl.py)
- `textual` — TUI framework (swl.py)

**Optional:** `cowsay`, `lolcat` — Completion message in updatesked.py

## License

GPLv3
