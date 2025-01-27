import gspread
from google.oauth2.service_account import Credentials

# Función para conectar con Google Sheets
def connect_google_sheets(sheet_url):
    creds = Credentials.from_service_account_file("credenciales.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url)
    return sheet

# Función para obtener los trámites de la hoja de Google Sheets
def get_tramites():
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/1qZX98WUaUGyUL5xSP0lHb7K7MfH7_ny8bRGOZnU1gGc/edit#gid=0"
        sheet = connect_google_sheets(sheet_url)
        worksheet = sheet.worksheet("Tramites")
        data = worksheet.get_all_records()
        return data
    except gspread.exceptions.WorksheetNotFound:
        st.error("No se encontró la hoja 'Tramites'. Verifica el nombre en Google Sheets.")
        return []
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets: {e}")
        return []

