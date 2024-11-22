# -*- coding: utf-8 -*-
import streamlit as st
import requests
import pandas as pd

import requests
import pandas as pd

# Función para obtener los datos de la API REST Countries
def obtener_datos_paises(api_url):
    """Realiza la petición GET y devuelve los datos como un DataFrame."""
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al obtener los datos de la API")
        return None

# URL de la API REST Countries
api_url = "https://restcountries.com/v3.1/all"

# Obtener los datos de la API
data = obtener_datos_paises(api_url)

# Procesar los datos si la respuesta es exitosa
if df is not None:
  paises = []
  regiones = []
  poblaciones = []
  areas = []
  fronteras = []
  idiomas = []
  zonas_horarias = []

  # Recorrer la lista de países en la respuesta
  for pais in df:
    paises.append(pais.get("name", {}).get("common", "Desconocido"))
    regiones.append(pais.get("region", "Desconocido"))
    poblaciones.append(pais.get("population", 0))
    areas.append(pais.get("area", 0))
    fronteras.append(len(pais.get("borders", [])))
    idiomas.append(len(pais.get("languages", {}).keys()))
    zonas_horarias.append(len(pais.get("timezones", [])))

  df = pd.DataFrame({'País': paises,'Región': regiones,'Población': poblaciones,'Área (km²)': areas,'Número de Fronteras': fronteras,'Número de Idiomas Oficiales': idiomas,'Número de Zonas Horarias': zonas_horarias})

  # Mostrar los primeros 5 registros del DataFrame
  st.write("Datos de los países:")
  st.write(df.head())

  # Mostrar más interactividad con Streamlit (filtro por región)
  region = st.selectbox("Selecciona una región:", df['Región'].unique())
  df_filtrado = df[df['Región'] == region]
  st.write(f"Países de la región {region}:")
  st.write(df_filtrado)

