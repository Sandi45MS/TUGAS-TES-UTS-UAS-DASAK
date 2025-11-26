import streamlit as st
from datetime import datetime
# Load CSS
def load_css():
    try:
        with open("style.css") as css:
            st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css()


st.set_page_config(page_title="Aplikasi Laporan Keuangan", layout="centered")

st.title("📘 Aplikasi Akuntansi Sederhana (Input - Output)")
st.write("Gunakan form berikut untuk memasukkan data akuntansi dasar.")

# Initialize session state
if "jurnal" not in st.session_state:
    st.session_state.jurnal = []
if "laba_rugi" not in st.session_state:
    st.session_state.laba_rugi = []
if "neraca" not in st.session_state:
    st.session_state.neraca = []
if "kredit" not in st.session_state:
    st.session_state.kredit = []

menu = st.sidebar.selectbox(
    "Pilih Menu",
    ["Jurnal Umum", "Laporan Laba Rugi", "Neraca", "Kredit / Hutang", "Lihat Semua Data"]
)

# ----------------------------- JURNAL UMUM --------------------------------
if menu == "Jurnal Umum":
    st.header("📒 Input Jurnal Umum")

    tanggal = st.date_input("Tanggal Transaksi", datetime.now())
    keterangan = st.text_input("Keterangan Transaksi")
    debit = st.number_input("Debit", min_value=0.0, step=1000.0)
    kredit = st.number_input("Kredit", min_value=0.0, step=1000.0)

    if st.button("Simpan Jurnal"):
        st.session_state.jurnal.append({
            "tanggal": str(tanggal),
            "keterangan": keterangan,
            "debit": debit,
            "kredit": kredit
        })
        st.success("Jurnal berhasil disimpan!")

    if st.session_state.jurnal:
        st.subheader("Data Jurnal Tersimpan")
        st.table(st.session_state.jurnal)

# ----------------------------- LABA RUGI --------------------------------
elif menu == "Laporan Laba Rugi":
    st.header("📗 Input Laporan Laba Rugi")

    tanggal = st.date_input("Tanggal Pencatatan", datetime.now())
    pendapatan = st.number_input("Pendapatan", min_value=0.0, step=1000.0)
    beban = st.number_input("Beban", min_value=0.0, step=1000.0)

    if st.button("Hitung dan Simpan Laba Rugi"):
        laba = pendapatan - beban
        st.session_state.laba_rugi.append({
            "tanggal": str(tanggal),
            "pendapatan": pendapatan,
            "beban": beban,
            "laba": laba
        })

        st.success(f"Laba bersih: {laba}")

    if st.session_state.laba_rugi:
        st.subheader("Data Laba Rugi")
        st.table(st.session_state.laba_rugi)

# ----------------------------- NERACA --------------------------------
elif menu == "Neraca":
    st.header("📘 Input Neraca Keuangan")

    tanggal = st.date_input("Tanggal Pencatatan", datetime.now())
    aset = st.number_input("Total Aset", min_value=0.0, step=1000.0)
    kewajiban = st.number_input("Total Kewajiban", min_value=0.0, step=1000.0)
    ekuitas = st.number_input("Total Ekuitas", min_value=0.0, step=1000.0)

    if st.button("Simpan Neraca"):
        st.session_state.neraca.append({
            "tanggal": str(tanggal),
            "aset": aset,
            "kewajiban": kewajiban,
            "ekuitas": ekuitas
        })
        st.success("Neraca berhasil disimpan!")

    if st.session_state.neraca:
        st.subheader("Data Neraca")
        st.table(st.session_state.neraca)

# ----------------------------- KREDIT / HUTANG --------------------------------
elif menu == "Kredit / Hutang":
    st.header("📙 Input Kredit / Hutang")

    tanggal = st.date_input("Tanggal Kredit", datetime.now())
    pemberi = st.text_input("Nama Pihak Pemberi Kredit")
    jumlah = st.number_input("Jumlah Kredit", min_value=0.0, step=1000.0)
    jatuh_tempo = st.date_input("Jatuh Tempo")

    if st.button("Simpan Kredit"):
        st.session_state.kredit.append({
            "tanggal": str(tanggal),
            "pemberi": pemberi,
            "jumlah": jumlah,
            "jatuh_tempo": str(jatuh_tempo)
        })
        st.success("Data kredit berhasil disimpan!")

    if st.session_state.kredit:
        st.subheader("Data Kredit")
        st.table(st.session_state.kredit)

# ----------------------------- SEMUA DATA --------------------------------
elif menu == "Lihat Semua Data":
    st.header("📚 Semua Data Akuntansi")

    st.subheader("📒 Jurnal Umum")
    st.table(st.session_state.jurnal)

    st.subheader("📗 Laba Rugi")
    st.table(st.session_state.laba_rugi)

    st.subheader("📘 Neraca")
    st.table(st.session_state.neraca)

    st.subheader("📙 Kredit / Hutang")
    st.table(st.session_state.kredit)

