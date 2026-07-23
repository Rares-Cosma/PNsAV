import streamlit as st
from pathlib import Path
import base64

BASE_DIR = Path(__file__).resolve().parent
STYLE_PATH = BASE_DIR.resolve().parent / "style.css"
LOGO_PATH = BASE_DIR / "pnsav_logo.PNG"

st.set_page_config(initial_sidebar_state="collapsed")

st.set_page_config(
    page_title="PNsAV About",
    page_icon="❓",
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

st.html("""
<div style="text-align:center; margin-top:60px;">

    <h1 style="
        font-size:60px;
        font-weight:700;
        color:white;
        margin-bottom:20px;
    ">
        About PNsAV
    </h1>
    <p style="
        font-size:22px;
        color:#d1d5db;
        max-width:900px;
        margin:auto;
        line-height:1.8;
    ">
        Probabilistic Neuro-symbolic Argumentation Validation model is a multi-layer neuro-symbolic reasoning system designed to perform validation of argument structures extracted from natural language.
         A constrained Large Language Model orchestration is employed as a semantic parser, identifying argumentative units, inferential relations, and domain concepts.
    </p>
    <br><br>

    <p style="
        font-size:22px;
        color:#d1d5db;
        max-width:900px;
        margin:auto;
        line-height:1.8;
    ">
        These structured arguments are processed by a set of formal validation layers, used 
        for checking the structural integrity as well as the presence of cycles and graph density. 
        We integrate a logic engine that takes into account each argument`s internal structure 
        through Spaans`s intrinsic strength, which is determined by numeric strengths assigned to
         premises and rules manually according to a specified rubric, and the global relationships 
        between arguments, to compute a converging final strength for every argument.
    </p>
    <div style="margin-top: 80px; max-width: 950px; margin-left: auto; margin-right: auto;">
        <h2 style="
            font-size: 38px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 35px;
            letter-spacing: 0.5px;
        ">
            The team behind the project
        </h2>
        <div style="
            display: flex;
            gap: 25px;
            justify-content: center;
            flex-wrap: wrap;
            text-align: left;
        ">
            <div style="
                flex: 1;
                min-width: 280px;
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                padding: 28px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            ">
                <h3 style="
                    font-size: 26px;
                    color: #ffffff;
                    margin-top: 0;
                    margin-bottom: 6px;
                    font-weight: 700;
                ">[Lăzărescu Larisa-Ioana]</h3>
                <span style="
                    display: inline-block;
                    font-size: 13px;
                    font-weight: 600;
                    letter-spacing: 1.2px;
                    color: #60a5fa;
                    text-transform: uppercase;
                    margin-bottom: 14px;
                ">Frontend & UI/UX Design</span>
                <p style="
                    font-size: 16px;
                    color: #9ca3af;
                    line-height: 1.6;
                    margin: 0;
                ">
                    S-a ocupat de proiectarea și dezvoltarea interfeței aplicației, creând un mediu intuitiv și modern pentru utilizatori.
                </p>
            </div>
            <div style="
                flex: 1;
                min-width: 280px;
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                padding: 28px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            ">
                <h3 style="
                    font-size: 26px;
                    color: #ffffff;
                    margin-top: 0;
                    margin-bottom: 6px;
                    font-weight: 700;
                ">[Cosma Rareș-Gabriel]</h3>
                <span style="
                    display: inline-block;
                    font-size: 13px;
                    font-weight: 600;
                    letter-spacing: 1.2px;
                    color: #60a5fa;
                    text-transform: uppercase;
                    margin-bottom: 14px;
                ">Backend & Core Logic</span>
                <p style="
                    font-size: 16px;
                    color: #9ca3af;
                    line-height: 1.6;
                    margin: 0;
                ">
                    A implementat modelele neuro-simbolice și algoritmii de validare a structurilor argumentative, asigurând procesarea riguroasă a datelor.
                </p>
            </div>
        </div>
    </div>
</div>
""")