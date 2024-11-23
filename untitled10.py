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
    
    # Cargar archivo o usar ejemplo
    st.subheader("Carga de Datos")
    uploaded_file = st.file_uploader("Sube un archivo CSV o Excel:", type=["csv", "xlsx"])
    
    if uploaded_file:
        try:
            # Detectar formato y cargar archivo
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            st.success("Archivo cargado exitosamente.")
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")
            df = pd.DataFrame()
    else:
        # Crear un DataFrame de ejemplo si no se sube archivo
        st.info("Usando datos de ejemplo porque no se subió archivo.")
        data = {'Categoría': ['A', 'B', 'C', 'D', 'E'],'Valor 1': [10, 20, 30, 40, 50],'Valor 2': [15, 25, 35, 45, 55],'Valor 3': [5, 15, 25, 35, 45],}
        df = pd.DataFrame(data)
    
    # Verificar si el DataFrame tiene datos
    if df.empty:
        st.error("No hay datos disponibles. Sube un archivo para continuar.")
    else:
        # Mostrar los datos originales
        st.subheader("Datos Originales")
        st.write(df)
    
        # Sección de gráficos interactivos
        st.subheader("Gráficos Interactivos")
    
        # Selección de tipo de gráfico
        tipo_grafico = st.selectbox("Selecciona el tipo de gráfico:", 
                                    ["Dispersión", "Línea", "Barras", "Histograma", "Pastel"])
    
        # Selección de variables
        columnas_numericas = df.select_dtypes(include=['number']).columns
        if len(columnas_numericas) > 0:
            columna_x = st.selectbox("Selecciona la columna para el eje X:", columnas_numericas)
            columna_y = st.selectbox("Selecciona la columna para el eje Y:", columnas_numericas)
    
            # Ajuste de rango para los ejes
            st.subheader("Ajustar Rango de los Ejes")
            rango_x = st.slider("Rango del eje X:", 
                                float(df[columna_x].min()), 
                                float(df[columna_x].max()), 
                                (float(df[columna_x].min()), float(df[columna_x].max())))
            rango_y = st.slider("Rango del eje Y:", 
                                float(df[columna_y].min()), 
                                float(df[columna_y].max()), 
                                (float(df[columna_y].min()), float(df[columna_y].max())))
            # Crear gráfico
            fig, ax = plt.subplots()
            if tipo_grafico == "Dispersión":
                ax.scatter(df[columna_x], df[columna_y], color='blue', alpha=0.7)
            elif tipo_grafico == "Línea":
                ax.plot(df[columna_x], df[columna_y], color='green', marker='o')
            elif tipo_grafico == "Barras":
                ax.bar(df[columna_x], df[columna_y], color='orange', alpha=0.7)
            elif tipo_grafico == "Histograma":
                ax.hist(df[columna_x], bins=10, color='purple', alpha=0.7)
                ax.set_ylabel("Frecuencia")
            elif tipo_grafico == "Pastel":
                if len(df[columna_x].unique()) <= 10:
                    ax.pie(df[columna_y], labels=df[columna_x], autopct='%1.1f%%')
                    ax.set_aspect('equal')
                else:
                    st.warning("El gráfico de pastel requiere menos de 10 categorías únicas en el eje X.")
                    st.stop()
    
            # Etiquetas y título
            if tipo_grafico != "Pastel":
                ax.set_title(f"{tipo_grafico}: {columna_y} vs {columna_x}")
                ax.set_xlabel(columna_x)
                ax.set_ylabel(columna_y)
    
            # Mostrar gráfico
            st.pyplot(fig)
    
            # Descargar gráfico en PNG
            st.subheader("Descargar Gráfico")
            buffer = io.BytesIO()
            fig.savefig(buffer, format='png')
            buffer.seek(0)
            st.download_button(
                label="Descargar gráfico como PNG",
                data=buffer,
                file_name="grafico.png",
                mime="image/png")
        else:
            st.warning("El DataFrame no contiene columnas numéricas para generar gráficos.")
    
         
        
    
