import streamlit as st
from utils.post_utils import generate_post, get_image_prompt
from utils.image_utils import create_image

if "display_post_page" not in st.session_state:
    st.session_state.display_post_page = "display_home"

def display_home():
    post_container = st.container()
    if st.session_state.current_post is None:
        st.markdown("##### Here's your post!")
        post = generate_post(
            st.session_state.purpose,
            st.session_state.persona,
            st.session_state.tone,
            st.session_state.verbosity,
            st.session_state.post_details
        )
        post_container.write(post)
    # @TODO Add in text area for user to request adjustments to the post

    if st.session_state.generate_image:
        with st.spinner("Generating image.  This may take a few moments..."):
            image_prompt = get_image_prompt(
                st.session_state.current_post,
                st.session_state.purpose,
                st.session_state.platform
            )
            st.write(image_prompt)
            if image_prompt:
                st.write("Prompt generated, now creating image(s)...")
                for size_choice in st.session_state.image_size_choices:
                    image = create_image(image_prompt, size_choice)
                    st.session_state.current_images.append(image)
    if st.session_state.current_images != []:
        st.markdown("### Your generated images:")
        for image in st.session_state.current_images:
            st.image(image, use_column_width=True)

def display_adjustments():
    pass

if st.session_state.display_post_page == "display_home":
    display_home()
