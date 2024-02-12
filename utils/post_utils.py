""" Helper utils for post generation """
from dependencies import get_openai_client
import logging
import streamlit as st
from openai import OpenAIError

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = get_openai_client()

if "current_post" not in st.session_state:
    st.session_state.current_post = None

def generate_post(
        purpose: str, persona: str = None, tone: str = None, platform: str = None, verbosity: int = 3,
        details: str = None):
    messages = [
        {
            "role": "system", "content": f"""
            You are a helpful assistant helping the user generate posts for their social media or
            just general content based on their parameters.  Optimize the content based on the purpose
            {purpose} of their post?, the platform {platform} they are posting on (if any),
            the persona {persona} they would like to embody (if any),
            and the tone {tone} they would like to convey (if any).
            On a scale of 1 to 5, their desired verbosity level is {verbosity}.  The details
            of the post they would like to generate are {details}.  Return only the post content
            and the appropriate hashtags.  Do not add any intro or outro to the post."""
        },
    ]

    message_placeholder = st.empty()
    full_response = ""
    if st.session_state.current_post is None:
        try:
            completion = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                stream=True,
            )
            for chunk in completion:
                if chunk.choices[0].finish_reason == "stop":
                    logging.debug("Received 'stop' signal from response.")
                    break
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.current_post = full_response
        except OpenAIError as e:
            logger.error(f"Error generating post: {e}")
            st.error(f"Error generating post: {e}")
    else:
        st.write(st.session_state.current_post)
        st.session_state.current_post = None