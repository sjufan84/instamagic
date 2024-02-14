import streamlit as st
from utils.post_utils import generate_post, get_image_prompt, alter_image
from utils.image_utils import create_image
from streamlit_extras.switch_page_button import switch_page

if "display_post_page" not in st.session_state:
    st.session_state.display_post_page = "display_home"

def display_home():
    if st.session_state.current_post is None:
        st.markdown("##### Here's your post!")
        post = generate_post(
            st.session_state.purpose,
            st.session_state.persona,
            st.session_state.tone,
            st.session_state.verbosity,
            st.session_state.post_details
        )
        if post:
            st.write(post)
            st.session_state.current_post = post

    if st.session_state.generate_image and st.session_state.current_images == [] and st.session_state.current_post is not None:
        if st.session_state.user_image_string:
            with st.spinner("Generating image.  This may take a few moments..."):
                image_prompt = alter_image(
                    st.session_state.user_image_string,
                    st.session_state.current_post,
                    st.session_state.post_details,
                    st.session_state.platform,
                    st.session_state.image_style
                )
                st.write(image_prompt)
                if image_prompt:
                    st.write("Prompt generated, now creating image(s)...")
                    for size_choice in st.session_state.image_size_choices:
                        image = create_image(image_prompt, size_choice)
                        st.session_state.current_images.append(image)
        else:
            with st.spinner("Generating image.  This may take a few moments..."):
                image_prompt = get_image_prompt(
                    st.session_state.current_post,
                    st.session_state.post_details,
                    st.session_state.platform,
                    st.session_state.image_style
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

    generate_new_post = st.button("Generate New Post")
    if generate_new_post:
        st.session_state.generate_image = False
        st.session_state.current_post = None
        st.session_state.current_images = []
        st.session_state.display_post_page = "display_adjustments"
        switch_page("Create Post")
        st.rerun()

def display_adjustments():
    pass

if st.session_state.display_post_page == "display_home":
    display_home()
elif st.session_state.display_post_page == "display_adjustments":
    display_adjustments()
