import streamlit as st
st.set_page_config(initial_sidebar_state="collapsed")

styles = ""
with open("style.css", "r") as style_file:
    styles = style_file.read()

st.html(f"<style>{styles}</style>")

st.title("Resurse suplimentare")
st.markdown("Documente suplimentare referitoare la framework-ul ASPIC+.")