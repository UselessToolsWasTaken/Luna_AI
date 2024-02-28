import datetime
import pytz
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
creds = None

calendar_id = []
formated_datetime = None
summary = None


def main():
    """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
    global creds
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())


def upcoming_events():
    global formated_datetime
    global summary
    with open(r'C:\Users\evryt\OneDrive\Documents\WorkProjectTXTs\calendar_id.txt', 'r') as file:
        for line in file:
            calendar_id.append(line.strip())

    service = build('calendar', 'v3', credentials=creds)
    warsaw_tz = pytz.timezone('Europe/Warsaw')
    now = datetime.datetime.now(tz=pytz.UTC).astimezone(warsaw_tz)
    end_time = now + datetime.timedelta(days=2)

    now_iso = now.isoformat()
    end_iso = end_time.isoformat()
    try:
        events_result = service.events().list(calendarId=calendar_id[0], timeMin=now_iso, timeMax=end_iso,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print("No upcoming events found.")

        nearest_event = events[0]
        start = nearest_event['start'].get('dateTime', nearest_event['start'].get('date'))
        summary = nearest_event.get('summary', 'No title')

        datetime_obj_utc = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
        datetime_obj_cet = datetime_obj_utc.astimezone(warsaw_tz)
        formated_datetime = datetime_obj_cet.strftime('%Y-%m-%d %H:%M')
        # print(f"Your next event is: {summary} at {formated_datetime} o'clock")

    except HttpError as error:
        print(f'An error occurred: {error}')
