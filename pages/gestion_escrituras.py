import streamlit as st

def gestion_escrituras():
    st.title("📜 Gestión de Escrituras")
    st.write("Administra todas las escrituras aquí.")

    # Barra lateral de navegación específica para esta página
    with st.sidebar:
        if st.button("Ir al Dashboard"):
            st.session_state["page"] = "Dashboard"
            st.rerun()
        if st.button("Ir a Usuarios"):
            st.session_state["page"] = "Usuarios"
            st.rerun()
        if st.button("Ir a Seguimiento"):
            st.session_state["page"] = "Seguimiento"
            st.rerun()
