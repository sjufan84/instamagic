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

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="INSTAMAGIC",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

def image_style_select(image_style_options: List[str], index: int = 0):
    """ Image Style Selection """
    image_style = st.selectbox(
        "What style of image would you like to generate?", image_style_options,
        index = index
    )
    return image_style

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
    "requested_post_adjustments", "requested_image_adjustments",
    "post_status"
]
default_values = [
    None, None, None, None, 3, None, [],
    "Create Post", "", False, None, "display_home",
    [], None, "Photorealistic", None, None, "Create Post"
]

for var, default_value in zip(session_vars, default_values):
    if var not in st.session_state:
        st.session_state[var] = default_value

def reset_session_state():
    for var, default_value in zip(session_vars, default_values):
        st.session_state[var] = default_value

def get_image_selection():
    """ Image Selection """
    image_selection = st.radio(
        "Would you like to include an image with your post?", ("Yes", "No"), index=1
    )
    if image_selection == "Yes":
        return True
    else:
        return False

def create_post_home():
    reset_session_state()
    st.markdown("### Create a New Post")
    square_choice = None
    stories_choice = None
    landscape_choice = None
    purpose = st.selectbox(
        "What is the purpose of your post?",
        options=post_purposes, index=0
    )
    logger.debug(f"Selected purpose: {purpose}")

    platform = st.selectbox(
        "Which platform are you posting on, if any?",
        options=platform_options, index=0
    )
    logger.debug(f"Selected platform: {platform}")

    persona = st.selectbox(
        "What persona would you like to embody for this post?",
        options=personas, index=0
    )
    logger.debug(f"Selected persona: {persona}")

    tone = st.selectbox(
        "What tone would you like to convey in your post?",
        options=post_tones, index=0
    )
    logger.debug(f"Selected tone: {tone}")

    verbosity = st.slider(
        "How verbose would you like your post to be?\
        (1 being very brief, 5 being very detailed)", 1, 5, value=3
    )
    logger.debug(f"Selected verbosity: {verbosity}")

    details = st.text_area(
        """Let us know about the details of your post
        This could be a description of your dining experience, notes about the book you just read
        or a summary of your recent travel adventure.  Give the basic framework of your post and
        let us do the rest!""",
        placeholder=""
    )
    logger.debug(f"Selected post details: {details}")

    generate_image = get_image_selection()
    if generate_image:
        st.session_state.generate_image = True
        picture_mode = st.selectbox(
            '###### 📸 Snap a Pic, 📤 Upload an Image, or Let Us Generate One For You!',
            ("Snap a pic", "Upload an image", "Let Us Generate One For You"), index=None,
        )
        if picture_mode == "Snap a pic":
            uploaded_image = st.camera_input("Snap a pic")
            if uploaded_image:
                if uploaded_image.name.endswith(".heic") or uploaded_image.name.endswith(".HEIC"):
                    image_string = heic_to_base64(uploaded_image)
                    st.session_state.user_image_string = image_string
                else:
                    image_string = encode_image(uploaded_image)
                st.session_state.user_image_string = image_string

        elif picture_mode == "Upload an image":
            # Show a file upoloader that only accepts image files
            uploaded_image = st.file_uploader(
                "Upload an image", type=["png", "jpg", "jpeg", "heic", "HEIC"]
            )
            # Convert the image to a base64 string
            if uploaded_image:
                # If the file type is .heic or .HEIC, convert to a .png using PIL
                if uploaded_image.name.endswith(".heic") or uploaded_image.name.endswith(".HEIC"):
                    image_string = heic_to_base64(uploaded_image)
                    st.session_state.user_image_string = image_string
                else:
                    image_string = encode_image(uploaded_image)
                st.session_state.user_image_string = image_string
        elif picture_mode == "Let Us Generate One For You":
            st.session_state.user_image_string = None
        image_style = image_style_select(dall_e_image_styles)

        st.markdown("**Choose the image size(s) for your post:**")
        square_choice = st.checkbox("Square", value=False)
        stories_choice = st.checkbox("Stories", value=False)
        landscape_choice = st.checkbox("Landscape", value=False)

        # If neither are checked, display a warning
        if not square_choice and not stories_choice and not landscape_choice:
            st.warning("Please select at least one image size.")

    create_post_button = st.button("Create Post")
    if create_post_button:
        if square_choice:
            st.session_state.image_size_choices.append("Square")
        if stories_choice:
            st.session_state.image_size_choices.append("Stories")
        if landscape_choice:
            st.session_state.image_size_choices.append("Landscape")
        st.session_state.purpose = purpose
        st.session_state.persona = persona
        st.session_state.tone = tone
        st.session_state.platform = platform
        st.session_state.verbosity = verbosity
        st.session_state.post_details = details
        st.session_state.generate_image = generate_image
        if generate_image:
            st.session_state.image_style = image_style
        st.session_state.post_page = "Display Post"
        st.rerun()

