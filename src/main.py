import argparse
from harvest.harvest_controller import HarvestController
from datetime import datetime, timedelta

def parse_args():
    parser = argparse.ArgumentParser(description="Harvest Timesheet Automation")
    parser.add_argument('--date', type=str, help="A single date (DD/MM/YYYY)")
    parser.add_argument('--start', type=str, help="Start date for range (DD/MM/YYYY)")
    parser.add_argument('--end', type=str, help="End date for range (DD/MM/YYYY)")
    parser.add_argument('--delete', action='store_true', help="Delete all time entries for the selected dates")
    parser.add_argument('--show', action='store_true', help="Show all time entries for the selected dates")
    return parser.parse_args()

def get_current_week_dates():
    today = datetime.today()
    monday = today - timedelta(days=today.weekday())
    return [monday + timedelta(days=i) for i in range(5)]

def get_date_range(start_str, end_str):
    start = datetime.strptime(start_str, "%d/%m/%Y")
    end = datetime.strptime(end_str, "%d/%m/%Y")
    return [start + timedelta(days=i) for i in range((end - start).days + 1)]

if __name__ == "__main__":
    args = parse_args()

    harvest_controller = HarvestController()

    if args.date:
        dates = [datetime.strptime(args.date, "%d/%m/%Y")]
    elif args.start and args.end:
        dates = get_date_range(args.start, args.end)
    else:
        dates = get_current_week_dates()

    if args.show:
        from_date = args.start if args.start else dates[0].strftime("%d/%m/%Y")
        to_date = args.end if args.end else dates[-1].strftime("%d/%m/%Y")
        entries = harvest_controller.sdk.get_time_entries(from_date, to_date)
        for entry in entries:
            print(f"Date: {entry['spent_date']}, Project: {entry['project']['name']}, Task: {entry['task']['name']}, Hours: {entry['hours']}, Notes: {entry['notes']}")
    elif args.delete:
        from_date = args.start if args.start else dates[0].strftime("%d/%m/%Y")
        to_date = args.end if args.end else dates[-1].strftime("%d/%m/%Y")
        harvest_controller.delete_time_entries_for_date(from_date, to_date)
    else:
        for date in dates:
            harvest_controller.fill_timesheet(date.strftime("%d/%m/%Y"))