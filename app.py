import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""

You have to act like a very high skilled or very experienced ATS(Application tracking System) with very deep understanding of tech field, software Engineering, DevOps Engineering, Full stack Egineering and overall Engineering related knowledge.
Your task and responsibilites are to extract key information from job description like job title, company, responsibilities, qualifications, skills, and required experience. Preprocess the text by removing stop words, converting to lowercase, and lemmatization.
And also extract relevant information like work experience, education, skills, and achievements from resume preprocess the text similarly to the job description.
You must consider the job market is very competitive and you should provide best assistance for improving the resumes so job description can match the resume and it will improve the ATS score.
Assign the percentage Matching based on Jd and the missing keywords with high accuracy and what things need to improve in resume to get shortlisted.
Generate insights and recommendations on how to tailor the resume to better align with the job description requirements so that ATS score will imporve.
consider below some questions and show result according with above context also.
How prevalent is this skill/keyword in the provided resume compared to similar resumes for the same job title?
Suggest ways to improve the resume to highlight this skill/keyword.
How well does the overall experience, skills, and achievements described in the resume match the requirements outlined in the job description?

resume:{text}
description:{jd}

I want the response in string having the below structure
{{"JD Match":"%",
"MissingKeywords:[]",
"Profile Summary":"",
"Improvement Suggestions ":"",
"Score improvement after changes ":"%"}}
"""

## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt)
        st.subheader(response)