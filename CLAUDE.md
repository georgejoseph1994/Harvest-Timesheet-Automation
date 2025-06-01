# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Setup and Dependencies:**
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```

**Running the Application:**
```bash
# From the project root
python src/main.py --date=17/05/2025              # Single date
python src/main.py --start=12/05/2025 --end=16/05/2025  # Date range
python src/main.py                                 # Current week (Mon-Fri)
python src/main.py --show --start=12/05/2025 --end=16/05/2025  # Show entries
python src/main.py --delete --date=17/05/2025     # Delete entries
```

**Date Format:** Always use DD/MM/YYYY format for all date inputs.

## Architecture

This is a Python application for automating Harvest timesheet entries with optional Google Calendar integration.

**Core Components:**
- `src/main.py` - CLI entry point with argument parsing for date ranges and operations
- `src/harvest/` - Harvest API integration layer
  - `harvest_controller.py` - Business logic for timesheet operations
  - `harvest_sdk.py` - Low-level Harvest API wrapper
- `src/google_calendar/` - Google Calendar API integration (read-only)
- `src/config/` - Configuration for timesheet entries

**Authentication & Configuration:**
- Harvest credentials stored in environment variables (`HARVEST_ACCOUNT_ID`, `HARVEST_ACCESS_TOKEN`, `HARVEST_BASE_URL`)
- Google Calendar uses OAuth2 flow with `credentials.json` and `token.json` files
- Timesheet entries configured in `config/harvest_config.py` (copy from example file)

**Key Patterns:**
- All internal dates use YYYY-MM-DD format; user-facing dates use DD/MM/YYYY
- SDK classes handle authentication and API calls
- Controller classes contain business logic
- Environment variables loaded via python-dotenv

**Google Calendar Integration:**
- Read-only access to calendar events for a given day
- Requires Google Cloud Console setup and OAuth2 credentials
- Located in `src/google_calendar/` directory