# -*- coding: utf-8 -*-
import pandas as pd
import requests
import streamlit as st


import pandas as pd
import requests
import streamlit as st

def obtener_datos_api(api_url):
    """Función que realiza la petición a la API y devuelve un DataFrame."""
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data)
    else:
        st.error('Error al obtener los datos de la API')
        return None

# Llamar la función para obtener los datos
api_url = "https://restcountries.com/v3.1/all"
df = obtener_datos_api(api_url)

# Si no se obtienen datos, detener la aplicación
if df is None:
    st.stop()

# Procesar y limpiar datos
df['Nombre'] = df['name'].apply(lambda x: x.get('common') if isinstance(x, dict) else None)
df['Región'] = df['region']
df['Población'] = df['population']
df['Área (km²)'] = df['area']
df['Fronteras'] = df['borders'].apply(lambda x: len(x) if isinstance(x, list) else 0)
df['Idiomas Oficiales'] = df['languages'].apply(lambda x: len(x) if isinstance(x, dict) else 0)
df['Zonas Horarias'] = df['timezones'].apply(lambda x: len(x) if isinstance(x, list) else 0)

# Filtrar columnas seleccionadas
columnas = ['Nombre', 'Región', 'Población', 'Área (km²)', 'Fronteras', 'Idiomas Oficiales', 'Zonas Horarias']
df_cleaned = df[columnas]

# Mostrar DataFrame con las columnas seleccionadas
st.title("Interacción con los datos:")
st.dataframe(df_cleaned)

# Interacción con Streamlit
columnas = st.multiselect('Selecciona las columnas a visualizar', df_cleaned.columns.tolist(), default=df_cleaned.columns.tolist())
df_seleccionado = df_cleaned[columnas]

st.write('Columna Seleccionada:')
st.write(df_seleccionado)

st.write("Media:", df_seleccionado.mean(numeric_only=True))
st.write("Mediana:", df_seleccionado.median(numeric_only=True))
st.write("Desviación estándar:", df_seleccionado.std(numeric_only=True))

columnas_ordenables = df_seleccionado.select_dtypes(include=['number', 'object']).columns
columna_ordenar = st.selectbox('Selecciona una columna para ordenar', columnas_ordenables)
orden = st.radio('Selecciona el orden:', ('Ascendente', 'Descendente'))

df_ordenado = df_seleccionado.sort_values(by=columna_ordenar, ascending=(orden == 'Ascendente'))
st.write('DataFrame Ordenado:')
st.write(df_ordenado)

columna_filtro = st.selectbox("Selecciona una columna para filtrar:", df.select_dtypes(include=['number']).columns)
if columna_filtro:
    min_val, max_val = st.slider(
        f"Selecciona el rango para {columna_filtro}:",
        float(df[columna_filtro].min()),
        float(df[columna_filtro].max()),
        (float(df[columna_filtro].min()), float(df[columna_filtro].max())))
    df_filtrado = df[(df[columna_filtro] >= min_val) & (df[columna_filtro] <= max_val)]
    st.write("**Datos Filtrados:**")
    st.write(df_filtrado)

# Exportar datos
st.subheader("Exportar Datos Filtrados")
formato = st.radio("Elige el formato para descargar:", ('CSV', 'Excel'))

@st.cache_data
def convertir_a_csv(df):
    return df.to_csv(index=False).encode('utf-8')

@st.cache_data
def convertir_a_excel(df):
    import io
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='DatosFiltrados')
    return buffer.getvalue()

if formato == 'CSV':
    st.download_button(
        label="Descargar en CSV",
        data=convertir_a_csv(df_filtrado),
        file_name='datos_filtrados.csv',
        mime='text/csv')
else:
    st.download_button(
        label="Descargar en Excel",
        data=convertir_a_excel(df_filtrado),
        file_name='datos_filtrados.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

     
   
     
           
    
         
        
    
