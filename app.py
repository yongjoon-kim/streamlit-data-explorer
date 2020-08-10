import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber Pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading Data...')
data = load_data(20000)
data_load_state.text('Loading Data Done!')

st.subheader('Raw Data')
if st.checkbox('Show Raw Data'):
    st.write(data)

st.subheader('Number of Pickups by Hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

st.subheader('All Pickup Locations')
st.map(data)

st.subheader('Pickup locations and the Frequency at Each Location')
st.text('Filter by Hour')
hour_to_filter = st.slider('Hour', 0, 24, 17)
filtered_data = data.loc[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.deck_gl_chart(
     viewport={
         'latitude': 40.71,
         'longitude': -74,
         'zoom': 11,
         'pitch': 50,
     },
     layers=[{
         'type': 'HexagonLayer',
         'data': filtered_data,
         'radius': 200,
         'elevationScale': 4,
         'elevationRange': [0, 1000],
         'pickable': True,
         'extruded': True,
     }, {
         'type': 'ScatterplotLayer',
         'data': filtered_data,
     }])