import streamlit as st
from pathlib import Path
import base64

BASE_DIR = Path(__file__).resolve().parent
STYLE_PATH = BASE_DIR.resolve().parent / "style.css"
LOGO_PATH = BASE_DIR / "pnsav_logo.PNG"

st.set_page_config(initial_sidebar_state="collapsed")

st.set_page_config(
    page_title="PNsAV Resources",
    page_icon="🗂️",
    layout="wide",
)

styles = ""
with open(STYLE_PATH, "r") as style_file:
    styles = style_file.read()

st.html(f"<style>{styles}</style>")

nav_container = st.container(key="navbar")
with nav_container:
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([7, 1, 1, 1])

    st.html("""
        <style>
        .st-key-navbar div[data-testid="stHorizontalBlock"] {
            align-items: center !important;
        }
        .st-key-navbar div[data-testid="stColumn"] {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        .st-key-navbar div[data-testid="stColumn"]:not(:first-child) {
            margin-top: -10px !important;
        }
        </style>
    """)

    with open(LOGO_PATH, "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()

    with nav_col1:
        st.html(f"""
        <div class="nav-bar">
            <div class="nav-logo">
                <a href="http://localhost:8501" id="logo"><img src="data:image/png;base64,{encoded_logo}" alt="Logo" style="height: 80px; width: auto; object-fit: contain;"></a>
            </div>
        </div>
    """)

    with nav_col2:
        if st.button("Resources", use_container_width=True):
            st.switch_page("pages/Resources.py")
    with nav_col3:
        if st.button("About", use_container_width=True):
            st.switch_page("pages/About.py")
    with nav_col4:
        if st.button("Contact", use_container_width=True):
            st.switch_page("pages/Contact.py")
st.html("<div style='margin-bottom: 0px;'></div>")

st.title("Resurse suplimentare")
st.markdown("Documente suplimentare referitoare la framework-ul ASPIC+.")