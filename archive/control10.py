import os
import io
from pathlib import Path
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload

load_dotenv()

# Configurações do .env
# GOOGLE_APPLICATION_CREDENTIALS="credentials.json"
# GOOGLE_DRIVE_FOLDER_ID="ID_DA_SUA_PASTA"

SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID')

def test_connection():
    try:
        # 1. Autenticação
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, 
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        service = build('drive', 'v3', credentials=creds)

        # 2. Listar arquivos da pasta
        query = f"'{FOLDER_ID}' in parents and trashed = false"
        results = service.files().list(
            q=query, 
            fields="files(id, name, mimeType)"
        ).execute()
        
        items = results.get('files', [])

        if not items:
            print('⚠️ Ninguém encontrado. Verifique se compartilhou a pasta com o e-mail do robô!')
        else:
            print('✅ Conexão estabelecida com sucesso!')
            print(f"📂 Arquivos encontrados na pasta (ID: {FOLDER_ID}):")
            for item in items:
                print(f" - {item['name']} (Tipo: {item['mimeType']})")

    except Exception as e:
        print(f"❌ Erro na conexão: {e}")

if __name__ == '__main__':
    test_connection()