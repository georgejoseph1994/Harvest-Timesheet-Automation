from harvest_sdk import HarvestSDK
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from config.harvest_config import timesheet_entries_for_a_day
load_dotenv()

class HarvestAgent:
    # constructor
    def __init__(self):
        self.sdk = HarvestSDK(
            account_id=os.getenv("HARVEST_ACCOUNT_ID"),
            access_token=os.getenv("HARVEST_ACCESS_TOKEN")
        )
    
    def fill_timesheet(self, date_str):
        # Convert date string to required format (YYYY-MM-DD)
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        spent_date = date_obj.strftime("%Y-%m-%d")

        for entry in timesheet_entries_for_a_day:
            try:
                self.sdk.create_time_entry(
                    project_id=entry['project_id'],
                    task_id=entry['task_id'],
                    spent_date=spent_date,
                    hours=entry['hours'],
                    notes=entry['notes'],
                )
                print(f"Created {entry['hours']}h entry for {entry['project_name']} - {entry['task_name']}")
            except requests.exceptions.RequestException as e:
                print(f"Error creating time entry: {str(e)}")
    
    def delete_time_entries_for_date(self, from_date, to_date):
        """Delete all time entries for the given date range"""
        entries = self.sdk.get_time_entries(from_date, to_date)

        for entry in entries:
            entry_id = entry["id"]
            del_response = self.sdk.delete_time_entry(entry_id)
            if del_response.status_code in (200, 204):
                print(f"Deleted time entry {entry_id} for {from_date} to {to_date}")
            else:
                print(f"Failed to delete entry {entry_id}: {del_response.text}")
