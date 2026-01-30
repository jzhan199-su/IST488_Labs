import streamlit as st
st.title('IST488Labs')
lab1 = st.Page('Labs/lab1.py', title = 'Lab 1')
lab2 = st.Page('Labs/lab2.py', title = 'Lab 2')

pg = st.navigation([lab1, lab2])
st.set_page_config(page_title = 'IST488 Labs',
                    initial_sidebar_state = 'expanded')

pg.run()