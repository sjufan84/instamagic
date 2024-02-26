import streamlit as st
from typing import List
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

def post_details():
    post_details = st.text_area("""Let us know about the details of your post
    This could be a description of your dining experience, notes about the book you just read
    or a summary of your recent travel adventure.  Give the basic framework of your post and
    let us do the rest!""")
    return post_details

def tone_select(tone_options: List[str]):
    """ Tone Selection """
    tone = st.selectbox("What tone would you like to convey in your post?\
    (Select 'Other' if you do not find the appropriate option')", tone_options)
    return tone

def image_style_select(image_style_options: List[str]):
    """ Image Style Selection """
    image_style = st.selectbox("What style of image would you like to generate?", image_style_options)
    return image_style

def purpose_select(purpose_options: List[str]):
    """ Purpose Selection """
    purpose = st.selectbox("What is the purpose of your post?  (Select 'Other' if\
    you do not find the appropriate option')", purpose_options)
    return purpose

def persona_select(persona_options: List[str]):
    """ Persona Selection """
    persona = st.selectbox("What persona would you like to embody for this post?  You can also\
    select 'Other' or 'None'.", persona_options)
    return persona

def platform_select(platform_options: List[str]):
    """ Platform Selection """
    platform = st.selectbox("Which platform are you posting on, if any?", platform_options)
    return platform

def set_verbosity():
    """ Verbosity Selection """
    verbosity = st.slider("How verbose would you like your post to be?\
    (1 being very brief, 5 being very detailed)", 1, 5, 3)
    return verbosity

def get_image_selection():
    """ Image Selection """
    image_selection = st.radio("Would you like to include an image with your post?", ("Yes", "No"), index=1)
    if image_selection == "Yes":
        return True
    else:
        return False

def create_post_home():
    square_choice = None
    stories_choice = None
    with st.form(key="create_post_form"):
        purpose = purpose_select(post_purposes)
        logger.debug(f"Selected purpose: {purpose}")

        platform = platform_select(platform_options)
        logger.debug(f"Selected platform: {platform}")

        persona = persona_select(personas)
        logger.debug(f"Selected persona: {persona}")

        tone = tone_select(post_tones)
        logger.debug(f"Selected tone: {tone}")

        verbosity = set_verbosity()
        logger.debug(f"Selected verbosity: {verbosity}")

        details = post_details()

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
            # If neither are checked, display a warning
            if not square_choice and not stories_choice:
                st.warning("Please select at least one image size.")

        create_post_button = st.form_submit_button("Create Post")
        if create_post_button:
            if square_choice:
                st.session_state.image_size_choices.append("Square")
            if stories_choice:
                st.session_state.image_size_choices.append("Stories")
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

    if st.session_state.post_page == "Display Post":
        st.markdown("##### Here's your post!")
        if st.session_state.requested_post_adjustments is not None:
            post = edit_post(
                post = st.session_state.current_post,
                requested_adjustments = st.session_state.requested_post_adjustments
            )
        elif st.session_state.current_post is not None and st.session_state.requested_post_adjustments is None:
            post = st.session_state.current_post
        else:
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
        # Create a textarea for the user to request changes to the post
        post_changes = st.text_area("Would you like to make any changes to the post?  If so, please specify.")
        change_post_button = st.button("Request Changes")
        if change_post_button:
            with st.spinner("Making requested changes..."):
                st.session_state.requested_post_adjustments = post_changes
                st.session_state.requested_image_adjustments = None
                st.rerun()

        if st.session_state.generate_image and st.session_state.current_images == []:
            if st.session_state.user_image_string:
                with st.spinner("Generating image.  This may take a few moments..."):
                    image_prompt = alter_image(
                        st.session_state.user_image_string,
                        st.session_state.current_post,
                        st.session_state.post_details,
                        st.session_state.platform,
                        st.session_state.image_style
                    )
                    st.markdown(f"""**@Babette this won't be in the final app, obviously,\
                    but thought you would find\
                    it interesting.  This is the prompt created and sent to dall-e** {image_prompt}""")
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
                    st.markdown(f"""**@Babette this won't be in the final app, obviously,\
                    but thought you would find\
                    it interesting.  This is the prompt created and sent to dall-e** {image_prompt}""")
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
            st.session_state.post_page = "Create Post"
            reset_session_state()
            st.rerun()

create_post_home()
