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

async def generate_post(
        purpose: str, persona: str = None, tone: str = None, platform: str = None, verbosity: int = 3,
        details: str = None):
    logger.debug(f"Generating post with purpose:\
    {purpose}, persona: {persona}, tone: {tone},\
    platform: {platform}, verbosity: {verbosity}, details: {details}")
    messages = [
        {
            "role": "system", "content": f"""
            You are a social media expert helping the user generate posts for
            just general content based on their parameters.  Optimize the content based on the purpose
            {purpose} of their post, the platform {platform} they are posting on (if any),
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

async def alter_image(
        image_url: str, post: str, prompt: str, platform: str = None,
        image_style: str = "Photorealistic"):
    """ Generate a new dall-e prompt based on the user prompt and the image """
    st.session_state.vision_status = "used"
    if image_style == "Photorealistic":
        messages = [
            {
                "role": "system", "content": [
                    {
                        "type": "text",
                        "text": f"""Based on the social media post {post} created from the input
                        {prompt} for {platform}, and using the provided image, generate a DALL-E
                        prompt for a highly realistic photo. Focus on capturing essential elements
                        such as the setting (e.g., hotel, restaurant), the main subject (e.g., food, travel),
                        and the post's tone (e.g., fun, serious) to enhance relevance and engagement.
                        Consider photographic details like scene composition, lighting, and perspective
                        to guide the image generation.  Include
                        specific photo settings, such as lens, aperture,
                        shutter speed, ISO, and any other relevant
                        details that would help the AI generate the most
                        hyper-photo-realistic photo possible. Aim for realism and context alignment without
                        including hands or text. Summarize this into a concise prompt for
                        creating an engaging, hyper-realistic photographic image."""
                    }
                ]
            },
            {
                "role" : "system", "content" : [
                    {
                        "type" : "text", "text" : "This is the image that was passed to you:"
                    },
                    {
                        "type" : "image_url", "image_url" : f"""data:image/jpeg;base64,
                        {st.session_state.user_image_string}"""
                    }
                ]
            },
        ]
    else:
        messages = [
            {
                "role": "system", "content": [
                    {
                        "type": "text",
                        "text": f"""Given a social media post {post} and its context {prompt}
                        for a specified platform {platform}, as well as the attached image,
                        create a DALL-E prompt for generating
                        an image in the style of {image_style} that maximizes engagement.
                        Consider the post's content,
                        target audience, and platform specifics to identify key visual elements.
                        Synthesize this analysis into a concise DALL-E prompt aimed at producing
                        an engaging and contextually appropriate image."""
                    }
                ]
            },
            {
                "role" : "system", "content" : [
                    {
                        "type" : "text", "text" : "This is the image that was passed to you:"
                    },
                    {
                        "type" : "image_url", "image_url" : f"""data:image/jpeg;base64,
                        {st.session_state.user_image_string}"""
                    }
                ]
            }
        ]

    try:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=500,
        )
        logger.debug(f"Response: {response}")
        prompt_response = response.choices[0].message.content
        logger.debug(f"Prompt response: {prompt_response}")
        st.session_state.vision_prompt = prompt_response
        return prompt_response
    except OpenAIError as e:
        logger.error(f"Error generating prompt for image alteration: {e}")
        return None


async def get_image_prompt(post: str, prompt: str, platform: str = None, image_style: str = "Photorealistic"):
    if image_style == "Photorealistic":
        messages = [
            {
                "role": "system",
                "content": f"""Given a social media post {post} and its context {prompt}
                for a specified platform {platform}, create a DALL-E prompt for generating
                a highly realistic image that maximizes engagement. Consider the post's content,
                target audience, and platform specifics to identify key visual elements.
                Detail essential photographic aspects to guide the image generation, focusing
                on attributes that enhance realism and relevance, such as scene composition, lighting,
                and perspective. Include
                specific photo settings, such as lens, aperture,
                shutter speed, ISO, and any other relevant
                details that would help the AI generate the most
                hyper-photo-realistic photo possible.Avoid including
                hands or text in the image. Synthesize this
                analysis into a concise DALL-E prompt aimed at producing
                an engaging and contextually appropriate image."""
            }
        ]
    else:
        messages = [
            {
                "role": "system",
                "content": f"""Given a social media post {post} and its context {prompt}
                for a specified platform {platform}, create a DALL-E prompt for generating
                an image in the style of {image_style} that maximizes engagement. Consider the post's content,
                target audience, and platform specifics to identify key visual elements.
                Synthesize this analysis into a concise DALL-E prompt aimed at producing
                an engaging and contextually appropriate image."""
            }
        ]
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            max_tokens=500,
        )
        logger.debug(f"Response: {response}")
        prompt_response = response.choices[0].message.content
        logger.debug(f"Prompt response: {prompt_response}")
        return prompt_response
    except OpenAIError as e:
        logger.error(f"Error generating prompt for image generation: {e}")
        return None

def edit_post(post: str, requested_adjustments: str):
    """ Edit a post based on user feedback """
    messages = [
        {
            "role": "system", "content": f"""
            You are a helpful assistant helping the user edit their social media post.  The user has
            requested the following adjustments: {requested_adjustments}.  The original post is:
            {post}.  Return the edited post with the requested adjustments."""
        },
    ]
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            max_tokens=500,
        )
        logger.debug(f"Response: {response}")
        return response.choices[0].message.content
    except OpenAIError as e:
        logger.error(f"Error editing post: {e}")
        return None

async def get_new_image_prompt(original_prompt: str, original_image: str, requested_adjustments: str):
    """ Generate a new dall-e prompt based on the user prompt and the image """
    messages = [
        {
            "role": "system", "content": [
                {
                    "type": "text",
                    "text": f"""
                    Given the original DALL-E prompt {original_prompt} and the original image,
                    create a new DALL-E prompt for generating an image that incorporates the
                    requested adjustments {requested_adjustments}.  The original image is:
                    """
                },
            ]
        },
        {
            "role" : "system", "content" : [
                {
                    "type" : "text", "text" : "This is the original image that was generated:"
                },
                {
                    "type" : "image_url", "image_url" : f"""data:image/jpeg;base64,
                    {st.session_state.user_image_string}"""
                }
            ]
        }
    ]
    try:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=500,
        )
        logger.debug(f"Response: {response}")
        return response.choices[0].message.content
    except OpenAIError as e:
        logger.error(f"Error generating prompt for image alteration: {e}")
        return None
