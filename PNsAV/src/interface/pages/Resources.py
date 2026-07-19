import streamlit as st
from pathlib import Path
import base64

BASE_DIR = Path(__file__).resolve().parent
STYLE_PATH = BASE_DIR.resolve().parent / "style.css"
LOGO_PATH = BASE_DIR / "pnsav_logo.PNG"

def display_pdf(pdf_path: Path):
    if not pdf_path.exists():
        st.error(f"File not found: {pdf_path}")
        return

    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    
    pdf_display = f'''
    <iframe 
        src="data:application/pdf;base64,{base64_pdf}" 
        width="100%" 
        height="800px" 
        type="application/pdf">
    </iframe>
    '''
    
    st.markdown(pdf_display, unsafe_allow_html=True)

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
                <a href="http://pnsav-engine.streamlit.app" id="logo"><img src="data:image/png;base64,{encoded_logo}" alt="Logo" style="height: 80px; width: auto; object-fit: contain;"></a>
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

st.title("Resources")
st.markdown("❗The scientific paper on PNsAV is at the bottom of this page.")

md_text = ""
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent

with open(ROOT / "README.md","r",encoding="utf-8") as f:
    md_text = f.read()

st.markdown(md_text, unsafe_allow_html=True)
display_pdf(ROOT / "documentation" / "paper" / "PNsAV.pdf")