from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd
import os

##port##
PORT = int(os.environ.get('PORT', 5500))


SPREADSHEET_ID = "1n030AYAJE2zCPIR1l8yvUV40Ne7ixLgIWIR3h0HbFrk"
RANGE_NAME = "Sheet1"


def get_google_sheet(spreadsheet_id, range_name):
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
    #convert Google sheet data to a Pandas DataFrame
    header = gsheet.get('values', [])[0]   # header
    values = gsheet.get('values', [])[1:]  # data
    if not values:
        print('No data found.')
    else:
        all_data = []
        for col_id, col_name in enumerate(header):
            column_data = []
            for row in values:
                column_data.append(row[col_id])
            ds = pd.Series(data=column_data, name=col_name)
            all_data.append(ds)
        df = pd.concat(all_data, axis=1)
        return df
    
def dictify(df = gsheet2df(gsheet = get_google_sheet(SPREADSHEET_ID, RANGE_NAME))):
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