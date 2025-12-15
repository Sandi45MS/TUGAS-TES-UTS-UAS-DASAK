import streamlit as st
import pandas as pd
import io
from datetime import datetime

# ---------------- LOAD CSS ----------------
def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css()

st.set_page_config(page_title="Aplikasi Akuntansi Excel", layout="centered")

st.title("📘 Aplikasi Akuntansi Terintegrasi Excel")
st.write("Upload, edit, dan buat file Excel transaksi secara langsung.")

# ---------------- SESSION STATE ----------------
if "data_excel" not in st.session_state:
    st.session_state.data_excel = pd.DataFrame()

# ---------------- SIDEBAR MENU ----------------
menu = st.sidebar.selectbox(
    "Menu Utama",
    [
        "📂 Upload Excel",
        "✏️ Edit Data Excel",
        "➕ Input Manual",
        "⬇️ Download Excel"
    ]
)

# ---------------- UPLOAD EXCEL ----------------
if menu == "📂 Upload Excel":
    st.header("📂 Upload File Excel")

    file = st.file_uploader("Upload Excel (.xlsx)", type=["xlsx"])

    if file:
        try:
            df = pd.read_excel(file)
            if df.empty:
                st.warning("File Excel kosong.")
            else:
                st.session_state.data_excel = df
                st.success("Excel berhasil dibaca.")
                st.dataframe(df)

        except Exception as e:
            st.error("Gagal membaca file Excel.")
            st.code(str(e))

# ---------------- EDIT DATA ----------------
elif menu == "✏️ Edit Data Excel":
    st.header("✏️ Edit Data Excel")

    if st.session_state.data_excel.empty:
        st.warning("Belum ada data Excel.")
    else:
        edited_df = st.data_editor(
            st.session_state.data_excel,
            num_rows="dynamic",
            use_container_width=True
        )
        st.session_state.data_excel = edited_df
        st.success("Perubahan disimpan sementara.")

# ---------------- INPUT MANUAL ----------------
elif menu == "➕ Input Manual":
    st.header("➕ Tambah Transaksi Baru")

    if st.session_state.data_excel.empty:
        st.info("Belum ada tabel. Kolom akan dibuat otomatis.")

        nama_transaksi = st.text_input("Nama Transaksi (Kolom Pertama)")
        jumlah = st.number_input("Jumlah", step=1000.0)
        bulan = st.text_input("Bulan")

        if st.button("Buat Tabel & Simpan"):
            st.session_state.data_excel = pd.DataFrame([{
                "Transaksi": nama_transaksi,
                "Jumlah": jumlah,
                "Bulan": bulan
            }])
            st.success("Tabel baru dibuat.")

    else:
        columns = st.session_state.data_excel.columns.tolist()

        input_data = {}
        for col in columns:
            input_data[col] = st.text_input(f"{col}")

        if st.button("Tambah Baris"):
            st.session_state.data_excel = pd.concat(
                [
                    st.session_state.data_excel,
                    pd.DataFrame([input_data])
                ],
                ignore_index=True
            )
            st.success("Transaksi ditambahkan.")

# ---------------- DOWNLOAD EXCEL ----------------
elif menu == "⬇️ Download Excel":
    st.header("⬇️ Download File Excel")

    if st.session_state.data_excel.empty:
        st.warning("Tidak ada data untuk didownload.")
    else:
        buffer = io.BytesIO()
        st.session_state.data_excel.to_excel(
            buffer,
            index=False,
            engine="openpyxl"
        )

        st.download_button(
            "Download Excel",
            data=buffer.getvalue(),
            file_name=f"transaksi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
