import streamlit as st
from utils import convert_to_video_address_link, extract_transcript_details, generate_gemini_content

# Update prompt for article generation
prompt = """
You are a highly talented article writer. Create an article with a headline like a professional writer or blogger using the transcription of the video.
"""

st.title("Video to Article Converter")
linkedin_profile_url = 'https://www.linkedin.com/in/devasheeshchopra?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app'
st.write(f"Developed by: [Dev Asheesh Chopra]({linkedin_profile_url})")
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
