from googleapiclient.discovery import build
from google.oauth2 import service_account

file_name = "2023-08"

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service.account.json'
PARENT_FOLDER_ID = "1qyMZb6P7H5oaq2zxoaqs17VJWSnHNgnG"

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload_file(file_path):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name' : f'{file_name}.xlsx',
        'parents' : [PARENT_FOLDER_ID]
    }

    file = service.files().create(
        body=file_metadata,
        media_body=file_path
    ).execute()

upload_file(f'/home/ricardo/code/statistic/src/credit_card/xlsx/{file_name}.xlsx')