import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

# Configure the API key for Google Generative AI
genai.configure(api_key="AIzaSyAW7LpbQSJJDQv4t_leWEJEu4LorMvtgsk")

# Define the prompt template
prompt_template = """You are an AI content writer. Your task is to take the transcript from this YouTube video and convert it into an amazing, super-structured article. The article should be engaging, well-organized, and highlight the key points in a way that's easy for readers to understand. Here is the transcript: """

# Function to fetch YouTube transcript
def fetch_youtube_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([entry['text'] for entry in transcript_list])
        return transcript
    except NoTranscriptFound:
        return None

# Function to generate the article from the YouTube transcript
def generate_article_from_transcript(transcript, prompt_template):
    prompt = prompt_template + transcript
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Streamlit app title
st.title("YouTube Video to Article Converter")

# Input field for the YouTube video link
youtube_link = st.text_input("Enter YouTube Video Link:")

# Display the YouTube video thumbnail if a link is provided
if youtube_link:
    video_id = youtube_link.split("v=")[1].split("&")[0]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

# Button to generate the article from the video
if st.button("Generate Article"):
    with st.spinner("Generating the article..."):
        # Fetch the transcript from the video
        transcript = fetch_youtube_transcript(video_id)
        if transcript:
            # Generate the article summary from the transcript
            article = generate_article_from_transcript(transcript, prompt_template)
            st.markdown("## Generated Article:")
            st.write(article)
        else:
            st.error("Sorry, no transcript found for this video.")
