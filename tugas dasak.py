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
st.title("📘 Aplikasi Akuntansi Berbasis Excel")

# ================= SESSION STATE =================
if "df_excel" not in st.session_state:
    st.session_state.df_excel = None

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

# ================= UPLOAD EXCEL =================
if menu == "📂 Upload Excel":
    st.header("📂 Upload File Excel")

    file = st.file_uploader("Upload Excel (.xlsx)", type=["xlsx"])

    if file:
        try:
            # ⚠️ HEADER = NONE (INI KUNCI UTAMA)
            df = pd.read_excel(file, header=None)

            st.session_state.df_excel = df
            st.success("Excel berhasil dibaca (struktur aman)")

            st.dataframe(df)

        except Exception as e:
            st.error(f"Gagal membaca Excel: {e}")

# ================= EDIT DATA =================
elif menu == "✏️ Edit Data":
    st.header("✏️ Edit Isi Excel")

    if st.session_state.df_excel is None:
        st.warning("Upload Excel terlebih dahulu")
    else:
        edited = st.data_editor(
            st.session_state.df_excel,
            num_rows="dynamic",
            use_container_width=True
        )

        st.session_state.df_excel = edited
        st.success("Perubahan tersimpan sementara")

# ================= TAMBAH TRANSAKSI =================
elif menu == "➕ Tambah Transaksi":
    st.header("➕ Tambah Baris Transaksi")

    if st.session_state.df_excel is None:
        st.warning("Upload Excel terlebih dahulu")
    else:
        jumlah_kolom = st.session_state.df_excel.shape[1]

        st.write("Isi sesuai urutan kolom Excel (A, B, C, dst)")

        new_row = []
        for i in range(jumlah_kolom):
            val = st.text_input(f"Kolom {i+1}", key=f"col_{i}")
            new_row.append(val)

        if st.button("Tambah"):
            st.session_state.df_excel.loc[len(st.session_state.df_excel)] = new_row
            st.success("Transaksi ditambahkan")

# ================= DOWNLOAD =================
elif menu == "⬇️ Download Excel":
    st.header("⬇️ Download Excel")

    if st.session_state.df_excel is None:
        st.warning("Tidak ada data")
    else:
        buffer = io.BytesIO()

        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            # ⚠️ index=False, header=False (INI KUNCI KEDUA)
            st.session_state.df_excel.to_excel(
                writer,
                index=False,
                header=False
            )

        st.download_button(
            "Download Excel",
            buffer.getvalue(),
            "hasil_akuntansi.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
