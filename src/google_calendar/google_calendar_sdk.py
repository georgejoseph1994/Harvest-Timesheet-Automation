import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

class GoogleCalendarSDK:
    def __init__(self, credentials_file="credentials.json", token_file="token.json"):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = self.get_calendar_service()

    def get_calendar_service(self):
        creds = None
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)
        with open(self.token_file, "w") as token:
            token.write(creds.to_json())
        return build("calendar", "v3", credentials=creds)

    def get_events_in_day(self, target_date, calendar_id="primary"):
        """Get all events for a particular day."""
        try:
            date_obj = datetime.datetime.strptime(target_date, "%Y-%m-%d")
            start_of_day = date_obj.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=datetime.timezone.utc)
            end_of_day = date_obj.replace(hour=23, minute=59, second=59, microsecond=999999, tzinfo=datetime.timezone.utc)
            events_result = (
                self.service.events()
                .list(
                    calendarId=calendar_id,
                    timeMin=start_of_day.isoformat(),
                    timeMax=end_of_day.isoformat(),
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])
            event_list = []
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                end = event["end"].get("dateTime", event["end"].get("date"))
                summary = event.get("summary", "(No Title)")
                attendees = event.get("attendees", [])
                guest_list = [a.get("email", "Unknown") for a in attendees] if attendees else []
                event_list.append({
                    "id": event.get("id"),
                    "summary": summary,
                    "start": start,
                    "end": end,
                    "guests": guest_list
                })
            return event_list
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []

if __name__ == "__main__":
    sdk = GoogleCalendarSDK()

    target_date = '2025-05-30'
    events = sdk.get_events_in_day(target_date)
    if not events:
        print("No events found for this day.")
    else:
        print(f"Events for {target_date}:")
        for event in events:
            guest_str = ", ".join(event["guests"]) if event["guests"] else "No guests"
            print(f"{event['summary']}\n  Start: {event['start']}\n  End:   {event['end']}\n  Guests: {guest_str}\n")