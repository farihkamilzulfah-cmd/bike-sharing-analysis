import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='darkgrid')

def create_daily_rent_df(df):
    daily_rent_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum"
    }).reset_index()
    return daily_rent_df

def create_seasonal_rent_df(df):
    # Mengelompokkan berdasarkan musim
    seasonal_rent_df = df.groupby('season')['cnt'].mean().reset_index()
    return seasonal_rent_df

def create_hourly_rent_df(df):
    # Mengelompokkan berdasarkan jam dan tipe hari (kerja/libur)
    hourly_rent_df = df.groupby(['workingday', 'hr'])['cnt'].mean().reset_index()
    return hourly_rent_df


all_df = pd.read_csv("Dashboard/main_data.csv")
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan input tanggal
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

# Menjalankan fungsi helper
daily_rent_df = create_daily_rent_df(main_df)
seasonal_rent_df = create_seasonal_rent_df(main_df)
hourly_rent_df = create_hourly_rent_df(main_df)


st.header('Bike Sharing Dashboard')

st.subheader('Daily Rentals Overview')
col1, col2, col3 = st.columns(3)

with col1:
    total_rent = main_df.cnt.sum()
    st.metric("Total Penyewaan", value=f"{total_rent:,}")

with col2:
    total_casual = main_df.casual.sum()
    st.metric("Penyewa Casual", value=f"{total_casual:,}")

with col3:
    total_registered = main_df.registered.sum()
    st.metric("Penyewa Terdaftar", value=f"{total_registered:,}")

st.subheader("Performa Penyewaan Berdasarkan Musim")

fig, ax = plt.subplots(figsize=(10, 6))

colors = sns.color_palette("viridis", len(seasonal_rent_df))

sns.barplot(
    x="season", 
    y="cnt", 
    data=seasonal_rent_df.sort_values(by="cnt", ascending=False),
    hue="season",
    palette=colors,
    ax=ax,
    legend=False
)

ax.set_title("Rata-rata Penyewaan per Musim", fontsize=15)
ax.set_xlabel(None)
ax.set_ylabel("Rata-rata Jumlah Penyewaan")
st.pyplot(fig)

with st.expander("Lihat Insight Musim"):
    st.write(
        """Grafik ini menunjukkan musim mana yang paling diminati pengguna. 
        Biasanya, musim **Fall** atau **Summer** mendominasi karena cuaca yang mendukung."""
    )

st.subheader("Pola Penyewaan per Jam: Hari Kerja vs Hari Libur")

fig, ax = plt.subplots(figsize=(12, 6))

sns.lineplot(
    data=hourly_rent_df, 
    x="hr", 
    y="cnt", 
    hue="workingday", 
    marker="o", 
    palette={0: "#D3D3D3", 1: "#72BCD4"},
    ax=ax
)

ax.set_title("Perbandingan Pola Jam: Hari Kerja (1) vs Hari Libur (0)", fontsize=15)
ax.set_xlabel("Jam (0-23)")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_xticks(range(0, 24))
ax.grid(True, linestyle='--', alpha=0.5)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, ['Hari Libur/Weekend', 'Hari Kerja'], title="Tipe Hari")

st.pyplot(fig)

with st.expander("Lihat Insight Pola Jam"):
    st.write(
        """Pada hari kerja, lonjakan terjadi pada jam berangkat dan pulang kantor (08:00 & 17:00). 
        Sedangkan pada hari libur, penyewaan lebih merata dan memuncak di siang hari."""
    )

st.caption('Copyright (c) Farih Kamil Zulfah 2026')