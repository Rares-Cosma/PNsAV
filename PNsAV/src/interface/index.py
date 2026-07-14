import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from st_click_detector import click_detector
from pathlib import Path
import subprocess
import json
import ast
import base64
from datetime import datetime

#TODO:
# 2) text analizat (partial)
# 4) larisa: ui/ux paper, about, contact
# 5) finish paper
# 6) resources
# 7) comentarii cod
# 8) documentatia

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
st.session_state["analysed_triggered"] = False

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
    </style>
    """)

    with open("pnsav_logo.PNG", "rb") as image_file:
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

col_stanga, col_dreapta = st.columns([1.5, 3.5], gap="medium")

with col_stanga:
    st.subheader("Text Input")
    uploaded_file = st.file_uploader("Drag & drop your file here", type=["txt"], label_visibility="collapsed")
    st.html("<div style='font-size:13px; font-weight:bold; color:#8b9eb7; margin-bottom:8px;'>Paste your text:</div>")
    
    # Input Text
    user_text = st.text_area("Text Input", height=200, placeholder="Paste your text...", label_visibility="collapsed")
    #st.html(f"<div style='text-align:right; font-size:11px; color:#53647a; margin-top:-5px; margin-bottom:15px;'>{len(user_text)} / 10000</div>")
    
    if st.button("Analyze", type="primary", use_container_width=True):
        if uploaded_file is not None:
            st.session_state["analysed_text"] = uploaded_file.read().decode("utf-8")
        else:
            st.session_state["analysed_text"] = user_text
        st.session_state["analysed_triggered"] = True

        worker_path = Path(__file__).resolve().parent.parent / "core" / "extract.py"

        if st.session_state["analysed_text"]:
            with st.spinner("Running background script..."):
                try:
                    process = subprocess.run(
                        ["python", str(worker_path), st.session_state["analysed_text"]],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    extracted = process.stdout.strip()
                    st.session_state["show_config_dialog"] = True
                    st.session_state["atoms"] = ast.literal_eval(extracted.split("@")[0])["atoms"]
                    st.session_state["rules"] = ast.literal_eval(extracted.split("@")[1])["rules"]
                    st.session_state["args"] = json.loads(extracted.split("@")[2])["arguments"]
                    st.session_state["attacks"] = ast.literal_eval(extracted.split("@")[3])
                    st.session_state["logs"] = ast.literal_eval(extracted.split("@")[4])
                except subprocess.CalledProcessError as e:
                    st.error(f"❌ Script `extract.py` returned {e.returncode}")
                    st.subheader("Console Output (Stderr):")
                    st.code(e.stderr if e.stderr else "No error text was written to stderr.", language="bash")


# ---------- Config dialog: same UI, "Run Engine" now actually runs it ----------
@st.dialog("Configure Analysis Parameters")
def config_dialog():
    st.subheader("Propagation Settings")
    kappa = st.slider("Kappa (Lipschitz bound)", 0.0, 0.99, 0.6, step=0.01)
    epsilon = st.number_input("Epsilon (convergence threshold)", value=0.0001, format="%.5f")
    iter_mode = st.radio("Iteration mode", ["Run until convergence (epsilon)", "Fixed number of iterations"])
    iters = 0
    if iter_mode == "Fixed number of iterations":
        iters = st.number_input("Number of iterations", min_value=1, value=50, step=1)

    st.divider()
    st.subheader("Atom Strengths")
    atom_strengths = {}
    for atom in st.session_state["atoms"]:
        atom_strengths[atom["id"]] = st.slider(
            f"{atom['id']}: {atom['text']}", 0.0, 1.0, 0.9, step=0.01, key=f"atom_{atom['id']}"
        )

    st.divider()
    st.subheader("Rule Strengths")
    rule_strengths = {}
    for rule in st.session_state["rules"]:
        if rule["type"] == "strict":
            st.write(f"{rule['id']} ({' + '.join(rule['premises'])} → {rule['conclusion']}): strict, fixed at 1.0")
            rule_strengths[rule["id"]] = 1.0
        else:
            rule_strengths[rule["id"]] = st.slider(
                f"{rule['id']} ({' + '.join(rule['premises'])} → {rule['conclusion']})",
                0.0, 1.0, 0.95, step=0.01, key=f"rule_{rule['id']}"
            )

    st.divider()
    if st.button("Run Engine", type="primary", use_container_width=True):
        # Bake user-assigned strengths back into the atoms/rules lists
        atoms_with_strength = [
            {**atom, "strength": atom_strengths[atom["id"]]}
            for atom in st.session_state["atoms"]
        ]
        rules_with_strength = [
            {**rule, "strength": rule_strengths[rule["id"]]}
            for rule in st.session_state["rules"]
        ]

        engine_path = Path(__file__).resolve().parent.parent / "core" / "engine.py"
        payload = json.dumps({
            "atoms": atoms_with_strength,
            "rules": rules_with_strength,
            "args": st.session_state["args"],
            "attacks": st.session_state["attacks"],
            "logs": st.session_state["logs"],
            "text": st.session_state["analysed_text"],
            "kappa": kappa,
            "epsilon": epsilon,
            "iters": int(iters),
        })

        with st.spinner("Building arguments, resolving attacks, running engine..."):
            try:
                process = subprocess.run(
                    ["python", str(engine_path)],
                    input=payload,
                    capture_output=True,
                    text=True,
                    check=True
                )
                st.session_state["analysis_data"] = process.stdout.strip()
                st.session_state["show_config_dialog"] = False
                st.rerun()
            except subprocess.CalledProcessError as e:
                st.error(f"❌ Script `engine.py` returned {e.returncode}")
                st.code(e.stderr if e.stderr else "No error text was written to stderr.", language="bash")

if st.session_state.get("show_config_dialog"):
    config_dialog()


with col_dreapta:
    st.subheader("Graph")
    g_col1, g_col2 = st.columns([3, 1])

    nodes, edges = [], []
    arguments, attacks = [], []

    data = st.session_state.get("analysis_data", "")

    if data:
        data_packets = data.split("@")

        # data_packets[0] = atoms
        # data_packets[1] = rules
        # data_packets[2] = arguments

        atoms = data_packets[0].split("-")
        id2text_atom = dict()
        for atom in atoms:
            if atom:
                atom = atom.split("|")
                id2text_atom[atom[0]] = atom[2]
        arguments = data_packets[2].split("-")
        attacks = data_packets[3].split("-")

        for arg in arguments:
            if arg:
                info = arg.split("|")
                print(info)

                color = "#2865FF" if info[1] == "atomic" else "#FF5733"
                size = 20 if info[1] == "atomic" else 25

                label = f"Argument {info[0]}\nType: {info[1]}\nConclusion: {id2text_atom[info[5]]}"
            
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
    st.html(f'''
        <div style="display: flex; justify-content: space-between; background-color: #121620; padding: 12px; border-radius: 6px; border: 1px solid #1f293d; margin-top: -10px; margin-bottom: 20px;">
            <div style="font-size: 11px; color: #53647a;">
                <b>Nodes:</b> {len(arguments)-1 if len(arguments)>1 else 0} | <b>Edges:</b> {len(attacks)-1 if len(attacks)>1 else 0}
            </div>
        </div>
    ''')

    col_text, col_loguri = st.columns([1, 1], gap="medium")
    
    with col_text:
        st.subheader("Analyzed text")
        text_html = """<div class="text-container" style="border: 1px solid #1f293d; padding: 15px; border-radius: 5px; background-color: #121620;"></div>"""
        if st.session_state["analysed_triggered"]:
            text_html = f"""
            <div class="text-container" style="border: 1px solid #1f293d; padding: 15px; border-radius: 5px; background-color: #121620;">
                <p>{st.session_state["analysed_text"]}</p>
            </div>
            """
        st.html(text_html)

    with col_loguri:
            st.subheader("Logs")
            ora_curenta=datetime.now().strftime("%H:%M:%S:")
            fhtml=""
            data = st.session_state.get("analysis_data", "")
            if data:
                data_packets = data.split("@")
                logs = data_packets[4].split("-")
                for log in logs:
                    info = log.split("|")
                    if len(info)>1:
                        text = info[0]
                        log_type = info[1]
                        color = {"valid":"dot-green", "warning":"dot-yellow", "error":"dot-red", "info":"dot-blue"}
                        content = f"""<div class="log-row">
                                        <div class="log-dot {color[log_type]}"></div>
                                        <div class="log-time">{ ora_curenta }:</div>
                                        <div class="log-text">{text}</div>
                                    </div>"""
                        fhtml+=content

            logs_html = f"""
                <div class="logs-container">
                    {fhtml}
                </div>
                """
            st.html(logs_html)

st.html("""
    <div style="text-align: center; color: #53647a; font-size: 12px; margin-top: 40px; padding: 15px 0; border-top: 1px solid #1f293d;">
        PNSAV Argument Validator &nbsp;&bull;&nbsp; @PNsAV 2026. All rights reserved.
    </div>
""")