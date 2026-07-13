import streamlit as st
st.set_page_config(initial_sidebar_state="collapsed")

st.set_page_config(
    page_title="PNsAV About",
    page_icon="❓",
    layout="wide",
)

styles = ""
with open("style.css", "r") as style_file:
    styles = style_file.read()

st.html(f"<style>{styles}</style>")

nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([7, 1, 1, 1])
with nav_col1:
    st.html("""
    <div class="nav-bar">
        <div class="nav-logo">
            ❓ PNsAV About
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

st.title("Despre PNsAV")
st.write("PNsAV este un instrument avansat de procesare a limbajului natural pentru maparea argumentării formale.")