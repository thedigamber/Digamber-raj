import requests
import io
from PIL import Image
import base64
import time
import uuid
import streamlit as st

# --- Hugging Face Image Generation Function with Retry ---
def generate_image_huggingface(prompt, width, height, style="Realistic", retries=3):
    try:
        # Access the API token from secrets
        api_token = st.secrets["huggingface"]["api_token"]
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

        # Map styles to Hugging Face models
        style_map = {
            "Anime": "nitrosocke/waifu-diffusion",
            "Realistic": "CompVis/stable-diffusion-v1-4",
            "Sci-Fi": "CompVis/stable-diffusion-v1-4",
            "Pixel": "nitrosocke/pixel-art-diffusion",
            "Fantasy": "nitrosocke/fantasy-diffusion",
            "Ghibli": "nitrosocke/Ghibli-Diffusion"
        }

        model = style_map.get(style, "CompVis/stable-diffusion-v1-4")

        data = {
            "inputs": prompt,
            "options": {
                "width": width,
                "height": height
            }
        }
        response = requests.post(f"https://api-inference.huggingface.co/models/{model}", headers=headers, json=data)
        response.raise_for_status()
        
        img_data = response.content
        img = Image.open(io.BytesIO(img_data))
        img_path = f"generated_image_{uuid.uuid4().hex}.png"
        img.save(img_path)
        
        return img_path
    except Exception as e:
        if retries > 0:
            st.warning(f"Image transformation failed: {str(e)}. Retrying...")
            time.sleep(5)  # Wait for 5 seconds before retrying
            return generate_image_huggingface(prompt, width, height, style, retries - 1)
        else:
            st.error(f"Image transformation failed after multiple retries: {str(e)}")
            return None

# --- Image Transformation Function ---
def transform_image(image, prompt, style="Ghibli", width=512, height=512):
    return generate_image_huggingface(prompt=prompt, width=width, height=height, style=style)

# --- Function to Parse User Input ---
def parse_user_input(user_input):
    style_keywords = ["Ghibli", "Anime", "Cyberpunk", "Pixar", "Realistic", "Fantasy", "Sci-Fi", "Pixel"]
    resolution_keywords = ["512x512", "768x768", "1024x1024"]
    
    style = "Realistic"
    resolution = "512x512"
    
    for word in user_input.split():
        if word in style_keywords:
            style = word
        if word in resolution_keywords:
            resolution = word
    
    return style, resolution
