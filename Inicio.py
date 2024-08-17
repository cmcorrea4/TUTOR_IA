import os
import streamlit as st
from PIL import Image
import PyPDF2
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter


st.title('Interfaz auditiva 👂')
#image = Image.open('Chat_pdf.png')
#st.image(image, width=350)
with st.sidebar:
   st.subheader("Este Agente, te ayudará a realizar algo de análisis sobre el PDF cargado")


pdfReader = PyPDF2.PdfReader(pdfFileObj)
pdf = st.file_uploader("Carga el archivo PDF", type="pdf")

   # extract the text
if pdf is not None:
      from langchain.text_splitter import CharacterTextSplitter
      pdf_reader = PdfReader(pdf)
      text = ""
      for page in pdf_reader.pages:
         text += page.extract_text()
