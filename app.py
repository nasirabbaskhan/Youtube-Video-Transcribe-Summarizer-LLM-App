import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai # type: ignore
from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


prompt = """You are Youtube video summarizer. You will be tacking the transcript text and summarizing
the entire video and providing the important summary inpoints within 250 words. 
Please provide the summery of the text given here:
"""
def generate_gemini_response(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([transcript_text+prompt])
    return response.text


## getting the transcript data from yb videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        
        transcript = ""
        for i in transcript_text:
            transcript+= " " + i["text"]
            
        return transcript
    except Exception as e:
        raise e
    
    
# streamlit app
st.set_page_config(page_title="YB videos Transcrpter")
st.title("Youtube Transcript to Detailed Notes Converter")

youtube_video_link = st.text_input("Enter Your Youtube video Link:")

if youtube_video_link:
    # to show the video themnel
    video_id = youtube_video_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True) 
    
    
if st.button("Get detailed Notes"):
    transcript_text = extract_transcript_details(youtube_video_link)
    if transcript_text:
        summary = generate_gemini_response(transcript_text,prompt)
        
        st.subheader("Detailed Notes::")
        st.write(summary)
        
    
