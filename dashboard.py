import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

#menyiapkan monthly_rent_bike_11_df
def create_monthly_rent_bike_11_df(df):
    year_11_df = df[df['yr'] == 0]
    
    monthly_rent_bike_11_df = year_11_df.groupby(by='mnth').agg({
    "cnt": "sum"
    }).reset_index()

    monthly_rent_bike_11_df['mnth'] = pd.Categorical(monthly_rent_bike_11_df['mnth'], ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']) 

    monthly_rent_bike_11_df = monthly_rent_bike_11_df.sort_values(by="mnth").reset_index(drop=True)

    monthly_rent_bike_11_df.rename(columns={
        "cnt": "total_rent",
        "mnth": "month"
    }, inplace=True)

    return monthly_rent_bike_11_df

#menyiapkan monthly_rent_bike_12_df
def create_monthly_rent_bike_12_df(df):
    year_12_df = df[df['yr'] == 1]
    
    monthly_rent_bike_12_df = year_12_df.groupby(by='mnth').agg({
    "cnt": "sum"
    }).reset_index()

    monthly_rent_bike_12_df['mnth'] = pd.Categorical(monthly_rent_bike_12_df['mnth'], ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']) 

    monthly_rent_bike_12_df = monthly_rent_bike_12_df.sort_values(by="mnth").reset_index(drop=True)

    monthly_rent_bike_12_df.rename(columns={
        "cnt": "total_rent",
        "mnth": "month"
    }, inplace=True)

    return monthly_rent_bike_12_df

#menyiapkan avg_weekly_rent_bike_df
def create_avg_weekly_rent_bike_df(df):
    avg_weekly_rent_bike_df = df.groupby(by="weekday").agg({
        "cnt": "mean"
    }).reset_index()

    avg_weekly_rent_bike_df.rename(columns={
        "cnt": "average_rent"
    }, inplace=True)

    avg_weekly_rent_bike_df['weekday'] = pd.Categorical(avg_weekly_rent_bike_df['weekday'], ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])

    avg_weekly_rent_bike_df = avg_weekly_rent_bike_df.sort_values(by='weekday').reset_index(drop=True)

    return avg_weekly_rent_bike_df

#membaca main_data.csv
main_df = pd.read_csv("main_data.csv")

#menghasilkan berbagai DataFrame yang dibutuhkan untuk membuat visualisasi data.
monthly_rent_bike_11_df = create_monthly_rent_bike_11_df(main_df)
monthly_rent_bike_12_df = create_monthly_rent_bike_12_df(main_df)
avg_weekly_rent_bike_df = create_avg_weekly_rent_bike_df(main_df)

#visualisasi data
st.title("Bike Sharing Dashboard :bike:")
st.subheader("Kelas Analisa Data dengan Python - Dicoding Indonesia")
st.text("Oleh: I Made Putra Utama")

st.markdown("---")

#membuat metriks untuk total rental oleh casual user, registered user, dan total rental secara keseluruhan
st.subheader("Metriks Total Penyewaan Berdasarkan Jenis Pengguna")

col1, col2, col3 = st.columns(3)

def formatted_ribu(total):
    formatted = f"{total // 1000} rb"

    return formatted

def formatted_juta(total):
    formatted = f"{total / 1_000_000:.2f} jt"

    return formatted

with col1:
    total_casual_user = main_df.casual.sum()
    if(total_casual_user >= 1000000):
        value_casual = formatted_juta(total_casual_user)
    else:
        value_casual = formatted_ribu(total_casual_user)

    st.metric("Pengguna Biasa", value=value_casual)
    
with col2:
    total_registered_user = main_df.registered.sum()
    if(total_registered_user >= 1000000):
        value_registered = formatted_juta(total_registered_user)
    else:
        value_registered = formatted_ribu(total_registered_user)

    st.metric("Pengguna Terdaftar", value=value_registered)

with col3:
    total_all_user = main_df.cnt.sum()
    if(total_all_user >= 1000000):
        value_all = formatted_juta(total_all_user)
    else:
        value_all = formatted_ribu(total_all_user)

    st.metric("Total Keseluruhan", value=value_all)

st.markdown("---")

#visualisasi tren penyewaan sepeda tahun 2011 dan 2012
st.subheader("Tren Penyewaan Sepeda Bulanan")

plt.style.use('dark_background')

fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(
    monthly_rent_bike_11_df["month"],
    monthly_rent_bike_11_df["total_rent"],
    marker='o', 
    linewidth=2,
    color="limegreen",
    label='2011'
)
ax.plot(
    monthly_rent_bike_12_df["month"],
    monthly_rent_bike_12_df["total_rent"],
    marker='o', 
    linewidth=2,
    color="dodgerblue",
    label='2012'
)
ax.tick_params(axis='y', labelsize=18)
ax.tick_params(axis='x', labelsize=18, rotation=45)
ax.legend(fontsize=18)

st.pyplot(fig)

#penjelasan visualisasi
with st.expander("Lihat pembahasan visualisasi"):
    st.write(
        """Tren penyewaan sepeda pada tahun 2011 dan 2012 memiliki pola yang hampir sama, yaitu mengalami tren peningkatan pada bulan Februari - Juni dan penurunan pada bulan Oktober - Desember. Namun pada tahun 2012 jumlah penyewaan sepeda per bulannya lebih banyak dibanding pada tahun 2011
        """
    )

st.markdown("---")

#visualisasi rata-rata sewa sepeda per hari
st.subheader("Rata-rata Sewa Sepeda per Hari")
    
colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#32CD32", "#D3D3D3"]

fig, ax = plt.subplots(figsize=(20, 10))
 
ax = sns.barplot(
        data=avg_weekly_rent_bike_df.sort_values(by='weekday'),
        x='weekday',
        y='average_rent',
        hue='weekday',
        palette=colors,
        dodge=False,
        legend=False,
        ax=ax
)

for index, value in enumerate(avg_weekly_rent_bike_df.sort_values(by='weekday')['average_rent']):
    plt.text(index, value + 0.5, f"{value:.0f}", color='white', ha='center', fontsize=18, va='bottom')

ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=18)
ax.tick_params(axis='y', labelsize=18)

st.pyplot(fig)

with st.expander("Lihat pembahasan visualisasi"):
    st.write(
        """Dalam rentang satu minggu, perbedaan rata-rata jumlah penyewaan sepeda antar harinya tidak menunjukkan perbedaan yang signifikan. Terlihat bahwa hari Jumat memiliki rata-rata jumlah penyewaan sepeda tertinggi dibandingkan dengan hari-hari lainnya, dengan angka rata-rata sekitar 4690
        """
    )

st.markdown('---')

st.caption('Copyright Putra Utama 2023')