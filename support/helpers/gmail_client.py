import os.path
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GmailClient:
    def __init__(self):
        self.creds = self.login()

    def login(self):
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def get_last_message(self, user_id):
        if not self.creds:
            return None

        try:
            service = build('gmail', 'v1', credentials=self.creds)
            results = service.users().messages().list(userId=user_id, maxResults=1).execute()
            messages = results.get('messages', [])

            if messages:
                message = service.users().messages().get(userId=user_id, id=messages[0]['id']).execute()
                return message
            else:
                print("No messages found.")
                return None
        except HttpError as e:
            print(f"An error occurred: {str(e)}")
            return None

    def check_that_email_was_received(self, email_from, email_subject, timeout):
        start_time = time.time()
        subject = None
        sender = None

        while (subject != email_subject or sender != f"<{email_from}>") and time.time() - start_time < timeout:
            message = self.get_last_message("me")

            if message and 'payload' in message and 'headers' in message['payload']:
                headers = message['payload']['headers']
                for header in headers:
                    if header['name'] == "Subject":
                        subject = header['value']
                    elif header['name'] == "From":
                        sender = header['value']

            time.sleep(1)

        if subject == email_subject and sender == f"<{email_from}>":
            return  # Email received successfully.

        raise TimeoutError(f"Email from <{email_from}> with subject '{email_subject}' not received within the timeout.")
