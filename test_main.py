import streamlit as st
import logging

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

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        return {
            'platform': platform,
            'persona': persona,
            'tone': tone,
            'verbosity': verbosity,
            'details': details,
            'purpose': purpose
        }

def main():
    st.title("Post Generator")

    current_values = {
        'platform': "Instagram",
        'persona': "None",
        'tone': "Casual",
        'verbosity': 3,
        'details': "",
        'purpose': "Other"
    }

    form_values = create_form(platform_options, personas, post_tones, post_purposes, current_values)

    if form_values:
        st.write(form_values)

if __name__ == "__main__":
    main()
