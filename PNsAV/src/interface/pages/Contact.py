import streamlit as st
st.set_page_config(initial_sidebar_state="collapsed")

styles = ""
with open("style.css", "r") as style_file:
    styles = style_file.read()

st.html(f"<style>{styles}</style>")

st.title("Ghid de Utilizare")
st.markdown("1. Încarcă un text sau un fișier.\n2. Apasă 'Analizează' pentru a rula backend-ul.")