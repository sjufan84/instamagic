import streamlit as st
from typing import List
import logging
from utils.image_utils import encode_image, heic_to_base64

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

def set_image_selection(image_selection: bool):
    st.session_state.generate_image = image_selection

def post_details(value: str = ""):
    post_details = st.text_area(
        """Let us know about the details of your post
        This could be a description of your dining experience, notes about the book you just read
        or a summary of your recent travel adventure.  Give the basic framework of your post and
        let us do the rest!""",
        placeholder=value
    )
    return post_details

def tone_select(tone_options: List[str], index: int = 0):
    """ Tone Selection """
    tone = st.selectbox(
        "What tone would you like to convey in your post?\
        (Select 'Other' if you do not find the appropriate option')", tone_options,
        index = index
    )
    return tone

def image_style_select(image_style_options: List[str], index: int = 0):
    """ Image Style Selection """
    image_style = st.selectbox(
        "What style of image would you like to generate?", image_style_options,
        index = index
    )
    return image_style

def purpose_select(purpose_options: List[str], index: int = 0):
    """ Purpose Selection """
    purpose = st.selectbox(
        "What is the purpose of your post?  (Select 'Other' if\
    you do not find the appropriate option')", purpose_options,
        index = index
    )
    return purpose

def persona_select(persona_options: List[str], index: int = 0):
    """ Persona Selection """
    # Set the value to the index of the persona session state if it exists
    persona = st.selectbox(
        "What persona would you like to embody for this post?", options=persona_options,
        index = index
    )
    return persona

def platform_select(platform_options: List[str], index: int = 0):
    """ Platform Selection """
    platform = st.selectbox(
        "Which platform are you posting on, if any?", options=platform_options,
        index = index
    )
    return platform

def set_verbosity(value: int = 3):
    """ Verbosity Selection """
    verbosity = st.slider(
        "How verbose would you like your post to be?\
        (1 being very brief, 5 being very detailed)", 1, 5,
        value=value
    )
    return verbosity

def get_image_selection():
    """ Image Selection """
    image_selection = st.radio(
        "Would you like to include an image with your post?", ("Yes", "No"), index=1
    )
    if image_selection == "Yes":
        return True
    else:
        return False

async def create_post_form(post_status: str = "Create Post"):
    st.write(st.session_state.current_post)
    st.write(st.session_state.post_details)
    st.write(st.session_state.post_status)
    square_choice = None
    stories_choice = None
    landscape_choice = None
    if post_status == "Create Post":
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

    elif post_status == "Edit Post":
        purpose = purpose_select(post_purposes, post_purposes.index(st.session_state.purpose))
        logger.debug(f"Selected purpose: {purpose}")

        platform = platform_select(platform_options, platform_options.index(st.session_state.platform))
        logger.debug(f"Selected platform: {platform}")

        persona = persona_select(personas, personas.index(st.session_state.persona))
        logger.debug(f"Selected persona: {persona}")

        tone = tone_select(post_tones, post_tones.index(st.session_state.tone))
        logger.debug(f"Selected tone: {tone}")

        verbosity = set_verbosity(st.session_state.verbosity)
        logger.debug(f"Selected verbosity: {verbosity}")

        details = post_details(st.session_state.post_details)
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
