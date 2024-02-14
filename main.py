""" Instamagic Home Page """
import logging
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.switch_page_button import switch_page

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="INSTAMAGIC",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Import Google Font in Streamlit CSS
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css?family=Anton');
        @import url('https://fonts.googleapis.com/css2?family=Arapey&display=swap');
    </style>
    """,
    unsafe_allow_html=True
)

def header():
    with stylable_container(
        key="header-main",
        css_styles="""
            h1 {
                color: #000000;
                font-size: 4em;
                text-align: center;
                font-family: 'Anton', sans-serif;
            }
            p {
                font-size: 1.1em;
                text-align: start;
                font-family: 'Arapey', serif;
            }
        """,
    ):
        # Create a centered header using HTML with bold font
        st.markdown(
            """<h1><b>INSTAMAGIC</b></h1>""", unsafe_allow_html=True
        )
        # Create a centered subheader using HTML with bold font
        st.markdown(
            """<p style='text-align:center; font-family:"Arapey";'>
            Create magical social media posts generated by AI, tailored to you.</p>""", unsafe_allow_html=True
        )
        st.markdown(
            """**How it works:** INSTAMAGIC uses cutting-edge AI to generate bespoke social media
            posts or other generative content tailored to meet your specific needs.
            Whether you are a foodie, a bookworm, a
            fitness enthusiast, a world traveler, or a pet lover, we have you covered!  Simply select the
            purpose of your post or content, specify the tone, persona, verbosity and platform (if any),
            and let the magic begin!  We can even generate an image to go with your post, either based
            entirely on your prompt
            and parameters, or taking into account an existing image you provide.  Have fun and let your
            creativity run wild!\n\n If you need some inspiration
            or more guidance on how to use INSTAMAGIC,
            click below to view some examples.  When you're ready to get started, click Let's Go! to begin"""
        )
        st.text("")
        col1, col2 = st.columns([1, 1], gap='medium')
        with col1:
            examples_button = st.button("View Examples", type='secondary', use_container_width=True)
            if examples_button:
                switch_page("Examples")
                st.rerun()
        with col2:
            start_button = st.button("Let's Go!", type='primary', use_container_width=True)
            if start_button:
                switch_page("Create Post")
                st.rerun()

def main():
    """ Main function """
    header()

if __name__ == "__main__":
    main()
