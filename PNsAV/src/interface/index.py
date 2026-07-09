import streamlit as st
import json
import time
from streamlit_agraph import agraph, Node, Edge, Config

st.set_page_config(layout="wide", page_title="Probabilistic Neurosymbolic Argument Validation Model")

st.title("PNsAV")
st.markdown("Probabilistic Neurosymbolic Argument Validation Model")

MOCK_ATOMS = {"atoms":[{"id":"a1","text":"An entity has a siren","kb_type":"premise","source_quote":"a vehicle has a siren"},{"id":"a2","text":"An entity is an emergency vehicle","kb_type":"premise","source_quote":"it is an emergency vehicle"},{"id":"a3","text":"An entity can run red lights","kb_type":"premise","source_quote":"it can run red lights"},{"id":"a4","text":"This entity is Engine 42","kb_type":"premise","source_quote":"Engine 42"},{"id":"a5","text":"This entity has a siren","kb_type":"premise","source_quote":"has a siren"}]}
MOCK_RULES = {"scratchpad":{"extracted_connectors":["If","If"],"disjunction_split_plan":"No OR disjunctions found; no split needed.","inversion_check":"No 'requires' inversion found."},"rules":[{"id":"r1","conclusion":"a2","premises":["a1"],"type":"defeasible"}, {"id":"r2","conclusion":"a3","premises":["a2"],"type":"defeasible"}, {"id":"r3","conclusion":"a1","premises":["a5"],"type":"strict"}]}
MOCK_ARGUMENTS = {"scratchpad":{"text_connectors_found":["If","If"],"rule_firing_verification":"P1 creates atomic arguments for all provided atoms..."},"arguments": [{"id":"A1","conclusion":"a1","top_rule":None,"sub_arguments":[],"type":"atomic"}, {"id":"A2","conclusion":"a2","top_rule":None,"sub_arguments":[],"type":"atomic"}, {"id":"A3","conclusion":"a3","top_rule":None,"sub_arguments":[],"type":"atomic"}, {"id":"A4","conclusion":"a4","top_rule":None,"sub_arguments":[],"type":"atomic"}, {"id":"A5","conclusion":"a5","top_rule":None,"sub_arguments":[],"type":"atomic"}, {"id":"A6","conclusion":"a1","top_rule":"r3","sub_arguments":["A5"],"type":"strict"}, {"id":"A7","conclusion":"a2","top_rule":"r1","sub_arguments":["A6"],"type":"defeasible"}, {"id":"A8","conclusion":"a3","top_rule":"r2","sub_arguments":["A7"],"type":"defeasible"}]}

st.title("🧠 Sistem de Extracție și Vizualizare Argumente")
st.caption("Pagina 2: Procesare, Analiză grafuri și loguri")

