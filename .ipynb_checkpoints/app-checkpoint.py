import streamlit as st
import pandas as pd
st.title('Movie Recommendation System')
option = st.selectbox(
    'how would you like to be contacted?',
    ('Email' ,'phone number mobile','home number')
)