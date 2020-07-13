import streamlit as st

# can add to any plot for darkmode template="plotly_dark"
def stylize():
    
    #Footer vanish
    hide_footer_style = """
    <style>
    .reportview-container .main footer {visibility: hidden;}    
    """
    st.markdown(hide_footer_style, unsafe_allow_html=True)

    #Hamburger menu vanish
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

    #DarkMode option
    if st.sidebar.checkbox('DarkMode'):
        st.markdown("""
    <style>
    body {
        color: #fff;
        background-color: #111;
        etc. 
    }
    </style>
        """, unsafe_allow_html=True)