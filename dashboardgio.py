import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime

with st.sidebar:
    st.subheader('Apa kabar? Selamat datang di app analisa bike renting by Dhia Religio')
    st.subheader("Dalam app ini akan tertera beberapa kesimpulan dari analisis data bike renting")
    st.image ("bike.jpg")
##Visualization
"""
Dhia Religio Musyaffa
ML-67 
Bangkit Academy Cohort 2024
"""
st.image("bangkit.png",width=400)

# Set the background to a light gray color
plt.rcParams['figure.facecolor'] = 'lightgray'
plt.rcParams['axes.facecolor'] = 'lightgray'

# Set the text color to a darker shade for better contrast
plt.rcParams['text.color'] = 'black'
plt.rcParams['axes.labelcolor'] = 'black'
plt.rcParams['xtick.color'] = 'black'
plt.rcParams['ytick.color'] = 'black'

st.header('Analisis Bike Sharing:')

# Untuk mempermudah maka menyiapkan Halper Function

def create_casual_register_df(df):
    casual_year_df = df.groupby("yr")["casual"].sum().reset_index()
    casual_year_df.columns = ["yr", "total_casual"]
    reg_year_df = df.groupby("yr")["registered"].sum().reset_index()
    reg_year_df.columns = ["yr", "total_registered"]  
    casual_register_df = casual_year_df.merge(reg_year_df, on="yr")
    return casual_register_df

def create_monthly_df(df):
    monthly_df = df.groupby(by=["mnth","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return monthly_df

def create_hourly_df(df):
    hourly_df = df.groupby(by=["hr","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return hourly_df

def create_byholiday_df(df):
    holiday_df = df.groupby(by=["holiday","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return holiday_df

def create_byworkingday_df(df):
    workingday_df = df.groupby(by=["workingday","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return workingday_df

def create_byseason_df(df):
    season_df = df.groupby(by=["season","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return season_df

def create_byweather_df(df):
    weather_df = df.groupby(by=["weathersit","yr"]).agg({
        "cnt": "sum"
    }).reset_index() 
    return weather_df

# Membuat Load Cleaned Data

day_clean_df = pd.read_csv("main_data.csv")
hour_df = pd.read_csv("hour.csv")

# Membuat Load Filter Data

day_clean_df["dteday"] = pd.to_datetime(day_clean_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
min_date = day_clean_df["dteday"].min()
max_date = day_clean_df["dteday"].max()

with st.sidebar:
    

    # Opsi untuk mengganti rentang waktu
    start_date, end_date = st.date_input(
        label='Analysis Time:',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
main_df = day_clean_df[(day_clean_df["dteday"] >= str(start_date)) & 
                       (day_clean_df["dteday"] <= str(end_date))]

second_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                       (hour_df["dteday"] <= str(end_date))]



# Fungsi helper untuk mengganti nilai tahun
def replace_year_values(df):
    return df.replace({"yr": {0: 2010, 1: 2011}})

# Mengganti nilai tahun pada semua DataFrame
casual_register_df = replace_year_values(create_casual_register_df(main_df))
monthly_df = replace_year_values(create_monthly_df(main_df))
hourly_df = replace_year_values(create_hourly_df(second_df))
holiday_df = replace_year_values(create_byholiday_df(main_df))
workingday_df = replace_year_values(create_byworkingday_df(main_df))
season_df = replace_year_values(create_byseason_df(main_df))
weather_df = replace_year_values(create_byweather_df(main_df))

#Membuka trend waktu penyewaan sepeda dari perbandingan Jam, Hari dan Tahun?

total_kasual = sum(day_clean_df["casual"])
total_teregistrasi =sum(day_clean_df["registered"])
print("Jumlah Pengguna Kasual adalah: ", total_kasual)
print("Jummlah Pengguna Teregistrasi adalah: ", total_teregistrasi)



# Data
sizes = [total_kasual, total_teregistrasi]  # Ukuran segmen pie plot
labels = ["Pengguna Kasual", "Pengguna Teregistrasi"]  # label untuk segmen pie plot

# Plot
fig, ax = plt.subplots(figsize=(7, 7))
pie = ax.pie(sizes, labels=labels, autopct='%1.2f%%', startangle=90, pctdistance=0.85, shadow=True)

# Customizing colors
colors = ["#FF9999", "#66B2FF"]  # warna untuk setiap segmen
for i, wedge in enumerate(pie[0]):
    wedge.set_edgecolor('white')
    wedge.set_facecolor(colors[i])


plt.setp(pie[2], size=15, weight="bold", color="black")
plt.setp(pie[1], size=12)
plt.title("Perbandingan Tipe Pengguna", fontsize=20)


ax.axis('equal')
st.pyplot(fig)

with st.expander('**Bagaimana Kesimpulannya?**'):
   st.markdown(
    """
   Setelah dijalankan kode untuk menghitung jumlah pengguna teregistrasi dan jumlah pengguna kasual dapat dilihat secara
     jelas jumlah pengguna teregistrasi lebih besar
     dari jumlah pengguna kasual yaitu sebanyak 2672662 dan 620017. Dari kode ini sebenarnya sudah cukup menarik 
     kesimpulan bahwa pengguna teregistrasi lebih banyak dari kasual, namun untuk menampilkan visualisasi data lebih
       jelas dilakukan kode untuk membuat pie plot untuk melihat presentase kedua variabel. Dapat dilihat untuk pengguna 
       teregistrasi sebanyak 81,17% dan kasual sebanyak 18,83%.
    """
)


# Membuat Scatter Plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(day_clean_df['hum'], day_clean_df['casual'], color='blue', alpha=0.5)  
ax.set_title('Scatter Plot antara Kelembaman dan Jumlah Pengguna Kasual')
ax.set_xlabel('Kelembaman')
ax.set_ylabel('Jumlah Pengguna Kasual')
ax.grid(True)  

st.pyplot(fig)

with st.expander('**Bagaimana Kesimpulannya?**'):
   st.markdown(
    """
   diatas merupakan visualisasi perbandingan jumlah penyewaan sepeda dengan gantinya musim
    """
)

st.subheader("Perbandingan Musim dan Jumlah Sewa")


# hitung mean(rata-rata) 'cnt' pada setiap musim
mean_cnt_by_season = day_clean_df.groupby('season')['cnt'].mean()

# Membuat barplot
fig, ax = plt.subplots(figsize=(8, 6))
mean_cnt_by_season.plot(kind='bar', color='blue', ax=ax)
ax.set_title('Hubungan antara Musim dan Jumlah Sewa')
ax.set_xlabel('Musim/season')
ax.set_ylabel('Jumlah Sewa/cnt')
plt.grid(True)  
st.pyplot(fig)


st.subheader("Perbandingan Suhu dan Jumlah Sewa")
# membuat scatter plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(day_clean_df['temp'], day_clean_df['cnt'], color='blue', alpha=0.5)  
ax.set_title('Scatter Plot antara Suhu dan Jumlah Sewa')
ax.set_xlabel('Suhu')
ax.set_ylabel('Jumlah Sewa')
ax.grid(True)  

# Show plot using st.pyplot()
st.pyplot(fig)
