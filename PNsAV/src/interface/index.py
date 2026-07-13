import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from st_click_detector import click_detector
from pathlib import Path
import subprocess
import json
from datetime import datetime

st.set_page_config(initial_sidebar_state="collapsed")

st.set_page_config(
    page_title="PNsAV",
    page_icon="⚙️",
    layout="wide",
)

data = ""
styles = ""
with open("style.css", "r") as style_file:
    styles = style_file.read()

st.html(f"<style>{styles}</style>")

if "current_page" not in st.session_state:
    st.session_state.current_page = "Workspace"

nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([7, 1, 1, 1])
with nav_col1:
    st.html("""
    <div class="nav-bar" id="click">
        <div class="nav-logo">
            ⚙️ PNsAV Analyzer
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

col_stanga, col_dreapta = st.columns([1.5, 3.5], gap="medium")

with col_stanga:
    st.subheader("ÎNCĂRCARE TEXT")
    uploaded_file = st.file_uploader("Trage fișierul aici", type=["txt", "pdf", "docx"], label_visibility="collapsed")
    st.html("<div style='font-size:13px; font-weight:bold; color:#8b9eb7; margin-bottom:8px;'>SAU INTRODU TEXT</div>")
    
    # Input Text
    user_text = st.text_area("Input Text Principal", height=200, placeholder="Introdu textul aici...", label_visibility="collapsed")
    st.html(f"<div style='text-align:right; font-size:11px; color:#53647a; margin-top:-5px; margin-bottom:15px;'>{len(user_text)} / 10000</div>")
    
    if st.button("Analizează", type="primary", use_container_width=True):
        if uploaded_file is not None:
            st.session_state["analysed_text"] = uploaded_file.read().decode("utf-8")
        else:
            st.session_state["analysed_text"] = user_text
        st.session_state["analysed_triggered"] = True

        worker_path = Path(__file__).resolve().parent.parent / "core" / "main.py"

        if st.session_state["analysed_text"]:
            with st.spinner("Running background script..."):
                process = subprocess.run(
                    ["python", str(worker_path), st.session_state["analysed_text"]],
                    capture_output=True,
                    text=True,
                    check=True 
                )

                data = process.stdout.strip()

    st.html("""
        <div class="custom-card" style="margin-top: 20px;">
            <div class="card-header" style="border:none; margin:0; padding:0;">ℹ️ INFORMAȚII</div>
            <div style="font-size:13px; color:#acb2be; margin-top:10px; line-height:1.5;">
                Încarcă un fișier sau introdu text pentru a începe analiza în limbaj natural.
            </div>
        </div>
    """)

with col_dreapta:
    st.subheader("GRAF")
    g_col1, g_col2 = st.columns([3, 1])

    nodes, edges = [], []

    if data:
        data_packets = data.split("@")
        print(data_packets)

        # data_packets[0] = atoms
        # data_packets[1] = rules
        # data_packets[2] = arguments

        atoms = data_packets[0].split("-")
        id2text_atom = dict()
        for atom in atoms:
            atom = atom.split("|")
            if len(atom)>=3:
                id2text_atom[atom[0]] = atom[2]
        arguments = data_packets[2].split("-")
        attacks = data_packets[3].split("-")

        for arg in arguments:
            info = arg.split("|")

            if len(info)>=5:
                color = "#2865FF" if info[1] == "atomic" else "#FF5733"
                size = 20 if info[1] == "atomic" else 25

                label = f"Argument {info[0]}\nType {info[1]}\nText {id2text_atom[info[5]]}"
            
                nodes.append(
                    Node(
                        id=str(info[0]), 
                        label=str(info[4]),
                        title=label,
                        size=size, 
                        color=color
                    )
                )
        
        for attack in attacks:
            info = attack.split("|")
            print(info)
            if len(info)>1:
                edges.append(
                    Edge(
                        source=info[2],
                        target=info[1],
                        type="CURVE_SMOOTH"
                    )
                )

    config = Config(
        width="100%", 
        height=320,
        directed=True, 
        physics=True, 
        hierarchical=False,
        nodeHighlightBehavior=True,
        collapsible=False
    )
 
    selected_node = agraph(nodes=nodes, edges=edges, config=config)
# modificam sa fie legenda gen
    st.html("""
        <div style="display: flex; justify-content: space-between; background-color: #121620; padding: 12px; border-radius: 6px; border: 1px solid #1f293d; margin-top: -10px; margin-bottom: 20px;">
            <div style="display: flex; gap: 20px;">
                <div class="legend-item"><div class="legend-color" style="background-color: #f97316;"></div><span>Concept principal</span></div>
                <div class="legend-item"><div class="legend-color" style="background-color: #3b82f6;"></div><span>Tehnologii</span></div>
                <div class="legend-item"><div class="legend-color" style="background-color: #22c55e;"></div><span>Procese</span></div>
            </div>
            <div style="font-size: 11px; color: #53647a;">
                <b>Noduri:</b> 8 | <b>Muchii:</b> 10
            </div>
        </div>
    """)

    col_text, col_loguri = st.columns([1, 1], gap="medium")
    
    # Zona TEXT ANALIZAT (HTML formatat cu culorile corecte)
    with col_text:
        st.subheader("TEXT ANALIZAT")
        #cand integram backend ul inlocuim acest string cu rezultatul
        text_html = """
        <div class="text-container" style="border: 1px solid #1f293d; padding: 15px; border-radius: 5px; background-color: #121620;">
        <span class="highlight-orange">Inteligența Artificială (IA)</span> reprezintă un domeniu vast...
        <br><br>
        <span class="highlight-blue">Machine Learning</span> permite sistemelor să învețe...
    </div>
    """
        st.html(text_html)

    with col_loguri:
            st.subheader("LOGURI")
            ora_curenta=datetime.now().strftime("%H:%M:%S:")
            logs_html = f"""
            <div class="logs-container">
            <div class="log-row">
                <div class="log-dot dot-blue"></div>
                <div class="log-time">{ ora_curenta }:</div>
                <div class="log-text">Fișier încărcat: <span style="color:#3b82f6;">document.txt</span></div>
            </div>
            <div class="log-row">
                <div class="log-dot dot-blue"></div>
                <div class="log-time">{ora_curenta}</div>
                <div class="log-text">Preprocesare text în curs...</div>
            </div>
            <div class="log-row">
                <div class="log-dot dot-blue"></div>
                <div class="log-time">{ora_curenta}</div>
                <div class="log-text">Extracție entități realizată (28 entități găsite)</div>
            </div>
            <div class="log-row">
                <div class="log-dot dot-blue"></div>
                <div class="log-time">{ora_curenta}</div>
                <div class="log-text">Analiză relații în curs...</div>
            </div>
            <div class="log-row">
                <div class="log-dot dot-green"></div>
                <div class="log-time">{ora_curenta}</div>
                <div class="log-text" style="color:#22c55e;">Graf generat cu succes (9 noduri, 24 muchii)</div>
            </div>
            <div class="log-row">
                <div class="log-dot dot-green"></div>
                <div class="log-time">{ora_curenta}</div>
                <div class="log-text" style="color:#22c55e;">Analiză încheiată cu succes</div>
            </div>
        </div>
        """
            st.html(logs_html)

st.html("""
    <div style="text-align: center; color: #53647a; font-size: 12px; margin-top: 40px; padding: 15px 0; border-top: 1px solid #1f293d;">
        PNSAV Analyzer v1.0.0 &nbsp;&bull;&nbsp; Creat cu ❤️ pentru analiza în limbaj natural
    </div>
""")