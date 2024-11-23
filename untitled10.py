# -*- coding: utf-8 -*-
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
# Si hay datos, mostrar el DataFrame, mostrar dataframe con las columna seleccionadas, permitir filtrado y mostrar gráficos.

if df is not None:
    # Selección de columnas relevantes
    df['Nombre'] = df['name'].apply(lambda x: x.get('common') if isinstance(x, dict) else None)
    df['Región'] = df['region']
    df['Población'] = df['population']
    df['Área (km²)'] = df['area']
    df['Fronteras'] = df['borders'].apply(lambda x: len(x) if isinstance(x, list) else 0)
    df['Idiomas Oficiales'] = df['languages'].apply(lambda x: len(x) if isinstance(x, dict) else 0)
    df['Zonas Horarias'] = df['timezones'].apply(lambda x: len(x) if isinstance(x, list) else 0)

    
    columnas = ['Nombre', 'Región', 'Población', 'Área (km²)', 'Fronteras', 'Idiomas Oficiales', 'Zonas Horarias']
    # Dataframe para trabajar
    df_cleaned = df[columnas]

    # Mostrar DataFrame con las columnas seleccionadas
    st.title("Interacción con los datos")
    st.header("Mostrar los datos originales")
    st.dataframe(df_cleaned)
    
    st.header("Selecciona una columna del dataframe utilizando un menú desplegable")
    columnas = st.multiselect('Selecciona las columnas a visualizar', df_cleaned.columns.tolist(), default=df_cleaned.columns.tolist())
    df_seleccionado = df_cleaned[columnas]
    # Mostrar el DataFrame con las columnas seleccionadas
    st.write('Columna Selecionada:')
    st.write(df_seleccionado)
    st.write("Estadísticas de las columnas seleccionadas:")
    st.write("Media:",)
    st.write(df_seleccionado.mean(numeric_only=True))
    st.write("Mediana:",)
    st.write(df_seleccionado.median(numeric_only=True))
    st.write("Desviación estándar:",)
    st.write(df_seleccionado.std(numeric_only=True))
    columna_ordenar = st.selectbox('Selecciona una columna para ordenar', df_seleccionado.columns)
    # Control para seleccionar el orden (ascendente o descendente)
    orden = st.radio('Selecciona el orden:', ('Ascendente', 'Descendente'))
    # Ordenar el DataFrame según la columna seleccionada y el orden elegido
    if orden == 'Ascendente':
        df_ordenado = df_seleccionado.sort_values(by=columna_ordenar, ascending=True)
    else:
        df_ordenado = df_seleccionado.sort_values(by=columna_ordenar, ascending=False)
    # Mostrar el DataFrame ordenado
    st.write('DataFrame Ordenado:')
    st.write(df_ordenado)
    st.subheader("Filtrar Datos")
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

    # Botón para descargar los datos filtrados
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
            writer.save()
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
    # Título de la aplicación
st.title("Gráficos Interactivos con Streamlit")

# Cargar datos
st.sidebar.header("Subir un archivo CSV")
uploaded_file = st.sidebar.file_uploader("Selecciona un archivo CSV", type=["csv"])

if uploaded_file:
    # Leer archivo CSV
    df = pd.read_csv(uploaded_file)

    # Mostrar una vista previa de los datos
    st.subheader("Vista previa de los datos")
    st.dataframe(df)
# Cargar los datos (reemplaza con tu fuente de datos)
df = pd.read_csv("datos.csv")

# Título de la aplicación
st.title("Explorador de Datos Interactivo")

# Selección de las columnas numéricas
columnas_numericas = df.select_dtypes(include=['number']).columns
x_axis = st.selectbox("Selecciona el eje X", columnas_numericas)
y_axis = st.selectbox("Selecciona el eje Y", columnas_numericas)

# Rango personalizado para los ejes
min_x = st.number_input("Mínimo para el eje X", value=df[x_axis].min())
max_x = st.number_input("Máximo para el eje X", value=df[x_axis].max())
min_y = st.number_input("Mínimo para el eje Y", value=df[y_axis].min())
max_y = st.number_input("Máximo para el eje Y", value=df[y_axis].max())

# Selección del tipo de gráfico
tipo_grafico = st.selectbox("Selecciona el tipo de gráfico", ["Dispersión", "Línea", "Barra", "Histograma", "Pastel"])

# Función para generar el gráfico
def generar_grafico(x, y, tipo, min_x, max_x, min_y, max_y):
    if tipo == "Dispersión":
        fig = px.scatter(df, x=x, y=y)
    elif tipo == "Línea":
        fig = px.line(df, x=x, y=y)
    elif tipo == "Barra":
        fig = px.bar(df, x=x, y=y)
    elif tipo == "Histograma":
        fig = px.histogram(df, x=x)
    else:
        fig = px.pie(df, values=y, names=x)
   
     
           
    
         
        
    
