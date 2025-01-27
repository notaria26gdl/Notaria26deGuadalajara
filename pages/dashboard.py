import streamlit as st

def show_dashboard():
    st.title("📊 Dashboard")
    st.write("Bienvenido al panel de control de Lestrip.")

    # Barra lateral de navegación específica para esta página
    with st.sidebar:
        if st.button("Ir a Gestión de Escrituras"):
            st.session_state["page"] = "Gestión de Escrituras"
            st.rerun()
        if st.button("Ir a Usuarios"):
            st.session_state["page"] = "Usuarios"
            st.rerun()
        if st.button("Ir a Seguimiento"):
            st.session_state["page"] = "Seguimiento"
            st.rerun()
