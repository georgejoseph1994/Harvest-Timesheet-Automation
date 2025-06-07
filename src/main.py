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


if __name__ == "__main__":
    args = parse_args()

    harvest_controller = HarvestController()
    date_utils = DateUtils(country=HOLIDAY_CONFIG["country"], state=HOLIDAY_CONFIG["state"])

    if args.date:
        print(f"Processing single date: {args.date}")
        dates = [datetime.strptime(args.date, "%d/%m/%Y")]
    elif args.start and args.end:
        dates, skipped_info = date_utils.process_date_range(args.start, args.end)
    else:
        print("No specific dates provided, processing current work week...")
        dates = date_utils.get_current_week_dates()
        print(f"Found {len(dates)} workdays in current week\n")

    if args.show:
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
        from_date = args.start if args.start else dates[0].strftime("%d/%m/%Y")
        to_date = args.end if args.end else dates[-1].strftime("%d/%m/%Y")
        print(f"Deleting time entries from {from_date} to {to_date}...")
        harvest_controller.delete_time_entries_for_date(from_date, to_date)
        print("Delete operation completed.")
    else:
        print(f"Starting timesheet filling for {len(dates)} workdays...")
        for i, date in enumerate(dates, 1):
            date_str = date.strftime("%d/%m/%Y")
            print(f"[{i}/{len(dates)}] Processing {date_str} ({date.strftime('%A')})...")
            harvest_controller.fill_timesheet(date_str)
        print("\nTimesheet filling completed for all workdays!")