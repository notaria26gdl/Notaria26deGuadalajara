import streamlit as st
from utils.google_sheets import connect_google_sheets

# URL de la hoja de Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/1qZX98WUaUGyUL5xSP0lHb7K7MfH7_ny8bRGOZnU1gGc/edit#gid=0"

try:
    sheet = connect_google_sheets(sheet_url)
    st.success("¡Conexión exitosa a Google Sheets!")
    worksheet = sheet.worksheet("Usuarios")
    data = worksheet.get_all_records()
    st.write("Datos obtenidos:", data)
except Exception as e:
    print(f"Error al conectar con Google Sheets: {e}")
