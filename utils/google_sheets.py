import streamlit as st
from google.oauth2.service_account import Credentials
import gspread

# Obtener credenciales desde Streamlit Secrets
def get_credentials_from_secrets():
    credentials_dict = {
        "type": st.secrets["google_credentials"]["type"],
        "project_id": st.secrets["google_credentials"]["project_id"],
        "private_key_id": st.secrets["google_credentials"]["private_key_id"],
        "private_key": st.secrets["google_credentials"]["private_key"].replace("\\n", "\n"),
        "client_email": st.secrets["google_credentials"]["client_email"],
        "client_id": st.secrets["google_credentials"]["client_id"],
        "auth_uri": st.secrets["google_credentials"]["auth_uri"],
        "token_uri": st.secrets["google_credentials"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["google_credentials"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["google_credentials"]["client_x509_cert_url"],
    }

    # Asegúrate de incluir los scopes para Google Sheets
    credentials = Credentials.from_service_account_info(
        credentials_dict,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    return credentials

# Conectar a Google Sheets usando las credenciales almacenadas
def connect_google_sheets(sheet_url):
    creds = get_credentials_from_secrets()
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url)
    return sheet
