import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from io import BytesIO
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse
import os
import google.generativeai as genai
import dotenv

# Configuration for Google Gemini API
api_key = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key='AIzaSyCO7WIRmXTQUPeiARLTklKLufkZRfjfg4U')

# Function to convert YouTube link to a generalized video address link
def convert_to_video_address_link(input_link):
    parsed_url = urlparse(input_link)
    
    if parsed_url.netloc == 'www.youtube.com' and parsed_url.path == '/watch':
        return input_link
    elif parsed_url.netloc == 'youtu.be':
        video_id = parsed_url.path[1:]
        return f'https://www.youtube.com/watch?v={video_id}'
    else:
        return input_link

# Function to extract transcript details from YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e

# Function to generate content using Google Gemini
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Function to generate a PDF from text data
def generate_pdf(text_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    content = []

    styles = getSampleStyleSheet()
    heading_style = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        fontSize=14,
        spaceAfter=12,
    )
    subheading_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=10,
    )
    normal_style = styles["BodyText"]
    bold_style = ParagraphStyle(
        'Bold',
        parent=normal_style,
        fontName='Helvetica-Bold',
    )

    paragraphs = text_data.split("\n")

    for paragraph in paragraphs:
        if paragraph.startswith("# "):
            content.append(Paragraph(paragraph[2:], heading_style))
        elif paragraph.startswith("## "):
            content.append(Paragraph(paragraph[3:], subheading_style))
        elif paragraph.startswith("### "):
            content.append(Paragraph(paragraph[4:], subheading_style))
        elif "**" in paragraph:
            parts = paragraph.split("**")
            for i, part in enumerate(parts):
                if i % 2 == 1:
                    content.append(Paragraph(part, bold_style))
                else:
                    content.append(Paragraph(part, normal_style))
        else:
            content.append(Paragraph(paragraph, normal_style))

    doc.build(content)

    buffer.seek(0)

    return buffer.getvalue()

# Streamlit app
st.title("Video to Article Converter")
st.write('developed by Gen AI tools')

# Input for YouTube video link
youtube_link = st.text_input("Enter YouTube Video Link:")

if st.button("Generate Article"):
    if youtube_link:
        # Convert and display video thumbnail
        generalised_link = convert_to_video_address_link(youtube_link)
        video_id = generalised_link.split("=")[1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
        
        try:
            # Extract transcript and generate article
            transcript_text = extract_transcript_details(generalised_link)
            if transcript_text:
                try:
                    # Update prompt for article generation
                    prompt = """
                    You are a highly talented article writer. Create an article with a headline like a professional writer or blogger using the transcription of the video.
                    """
                    article = generate_gemini_content(transcript_text, prompt)
                    
                    # Display the article
                    st.write(article)
                    
                    # Add Copy to Clipboard button
                    st.text_area("Article Content", article, height=500, key="article_text_area", disabled=True)
                    st.button("Copy to Clipboard", on_click=lambda: st.experimental_set_query_params(text=article))
                
                except Exception as err:
                    st.markdown("Error generating article. Please try again later.")
                
        except Exception as e:
            st.markdown("Error fetching transcript for the provided video.")
