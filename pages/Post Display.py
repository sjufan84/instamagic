import streamlit as st
from utils.post_utils import generate_post, get_image_prompt

if "display_post_page" not in st.session_state:
    st.session_state.display_post_page = "display_home"

def display_home():
    post_container = st.container()
    if st.session_state.current_post is None:
        with st.spinner("Generating post..."):
            post = generate_post(
                st.session_state.purpose,
                st.session_state.persona,
                st.session_state.tone,
                st.session_state.verbosity,
                st.session_state.post_details
            )
            post_container.write(post)
    if st.session_state.generate_image:
        with st.spinner("Generating image.  This may take a few moments..."):
            image_prompt = get_image_prompt(
                st.session_state.current_post,
                st.session_state.purpose,
                st.session_state.platform
            )
            st.write(image_prompt)

if st.session_state.display_post_page == "display_home":
    display_home()
