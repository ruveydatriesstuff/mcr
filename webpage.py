import streamlit as st
import generator as mcrgen


def onopen():
    '''
    Creates the n-gram models when the page is opened. 
    '''
    mcrgen.globalize()


def generate():
    '''
    Generates lyrics using the generator and prints them on the webpage.
    The lyrics are printed in a codeblock arbitrarily, based on aesthetic preference.
    '''
    st.code(mcrgen.main(), language="none")


onopen()
st.header("My Computational Romance")
st.text("A My Chemical Romance lyrics generator using n-grams. ")
st.text("Created for LING360 Computational Linguistics at Boğaziçi University. ")

gen_button = st.button("Generate")

if gen_button:
    generate()
else:
    st.text("Press the Generate button above to get started. ")
