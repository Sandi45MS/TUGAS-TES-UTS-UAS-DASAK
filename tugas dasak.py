import streamlit as st
import pandas as pd
import io

# ================= CSS =================
def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css()

st.set_page_config(
    page_title="Aplikasi Akuntansi Excel",
    layout="centered"
)

st.title("📘 Aplikasi Akuntansi Terintegrasi Excel")
st.caption("Upload • Edit • Tambah Transaksi • Download Excel")

# ================= SESSION STATE =================
if "df_excel" not in st.session_state:
    st.session_state.df_excel = None

# ================= MENU =================
menu = st.sidebar.selectbox(
    "Menu",
    [
        "📂 Upload Excel",
        "✏️ Edit & Tambah Transaksi",
        "⬇️ Download Excel"
    ]
)

# ================= UPLOAD EXCEL =================
if menu == "📂 Upload Excel":
    st.header("📂 Upload File Excel")

    file = st.file_uploader(
        "Upload file Excel (.xlsx)",
        type=["xlsx"]
    )

    if file:
        try:
            # PENTING: header=0 → baris pertama jadi header
            df = pd.read_excel(file, header=0)

            st.session_state.df_excel = df
            st.success("Excel berhasil dibaca")

            st.subheader("Preview Data")
            st.dataframe(df)

        except Exception as e:
            st.error("Gagal membaca file Excel")
            st.code(str(e))

# ================= EDIT DATA =================
elif menu == "✏️ Edit & Tambah Transaksi":
    st.header("✏️ Edit & Tambah Transaksi")

    if st.session_state.df_excel is None:
        st.warning("Silakan upload file Excel terlebih dahulu")
    else:
        st.info("Kolom akan tetap seperti Excel asli (A, B, C, dst tidak berubah)")

        # INI KUNCI UTAMA AGAR KOLOM TIDAK RUSAK
        edited_df = st.data_editor(
            st.session_state.df_excel,
            num_rows="dynamic",
            use_container_width=True
        )

        # Simpan kembali TANPA mengubah kolom
        st.session_state.df_excel = edited_df

        st.success("Perubahan disimpan sementara")

# ================= DOWNLOAD =================
elif menu == "⬇️ Download Excel":
    st.header("⬇️ Download Excel")

    if st.session_state.df_excel is None:
        st.warning("Belum ada data Excel")
    else:
        buffer = io.BytesIO()

        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            st.session_state.df_excel.to_excel(
                writer,
                index=False,
                sheet_name="Sheet1"  # Nama sheet default
            )

        st.download_button(
            label="Download Excel",
            data=buffer.getvalue(),
            file_name="laporan_transaksi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
