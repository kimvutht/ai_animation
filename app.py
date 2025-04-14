import streamlit as st
import requests
import mimetypes
import os

st.title("🖼️ Animation: Image-to-Video")

# API inputs
api_key = st.text_input("API Key", type="password")
api_url = st.text_input("API URL")

# Image upload
uploaded_file = st.file_uploader("Upload a .jpg or .png image", type=["jpg", "jpeg", "png"])

# Prompt and parameters
prompt = st.text_area("Prompt", value="The boy gently strums the guitar while his fingers shift along the fretboard. His hair moves subtly in the breeze. Leaves sway in the background trees, and clouds drift slowly across the sky. A soft parallax effect creates depth between the boy, the guitar, and the distant foliage. Light shifts naturally with a warm outdoor ambiance.")
num_frames = st.number_input("Number of frames", min_value=1, value=33)
fps = st.number_input("FPS", min_value=1, value=16)
height = st.number_input("Height", min_value=64, value=512)
width = st.number_input("Width", min_value=64, value=512)

if st.button("Generate Video"):
    if not (api_key and api_url and uploaded_file):
        st.warning("Please provide API Key, URL, and upload an image.")
    else:
        # Guess MIME type
        mime_type, _ = mimetypes.guess_type(uploaded_file.name)
        if mime_type is None:
            st.error("Unsupported image format. Please use .jpg or .png.")
        else:
            params = {
                "prompt": prompt,
                "num_frames": num_frames,
                "fps": fps,
                "height": height,
                "width": width
            }
            headers = {
                "Authorization": f"Bearer {api_key}"
            }

            files = {
                "image": (uploaded_file.name, uploaded_file, mime_type)
            }

            with st.spinner("Generating video..."):
                response = requests.post(api_url, headers=headers, data=params, files=files)

                if response.status_code == 200:
                    output_path = "output_video.mp4"
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    st.success("✅ Video generated successfully!")
                    with open(output_path, "rb") as f:
                        st.download_button("Download Video", f, file_name="output_video.mp4")
                else:
                    st.error(f"❌ Error {response.status_code}")
                    try:
                        st.json(response.json())
                    except:
                        st.text(response.text)
