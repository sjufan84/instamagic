import logging
import base64
import io
import streamlit as st
from pydantic import BaseModel, Field
from openai import OpenAIError
from dependencies import get_openai_client
from PIL import Image

# Create the OpenAI client
client = get_openai_client()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Decode Base64 JSON to Image
def decode_image(image_data, image_name):
    """ Decode the image data from the given image request. """
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

def create_image(prompt : str, size_choice : str):
    """ Generate an image from the given image request. """
    logger.debug(f"Generating image for prompt: {prompt} with size: {size_choice}")
    # Generate the image
    if size_choice == "Square":
        size = "1024x1024"
    elif size_choice == "Stories":
        size = "1024x1792"
    try:
        response = client.images.generate(
            prompt=prompt,
            model="dall-e-3",
            size=size,
            quality="standard",
            n=1,
            style="vivid",
            response_format="b64_json"
        )
        decoded_image = decode_image(image_data=response.data[0].b64_json, image_name="image.png")

        return decoded_image

    except OpenAIError as e:
        logger.error(f"Error generating image: {e}")
        return {"error": str(e)}

def heic_to_base64(heic_path):
    # Read HEIC file
    heif_file = Image.open(heic_path)

    # Convert to RGB
    img = heif_file.convert("RGB")

    # Create an in-memory file object
    buffer = io.BytesIO()

    # Save the image to the in-memory file object
    img.save(buffer, format="JPEG")

    # Encode to Base64
    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return img_base64

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

def image_options():
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
        st.text("")
