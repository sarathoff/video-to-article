import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()  # Load all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are a YouTube video summarizer. You will watch the YouTube video 
and summarize the entire content into a more engaging article or blog post, 
highlighting the key points. Please provide the summary for the following video link: """

## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(youtube_video_url, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + youtube_video_url)
    return response.text

st.title("YouTube Video to Article Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Article"):
    with st.spinner("Generating the article..."):
        summary = generate_gemini_content(youtube_link, prompt)
    st.markdown("## Article Summary:")
    st.write(summary)
