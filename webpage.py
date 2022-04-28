import streamlit as st
import generator as mcrgen


def onopen():
    mcrgen.globalize()


def generate():
    st.code(mcrgen.main(), language="none")


onopen()
st.header("MCR Lyrics Generator")
st.text("Welcome to a work in progress for our Computational Linguistics class.")
gen_button = st.button("Generate")

if gen_button:
    generate()
else:
    st.text("Press the Generate button above to get started. ")
