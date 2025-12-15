import streamlit as st
import pandas as pd
import io

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="Aplikasi Akuntansi Excel",
    layout="wide"
)

# ------------------ LOAD CSS ------------------
def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css()

st.title("📘 Aplikasi Akuntansi Berbasis Excel")
st.caption("Upload • Edit • Tambah Data • Download Excel")

# ------------------ SESSION STATE ------------------
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

# ------------------ SIDEBAR MENU ------------------
menu = st.sidebar.radio(
    "Menu",
    [
        "📂 Upload Excel",
        "📋 Lihat & Edit Tabel",
        "➕ Tambah Transaksi",
        "⬇️ Download Excel"
    ]
)

# ==================================================
# 📂 UPLOAD EXCEL
# ==================================================
if menu == "📂 Upload Excel":
    st.header("📂 Upload File Excel")

    file = st.file_uploader(
        "Upload file Excel (.xlsx)",
        type=["xlsx"]
    )

    if file:
        try:
            df = pd.read_excel(file)
            st.session_state.df = df
            st.success("File Excel berhasil dimuat")
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error("Gagal membaca file Excel")

# ==================================================
# 📋 LIHAT & EDIT TABEL
# ==================================================
elif menu == "📋 Lihat & Edit Tabel":
    st.header("📋 Edit Data Excel")

    if st.session_state.df.empty:
        st.warning("Belum ada data Excel")
    else:
        edited_df = st.data_editor(
            st.session_state.df,
            num_rows="dynamic",
            use_container_width=True
        )
        st.session_state.df = edited_df
        st.success("Perubahan tersimpan (sementara)")

# ==================================================
# ➕ TAMBAH TRANSAKSI (DINAMIS)
# ==================================================
elif menu == "➕ Tambah Transaksi":
    st.header("➕ Tambah Baris Data")

    if st.session_state.df.empty:
        st.warning("Upload Excel terlebih dahulu")
    else:
        new_row = {}

        st.subheader("Isi Data Transaksi")
        for col in st.session_state.df.columns:
            new_row[col] = st.text_input(f"{col}")

        if st.button("Tambah ke Tabel"):
            st.session_state.df = pd.concat(
                [st.session_state.df, pd.DataFrame([new_row])],
                ignore_index=True
            )
            st.success("Data berhasil ditambahkan")

# ==================================================
# ⬇️ DOWNLOAD EXCEL
# ==================================================
elif menu == "⬇️ Download Excel":
    st.header("⬇️ Download File Excel")

    if st.session_state.df.empty:
        st.warning("Tidak ada data untuk di-download")
    else:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            st.session_state.df.to_excel(writer, index=False)

        st.download_button(
            label="Download Excel",
            data=buffer.getvalue(),
            file_name="hasil_akuntansi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
