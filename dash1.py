import streamlit as st
import pandas as pd
import zipfile

# ========================== CONFIGURACIÓN INICIAL ==========================
st.set_page_config(page_title="Dashboard Empresarial", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        body {
            background-color: #f9f9f9;
            color: #1f1f1f;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 18px;
            padding: 10px;
            border-bottom: 3px solid transparent;
        }
        .stTabs [aria-selected="true"] {
            border-bottom: 3px solid #004b8d;
            color: #004b8d;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Panel Empresarial")
tabs = st.tabs(["🏠 Dashboard", "🧮 Calculadora", "🔧 Por definir"])

# ========================== PESTAÑA 1: DASHBOARD ==========================
with tabs[0]:
    st.subheader("📂 Cargar base de datos")

    uploaded_file = st.file_uploader("Sube un ZIP que contenga el archivo 'DF.csv'", type="zip")

    @st.cache_data
    def load_zip_csv(upload, internal_name="DF.csv"):
        with zipfile.ZipFile(upload) as z:
            with z.open(internal_name) as f:
                return pd.read_csv(f)

    df = None
    df_filtrado = None

    if uploaded_file:
        try:
            df = load_zip_csv(uploaded_file)
            st.success("✅ Datos cargados exitosamente")
            st.dataframe(df.head())

            # ========== FILTROS ==========
            with st.container():
                st.markdown("### 🎚️ Filtros del dashboard")
                col1, col2, col3 = st.columns(3)

                with col1:
                    categoria_sel = st.multiselect("Categoría de producto", df['Categoría'].dropna().unique(), default=df['Categoría'].dropna().unique())
                with col2:
                    region_sel = st.multiselect("Región", df['region'].dropna().unique(), default=df['region'].dropna().unique())
                with col3:
                    mes_sel = st.multiselect("Mes", sorted(df['mes'].dropna().unique()), default=sorted(df['mes'].dropna().unique()))

                df_filtrado = df[
                    (df['Categoría'].isin(categoria_sel)) &
                    (df['region'].isin(region_sel)) &
                    (df['mes'].isin(mes_sel))
                ]

            # ========== KPIs ==========
            st.markdown("## 🧭 Visión General de la Operación")
            with st.container():
                st.markdown("### 🔢 Indicadores clave")
                col1, col2, col3, col4, col5 = st.columns(5)

                with col1:
                    st.metric(label="Total de pedidos", value=f"{len(df_filtrado):,}")
                with col2:
                    pct_ontime = df_filtrado['entrega_a_tiempo'].mean() * 100
                    st.metric(label="Entregas a tiempo (%)", value=f"{pct_ontime:.1f}%")
                with col3:
                    pct_flete_alto = (df_filtrado['costo_de_flete'] / df_filtrado['precio'] > 0.5).mean() * 100
                    st.metric(label="Flete > 50% del producto (%)", value=f"{pct_flete_alto:.1f}%")
                with col4:
                    pct_anticipadas = (df_filtrado['desviacion_vs_promesa'] < -5).mean() * 100
                    st.metric(label="Entregas anticipadas (%)", value=f"{pct_anticipadas:.1f}%")
                with col5:
                    clientes_frecuentes = df_filtrado['cliente_id'].value_counts().gt(5).sum()
                    st.metric(label="Clientes frecuentes", value=clientes_frecuentes)

            # ========== GRÁFICAS ==========
            with st.container():
                st.markdown("### 📊 Análisis visual")
                tab1, tab2, tab3 = st.tabs(["Pedidos por Año", "Centros de Distribución", "Demanda por Estado"])
                with tab1: st.write("⬅️ Aquí irá la gráfica de pedidos por año.")
                with tab2: st.write("⬅️ Aquí irá el treemap o barras de centros de distribución.")
                with tab3: st.write("⬅️ Aquí irá la gráfica de estados con más entregas.")

            # ========== INSIGHTS ==========
            with st.container():
                st.markdown("### 🔍 Hallazgos operativos clave")
                st.info("""
                • Muchos pedidos llegan antes de tiempo → rutas mal optimizadas.  
                • Hay días con camiones medio vacíos → oportunidad para consolidación.  
                • Alta proporción de pedidos con flete muy caro respecto al producto.  
                """)

            # ========== MODELOS ==========
            with st.container():
                st.markdown("### 🤖 Modelos de predicción")
                col1, col2 = st.columns(2)
                with col1:
                    st.success("Modelo de clasificación de días de entrega: Accuracy ~69%, F1 ~68")
                with col2:
                    st.success("Modelo de regresión del flete: R² ~0.71")
                st.caption("Estos modelos pueden usarse para consolidar entregas, prevenir sobrecostos y predecir el precio antes de la compra.")

        except Exception as e:
            st.error(f"⚠️ Error al cargar los datos: {e}")

# ========================== PESTAÑA 2: CALCULADORA ==========================
with tabs[1]:
    st.subheader("🧮 Herramienta de Cálculo")
    st.warning("Aquí se incluirán funciones interactivas para cálculos personalizados.")

# ========================== PESTAÑA 3: POR DEFINIR ==========================
with tabs[2]:
    st.subheader("🔧 Contenido en Desarrollo")
    st.success("Esta sección está en construcción. Pronto habrá más.")

