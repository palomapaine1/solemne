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



     
   
     
           
    
         
        
    
