# dashboard.py

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load your cleaned dataset (update the path accordingly)
df = pd.read_csv("owid-covid-data.csv")

# Filter countries of interest
selected_countries = ['Kenya', 'United States', 'India']
df = df[df['location'].isin(selected_countries)]

# Drop rows with missing critical data
df = df.dropna(subset=['date', 'total_cases', 'total_deaths', 'total_vaccinations'])

# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Fill or interpolate missing numeric values
numeric_columns = ['total_cases', 'total_deaths', 'new_cases', 'new_deaths', 'total_vaccinations']
df[numeric_columns] = df[numeric_columns].interpolate()

# Sidebar: User Input
st.sidebar.header("Filter Options")
country = st.sidebar.selectbox("Select a Country", df['location'].unique())
start_date = st.sidebar.date_input("Start Date", df['date'].min())
end_date = st.sidebar.date_input("End Date", df['date'].max())

# Filter Data
df_filtered = df[(df['location'] == country) & (df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

# Title
st.title(f"COVID-19 Dashboard for {country}")

# Total Cases Over Time
st.subheader("Total Cases Over Time")
fig1, ax1 = plt.subplots()
ax1.plot(df_filtered['date'], df_filtered['total_cases'], color='blue')
ax1.set_xlabel('Date')
ax1.set_ylabel('Total Cases')
st.pyplot(fig1)

# Total Deaths Over Time
st.subheader("Total Deaths Over Time")
fig2, ax2 = plt.subplots()
ax2.plot(df_filtered['date'], df_filtered['total_deaths'], color='red')
ax2.set_xlabel('Date')
ax2.set_ylabel('Total Deaths')
st.pyplot(fig2)

# Vaccinations Over Time
st.subheader("Total Vaccinations Over Time")
fig3, ax3 = plt.subplots()
ax3.plot(df_filtered['date'], df_filtered['total_vaccinations'], color='green')
ax3.set_xlabel('Date')
ax3.set_ylabel('Total Vaccinations')
st.pyplot(fig3)

# Death Rate
df_filtered['death_rate'] = df_filtered['total_deaths'] / df_filtered['total_cases']
st.subheader("Death Rate Over Time")
fig4, ax4 = plt.subplots()
ax4.plot(df_filtered['date'], df_filtered['death_rate'], color='purple')
ax4.set_xlabel('Date')
ax4.set_ylabel('Death Rate')
st.pyplot(fig4)

# Show raw data
if st.checkbox("Show Raw Data"):
    st.write(df_filtered)
