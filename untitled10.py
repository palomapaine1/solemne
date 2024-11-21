# -*- coding: utf-8 -*-
"""Untitled10.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qTA8Z609-qp2e6v5iHofjmWSbVeoCzDz
"""

import streamlit as st
import requests
import pandas as pd

def obtener_datos_api(api_url):
"""Función que realiza la petición a la API y devuelve un
DataFrame."""
response = requests.get(api_url)
if response.status_code == 200:
data = response.json()
return pd.DataFrame(data)
else:
st.error('Error al obtener los datos de la API')
return None
# Llamar la función para obtener los datos
api_url="https://restcountries.com/v3.1/all"
df = obtener_datos_api(api_url)
# Si hay datos, mostrar el DataFrame, mostrar dataframe con las columnas
seleccionadas, permitir filtrado y mostrar gráficos.
if df is not None:
# Mostrar las primeras 5 filas del dataframe
st.write(df.head())