import streamlit as st
from dbhelper import DB
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
import pandas as pd
import numpy as np

st.set_page_config(layout='wide')
db=DB()
st.sidebar.title('Flights Analytics')
user_option=st.sidebar.selectbox('Menu',['Select One','Check Flights','Analytics'])
if user_option=='Check Flights':
    st.title('Check Flights')
    col1,col2,col3=st.columns(3)
    city_dest=db.fetch_dest_city_names()
    source_city=db.fetch_source_city_names()
    with col1:
        source=st.selectbox('Source',sorted(source_city))
    with col2:
        destination=st.selectbox('Destination', sorted(city_dest))
    with col3:
        flight_date = st.date_input('Select Flight Date', min_value=date(2013, 1, 1))
    if st.button('Search'):
        formatted_date = flight_date.strftime('%Y-%m-%d')
        results=db.fetch_all_flights(source,destination,formatted_date)

        if results:
            df=pd.DataFrame(results,columns=['Flight Date', 'Departure Time', 'Arrival Time', 'Airline Name', 'Origin', 'Destination'])
            st.write(df)
        else:
            st.write('No Flights found for the selected criteria')
elif user_option=='Analytics':
    airline,frequency=db.fetch_airline_frequency()
    fig = go.Figure(
        go.Pie(
            labels=airline,
            values=frequency,
            hoverinfo="label+percent",
            textinfo="value"
        ))

    st.header("Frequency of Flights")
    st.plotly_chart(fig)

    st.header("Busiest Airports")
    city, frequency1 = db.busy_airport()
    fig = px.bar(
        x=city,
        y=frequency1
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    st.header("Daily Frequency of Flights")
    date, frequency2 = db.daily_frequency()

    print(len(date))
    print(len(frequency2))
    fig = px.line(
        x=date,
        y=frequency2
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

else:
    st.title('Flights Analytics')
    st.write('''
    The Flight Analytics Project is built using Streamlit and MySQL to provide users with insights into flight data.
    Users can check specific flights between airports by entering the origin, destination, and date, retrieving details like departure, arrival times, and airline names. 
    The project also includes visual analytics to identify the busiest airports, most frequent flight routes, and overall traffic patterns. 
    Users can analyze flight trends over time, such as the number of flights per day, delays, and busiest times. 
    The application offers a user-friendly interface with options for querying, filtering, and visualizing flight data dynamically.
    ''')