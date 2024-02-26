import streamlit as st
from typing import List
import asyncio
import logging
# from streamlit_extras.switch_page_button import switch_page
from utils.image_utils import encode_image, heic_to_base64
from utils.post_utils import (
    generate_post, get_image_prompt, alter_image,
    edit_post, get_new_image_prompt
)
from utils.image_utils import create_image
from forms.create_post_form import create_post_form

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="INSTAMAGIC",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

dall_e_image_styles = sorted([
    "Photorealistic",
    "Digital Art",
    "Graphic Art",
    "Oil Painting",
    "Watercolor Painting",
    "Ink Drawing",
    "Pencil Sketch",
    "Charcoal Drawing",
    "Pastel Drawing",
    "Abstract Art",
    "Surrealism",
    "Pop Art",
    "Concept Art",
    "Pixel Art",
    "Minimalist Art",
    "Vintage Photography",
    "Street Art",
    "3D Render",
    "Anime/Manga Style",
    "Storybook Illustration",
    "Fantasy Art",
    "Sci-Fi Art",
    "Gothic Art",
    "Art Nouveau",
    "Art Deco",
    "Cubism",
    "Impressionism",
])


post_tones = sorted([
    "Angry",
    "Casual",
    "Confused",
    "Conversational",
    "Critical",
    "Educational",
    "Empathetic",
    "Encouraging",
    "Excited",
    "Grateful",
    "Happy",
    "Humorous",
    "Informative",
    "Inspirational",
    "Mysterious",
    "Nostalgic",
    "Optimistic",
    "Other",
    "Passionate",
    "Pessimistic",
    "Professional",
    "Questioning",
    "Reflective",
    "Romantic",
    "Sarcastic",
    "Serious",
    "Skeptical",
    "Sympathetic",
    "Whimsical",
])

# Purpose options list
post_purposes = sorted([
    "Restaurant Review",
    "Book Review",
    "Family Update",
    "Travel Experience",
    "Recipe Share",
    "Health & Fitness Progress",
    "Personal Achievement",
    "Work or Career News",
    "Educational Content",
    "Event Announcement",
    "Hobby or Craft Showcase",
    "Pet Update",
    "Music or Playlist Recommendation",
    "Movie or TV Show Review",
    "Tech Gadget Review",
    "Fashion or Beauty Tips",
    "Sports Update",
    "DIY Project",
    "Gaming Experience",
    "Charity or Cause Awareness",
    "Political Opinion",
    "Business Promotion",
    "Meme or Funny Content",
    "Question or Poll",
    "Life Advice or Tips",
    "Nature and Outdoor Adventures",
    "Art and Photography",
    "Science and Discovery",
    "Cultural Experience",
    "Daily Thoughts or Reflections",
])

personas = sorted([
    "The Adventurer",
    "The Foodie",
    "The Bookworm",
    "The Fitness Guru",
    "The Fashionista",
    "The Tech Enthusiast",
    "The Artist",
    "The Comedian",
    "The Philosopher",
    "The Environmentalist",
    "The Musician",
    "The Historian",
    "The Scientist",
    "The Activist",
    "The Entrepreneur",
    "The Mentor",
    "The Storyteller",
    "The Traveler",
    "The Wellness Advocate",
    "The DIY Enthusiast",
    "The Gamer",
    "The Movie Buff",
    "The Pet Lover",
    "The Home Chef",
    "The Gardener",
    "The Collector",
    "The Volunteer",
    "The Parent",
    "The Student",
    "The Professional"
])

platform_options = sorted([
    "Instagram",
    "Facebook",
    "Twitter",
    "LinkedIn",
    "Pinterest",
    "TikTok",
    "Snapchat",
    "YouTube",
])

session_vars = [
    "purpose", "persona", "tone", "platform",
    "verbosity", "current_post", "current_images",
    "post_page", "post_details", "generate_image",
    "current_image_prompt", "display_post_page",
    "image_size_choices", "user_image_string", "image_style",
    "requested_post_adjustments", "requested_image_adjustments"
]
default_values = [
    None, None, None, None, 3, None, [],
    "Create Post", None, False, None, "display_home",
    [], None, "Photorealistic", None, None
]

for var, default_value in zip(session_vars, default_values):
    if var not in st.session_state:
        st.session_state[var] = default_value

def reset_session_state():
    for var, default_value in zip(session_vars, default_values):
        st.session_state[var] = default_value

async def create_post_home():
    st.write(st.session_state.post_page)
    create_post_form()
    if st.session_state.post_page == "Display Post":
        st.markdown("##### Here's your post!")
        post = await generate_post(
            st.session_state.purpose,
            st.session_state.persona,
            st.session_state.tone,
            st.session_state.verbosity,
            st.session_state.post_details
        )
        if post:
            st.write(post)
            st.session_state.current_post = post
        
        st.markdown("**If you would like to make any changes to your post,\
        you can simply change anything within the form above and resubmit!**")

        if st.session_state.generate_image:
            if st.session_state.user_image_string:
                with st.spinner("Generating image.  This may take a few moments..."):
                    image_prompt = await alter_image(
                        st.session_state.user_image_string,
                        st.session_state.current_post,
                        st.session_state.post_details,
                        st.session_state.platform,
                        st.session_state.image_style
                    )
                    if image_prompt:
                        st.write("Prompt generated, now creating image(s)...")
                        for size_choice in st.session_state.image_size_choices:
                            image = await create_image(image_prompt, size_choice)
                            st.session_state.current_images.append(image)

            else:
                with st.spinner("Generating image(s).  This may take a few moments..."):
                    image_prompt = await get_image_prompt(
                        st.session_state.current_post,
                        st.session_state.post_details,
                        st.session_state.platform,
                        st.session_state.image_style
                    )
               
                    if image_prompt:
                        st.write("Prompt generated, now creating image(s)...")
                        for size_choice in st.session_state.image_size_choices:
                            image = await create_image(image_prompt, size_choice)
                            st.session_state.current_images.append(image)

        if st.session_state.current_images != []:
            st.markdown("### Your generated images:")
            for image in st.session_state.current_images:
                st.image(image, use_column_width=True)

        st.session_state.post_page = "Create Post"

        generate_new_post = st.button("Generate New Post")
        if generate_new_post:
            st.session_state.post_page = "Create Post"
            reset_session_state()
            st.rerun()

asyncio.run(create_post_home())
