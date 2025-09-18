import google.generativeai as genai
import cv2
from PIL import Image
import os
import numpy as np

def extract_text_image(image_path):
    file_bytes = np.asarray(bytearray(image_path.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    # Lets load and process the image
    #image = cv2.imread('notes1.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # convert BGR to RGB
    image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert BGR to greyscale
    _, image_bw = cv2.threshold(image_grey, 140,255, cv2.THRESH_BINARY) # to convert to black and white

    # The Image that cv2 gives is in numpy array format, we need to convert it to image object
    final_image = Image.fromarray(image_bw)

    # Configure Genai Model
    key = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key = key)
    model = genai.GenerativeModel('gemini-2.5-flash-lite')

    # Let's write prompt for OCR
    prompt = '''You act as an OCR application on the given image and extract the text from it.
            Give only the text as output, do not give any other explain or description. '''
    
    # Let's extract and return the text
    response = model.generate_content([prompt, final_image])
    output_text = response.text
    return output_text

