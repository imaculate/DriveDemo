import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]


def getCredentials():
  creds = None
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
  return creds
def getFolders():
  """Shows basic usage of the Drive v3 API.
  Returns all the folders user has access to
  """
  
  folders = []

  try:
    service = build("drive", "v3", credentials=getCredentials())
    page_token = None

    while True:
      # Call the Drive v3 API
      results = (
          service.files()
          .list(q="mimeType = 'application/vnd.google-apps.folder'",
                spaces="drive",
                fields="nextPageToken, files(id, name)",
                pageToken = page_token)
          .execute()
      )
      items = results.get("files", [])

      for item in items:
        folders.append(item['name'])
      
      if page_token is None:
        break
  except HttpError as error:
    print(f"An error occurred: {error}")
  
  return folders
  

if __name__ == "__main__":
  print("Folders:\n" + "\n".join(getFolders()))