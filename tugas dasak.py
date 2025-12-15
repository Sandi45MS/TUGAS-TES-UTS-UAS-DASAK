import streamlit as st
import pandas as pd
import io
from datetime import datetime

# ================= CSS LOADER =================
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

st.title("📊 Aplikasi Akuntansi Berbasis Excel")
st.caption("Input • Edit • Download | Streamlit + GitHub")

# ================= SESSION STATE =================
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["BULAN", "TRANSAKSI", "KAS", "PIUTANG", "UTANG", "MODAL"]
    )

# ================= SIDEBAR MENU =================
menu = st.sidebar.selectbox(
    "Menu",
    [
        "📂 Buka File Excel",
        "➕ Tambah Transaksi",
        "✏️ Edit Data Excel",
        "⬇️ Download Excel"
    ]
)

# ================= MENU 1 : UPLOAD EXCEL =================
if menu == "📂 Buka File Excel":
    st.header("📂 Upload File Excel")

    file = st.file_uploader(
        "Upload file Excel dengan format:",
        type=["xlsx"]
    )

    st.info("Header wajib: BULAN, TRANSAKSI, KAS, PIUTANG, UTANG, MODAL")

    if file:
        try:
            df = pd.read_excel(file)
            df.columns = df.columns.str.upper()
            st.session_state.data = df
            st.success("Excel berhasil dibaca")
            st.dataframe(df)
        except:
            st.error("Format Excel tidak sesuai")

# ================= MENU 2 : TAMBAH TRANSAKSI =================
elif menu == "➕ Tambah Transaksi":
    st.header("➕ Tambah Transaksi Baru")

    with st.form("form_transaksi"):
        bulan = st.number_input("Bulan", min_value=1, max_value=12, step=1)
        transaksi = st.text_input("Nama Transaksi")

        kas = st.number_input("Kas", step=1000.0)
        piutang = st.number_input("Piutang", step=1000.0)
        utang = st.number_input("Utang", step=1000.0)
        modal = st.number_input("Modal", step=1000.0)

        submit = st.form_submit_button("Simpan Transaksi")

    if submit:
        new_row = {
            "BULAN": bulan,
            "TRANSAKSI": transaksi,
            "KAS": kas,
            "PIUTANG": piutang,
            "UTANG": utang,
            "MODAL": modal
        }

        st.session_state.data = pd.concat(
            [st.session_state.data, pd.DataFrame([new_row])],
            ignore_index=True
        )

        st.success("Transaksi berhasil ditambahkan")
        st.dataframe(st.session_state.data)

# ================= MENU 3 : EDIT DATA =================
elif menu == "✏️ Edit Data Excel":
    st.header("✏️ Edit Data Excel")

    if st.session_state.data.empty:
        st.warning("Data masih kosong")
    else:
        edited_df = st.data_editor(
            st.session_state.data,
            num_rows="dynamic",
            use_container_width=True
        )
        st.session_state.data = edited_df
        st.success("Perubahan disimpan (sementara)")

# ================= MENU 4 : DOWNLOAD =================
elif menu == "⬇️ Download Excel":
    st.header("⬇️ Download Excel")

    if st.session_state.data.empty:
        st.warning("Tidak ada data untuk di-download")
    else:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            st.session_state.data.to_excel(
                writer,
                index=False,
                sheet_name="DATA_AKUNTANSI"
            )

        st.download_button(
            label="Download Excel",
            data=buffer.getvalue(),
            file_name="laporan_akuntansi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
