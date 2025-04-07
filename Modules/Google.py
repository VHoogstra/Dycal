import datetime
import json
import os.path
from logging import exception
from pprint import pprint

import arrow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from Modules.ConfigLand import ConfigLand
from Modules.Constants import Constants


class Google:
    creds = None
    SCOPES: list[str] = ["https://www.googleapis.com/auth/calendar.app.created"]
    calendar = None
    event = None

    def __init__(self):
        print("Google")

    def login(self):
        config = ConfigLand()
        googleConfig = config.getKey('google')
        if 'credentials' in googleConfig and googleConfig['credentials'] is not None:
            credentials_dict = googleConfig['credentials']
            self.creds = Credentials(credentials_dict["token"],
                                     refresh_token=credentials_dict["refresh_token"],
                                     token_uri=credentials_dict["token_uri"],
                                     client_id=credentials_dict["client_id"],
                                     client_secret=credentials_dict["client_secret"],
                                     scopes=credentials_dict["scopes"])

        if not self.creds or not self.creds.valid:
            print('No valid credentials found.')
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)
                googleConfig['credentials'] = json.loads(self.creds.to_json())
            # Save the credentials for the next run

            config.storeKey('google', googleConfig)

    def getService(self):
        return build('calendar', 'v3', credentials=self.creds)

    def main(self):
        self.login()
        self.calendar = Calendar(self.getService())
        try:
            calendar = self.calendar.create("ZT DYF")
            # build events class
            self.event = Event(self.getService(), calendar['id'])

            pprint(calendar)
            # look for calendar
            print(self.calendar.get(
                'ab7e56a19bcda7a349b4c3f8a1a0456e8c5f30df5241be601526ab8ebe364f86@group.calendar.google.com'))
        except HttpError as error:
            raise error


class Calendar:
    def __init__(self, service):
        self.service = service
        if service is None:
            raise Exception("Service cannot be None")

    def get(self, calendarId):

        return self.service.calendars().get(calendarId=calendarId).execute()

    def list(self):
        calendars = []
        page_token = None
        while True:
            calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                calendars.append((calendar_list_entry['summary'], calendar_list_entry['id']))
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        return calendars

    def update(self, calendar):
        return self.service.calendars().update(calendarId=calendar['id'], body=calendar).execute()

    def create(self, name):
        return {
            'summary': name,
            'description': "",
            'id': "ab7e56a19bcda7a349b4c3f8a1a0456e8c5f30df5241be601526ab8ebe364f86@group.calendar.google.com",
        }
        calendar = {
            'summary': name,
            'timeZone': Constants.timeZone
        }
        return self.service.calendars().insert(body=calendar).execute()


class Event:
    def __init__(self, service, calendarId):
        if service is None:
            raise Exception("Service cannot be None")
        self.service = service
        self.calendarId = calendarId

    def list(self):
        beforeDate = arrow.get(tzinfo=Constants.timeZone).shift(days=-1)
        page_token = None
        returnEvents = []
        while True:
            events = self.service.events().list(
                orderBy="startTime",
                singleEvents=True,
                timeMin=beforeDate,
                calendarId=self.calendarId,
                pageToken=page_token
            ).execute()
            for event in events['items']:
                returnEvents.append(event)
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        return returnEvents

    def get(self):
        return self.service.events().get(calendarId='primary', eventId='eventId').execute()

    def update(self, event, calendar_id):
        return self.service.events().update(calendarId=calendar_id, eventId=event['id'], body=event).execute()

    def remove(self, event):
        self.service.events().delete(calendarId='primary', eventId=event['id']).execute()
