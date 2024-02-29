import streamlit as st
import logging
import asyncio
from typing import List
from utils.image_utils import encode_image, heic_to_base64
from utils.post_utils import generate_post

logger = logging.getLogger(__name__)

if "current_post" not in st.session_state:
    st.session_state.current_post = None

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
    "Pissed Off",
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
    "Other",
])

personas = sorted([
    "Adventurer",
    "Foodie",
    "Bookworm",
    "Fitness Guru",
    "Fashionista",
    "Tech Enthusiast",
    "Artist",
    "Comedian",
    "Philosopher",
    "Environmentalist",
    "Musician",
    "Historian",
    "Scientist",
    "Activist",
    "Entrepreneur",
    "Mentor",
    "Storyteller",
    "Traveler",
    "Wellness Advocate",
    "DIY Enthusiast",
    "Gamer",
    "Movie Buff",
    "Pet Lover",
    "Home Chef",
    "Gardener",
    "Collector",
    "Volunteer",
    "Parent",
    "Student",
    "Professional",
    "Other",
    "None",
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

def image_style_select(image_style_options: List[str], index: int = 0):
    """ Image Style Selection """
    image_style = st.selectbox(
        "What style of image would you like to generate?", image_style_options,
        index = index
    )
    return image_style

def get_image_selection():
    """ Image Selection """
    image_selection = st.radio(
        "Would you like to include an image with your post?", ("Yes", "No"), index=1
    )
    if image_selection == "Yes":
        return True
    else:
        return False

def select_platform(platform_options, current_platform):
    if current_platform not in platform_options:
        platform = st.text_input(
            "Please specify the platform you are posting on",
            value=current_platform)
    else:
        platform = st.selectbox(
            "Which platform are you posting on, if any?",
            options=platform_options, index=platform_options.index(current_platform)
        )
    return platform

def select_persona(personas, current_persona):
    if current_persona not in personas:
        persona = st.text_input(
            "Please specify the persona you would like to embody",
            value=current_persona)
    else:
        persona = st.selectbox(
            "What persona would you like to embody for this post?",
            options=personas, index=personas.index(current_persona)
        )
        if persona == "Other":
            persona = st.text_input(
                "Please specify the persona you would like to embody",
                value=current_persona)
    return persona

def select_tone(post_tones, current_tone):
    if current_tone not in post_tones:
        tone = st.text_input(
            "What tone would you like to convey in your post?",
            value=current_tone)
    else:
        tone = st.selectbox(
            "What tone would you like to convey in your post?",
            options=post_tones, index=post_tones.index(current_tone)
        )
        if tone == "Other":
            tone = st.text_input(
                "What tone would you like to convey in your post?",
                value=current_tone)
    return tone

def select_verbosity(current_verbosity):
    verbosity = st.slider(
        "How verbose would you like your post to be?\
        (1 being very brief and perfect for X, 5 being very detailed)",
        1, 5, value=current_verbosity
    )

    return verbosity

def input_details(current_details):
    details = st.text_area(
        """Share some details! Jot down personalized details
        for us to tailor your post. Just give us the outline,
        and we'll handle the rest!""", value=current_details
    )
    return details

def select_purpose(post_purposes, current_purpose):
    if current_purpose not in post_purposes:
        purpose = st.text_input(
            "Please specify the purpose of your post",
            value=current_purpose)
    else:
        purpose = st.selectbox(
            "What is the purpose of your post?",
            options=post_purposes, index=post_purposes.index(current_purpose)
        )
    if purpose == "Other":
        purpose = st.text_input(
            "Please specify the purpose of your post",
            value=current_purpose)
    logger.debug(f"Selected purpose: {purpose}")
    return purpose

def create_form(platform_options, personas, post_tones, post_purposes, current_values):
    with st.form(key='my_form'):
        platform = select_platform(platform_options, current_values['platform'])
        persona = select_persona(personas, current_values['persona'])
        tone = select_tone(post_tones, current_values['tone'])
        verbosity = select_verbosity(current_values['verbosity'])
        details = input_details(current_values['details'])
        purpose = select_purpose(post_purposes, current_values['purpose'])

        submit_button = st.form_submit_button(label='Generate Post!')

    if submit_button:
        return {
            'platform': platform,
            'persona': persona,
            'tone': tone,
            'verbosity': verbosity,
            'details': details,
            'purpose': purpose
        }

def select_image():
    generate_image = get_image_selection()
    if generate_image:
        st.session_state.generate_image = True
        picture_mode = st.selectbox(
            '###### 📸 Snap a Pic, 📤 Upload an Image, or Let Us Generate One For You! If you take a picture\
            or upload an image, the AI will use that image as the basis for its generation.',
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
        square_choice = st.checkbox("Square (Perfect for Instagram)", value=False)
        stories_choice = st.checkbox("""Verticle (Perfect for Instagram Stories,
        TikTok and Pinterest)""", value=False)
        landscape_choice = st.checkbox("""Rectangle (Perfect for Facebook, LinkedIn
        and X)""", value=False)

        # If neither are checked, display a warning
        if not square_choice and not stories_choice and not landscape_choice:
            st.warning("Please select at least one image size.")

        return {
            'image_style': image_style,
            'square_choice': square_choice,
            'stories_choice': stories_choice,
            'landscape_choice': landscape_choice
        }

async def main():
    st.title("Post Generator")
    post = None
    post_container = st.empty()
    images_container = st.empty()
    current_values = {
        'platform': "Instagram",
        'persona': "None",
        'tone': "Casual",
        'verbosity': 3,
        'details': "",
        'purpose': "Other"
    }
    form_values = None

    with post_container.container():
        platform = select_platform(platform_options, current_values['platform'])
        persona = select_persona(personas, current_values['persona'])
        if persona == "Other":
            persona = st.text_input(
                "Please specify the persona you would like to embody",
                value=current_values['persona'])
        tone = select_tone(post_tones, current_values['tone'])
        verbosity = select_verbosity(current_values['verbosity'])
        details = input_details(current_values['details'])
        purpose = select_purpose(post_purposes, current_values['purpose'])

        submit_button = st.button(label='Generate Post!')

    if submit_button:
        form_values = {
            'platform': platform,
            'persona': persona,
            'tone': tone,
            'verbosity': verbosity,
            'details': details,
            'purpose': purpose
        }
    # Call the generate_post function with the form_values
    post = await generate_post(form_values)
    if post:
        post_container.markdown(post)

if __name__ == "__main__":
    asyncio.run(main())
