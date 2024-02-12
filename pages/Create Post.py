import streamlit as st
from typing import List
import logging
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.switch_page_button import switch_page

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Purpose options list
post_purposes = [
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
    "Other"
]

personas = [
    "The Adventurer - loves to explore new places and try new things",
    "The Foodie - passionate about all things culinary",
    "The Bookworm - always has their nose in a book",
    "The Fitness Guru - dedicated to a healthy lifestyle and fitness",
    "The Fashionista - always on top of the latest trends",
    "The Tech Enthusiast - fascinated by the latest gadgets and technology",
    "The Artist - sees the world through a creative lens",
    "The Comedian - finds humor in everyday situations",
    "The Philosopher - loves to ponder and discuss life's big questions",
    "The Environmentalist - committed to sustainability and protecting the planet",
    "The Musician - lives and breathes music",
    "The Historian - fascinated by history and how it shapes our world",
    "The Scientist - driven by curiosity and a love for discovery",
    "The Activist - passionate about social causes and making a difference",
    "The Entrepreneur - always looking for the next big idea",
    "The Mentor - loves to share knowledge and help others grow",
    "The Storyteller - has a knack for captivating narratives",
    "The Traveler - always planning their next adventure",
    "The Wellness Advocate - focuses on mental and emotional well-being",
    "The DIY Enthusiast - loves tackling projects and building things",
    "The Gamer - lives for the thrill of the game",
    "The Movie Buff - a connoisseur of films and television series",
    "The Pet Lover - dedicated to their furry (or scaly) friends",
    "The Home Chef - finds joy in cooking and baking",
    "The Gardener - has a green thumb and loves being in nature",
    "The Collector - passionate about their collection, be it art, stamps, or anything else",
    "The Volunteer - spends their time helping others and giving back",
    "The Parent - shares the joys and challenges of parenting",
    "The Student - on a journey of learning and discovery",
    "The Professional - focused on career and professional development",
    "Other",
    None
]

platform_options = [
    "Instagram",
    "Facebook",
    "Twitter",
    "LinkedIn",
    "Pinterest",
    "TikTok",
    "Snapchat",
    "YouTube",
    None
]

def purpose_select(purpose_options: List[str]):
    """ Purpose Selection """
    purpose = st.selectbox("What is the purpose of your post?  (Select 'Other' if\
    you do not find the appropriate option')", purpose_options)
    return purpose

def other_purpose():
    """ Other Purpose option if use selects "Other" """
    other_purpose = st.text_input("Please specify the purpose of your post")
    return other_purpose

def persona_select(persona_options: List[str]):
    """ Persona Selection """
    persona = st.selectbox("What persona would you like to embody for this post?  You can also\
    select 'Other' or 'None'.", persona_options)
    return persona

def other_persona():
    """ Other Persona option if use selects "Other" """
    other_persona = st.text_input("Please specify the persona you would like to embody")
    return other_persona

def platform_select(platform_options: List[str]):
    """ Platform Selection """
    platform = st.selectbox("Which platform are you posting on, if any?", platform_options)
    return platform

def create_post_home():
    purpose = purpose_select(post_purposes)
    if purpose == "Other":
        purpose = other_purpose()
    logger.debug(f"Selected purpose: {purpose}")
    platform = platform_select(platform_options)
    logger.debug(f"Selected platform: {platform}")
    persona = persona_select(personas)
    if persona == "Other":
        persona = other_persona()
    logger.debug(f"Selected persona: {persona}")
    
create_post_home()
