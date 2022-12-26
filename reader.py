from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd
import os

##port##
PORT = int(os.environ.get('PORT', 5500))

#add sheet id to link with google sheets
SPREADSHEET_ID = ""
#name of sheet
RANGE_NAME = "Sheet1"


def get_google_sheet(spreadsheet_id, range_name):
    """
    Retrieve data from a Google Sheets spreadsheet and sheet.

    Parameters:
    - spreadsheet_id (str): The ID of the Google Sheets spreadsheet.
    - range_name (str): The name of the sheet in the spreadsheet.

    Returns:
    - dict: A dictionary containing the data from the specified spreadsheet and sheet.
    """
    scopes = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    # setup the Sheets API
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', scopes)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    # call the Sheets API
    gsheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return gsheet

def gsheet2df(gsheet):
    """
    Convert data from a Google Sheets spreadsheet into a Pandas DataFrame.

    Parameters:
    - gsheet (dict): A dictionary containing the data from a Google Sheets spreadsheet.

    Returns:
    - Pandas DataFrame: A DataFrame containing the data from the input dictionary.
    """
    # extract header row
    header = gsheet.get('values', [])[0]
    # extract data
    values = gsheet.get('values', [])[1:]
    if not values:
        print('No data found.')
    else:
        all_data = []
        # create a Pandas Series for each column
        for col_id, col_name in enumerate(header):
            column_data = []
            for row in values:
                column_data.append(row[col_id])
            ds = pd.Series(data=column_data, name=col_name)
            all_data.append(ds)
        # concatenate the Series objects into a single DataFrame
        df = pd.concat(all_data, axis=1)
        return df

def dictify(df = gsheet2df(gsheet = get_google_sheet(SPREADSHEET_ID, RANGE_NAME))):
    """
    Convert a Pandas DataFrame into a list of dictionaries.

    Parameters:
    - df (Pandas DataFrame, optional): The DataFrame to be converted. Defaults to the DataFrame returned by
    the google sheets API
    """
    list_dict = []

    for row in list(df.iterrows()):
        list_dict.append(dict(row))

    return list_dict

#####testing #####
# gsheet = get_google_sheet(SPREADSHEET_ID, RANGE_NAME)
# df = gsheet2df(gsheet)
# dfj = dictify(df)

# print('Dataframe size = ', df.shape)
# print(df.head())
# print("\n \n \n \n")
# print (dfj)

print(dictify())
