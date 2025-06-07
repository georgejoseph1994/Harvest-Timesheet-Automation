from datetime import date

HOLIDAY_CONFIG = {
    "country": "AU",  # Australia
    "state": "VIC"    # Victoria (Melbourne)
}

timesheet_entries_for_a_day = [
    {
        "project_name": "Product & Development",
        "task_name": "Team Management & Strategy",
        "hours": 2,
        "notes": "Team Management & Strategy",
        # "project_id": Fill this with the project ID from Harvest
        # "task_id": Fill this with the task ID from Harvest
    },
    {
        "project_name": "General",
        "task_name": "Internal Meeting",
        "hours": 2,
        "notes": "Internal Meeting",
        # "project_id": Fill this with the project ID from Harvest
        # "task_id": Fill this with the task ID from Harvest
    },
    {
        "project_name": "Product & Development",
        "task_name": "Development & Technical Work",
        "hours": 4,
        "notes": "Development & Technical Work",
        # "project_id": Fill this with the project ID from Harvest
        # "task_id": Fill this with the task ID from Harvest
    }
]