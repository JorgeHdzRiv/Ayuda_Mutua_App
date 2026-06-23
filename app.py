import streamlit as st
import re
import pandas as pd
from sklearn.cluster import KMeans
import plotly.express as px
from database import obtener_datos, insertar_donativo, verificar_usuario

st.set_page_config(page_title="Ayuda Mutua - Sistema", layout="wide")

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    div[data-testid="metric-container"], .stDataFrame, .stTable {
        background-color: var(--secondary-background-color);
        border-radius: 10px;
        padding: 15px 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid var(--border-color);
        color: var(--text-color);
    }
    canvas { background-color: transparent !important; }
    </style>
""", unsafe_allow_html=True)

# Inicializar estados de sesión
if "logueado" not in st.session_state:
    st.session_state.logueado = False
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""

# --- FUNCIÓN DE LOGIN ---
def login():
    st.title("🔐 Iniciar Sesión")
    st.write("Sistema de Gestión Interna - Ayuda Mutua")
    
    with st.container():
        # Formulario normal para usuarios registrados
        with st.form("form_login"):
            user_input = st.text_input("Usuario (nombre.apellido)")
            password = st.text_input("Contraseña", type="password")
            
            submitted = st.form_submit_button("Acceder", width="stretch")
            
            if submitted:
                patron = r"^[a-z]+\.[a-z]+$"
                if not re.match(patron, user_input.lower()):
                    st.error("Formato inválido. Debe ser: nombre.apellido")
                else:
                    usuario_db = verificar_usuario(user_input.lower(), password)
                    if usuario_db:
                        st.session_state.logueado = True
                        nombre_limpio = user_input.replace(".", " ").title()
                        st.session_state.usuario_actual = nombre_limpio
                        st.rerun()
                    else:
                        st.error("Usuario o contraseña incorrectos")
        
        # Separador visual
        st.markdown("---")
        st.write("¿Quieres probar el sistema sin una cuenta?")
        
        # Botón de acceso rápido para invitados
        if st.button("Explorar como Invitado (Modo Demo)", width="stretch"):
            st.session_state.logueado = True
            st.session_state.usuario_actual = "Invitado Fundacion"
            st.rerun()

# --- LÓGICA PRINCIPAL ---
if not st.session_state.logueado:
    login()
else:
    # Navegación Lateral
    st.sidebar.title("♡ Ayuda Mutua")
    st.sidebar.markdown("---")
    
    choice = st.sidebar.radio("Navegación", ["Panel de Control", "Registro de Donativos", "Donantes", "Análisis Avanzado"])
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logueado = False
        st.session_state.usuario_actual = ""
        st.rerun()

    donativos = obtener_datos("donativos")
    donantes = obtener_datos("donantes")
    eventos = obtener_datos("eventos")

    # --- PANEL DE CONTROL ---
    if choice == "Panel de Control":
        st.markdown(f"### Bienvenido/a, {st.session_state.usuario_actual}") 
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_monto = sum(d['monto'] for d in donativos) if donativos else 0
        total_donantes = len(donantes) if donantes else 0
        total_eventos = len(eventos) if eventos else 0
        
        col1.metric("DONATIVOS RECIBIDOS", f"${total_monto:,.0f}")
        col2.metric("DONANTES ACTIVOS", str(total_donantes))
        col3.metric("EVENTOS REGISTRADOS", str(total_eventos))
        col4.metric("INVENTARIO", "En desarrollo") 
        
        st.markdown("<br>", unsafe_allow_html=True)

        col_grafica, col_evento = st.columns([3, 1])
        
        with col_grafica:
            st.markdown("#### Donativos recibidos")
            if donativos:
                df = pd.DataFrame(donativos)
                df['fecha'] = pd.to_datetime(df['fecha'])
                df_grouped = df.groupby(df['fecha'].dt.to_period('M')).agg({'monto':'sum'}).reset_index()
                df_grouped['fecha'] = df_grouped['fecha'].dt.to_timestamp()
                
                st.line_chart(data=df_grouped, x='fecha', y='monto', width="stretch")
            else:
                st.info("No hay donativos para graficar.")
                
        with col_evento:
            st.markdown("#### Próximo Evento")
            if eventos:
                df_evt = pd.DataFrame(eventos).sort_values(by='fecha', ascending=False)
                prox_evt = df_evt.iloc[0]
                st.info(f"**{prox_evt['nombre']}**\n\n📅 {prox_evt['fecha']}\n\n📍 {prox_evt['lugar']}")
            else:
                st.info("No hay eventos próximos.")
            
        st.markdown("---")
        st.markdown("#### Últimos registros de donativos")
        if donativos:
            df_display = pd.DataFrame(donativos)[['id_donativo', 'id_donante', 'monto', 'fecha', 'metodo']]
            st.dataframe(df_display, width="stretch", hide_index=True)

    # --- REGISTRO DE DONATIVOS ---
    elif choice == "Registro de Donativos":
        st.title("Registro de Donativos")
        st.write("Gestión y seguimiento de contribuciones")
        
        # Validar si es el invitado
        es_invitado = (st.session_state.usuario_actual == "Invitado Fundacion")
        if es_invitado:
            st.warning("Estás en modo demostración. No se permite guardar nuevos registros.")

        nombres_donantes = {d['nombre_completo']: d['id_donante'] for d in donantes}
        
        if not donantes:
            st.warning("No hay donantes registrados en la base de datos.")
        else:
            with st.container():
                with st.form("form_donativo", clear_on_submit=True):
                    st.markdown("#### + Nuevo registro")
                    donante_sel = st.selectbox("Nombre del Donante", options=list(nombres_donantes.keys()))
                    
                    col_monto, col_fecha = st.columns(2)
                    monto = col_monto.number_input("Monto (MXN)", min_value=0.0)
                    fecha = col_fecha.date_input("Fecha")
                    
                    metodo = st.radio("Método de pago", ["Transferencia", "Efectivo", "Cheque"], horizontal=True)
                    
                    # AQUÍ ES DONDE VA EL BOTÓN, dentro del form, usando la variable es_invitado
                    submitted = st.form_submit_button("Guardar Registro", disabled=es_invitado)
                    
                    if submitted and not es_invitado:
                        try:
                            insertar_donativo(nombres_donantes[donante_sel], monto, str(fecha), metodo)
                            st.success("Donativo guardado exitosamente.")
                        except Exception as e:
                            st.error(f"Error: {e}")

    # --- DONANTES ---
    elif choice == "Donantes":
        st.title("Directorio de Donantes")
        st.write("Lista completa de donantes registrados en la fundación.")
        
        if donantes:
            df_donantes = pd.DataFrame(donantes)
            if 'created_at' in df_donantes.columns:
                df_donantes = df_donantes.drop(columns=['created_at'])
            
            st.dataframe(df_donantes, width="stretch", hide_index=True)
        else:
            st.info("Aún no hay donantes registrados.")

    # --- ANÁLISIS AVANZADO (DATA SCIENCE) ---
    elif choice == "Análisis Avanzado":
        st.title("🧠 Análisis de Donantes (Machine Learning)")
        st.write("Segmentación automática de donantes utilizando el algoritmo K-Means.")

        if donativos and donantes:
            # 1. Preparación de los datos (Feature Engineering)
            df_donativos = pd.DataFrame(donativos)
            df_donantes = pd.DataFrame(donantes)

            # Agrupar donativos por donante
            df_rfm = df_donativos.groupby('id_donante').agg(
                Frecuencia=('id_donativo', 'count'),
                Monto_Total=('monto', 'sum')
            ).reset_index()

            # Unir con nombres
            df_final = pd.merge(df_rfm, df_donantes[['id_donante', 'nombre_completo']], on='id_donante')

            # 2. Modelo de Machine Learning (K-Means)
            if len(df_final) >= 3: 
                st.markdown("#### Clustering de Comportamiento")
                
                X = df_final[['Frecuencia', 'Monto_Total']]
                
                kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
                df_final['Cluster'] = kmeans.fit_predict(X)

                nombres_clusters = {0: "Ocasionales", 1: "Frecuentes", 2: "Grandes Donadores"}
                df_final['Segmento'] = df_final['Cluster'].map(nombres_clusters)

                # 3. Visualización con Plotly
                fig = px.scatter(
                    df_final, 
                    x='Frecuencia', 
                    y='Monto_Total', 
                    color='Segmento',
                    hover_name='nombre_completo',
                    size='Monto_Total',
                    title="Distribución de Segmentos de Donantes",
                    labels={'Frecuencia': 'Número de Donativos', 'Monto_Total': 'Monto Total (MXN)'},
                    template="plotly_white"
                )
                
                st.plotly_chart(fig, width='stretch')

                # 4. Tabla de resultados analíticos
                st.markdown("#### Detalle de Segmentación")
                st.dataframe(df_final[['nombre_completo', 'Frecuencia', 'Monto_Total', 'Segmento']].sort_values(by='Monto_Total', ascending=False), width="stretch", hide_index=True)
            else:
                st.warning("Se necesitan más datos para generar los clusters de Machine Learning.")
        else:
            st.info("No hay datos suficientes para realizar el análisis.")