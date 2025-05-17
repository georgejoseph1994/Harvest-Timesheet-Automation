import requests
import os
from datetime import datetime
from HarvestSDK import HarvestSDK
from dotenv import load_dotenv
from config.harvest_config import timesheet_entries_for_a_day

load_dotenv()

def fill_timesheet(date_str, account_id, access_token):
    # Convert date string to required format (YYYY-MM-DD)
    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
    spent_date = date_obj.strftime("%Y-%m-%d")
    
    # Initialize Harvest client
    harvest = HarvestSDK(account_id, access_token)
    
    for entry in timesheet_entries_for_a_day:
        try:
            harvest.create_time_entry(
                project_id=entry['project_id'],
                task_id=entry['task_id'],
                spent_date=spent_date,
                hours=entry['hours'],
                notes=entry['notes'],
            )
            
            print(f"Created {entry['hours']}h entry for {entry['project_name']} - {entry['task_name']}")
        except requests.exceptions.RequestException as e:
            print(f"Error creating time entry: {str(e)}")


if __name__ == "__main__":
    HARVEST_ACCOUNT_ID = os.getenv("HARVEST_ACCOUNT_ID")
    HARVEST_ACCESS_TOKEN = os.getenv("HARVEST_ACCESS_TOKEN")
    
    fill_timesheet('07/01/2025', HARVEST_ACCOUNT_ID, HARVEST_ACCESS_TOKEN)
    



    