from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def contruindo_relatorio(service, creds, SAMPLE_SPREADSHEET_ID, lista):
    # Quantidade Pedidos estão fechado
    quant_terminado = len(lista)
    celula= "Página1!"+str("D2")
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    body = {'values': [[quant_terminado]]}
    result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=celula,valueInputOption="USER_ENTERED", body=body).execute()

    # Quais são os pedidos estão fechados
    for id_cliente in range(len(lista)):
        texto= lista[id_cliente]
        celula= "Página1!"+str("A%i"%(id_cliente+2))
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        body = {'values': [[texto]]}
        result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=celula,valueInputOption="USER_ENTERED", body=body).execute()    


def main(lista):
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # The ID and range of a sample spreadsheet.
    padrao_planilha= input("deseja usar a mesma planilha. y ou digite qualquer coisa\n").lower()
    if padrao_planilha == "y":
        SAMPLE_SPREADSHEET_ID = '1RDZli3pQ3wFVgjJ2NnB5OE47VMsvhkDkLnyeEZs-563'
    else:
        SAMPLE_SPREADSHEET_ID = input("INSERIR A PARTE DO URL DO GOOGLE SHEETS, EX: 1RDZli3pQ3wFVgjJ2NnB5OE47VMsvhkDkLnyeEZs-563 \n")

    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    lista= lista
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
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    contruindo_relatorio(service, creds, SAMPLE_SPREADSHEET_ID, lista)
