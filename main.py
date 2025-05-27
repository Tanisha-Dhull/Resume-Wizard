import streamlit as st 
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv



st.set_page_config(page_title="AI resume critqer", page_icon="✌️", layout="centered")
load_dotenv( )

st.markdown(
    """
    <style>
    body {
        background-color: #ffe6fa !important;
    }
    .stApp {
        background: linear-gradient(135deg, #ffe6fa 0%, #ffe0e9 100%);
        color: #5e2660;
        font-family: 'Segoe UI', 'Arial', sans-serif;
    }
    .st-bb {
        background-color: #f9dafb !important;
        color: #bc3c91 !important;
    }
    label, .st-cm, .st-cs, .st-cz, .css-145kmo2, .stFileUploader label, .stTextInput label {
    color: #d72660 !important;  /* Use any pink you like */
    font-weight: bold;
}

    .stButton>button {
        color: white;
        background: linear-gradient(90deg,#f857a6,#ff5858);
        border-radius: 20px;
        border: none;
        font-weight: bold;
        padding: 10px 24px;
        font-size: 18px;
        margin-top: 10px;
        transition: background 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #ff5858, #f857a6);
        color: #fff;
        box-shadow: 0 0 10px #ff99cc;
    }
    /* Custom title */
    h1 {
        color: #d72660 !important;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        text-shadow: 2px 2px 5px #ffb3de66;
    }
    /* Custom subheader */
    .stMarkdown h3 {
        color: #bc3c91;
    }
    /* File uploader area */
    .css-1lcbmhc {
        background-color: #f9dafb !important;
        border: 2px dashed #bc3c91 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



st.title("Resume Wizard")
st.markdown ("Upload your resume and let the Resume Wizard work its magic with AI-powered feedback. ")

OPENAI_API_KEY = os.getenv("OPEN_API_KEY")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "txt"])

job_role = st.text_input("Enter the job role ")

analyze = st.button("Analyze Resume ")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = " "
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
        return text


def extract_text_from_file(uploaded_file):
    if uploaded_file.type =="application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")
    


if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("File doesn't have any content")
            st.stop()
        
        prompt = f""" please analyze this resume and provide constructive feedback .
        Focus on the following aspects:
        1. Content clarity ad impact 
        2. Skils presentation 
        3. Experience descriptions
        4. Specific improvemnets for {job_role if job_role else 'general job application '}
        Resume content:
        {file_content}
        please provide your analysis in a clear , structed format with specific recommadtions for certicates , courses from different websites """

        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-instruct",

            messages=[
                {"role": "system", "content":" You are an expert resume reviwer with years of experience in HR and recruitment."},
                {"role" : "user" , "content" : prompt }], 
            temperature = 0.07,
            max_tokens=500
            )
        st.markdown("### Analysis Results")
        st.markdown(response.choice[0].message.content)

    except Exception as e :
        st.error(f"An error occured:{str(e)}")