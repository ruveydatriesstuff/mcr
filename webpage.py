import streamlit as st
import generator as mcrgen


def onopen():
    mcrgen.globalize()


def generate():
    st.code(mcrgen.main(), language="none")


onopen()
st.header("My Computational Romance")
st.text("A My Chemical Romance lyrics generator using n-grams. \n")
st.caption("Created to fulfill the requirements of LING360 Computational Linguistics at Boğaziçi University. ")
gen_button = st.button("Generate")

if gen_button:
    generate()
else:
    st.text("Press the Generate button above to get started. ")
