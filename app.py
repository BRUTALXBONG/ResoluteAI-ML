import streamlit as st
import pandas as pd

# Read the raw data
raw_data = pd.read_csv("C:\\Users\\User\\Downloads\\rawdata - inputsheet.csv")

# Combine Date and Time into a single datetime column
raw_data['DateTime'] = pd.to_datetime(raw_data['date'] + ' ' + raw_data['time'])

# Calculate the duration for each activity
raw_data['Duration'] = raw_data.groupby(['date', 'location'])['DateTime'].diff().dt.total_seconds().fillna(0)

# Group by Date and Activity and sum the durations
result = raw_data.groupby(['date', 'position', 'activity'])['Duration'].sum().reset_index()

# Pivot the data to have 'inside' and 'outside' as columns
result_pivot = result.pivot_table(index=['date'], columns=['position', 'activity'], values='Duration', aggfunc='sum').fillna(0)

# Calculate date-wise total duration for each inside and outside
datewise_duration_inside = result_pivot['inside'].sum(axis=1)
datewise_duration_outside = result_pivot['outside'].sum(axis=1)

# Calculate date-wise number of picking and placing activities done
datewise_activities = raw_data.pivot_table(index='date', columns='activity', values='position', aggfunc='count').fillna(0)

# Streamlit web application
st.title('Data Analysis Results')

# Display date-wise total duration for each inside and outside
st.subheader('Date-wise total duration for each inside and outside')
st.write(datewise_duration_inside)
st.write(datewise_duration_outside)

# Display date-wise number of picking and placing activities done
st.subheader('Date-wise number of picking and placing activities done')
st.write(datewise_activities)

