import streamlit as st
from typing import List
import logging
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.switch_page_button import switch_page

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

post_tones = [
    "Happy - conveys joy and positivity",
    "Angry - expresses frustration or displeasure",
    "Confused - shows uncertainty or perplexity",
    "Professional - maintains a formal and business-like manner",
    "Optimistic - looks at the bright side and expects the best",
    "Pessimistic - tends to see the worst aspect of things or believe that the worst will happen",
    "Inspirational - motivates and uplifts the audience",
    "Sarcastic - uses irony to mock or convey contempt",
    "Humorous - light-hearted and funny",
    "Serious - no-nonsense and straightforward",
    "Informative - provides useful information and insights",
    "Casual - friendly and relaxed",
    "Excited - shows enthusiasm or eagerness",
    "Reflective - thoughtful, considering past experiences",
    "Critical - analyzing and judging rigorously or in detail",
    "Sympathetic - expresses understanding and compassion for others",
    "Mysterious - arouses curiosity or intrigue",
    "Romantic - pertaining to the feelings or notions of romance",
    "Nostalgic - longing for the past, or with a wistful affection for a period or place",
    "Motivational - encourages action or determination",
    "Grateful - shows appreciation or thankfulness",
    "Educational - aims to educate or instruct the reader",
    "Questioning - inquiring or probing, often reflects a desire for knowledge",
    "Conversational - simulates a personal dialogue or conversation",
    "Encouraging - gives support, confidence, or hope to the reader",
    "Empathetic - shows an ability to understand and share the feelings of others",
    "Skeptical - not easily convinced; having doubts or reservations",
    "Passionate - shows a strong belief or a powerful emotion",
    "Whimsical - playfully quaint or fanciful, especially in an appealing and amusing way",
    "Other",
    None
]

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

def tone_select(tone_options: List[str]):
    """ Tone Selection """
    tone = st.selectbox("What tone would you like to convey in your post?  (Select 'Other' if you do not find the appropriate option')", tone_options)
    return tone

def other_tone():
    """ Other Tone option if use selects "Other" """
    other_tone = st.text_input("Please specify the tone you would like to convey")
    return other_tone

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
    tone = tone_select(post_tones)
    if tone == "Other":
        tone = other_tone()
    logger.debug(f"Selected tone: {tone}")
    st.write(f"Your post will be tailored to the purpose of {purpose}, the persona of {persona}, and the tone of {tone}.")

create_post_home()
