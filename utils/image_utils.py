import logging
import base64
import io
from pydantic import BaseModel, Field
import streamlit as st
from openai import OpenAIError
from dependencies import get_openai_client
from PIL import Image

# Create the OpenAI client
client = get_openai_client()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if "image" not in st.session_state:
    st.session_state["image"] = None
if "size_choice" not in st.session_state:
    st.session_state["size_choice"] = "1024x1024"

# Decode Base64 JSON to Image
def decode_image(image_data, image_name):
    """ Decode the image data from the given image request. """
    logger.debug(f"Decoding image: {image_data}")
    # Decode the image
    image_bytes = base64.b64decode(image_data)
    # Convert the bytes to an image
    image = Image.open(io.BytesIO(image_bytes))
    # Save the image
    image.save(image_name)
    return image

class ImageRequest(BaseModel):
    """ Image Request Model """
    prompt: str = Field(..., title="Prompt", description="The prompt to generate an image from.")

async def generate_image(prompt : str):
    """ Generate an image from the given image request. """
    logger.debug(f"Generating image for prompt: {prompt}")
    # Generate the image
    try:
        response = client.images.generate(
            prompt=prompt,
            model="dall-e-3",
            size=f"{st.session_state['size_choice']}",
            quality="standard",
            n=1,
            response_format="b64_json"
        )
        for i in range(len(response.data)):
            logger.debug(f"Image {i}: {response.data[i].b64_json}")
            image = decode_image(response.data[i].b64_json, f"image{i}.png")

        st.session_state["image"] = image
        logger.debug(f"Session state image: {st.session_state['image']}")
        return image

    except OpenAIError as e:
        logger.error(f"Error generating image: {e}")
        return {"error": str(e)}
