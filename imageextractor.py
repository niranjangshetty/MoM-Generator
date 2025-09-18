import google.generativeai as genai
import os
from pdfExtractor import text_extractor_pdf
import streamlit as st
from docxExtractor import text_extractor_docx
from imageExtractor import extract_text_image


#configure the model
key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')


# Upload file in sidebar

user_text = None
st.sidebar.title(':orange[Upload your MOM notes here : ]')
st.sidebar.subheader('Only Image, PDFs and docs file are allowed to upload')
user_file = st.sidebar.file_uploader("Upload your file", type =['pdf', 'jpg', 'docx', 'png', 'jpeg'])
if user_file:
    if user_file.type == 'application/pdf':

        user_text = text_extractor_pdf(user_file)
    elif user_file.type  == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        user_text = text_extractor_docx(user_file) 
        
    elif user_file.type in ['image/jpg', 'image/jpeg', 'image/png']:
        user_text = extract_text_image(user_file)
    else:
        st.sidebar.error('Upload correct file format')

# MAIN PAGE :

st.title(':blue["___MINUTES OF MEETING___"]\n :orange[*AI ASSISTED MOM GENERATOR IN A STANDARDIZED FORM FOR MEETING NOTES*]')
tips = '''TIPS TO USE THIS APP:
1. Upload your meeting in side bar (Image , PDF or DOCX)
2. Click on generate MOM and get the standardized MOM's'''
st.write(tips)


if st.button('Generate MOM'):
     if user_text is None:
          st.error('Some error Occured - Text is not generated')

     else:
          with st.spinner('Processing your Data, it might take few Seconds..........'):
               prompt = f'''Assume you are expert in Creating MINUTES OF MEETING. User has provided notes of meeting in text format .
               Using this data , you need to create a standardized minutes of Meetings for the user
            
               It should be so specific and consice so anybody can easily understand without any confusions
               Highlight bullet points in bolds

               SHow everyting in proper format. you can use docx or format. THis format should be as follows
               Output must follow word or docx format, strictly in the following manner
               Title - Title of meeting
               Heading : Meeting Agenda
               Subheading - Name of attendies (if attendees name is not there , then keep it NA)
               subheading - Date  of meeting and place of meeting(place means - name of conference/meeting room, if not provided then keep it online)
               Body : The body must follow the following sequence of points:
               * KEY POINTS DISCUSSED
               * HIGHLIGHT ANY DECISION THAT HAS BEEN FINALIZED
               * MENTION ACTIONABLE ITEMS 
               * ANY ADDITIONAL NOTES
               * ANY DEADLINE THAT HAS BEEN DISCUSSED
               * ANY NEXT MEETING DATE THAT HAS BEEN DISCUSSED
               * 2 to 3 line of summary
               * Use Bullet points and highlight or bold important keywords such as CONTEXT IS CLEAR 
               * Generate the output in such a way that it can be copied and pasted in word 

               data provided by user is as follows : {user_text} '''
  
               response = model.generate_content(prompt)
               st.write(response.text)
               

               st.download_button(label='Click to Download',
                                   data = response.text,
                                  file_name= 'MOM.txt',
                                   mime='text/plain' )
