import requests
import os

class HarvestSDK:
    def __init__(self, account_id, access_token):
        self.base_url = os.getenv("HARVEST_BASE_URL")
        self.headers = {
            "Harvest-Account-ID": account_id,
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "User-Agent": "Python Harvest API Client"
        }
    
    def get_user_id(self):
        """Get the current user's ID"""
        response = requests.get(f"{self.base_url}/users/me.json", headers=self.headers)
        response.raise_for_status()
        return response.json()["id"]
    
    def get_project_tasks(self):
        """Get all projects and their associated tasks through time entries"""
        try:
            print("Fetching assigned projects through time entries...")
            # Get recent time entries to find your assigned projects
            response = requests.get(
                f"{self.base_url}/time_entries.json",
                headers=self.headers,
                params={
                    "user_id": self.get_user_id(),
                    "per_page": 100  # Get more entries to ensure we catch all projects
                }
            )
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                entries = response.json()["time_entries"]
                
                # Extract unique projects and their tasks
                projects = {}
                for entry in entries:
                    project = entry["project"]
                    project_id = project["id"]
                    
                    if project_id not in projects:
                        projects[project_id] = {
                            "id": project_id,
                            "name": project["name"],
                            "tasks": {}
                        }
                    
                    task = entry["task"]
                    task_id = task["id"]
                    if task_id not in projects[project_id]["tasks"]:
                        projects[project_id]["tasks"][task_id] = {
                            "id": task_id,
                            "name": task["name"]
                        }
                
                # Convert to list format matching original API
                project_list = []
                for project in projects.values():
                    project_list.append({
                        "id": project["id"],
                        "name": project["name"],
                        "tasks": list(project["tasks"].values())
                    })
                
                print(f"Found {len(project_list)} projects from your time entries")
                return project_list
            else:
                response.raise_for_status()
            
        except requests.exceptions.RequestException as e:
            print(f"Error in get_project_tasks: {str(e)}")
            raise

    def create_time_entry(self, project_id, task_id, spent_date, hours, notes=None):
        """Create a time entry"""
        payload = {
            "project_id": project_id,
            "task_id": task_id,
            "spent_date": spent_date,
            "hours": hours,
            "notes": notes
        }
        
        response = requests.post(
            f"{self.base_url}/time_entries.json",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()
