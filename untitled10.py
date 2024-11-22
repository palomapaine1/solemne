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

    # Filtrar columnas seleccionadas
    columnas = ['Nombre', 'Región', 'Población', 'Área (km²)', 'Fronteras', 'Idiomas Oficiales', 'Zonas Horarias']
    df_cleaned = df[columnas]

    # Mostrar DataFrame con las columnas seleccionadas
    st.write("Datos Filtrados:")
    st.dataframe(df_cleaned)

    # Filtrado interactivo por población mínima
    min_poblacion = st.slider("Filtra por población mínima:", int(df_cleaned['Población'].min()), int(df_cleaned['Población'].max()), step=1000000)
    df_filtered = df_cleaned[df_cleaned['Población'] >= min_poblacion]
    st.write(f"Datos filtrados con población mayor o igual a {min_poblacion}:")
    st.dataframe(df_filtered)
