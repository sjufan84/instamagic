""" Helper utils for post related functions """
import logging
import json
from pydantic import BaseModel, Field
from openai import OpenAIError
import streamlit as st
from dependencies import get_openai_client

# Create the OpenAI client
client = get_openai_client()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if "current_model" not in st.session_state:
    st.session_state.current_model = "gpt-3.5-turbo-1106"
if "model_selection" not in st.session_state:
    st.session_state.model_selection = "GPT-3.5"

logger.debug(f"Current model: {st.session_state.current_model}")

class ImagePostResponse(BaseModel):
    """ Image Post Response Model """
    post: str = Field(..., title="post", description="The generated post text.")
    hashtags: str = Field(..., title="hashtags", description="The generated hashtags.")
    image_prompt: str = Field(..., title="image_prompt", description="The prompt used to generate the image.")

class TextPostResponse(BaseModel):
    """ Text Post Response Model """
    post: str = Field(..., title="post", description="The generated post text.")
    hashtags: str = Field(..., title="hashtags", description="The generated hashtags.")

initial_message = [
    {
        "role" : "system", "content" : """You are a helpful assistant helping a user optimize and
        create posts for Instagram.The goal is to help the user generate amazing posts based on their prompt
        and potentially an image that they have uploaded."""
    }
]


async def get_messages(post_option: str, prompt: str):
    """ Get the messages for the post option """
    messages = []
    if post_option == "with_image":
        messages = [
            {
                "role": "system",
                "content": f"""The user would like for you to generate an Instagram post optimized
                for engagement and virality based on the prompt {prompt} they have given.
                Your response should be returned as a JSON object in the following format:

                post: str = The post to be generated.
                hashtags: List[str] = The hashtags to be generated.
                image_prompt: str = An image prompt to send to dall-e for generation based on the user prompt.
                Should be photo-realistic and life-like as possible.

                Ensure that the post is presented in a clear and organized manner
                and that it adheres to the {ImagePostResponse} schema as outlined above."""
            },
            {
                "role" : "system", "content" : """Example Response:\n
                {
                    "post": "This is the post that was generated.",
                    "hashtags": ["hashtag1", "hashtag2", "hashtag3"],
                    "image_prompt": "This is the image prompt that was generated."
                }"""
            }
        ]

        total_messages = initial_message + messages

    elif post_option == "no_image":
        messages = [
            {
                "role": "system", "content": f"""The user would like
                for you to generate an Instagram post optimized
                for engagement and virality based on the prompt {prompt} they have given.
                Your response should be returned as a JSON object in the following format:

                post: str = The post to be generated.
                hashtags: List[str] = The hashtags to be generated.

                Ensure that the post is presented in a clear and organized manner
                and that it adheres to the {TextPostResponse} schema as outlined above."""
            },
            {
                "role": "system", "content": """Example Response:\n
                {
                    "post": "This is the post text that was generated.",
                    "hashtags": ["hashtag1", "hashtag2", "hashtag3"]
                }"""
            }
        ]

        total_messages = initial_message + messages

    logger.debug(f"Total messages: {total_messages}")

    return total_messages


async def create_post(post_type: str, prompt: str):
    """ Generate a post based on a user prompt"""
    messages = await get_messages(post_type, prompt)
    i = 0
    max_retries = 3
    while i < max_retries:
        try:
            logger.debug(f"Trying model: {st.session_state.current_model}")
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=messages,
                temperature=0.75,
                top_p=1,
                max_tokens=750,
                response_format={"type": "json_object"}
            )
            post_response = json.loads(response.choices[0].message.content)
            logger.debug(f"Response: {post_response}")
            logger.debug(f"Response type: {type(post_response)}")
            return {
                "post": post_response["post"], "hashtags": post_response["hashtags"],
                "image_prompt": post_response["image_prompt"] if "image_prompt" in post_response else None
            }

        except OpenAIError as e:
            logger.error(f"Error with model: {st.session_state.current_model}. Error: {e}")
            i += 1

    logger.warning("All models failed. Returning None.")
    return None

async def alter_image(prompt: str, image_url: str):
    """ Generate a new dall-e prompt based on the user prompt and the image """
    messages = [
        {
            "role": "system", "content": [
                {
                    "type" : "text", "text" : f"""The user has uploaded an
                    image and a prompt {prompt} that they
                    would like to convert into a viral Instagram post. Based on the prompt and the image,
                    create an image prompt for dall-e that takes the original image and
                    optimizes it for maxiumum engagement on Instagram.  You only need to
                    focus on the new image prompt for
                    dall-e.  Only return the prompt for dall-e to use to generate the new, optimized image."""
                }
            ]
        },
        {
            "role" : "system", "content" : [
                {
                    "type" : "text", "text" : "This is the image that was passed to you:"
                },
                {
                    "type" : "image_url", "image_url" : f"data:image/jpeg;base64,{image_url}"
                }
            ]
        }
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=250,
        )
        logger.debug(f"Response: {response}")
        prompt_response = response.choices[0].message.content
        logger.debug(f"Prompt response: {prompt_response}")
        return prompt_response
    except OpenAIError as e:
        logger.error(f"Error generating prompt for image alteration: {e}")
        return None
