from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    messages = service.users().messages()
    notifications = messages.list(userId='me', labelIds='INBOX', q=None, pageToken=None, maxResults=None, includeSpamTrash=None).execute()

    typicalID = []
    for m in notifications['messages']:
        if m['id']:
            typicalID.append(m['id'])

    info = []
    for Ids in typicalID:
        info.append(messages.get(userId='me', id=Ids, format=None, metadataHeaders=None).execute())

    # if not labels:
    #     print('No labels found.')
    # else:
    #     print('Labels:')
    #     for label in labels:
    #         print(label['name'])

    # if not notifications:
    #     print('No notifications found')
    # else:
    #     print('Notifications:')
    #     print(notifications)

    if not info:
        print('No info found')
    else:
        print('Info:')
        for m in info:
            names = m['payload']['headers']
            # print(names)
            for n in names:
                if n['name'] == 'Subject':
                    print(n['value'])
                    print('===================================')
        # for notif in notifications:
        #     print(notif['messages'])
if __name__ == '__main__':
    main()
