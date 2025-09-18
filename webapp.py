import google.generativeai as genai
import os
import streamlit as st
from pdfextractor import text_extractor_pdf
from docx_extractor import text_extractor_docx
from imageextractor import extract_text_image

# Configure Genai Model
key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key = key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# Upload file in sidebar
user_text = None
st.sidebar.title(':orange[Upload you MoM notes here:]')
st.sidebar.subheader(':blue[Upload only Images, PDFs or Docx files]')
user_file = st.sidebar.file_uploader('Upload your file', type=['pdf', 'docx', 'png', 'jpg', 'jpeg'])
if user_file:
    if user_file.type == 'application/pdf':
        user_text = text_extractor_pdf(user_file)
    elif user_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        user_text = text_extractor_docx(user_file)
    elif user_file.type in ['image/jpeg', 'image/png']:
        user_text = extract_text_image(user_file)
    else:
        st.sidebar.error('Upload Correct file format')

# Main Page
st.title(':blue[Minutes of Meeting]: :green[AI Assisted MoM generator in a standardized form]')
tips = '''Tips to use this app:
* Upload your meeting in sidebar (Image, ODF or DOCX)
* Click on the generate MoM and get the standardized MoMs'''
st.write(tips)

if st.button('Generate MoM'):
    if user_text is None:
        st.error('Text is not Generated')
    else:
        with st.spinner('Processing your data...'):
            prompt = f'''Assume you are expert in creating minutes of meeting. User has provided 
            notes of a meeting in text format. Using this data you need to create a standardized minutes
            minutes of meeting for the user.

            Keep the format strictly as mentioned below
            Title : Title of Meeting
            Heading : Meeting Agenda
            Subheading : Name of Attendees(Keep it None if this is not provided)
            Subheading : Date of Meeting and venue of meeting()
            Body : The body must follow following sequence of points
            * Key points discussed
            * Highligh any Decision that has been finalised.
            * Mention Actionable items.
            * Any additional Notes.
            * Any deadlines that has been discussed.
            * Any next meeting date that has been discussed.
            * 2-3 line summary.
            * Use bullet points and highlight or bold important keywords such that context is clear.
            * Generate the output in such a format that it can be copied and pasted in word to create pdf
            
            The data provided by user is as follows {user_text}'''

            response = model.generate_content(prompt)
            st.write(response.text)

            st.download_button(label='Click to Download',
                               data = response.text,
                               file_name='MoM.txt',
                               mime = 'text/plain')
