from utils.google_sheets import get_credentials_from_secrets

try:
    print("Importación exitosa")
except ImportError as e:
    print(f"Error de importación: {e}")