def edit_post_page():
    st.markdown("### Edit Your Post")
    purpose = st.selectbox(
        "What is the purpose of your post?",
        options=post_purposes, index=post_purposes.index(st.session_state.purpose)
    )
    logger.debug(f"Selected purpose: {purpose}")

    platform = st.selectbox(
        "Which platform are you posting on, if any?",
        options=platform_options, index=platform_options.index(st.session_state.platform)
    )

    persona = st.selectbox(
        "What persona would you like to embody for this post?",
        options=personas, index=personas.index(st.session_state.persona)
    )

    tone = st.selectbox(
        "What tone would you like to convey in your post?",
        options=post_tones, index=post_tones.index(st.session_state.tone)
    )

    verbosity = st.slider(
        "How verbose would you like your post to be?\
        (1 being very brief, 5 being very detailed)", 1, 5, value=st.session_state.verbosity
    )

    details = st.text_area(
        """Let us know about the details of your post
        This could be a description of your dining experience, notes about the book you just read
        or a summary of your recent travel adventure.  Give the basic framework of your post and
        let us do the rest!""",
        value=st.session_state.post_details
    )

    create_new_post_button = st.button("Create New Post")
    if create_new_post_button:
        st.session_state.purpose = purpose
        st.session_state.persona = persona
        st.session_state.tone = tone
        st.session_state.platform = platform
        st.session_state.verbosity = verbosity
        st.session_state.post_details = details
        st.session_state.post_page = "Display Post"
        st.rerun()

async def display_post():
    st.markdown("#### Here's your post!")
    generating_images = False
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

    edit_post_button = st.button("Edit Post", use_container_width=True)
    if edit_post_button:
        edit_post_page()

    if st.session_state.generate_image and st.session_state.current_images == []:
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
                    generating_images = True
                    st.write("Prompt generated, now creating image(s)...")
                    for size_choice in st.session_state.image_size_choices:
                        image = await create_image(image_prompt, size_choice)
                        st.session_state.current_images.append(image)
                        st.image(image, use_column_width=True)
                generating_images = False

        else:
            with st.spinner("Generating image(s).  This may take a few moments..."):
                image_prompt = await get_image_prompt(
                    st.session_state.current_post,
                    st.session_state.post_details,
                    st.session_state.platform,
                    st.session_state.image_style
                )

                if image_prompt:
                    generating_images = True
                    st.write("Prompt generated, now creating image(s)...")
                    for size_choice in st.session_state.image_size_choices:
                        image = await create_image(image_prompt, size_choice)
                        st.session_state.current_images.append(image)
                        st.image(image, use_column_width=True)
                generating_images = False

    elif st.session_state.current_images != [] and generating_images is False:
        for image in st.session_state.current_images:
            st.image(image, use_column_width=True)

    generate_new_post = st.button("Start Over", use_container_width=True)
    if generate_new_post:
        st.session_state.post_page = "Create Post"
        st.rerun()

if st.session_state.post_page == "Create Post":
    create_post_home()
elif st.session_state.post_page == "Display Post":
    asyncio.run(display_post())
