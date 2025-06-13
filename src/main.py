import argparse
from harvest.harvest_controller import HarvestController
from datetime import datetime, timedelta
from utils.date_utils import DateUtils
from config.harvest_config import HOLIDAY_CONFIG

def parse_args():
    parser = argparse.ArgumentParser(description="Harvest Timesheet Automation")
    parser.add_argument('--date', type=str, help="A single date (DD/MM/YYYY)")
    parser.add_argument('--start', type=str, help="Start date for range (DD/MM/YYYY)")
    parser.add_argument('--end', type=str, help="End date for range (DD/MM/YYYY)")
    parser.add_argument('--delete', action='store_true', help="Delete all time entries for the selected dates")
    parser.add_argument('--show', action='store_true', help="Show all time entries for the selected dates")
    return parser.parse_args()

def validate_date_format(date_str, date_format="%d/%m/%Y"):
    try:
        datetime.strptime(date_str, date_format)
    except ValueError:
        print(f"Error: Invalid date format '{date_str}'. Expected format is DD/MM/YYYY")
        exit(1)


if __name__ == "__main__":
    args = parse_args()

    harvest_controller = HarvestController()
    date_utils = DateUtils(country=HOLIDAY_CONFIG["country"], state=HOLIDAY_CONFIG["state"])

    if args.date:
        validate_date_format(args.date)
        print(f"Processing single date: {args.date}")
        dates = [datetime.strptime(args.date, "%d/%m/%Y")]
    elif args.start and args.end:
        validate_date_format(args.start)
        validate_date_format(args.end)
        # For date ranges, we'll process dates one by one with real-time feedback
        dates = None  # We'll use the generator instead
    else:
        print("No specific dates provided, processing current work week...")
        dates = date_utils.get_current_week_dates()
        print(f"Found {len(dates)} workdays in current week\n")

    if args.show:
        if args.start and args.end:
            print("Collecting time entries for date range...")
            # For ranges, get all workdays first then fetch entries
            workdays, _ = date_utils.process_date_range(args.start, args.end, verbose=False)
            from_date = args.start
            to_date = args.end
        else:
            from_date = args.start if args.start else dates[0].strftime("%d/%m/%Y")
            to_date = args.end if args.end else dates[-1].strftime("%d/%m/%Y")

        print(f"Fetching time entries from {from_date} to {to_date}...")
        entries = harvest_controller.sdk.get_time_entries(from_date, to_date)

        if entries:
            print(f"\nFound {len(entries)} time entries:")
            print("-" * 80)
            for entry in entries:
                print(f"Date: {entry['spent_date']}, Project: {entry['project']['name']}, Task: {entry['task']['name']}, Hours: {entry['hours']}, Notes: {entry['notes']}")
        else:
            print("No time entries found for the specified date range.")
    elif args.delete:
        if args.start and args.end:
            print("Preparing to delete time entries for date range...")
            # For ranges, get all workdays first then delete entries
            workdays, _ = date_utils.process_date_range(args.start, args.end, verbose=False)
            from_date = args.start
            to_date = args.end
        else:
            from_date = args.start if args.start else dates[0].strftime("%d/%m/%Y")
            to_date = args.end if args.end else dates[-1].strftime("%d/%m/%Y")

        print(f"Deleting time entries from {from_date} to {to_date}...")
        harvest_controller.delete_time_entries_for_date(from_date, to_date)
        print("Delete operation completed.")
    else:
        if args.start and args.end:
            # Use generator for real-time feedback on date ranges
            print("Starting timesheet filling with real-time progress...")
            for date in date_utils.process_date_range_with_feedback(args.start, args.end):
                date_str = date.strftime("%d/%m/%Y")
                harvest_controller.fill_timesheet(date_str)
        else:
            # Process pre-calculated dates for single date or current week
            print(f"Starting timesheet filling for {len(dates)} workdays...")
            print("=" * 80)
            for i, date in enumerate(dates, 1):
                date_str = date.strftime("%d/%m/%Y")
                print(f"\n[{i}/{len(dates)}] Processing {date_str} ({date.strftime('%A')})...")
                print("-" * 60)
                harvest_controller.fill_timesheet(date_str)
                print("-" * 60)
            print(f"\n{'=' * 80}")
            print("Timesheet filling completed for all workdays!")
            print("=" * 80)