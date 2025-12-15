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

st.set_page_config("Aplikasi Akuntansi Excel", layout="centered")
st.title("📘 Aplikasi Akuntansi Terhubung Excel")

# ================= SESSION =================
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

# ================= MENU =================
menu = st.sidebar.selectbox(
    "Menu",
    [
        "📂 Upload Excel",
        "✏️ Edit Data",
        "➕ Tambah Transaksi",
        "⬇️ Download Excel"
    ]
)

# ================= UPLOAD =================
if menu == "📂 Upload Excel":
    st.header("📂 Upload File Excel")

    file = st.file_uploader("Upload Excel (.xlsx)", type=["xlsx"])

    if file:
        try:
            df = pd.read_excel(file)  # kolom pertama otomatis jadi header
            st.session_state.df = df
            st.success("Excel berhasil dibaca")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Gagal membaca Excel: {e}")

# ================= EDIT =================
elif menu == "✏️ Edit Data":
    st.header("✏️ Edit Data Excel")

    if st.session_state.df.empty:
        st.warning("Belum ada data Excel")
    else:
        edited = st.data_editor(
            st.session_state.df,
            num_rows="dynamic",
            use_container_width=True
        )
        st.session_state.df = edited
        st.success("Perubahan tersimpan (sementara)")

# ================= TAMBAH =================
elif menu == "➕ Tambah Transaksi":
    st.header("➕ Tambah Transaksi Baru")

    if st.session_state.df.empty:
        st.warning("Upload Excel terlebih dahulu")
    else:
        data_baru = {}
        for col in st.session_state.df.columns:
            data_baru[col] = st.text_input(f"Isi {col}")

        if st.button("Tambah"):
            st.session_state.df = pd.concat(
                [st.session_state.df, pd.DataFrame([data_baru])],
                ignore_index=True
            )
            st.success("Transaksi ditambahkan")

# ================= DOWNLOAD =================
elif menu == "⬇️ Download Excel":
    st.header("⬇️ Download Excel")

    if st.session_state.df.empty:
        st.warning("Tidak ada data")
    else:
        buffer = io.BytesIO()
        st.session_state.df.to_excel(buffer, index=False)

        st.download_button(
            "Download Excel",
            buffer.getvalue(),
            "hasil_transaksi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
