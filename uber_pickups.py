# Importamos librerias
import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')     # Titulo de la app

# función para cargar los datos
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data     # permite almacenar en caché los datos. En caso de no variar el codigo de la funcion y el parametro, lanza el mismo resultado ahorrando tiempo. 
def load_data(nrows):
    # Esta funcion load_data descarga algunos datos, los coloca en un marco de datos de Pandas y 
    # convierte la columna de fecha de texto a fecha y hora.
    # La función acepta un único parámetro (nrows), que especifica 
    # el n° de filas que desea cargar en el marco de datos.
    
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Cree un elemento de texto e informe al lector que los datos se están cargando.
data_load_state = st.text('Loading data...')

# Carga 10.000 registros en el dataframe.
data = load_data(10000)

# Notifica al usuario que los datos se cargaron.
data_load_state.text('Loading data...done!')

if st.checkbox('Show raw data'): # Si está tildado el checkbox, hace lo siguiente:
    st.subheader('Raw data')     # Agrega subtitulo
    st.write(data)               # Imprime dataframe

st.subheader('Number of pickups by hour')   # Agrega subtitulo
# Dibuja un histograma para ver las horas de mayor actividad de Uber en Nueva York
hist_values = np.histogram( data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)   # Metodo para dibujar el histograma

# Para mostrar la concentración de recolección, usemos 
# st.map() la función para superponer los datos en un mapa de Nueva York.
st.subheader('Map of all pickups')  # Agrega subtitulo
st.map(data)    # Genera mapa con los datos del dataframe


# Filtro control deslizante
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h

# Dibuja el mapa mostrando la concentración de recolecciones a las 17:00.
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)

