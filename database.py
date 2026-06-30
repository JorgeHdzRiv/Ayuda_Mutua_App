import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Inicialización del cliente
url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

# --- Funciones de Acceso a Datos ---
def obtener_datos(tabla):
    """Obtiene todos los registros de una tabla, ordenados por fecha de creación."""
    return supabase.table(tabla).select("*").order("created_at", desc=True).execute().data

def insertar_donativo(id_donante, monto, fecha, metodo):
    """Inserta un nuevo donativo. La columna created_at se genera automáticamente en BD."""
    data = {
        "id_donante": id_donante,
        "monto": monto,
        "fecha": fecha,
        "metodo": metodo
    }
    return supabase.table("donativos").insert(data).execute()

def insertar_evento(nombre, fecha, lugar):
    """Inserta un nuevo evento."""
    data = {
        "nombre": nombre,
        "fecha": fecha,
        "lugar": lugar
    }
    return supabase.table("eventos").insert(data).execute()

def verificar_usuario(username, password):
    """Verifica si las credenciales coinciden en la base de datos."""
    respuesta = supabase.table("usuarios").select("*").eq("nombre", username).eq("password", password).execute()
    
    if respuesta.data:
        return respuesta.data[0]  # Retorna el diccionario con los datos del usuario
    return None