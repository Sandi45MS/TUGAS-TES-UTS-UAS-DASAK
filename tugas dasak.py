import streamlit as st
import pandas as pd
import io
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Aplikasi Akuntansi Terintegrasi",
    layout="centered"
)

# ---------------- LOAD CSS ----------------
def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css()

# ---------------- INIT STATE ----------------
def init_df(cols):
    return pd.DataFrame(columns=cols)

if "data" not in st.session_state:
    st.session_state.data = {
        "jurnal": init_df(["tanggal", "keterangan", "debit", "kredit"]),
        "laba_rugi": init_df(["tanggal", "pendapatan", "beban", "laba"]),
        "neraca": init_df(["tanggal", "aset", "kewajiban", "ekuitas"]),
        "kredit": init_df(["tanggal", "pemberi", "jumlah", "jatuh_tempo"])
    }

# ---------------- TITLE ----------------
st.title("📘 Aplikasi Akuntansi Terintegrasi")
st.write("Input • Edit • Import • Export Excel")

# ---------------- SIDEBAR ----------------
menu = st.sidebar.selectbox(
    "Menu Utama",
    [
        "📒 Jurnal Umum",
        "📗 Laba Rugi",
        "📘 Neraca",
        "📙 Kredit / Hutang",
        "📂 Import Excel",
        "✏️ Edit Data",
        "⬇️ Export Excel"
    ]
)

# ---------------- JURNAL ----------------
if menu == "📒 Jurnal Umum":
    st.subheader("Input Jurnal Umum")

    tgl = st.date_input("Tanggal", datetime.now())
    ket = st.text_input("Keterangan")
    d = st.number_input("Debit", 0.0)
    k = st.number_input("Kredit", 0.0)

    if st.button("Simpan"):
        st.session_state.data["jurnal"].loc[len(st.session_state.data["jurnal"])] = [
            str(tgl), ket, d, k
        ]

    st.dataframe(st.session_state.data["jurnal"])

# ---------------- LABA RUGI ----------------
elif menu == "📗 Laba Rugi":
    st.subheader("Laporan Laba Rugi")

    tgl = st.date_input("Tanggal", datetime.now())
    p = st.number_input("Pendapatan", 0.0)
    b = st.number_input("Beban", 0.0)

    if st.button("Hitung & Simpan"):
        st.session_state.data["laba_rugi"].loc[
            len(st.session_state.data["laba_rugi"])
        ] = [str(tgl), p, b, p - b]

    st.dataframe(st.session_state.data["laba_rugi"])

# ---------------- NERACA ----------------
elif menu == "📘 Neraca":
    st.subheader("Neraca")

    tgl = st.date_input("Tanggal", datetime.now())
    a = st.number_input("Aset", 0.0)
    kw = st.number_input("Kewajiban", 0.0)
    e = st.number_input("Ekuitas", 0.0)

    if st.button("Simpan"):
        st.session_state.data["neraca"].loc[
            len(st.session_state.data["neraca"])
        ] = [str(tgl), a, kw, e]

    st.dataframe(st.session_state.data["neraca"])

# ---------------- KREDIT ----------------
elif menu == "📙 Kredit / Hutang":
    st.subheader("Kredit / Hutang")

    tgl = st.date_input("Tanggal", datetime.now())
    p = st.text_input("Pemberi Kredit")
    j = st.number_input("Jumlah", 0.0)
    jt = st.date_input("Jatuh Tempo")

    if st.button("Simpan"):
        st.session_state.data["kredit"].loc[
            len(st.session_state.data["kredit"])
        ] = [str(tgl), p, j, str(jt)]

    st.dataframe(st.session_state.data["kredit"])

# ---------------- IMPORT EXCEL ----------------
elif menu == "📂 Import Excel":
    st.subheader("Import File Excel")

    file = st.file_uploader("Upload Excel", type=["xlsx"])

    if file:
        try:
            st.session_state.data["jurnal"] = pd.read_excel(file, "Jurnal")
            st.session_state.data["laba_rugi"] = pd.read_excel(file, "LabaRugi")
            st.session_state.data["neraca"] = pd.read_excel(file, "Neraca")
            st.session_state.data["kredit"] = pd.read_excel(file, "Kredit")
            st.success("Excel berhasil dimuat")
        except:
            st.error("Format sheet tidak sesuai")

# ---------------- EDIT DATA ----------------
elif menu == "✏️ Edit Data":
    sheet = st.selectbox(
        "Pilih Data",
        ["jurnal", "laba_rugi", "neraca", "kredit"]
    )

    st.session_state.data[sheet] = st.data_editor(
        st.session_state.data[sheet],
        num_rows="dynamic"
    )

# ---------------- EXPORT EXCEL ----------------
elif menu == "⬇️ Export Excel":
    st.subheader("Download Excel")

    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        st.session_state.data["jurnal"].to_excel(writer, "Jurnal", index=False)
        st.session_state.data["laba_rugi"].to_excel(writer, "LabaRugi", index=False)
        st.session_state.data["neraca"].to_excel(writer, "Neraca", index=False)
        st.session_state.data["kredit"].to_excel(writer, "Kredit", index=False)

    st.download_button(
        "Download File Excel",
        buffer.getvalue(),
        "laporan_akuntansi.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
