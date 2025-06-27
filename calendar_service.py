from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import settings
from datetime import datetime
import dateutil.parser

def create_event(summary, start_time, end_time):
    
    creds = service_account.Credentials.from_service_account_file(
        settings.credentials_file,
        scopes=['https://www.googleapis.com/auth/calendar']
    )
    service = build('calendar', 'v3', credentials=creds)
    event = {
        'summary': summary,
        'start': {'dateTime':dateutil.parser.isoparse(start_time).isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime':dateutil.parser.isoparse(start_time).isoformat(), 'timeZone': 'Asia/Kolkata'},
    }
    return service.events().insert(calendarId=settings.calendar_id, body=event).execute()
#datetime.fromisoformat(end_time)