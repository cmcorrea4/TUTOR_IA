import os
import streamlit as st
from PIL import Image
import PyPDF2
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from gtts import gTTS
import base64
import glob
import time
from streamlit_lottie import st_lottie
import json


st.title('Interfaz auditiva 👂')
#image = Image.open('Chat_pdf.png')
#st.image(image, width=350)
with st.sidebar:
   st.subheader("Este Agente, te ayudará a realizar algo de análisis sobre el PDF cargado")
with open('ani_audio.json') as source:
         animation=json.load(source)
st.lottie(animation,width =350)
#pdfReader = PyPDF2.PdfReader(pdfFileObj)
pdf = st.file_uploader("Carga el archivo PDF", type="pdf")

   # extract the text
if pdf is not None:
      from langchain.text_splitter import CharacterTextSplitter
      pdf_reader = PdfReader(pdf)
      text = ""
      for page in pdf_reader.pages:
         text += page.extract_text()


tld='com'
option_lang = st.selectbox(
    "Selecciona el lenguaje",
    ("Español", "English"))
if option_lang=="Español" :
    lg='es'
if option_lang=="English" :
    lg='en'

try:
    os.mkdir("temp")
except:
    pass

def text_to_speech(text, tld,lg):
    
    tts = gTTS(text,lang=lg) # tts = gTTS(text,'en', tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text


#display_output_text = st.checkbox("Verifica el texto")

if st.button("convertir a Audio"):
     result, output_text = text_to_speech(text, 'com',lg)#'tld
     audio_file = open(f"temp/{result}.mp3", "rb")
     audio_bytes = audio_file.read()
     st.markdown(f"## Tú audio:")
     st.audio(audio_bytes, format="audio/mp3", start_time=0)

     #if display_output_text:
     
     #st.write(f" {output_text}")
    
#if st.button("ElevenLAabs",key=2):
#     from elevenlabs import play
#     from elevenlabs.client import ElevenLabs
#     client = ElevenLabs(api_key="a71bb432d643bbf80986c0cf0970d91a", # Defaults to ELEVEN_API_KEY)
#     audio = client.generate(text=f" {output_text}",voice="Rachel",model="eleven_multilingual_v1")
#     audio_file = open(f"temp/{audio}.mp3", "rb")

     with open(f"temp/{result}.mp3", "rb") as f:
         data = f.read()

     def get_binary_file_downloader_html(bin_file, file_label='File'):
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
        return href
     st.markdown(get_binary_file_downloader_html("audio.mp3", file_label="Audio File"), unsafe_allow_html=True)

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)


remove_files(7)
