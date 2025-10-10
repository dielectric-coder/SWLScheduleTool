# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This repository contains a collection of Python tools for Shortwave Listener (SWL) radio enthusiasts. The tools help manage and query broadcasting schedules from the EiBi (Eike Bierwirth) shortwave frequency database.

## Common Commands

### Update Schedule Data
```bash
# Update schedules for a specific period (e.g., a25 for summer 2025, b25 for winter 2025)
python3 updatesked.py a25
python3 updatesked.py b25

# The format is: [a|b]<2-digit-year>
# 'a' = summer season, 'b' = winter season
```

### Check Broadcasting Schedules
```bash
# Check what stations are broadcasting on a specific frequency (in kHz)
python3 checksked.py 15400
python3 checksked.py 9580

# This shows all stations scheduled for that frequency at the current UTC time
# Active broadcasts are highlighted in green with remaining time
```

### Direct Script Execution
Both scripts are designed to be executable:
```bash
./updatesked.py a25
./checksked.py 15400
```

## Architecture Overview

### Core Components

1. **`updatesked.py`**: Schedule data updater
   - Downloads current broadcasting schedules from eibispace.de
   - Processes multiple file types: CSV schedules, frequency data, broadcaster data, README
   - Converts encoding from ISO-8859-1 to UTF-8 for compatibility
   - Creates "current" versions of all data files

2. **`checksked.py`**: Schedule query tool
   - Reads CSV schedule data and searches by frequency
   - Calculates real-time broadcast status using current UTC time
   - Handles broadcasts that cross midnight boundary
   - Color-codes active broadcasts with remaining time calculation

3. **Data Directory**: `swl-schedules-data/`
   - Contains downloaded and processed schedule files
   - Files are named with season codes (e.g., `sked-a25.csv`, `freq-current.dat`)
   - "current" versions are the active working files

### Data Flow

1. **Data Download**: `updatesked.py` fetches data from http://eibispace.de/dx/
2. **Data Processing**: Files are converted from ISO-8859-1 to UTF-8 encoding
3. **Data Storage**: Processed files stored as "current" versions for active use
4. **Data Query**: `checksked.py` reads processed CSV and displays relevant broadcasts

### Reference Files

- **`countrycode.dat`**: ITU country codes and names
- **`targetcode`**: Broadcast target area codes (geographical regions)
- **`transmittersite`**: Transmitter site codes by country with coordinates
- **`swl-schedules-data/README-current.TXT`**: Detailed format documentation

## CSV Data Format

The schedule CSV uses semicolon separation with these fields:
- Frequency (kHz)
- Time range (UTC, format: HHMM-HHMM)
- Days of operation
- ITU country code
- Station name
- Language code
- Target area
- Transmitter site
- Persistence code
- Start/Stop dates

## Development Guidelines

### File Paths
- The hardcoded path in `checksked.py` (`/home/mikel/Documents/Radio/sw-schedules`) should be made configurable or use relative paths
- `updatesked.py` correctly uses script directory for data storage

### Time Handling
- All times are in UTC
- The system handles broadcasts crossing midnight (e.g., 2300-0200)
- Remaining time calculations account for minute-level precision

### Encoding
- Input files from EiBi are in ISO-8859-1 (Latin-1)
- Processing converts to UTF-8 for broader compatibility
- CSV reading uses `latin-1` encoding for compatibility

### Error Handling
- Both scripts include error handling for missing files and network issues
- `updatesked.py` continues processing other files if one fails
- Input validation ensures proper schedule period format

### Dependencies
- Python 3.6+ (uses f-strings)
- Standard library only (no external dependencies)
- Optional: `cowsay` and `lolcat` for completion messages

## Broadcasting Season Format

Schedule periods follow the pattern: `[a|b]<YY>`
- `a`: Summer broadcasting season
- `b`: Winter broadcasting season  
- `YY`: Two-digit year (e.g., 25 for 2025)

Examples: `a25` (Summer 2025), `b24` (Winter 2024/2025)

## Color Coding

In `checksked.py` output:
- **Green highlight**: Currently active broadcasts
- **"ON AIR"**: Indicates live transmission with remaining time
- Plain text: Scheduled but not currently broadcasting

## Data Sources

Primary data source: EiBi (Eike Bierwirth) database at http://eibispace.de/dx/
- Comprehensive shortwave broadcasting schedules
- Updated seasonally (typically twice per year)
- Includes technical details like transmitter sites and target areas
- Free to use with no warranty on accuracy

## File Extensions and Types

- `.py`: Python scripts (main executables)
- `.csv`: Schedule data (semicolon-separated)
- `.dat`: Reference data (country codes, transmitter sites)
- `.txt`: Frequency lists and README files