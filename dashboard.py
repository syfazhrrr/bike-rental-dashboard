import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 

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

# Memastikan rentang tanggal default valid
date_range = st.sidebar.date_input(
    "Select Date Range", 
    [min_date, max_date], 
    min_value=min_date, 
    max_value=max_date
)

# Menangani jika pengguna memilih hanya satu tanggal atau tidak memilih sama sekali
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
elif isinstance(date_range, pd.Timestamp):  # Jika hanya satu tanggal yang dipilih
    start_date = end_date = pd.to_datetime(date_range)
else:
    start_date, end_date = min_date, max_date  # Default ke rentang penuh jika tidak valid

# Filter dataset berdasarkan rentang tanggal
day_df_filtered = day_df[(day_df['dteday'] >= start_date) & (day_df['dteday'] <= end_date)]
hour_df_filtered = hour_df[(hour_df['dteday'] >= start_date) & (hour_df['dteday'] <= end_date)]

# Menampilkan informasi filtering
st.write(f"***Showing data from*** {start_date.date()} ***to*** {end_date.date()}")
st.write(f"***Filtered Data Count:*** {len(day_df_filtered)} rows")

# Waktu Operasional
st.sidebar.markdown("**Operating Hours**")
st.sidebar.text("Monday - Sunday | 24 Hours 🕐")

# Kontak
st.sidebar.markdown("**Contact**")
st.sidebar.markdown("📞 1234567890")

# Metrik Awal
st.title("Bike Rental Dashboard 🚴")
st.subheader("Bike Rental Analysis")

# Total Sharing Bike (Menggunakan Data yang Difilter)
total_rentals = day_df_filtered['cnt'].sum()
st.metric(label="Total Sharing Bike", value=f"{total_rentals:,}")

# Tren Peminjaman Harian (Menggunakan Data yang Difilter)
daily_rentals = day_df_filtered.groupby('dteday')['cnt'].sum().reset_index()
st.subheader("Daily Rental Trends")
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(daily_rentals['dteday'], daily_rentals['cnt'], marker='o', linestyle='-', color='#8C2981')
plt.xlabel("Date")
plt.ylabel("Number of Rentals")
plt.grid()
st.pyplot(fig)

# Pengaruh Kondisi Cuaca terhadap Peminjaman (Menggunakan Data yang Difilter)
st.subheader("The Effect of Weather Conditions on Rentals")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="weathersit", y="cnt", data=day_df_filtered, palette="magma", estimator=np.mean, ax=ax)
plt.xlabel("Weather Condition (1: Clear, 2: Cloudy, 3: Light Rain)")
plt.ylabel("Number of Rentals")
st.pyplot(fig)

# Perbedaan Pola Peminjaman: Hari Kerja vs Akhir Pekan (Menggunakan Data yang Difilter)
st.subheader("Rental Patterns: Weekdays vs Weekends")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=hour_df_filtered[hour_df_filtered["workingday"] == 1], x="hr", y="cnt", label="Hari Kerja", color="#FF4500", ax=ax)
sns.lineplot(data=hour_df_filtered[hour_df_filtered["workingday"] == 0], x="hr", y="cnt", label="Akhir Pekan", color="#FFA07A", ax=ax)
plt.xlabel("Hours of the day")
plt.ylabel("Number of Rentals")
plt.legend()
st.pyplot(fig)

# Waktu dengan Permintaan Tertinggi dan Terendah (Menggunakan Data yang Difilter)
st.subheader("Time with Highest and Lowest Rentals")
hourly_avg = hour_df_filtered.groupby("hr")["cnt"].mean()
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=hourly_avg.index, y=hourly_avg.values, palette="magma", ax=ax)
plt.xlabel("Hours of the day")
plt.ylabel("Average Rental Amount")
plt.xticks(range(24))
st.pyplot(fig)

# Clustering Waktu Peminjaman (Menggunakan Data yang Difilter)
def categorize_hour(hr):
    if 5 <= hr < 12:
        return "Morning"
    elif 12 <= hr < 17:
        return "Afternoon"
    elif 17 <= hr < 21:
        return "Evening"
    else:
        return "Night"

hour_df_filtered["time_category"] = hour_df_filtered["hr"].apply(categorize_hour)
cluster = hour_df_filtered.groupby("time_category")["cnt"].mean()
st.subheader("Number of rentals based on time span")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=cluster.index, y=cluster.values, palette="magma", ax=ax)
st.pyplot(fig)

with st.expander("📌 Explanation"):
    st.write("""
    This dashboard is designed to help understand **bike rental patterns** over a specific period. By analyzing rental data, we can identify key factors that influence the number of rentals and how usage patterns change over time. Some important aspects analyzed in this dashboard include:

    1. **Daily Rental Trends**  
       Bike rentals are not always stable every day. There are days when demand is higher (e.g., weekends or holidays) and other days when demand is lower.

    - **The effect of Weather Conditions**  
      Weather plays a significant role in bike rentals. On sunny days, people tend to rent bikes more frequently. Conversely, during rainy or stormy weather, the number of rentals typically decreases significantly.

    - **Weekday vs. Weekend Patterns**  
      Bike rental behavior differs between weekdays and weekends. On weekdays, demand is usually high during rush hours, such as in the morning and evening when people commute to and from work. On weekends, rental patterns are more flexible and may peak in the afternoon or evening.

    - **Hourly Rental Trends**  
      Identifying peak rental hours helps optimize bike availability and distribution. This information ensures that bikes are accessible when most needed and prevents shortages at specific times.

    - **Rental Grouping by Time of Day**  
      To gain deeper insights, rentals are categorized into different time segments: morning, afternoon, evening, and night. This helps in understanding demand patterns based on user habits throughout the day.

    🔍 **Conclusion:**  
    - The best time to rent a bike may vary depending on the season, weather conditions, and daily activity patterns.  
    - Users can adjust the filters in the dashboard to explore rental trends based on their specific needs.  
    """)

# Catatan Akhir
st.write("This dashboard presents an in-depth analysis of bicycle rental patterns based on time, weather, and daily habits.")
st.write("Copyright (c), created by Syifa Azzahra Susilo")