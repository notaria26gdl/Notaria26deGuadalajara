import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import bcrypt

def manage_users():
    st.title("👤 Gestión de Usuarios")
    st.subheader("Agregar Nuevo Usuario")

    # Barra lateral de navegación
    with st.sidebar:
        if st.button("Ir al Dashboard"):
            st.session_state["page"] = "Dashboard"
            st.rerun()
        if st.button("Ir a Gestión de Escrituras"):
            st.session_state["page"] = "Gestión de Escrituras"
            st.rerun()
        if st.button("Ir a Seguimiento"):
            st.session_state["page"] = "Seguimiento"
            st.rerun()

    # Campos para agregar un nuevo usuario
    new_user = st.text_input("Usuario")
    new_password = st.text_input("Contraseña", type="password")
    role = st.selectbox("Rol", ["administrador", "notario", "cliente"])

    if st.button("Agregar Usuario"):
        if new_user and new_password:
            # Cifrar la contraseña antes de guardarla
            hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

            try:
                # Conectar con Google Sheets
                creds = Credentials.from_service_account_file("credenciales.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
                client = gspread.authorize(creds)
                sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1qZX98WUaUGyUL5xSP0lHb7K7MfH7_ny8bRGOZnU1gGc/edit#gid=0")
                worksheet = sheet.worksheet("Usuarios")

                # Agregar nuevo usuario a la hoja
                worksheet.append_row([new_user.strip().lower(), hashed_password, role])

                st.success(f"Usuario {new_user} agregado exitosamente con rol {role}.")
            except Exception as e:
                st.error(f"Error al conectar con Google Sheets: {e}")

        else:
            st.error("Por favor, completa todos los campos.")

    # Mostrar usuarios existentes en la hoja
    st.subheader("Usuarios Registrados")
    try:
        creds = Credentials.from_service_account_file("credenciales.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
        client = gspread.authorize(creds)
        sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1qZX98WUaUGyUL5xSP0lHb7K7MfH7_ny8bRGOZnU1gGc/edit#gid=0")
        worksheet = sheet.worksheet("Usuarios")
        users_data = worksheet.get_all_records()

        if users_data:
            st.table(users_data)
        else:
            st.info("No hay usuarios registrados.")
    except Exception as e:
        st.error(f"No se pudieron obtener los usuarios: {e}")
