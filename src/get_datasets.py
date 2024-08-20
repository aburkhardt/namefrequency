import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

#get google sheet dataset
#which is an example MAPP export from L26
def authenticate_google():
    """Authenticate & return Google Sheets API service instance"""
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None

    # Load credentials from token.pickle
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If pickle-free, prompt user login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    #build sheets api service
    service = build('sheets', 'v4', credentials=creds)
    return service


def get_gsheet_values(service, gbook, sheet):
    """pulls down the header and values of the given gsheet_id"""
    gsheet = (service.spreadsheets()
                    .values()
                    .get(spreadsheetId=gbook, range=sheet)
                    .execute())

    return gsheet
    

def make_gsheet_usable(gsheet):
    """
    Processes the Google Sheets JSON to ensure data integrity and usability.
    
    - Sets all fields to object type.
    - Ensures the first data row matches the header length.
    - Converts list to list of dictionaries using the first row as keys.
    """
    values = gsheet.get("values", [])

    if not values:
        raise ValueError("No data found.")
       
    header = values[0]
    data_rows = values[1:]

    if not data_rows:
        raise ValueError("No data rows found.")

    header_count = len(header)
    first_data_row_count = len(data_rows[0])
    
    if first_data_row_count != header_count:
        diff = header_count - first_data_row_count
        data_rows[0].extend([''] * diff)
    
    #convert list to list of dicts using the first row as keys
    keys = header
    Name_dict = [dict(zip(keys, row)) for row in data_rows]
    
    return Name_dict

def get_data(gbook, sheet):
    service = authenticate_google()
    gsheet_data = get_gsheet_values(service, gbook, sheet)
    processed_data = make_gsheet_usable(gsheet_data)
    return processed_data