import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
day_df = pd.read_csv("daycleaned.csv")
hour_df = pd.read_csv("hourcleaned.csv")

# Mengubah kolom tanggal
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Mapping untuk musim dan kondisi cuaca
season = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weather = {1: 'Clear', 2: 'Cloudy', 3: 'Light Rain', 4: 'Thunderstorm'}

day_df['season'] = day_df['season'].map(season)
hour_df['season'] = hour_df['season'].map(season)
day_df['weathersit'] = day_df['weathersit'].map(weather)
hour_df['weathersit'] = hour_df['weathersit'].map(weather)

# Sidebar
st.sidebar.image("bike logo2.jpg", width=300)
st.sidebar.markdown("## **City Bike Rental**")

# Rentang Tanggal
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

day_df_filtered = day_df[(day_df['dteday'] >= pd.to_datetime(date_range[0])) & (day_df['dteday'] <= pd.to_datetime(date_range[1]))]
hour_df_filtered = hour_df[(hour_df['dteday'] >= pd.to_datetime(date_range[0])) & (hour_df['dteday'] <= pd.to_datetime(date_range[1]))]

# Waktu Operasional
st.sidebar.markdown("**Operating Hours**")
st.sidebar.text("Monday - Sunday | 24 Hours 🕐")

# Kontak
st.sidebar.markdown("**Contact**")
st.sidebar.markdown("📞 1234567890")

# Metrik Awal
st.title("Bike Rental Dashboard 🚴")
st.subheader("Bike Rental Analysis")

# Total Sharing Bike
total_rentals = day_df['cnt'].sum()
st.metric(label="Total Sharing Bike", value=f"{total_rentals:,}")

# Tren Peminjaman Harian
daily_rentals = day_df.groupby('dteday')['cnt'].sum().reset_index()
st.subheader("Daily Rental Trends")
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(daily_rentals['dteday'], daily_rentals['cnt'], marker='o', linestyle='-', color='#8C2981')
plt.xlabel("Date")
plt.ylabel("Number of Rentals")
plt.grid()
st.pyplot(fig)

# PERTANYAAN BISNIS
# 1. Pengaruh Kondisi Cuaca terhadap Peminjaman
st.subheader("The Effect of Weather Conditions on Rentals")
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x="weathersit", y="cnt", data=day_df, palette="magma", ax=ax)
plt.xlabel("Weather Condition")
plt.ylabel("Number of Rentals")
st.pyplot(fig)

# 2. Perbedaan Pola Peminjaman: Hari Kerja vs Akhir Pekan
st.subheader("Rental Patterns: Weekdays vs Weekends")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=hour_df[hour_df["workingday"] == 1], x="hr", y="cnt", label="Hari Kerja", color="#FF4500", ax=ax)
sns.lineplot(data=hour_df[hour_df["workingday"] == 0], x="hr", y="cnt", label="Akhir Pekan", color="#FFA07A", ax=ax)
plt.xlabel("Hours of the day")
plt.ylabel("Number of Rentals")
plt.legend()
st.pyplot(fig)

# 3. Waktu dengan Permintaan Tertinggi dan Terendah
st.subheader("Time with Highest and Lowest Rentals")
hourly_avg = hour_df.groupby("hr")["cnt"].mean()
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=hourly_avg.index, y=hourly_avg.values, palette="magma", ax=ax)
plt.xlabel("Hours of the day")
plt.ylabel("Average Rental Amount")
plt.xticks(range(24))
st.pyplot(fig)

# Analisis Clustering (Lanjutan)
def categorize_hour(hr):
    if 5 <= hr < 12:
        return "Morning"
    elif 12 <= hr < 17:
        return "Afternoon"
    elif 17 <= hr < 21:
        return "Evening"
    else:
        return "Night"

hour_df["time_category"] = hour_df["hr"].apply(categorize_hour)
cluster = hour_df.groupby("time_category")["cnt"].mean()
st.subheader("Number of rentals based on time span")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=cluster.index, y=cluster.values, palette="magma", ax=ax)
st.pyplot(fig)

st.write("This dashboard presents an in-depth analysis of bicycle rental patterns based on time, weather, and daily habits.")
st.write("Copyright (c), created by Syifa Azzahra Susilo")