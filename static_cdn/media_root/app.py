#import libraries needed
from fastapi import (
    FastAPI,
    UploadFile,
    File,
    status,
    Request
)
from fastapi.responses import JSONResponse
from typing import Optional
from fastapi.staticfiles import StaticFiles

import aiofiles
import random
import requests
from dotenv import load_dotenv
import os
# import shutil
import uuid
from pathlib import Path
from tempfile import NamedTemporaryFile
import os
import fitz
from io import StringIO
from nltk.tokenize import sent_tokenize
import json
import nltk
import cohere
from gtts import gTTS

# nltk.download('punkt')

#initialize FastAPI server
app = FastAPI()

# Constant Variables and keys for APIs
load_dotenv()
cohere_secret_key = os.environ.get("CO_SECRET_KEY")
co = cohere.Client(cohere_secret_key)

"""
Functions
"""
# Save file
def gen_name(fileinput):
    path = fileinput
    print(path)
    index = path.find(".")
    f_ext = path[index+1:]
    tan = random.randint(100, 10684)
    outfile = str("Scribble2speak" + str(tan))# + f_ext)
    return f"{outfile}.{f_ext}"
 
def gen_fname():
    tan = random.randint(100, 10684)
    outfile = str("Scribble2speak" + str(tan))
    return f"{outfile}"

# Extract Data from PDF
def read_pdf(filename):
  context = ""
  
  # Open the PDF file
  with fitz.open(filename) as pdf_file:
  
    # Get the number of pages in the PDF file
    num_pages = pdf_file.page_count
    
    # Loop through each page in the PDF file
    for page_num in range(num_pages):
      
      # Get the current page
      page = pdf_file[page_num]
      
      # Get the text from the current page
      page_text = page.get_text()
      
      # Append the text to context
      context += page_text
  return context


# Split Data in PDF
def split_text(text, chunk_size=5000):
  """
  Splits the given text into chunks of approximately the specified chunk size.
  
  Args:
  text (str): The text to split.
  
  chunk_size (int): The desired size of each chunk (in characters).
  
  Returns:
  List[str]: A list of chunks, each of approximately the specified chunk size.
  """
  
  chunks = []
  current_chunk = StringIO()
  current_size = 0
  sentences = sent_tokenize(text)
  for sentence in sentences:
    sentence_size = len(sentence)
    if sentence_size > chunk_size:
      while sentence_size > chunk_size:
        chunk = sentence[:chunk_size]
        chunks.append(chunk)
        sentence = sentence[chunk_size:]
        sentence_size -= chunk_size
        current_chunk = StringIO()
        current_size = 0
    if current_size + sentence_size < chunk_size:
      current_chunk.write(sentence)
      current_size += sentence_size
    else:
      chunks.append(current_chunk.getvalue())
      current_chunk = StringIO()
      current_chunk.write(sentence)
      current_size = sentence_size
  if current_chunk:
     chunks.append(current_chunk.getvalue())
#   print(chunks)
  return chunks


# Summarize data with AI
"""
model - command or command-lite. Generally, lite models are faster while larger models will perform better.
temperature - This parameter ranges from 1 to 5, and controls the randomness of the output. Higher values tend to generate more creative outcomes, and gives you the opportunity of generating various summaries for the same input text. It also might include more hallucinations, and it might make the model less likely to ground its replies in the context you've provided when using retrieval augmented generation. Use a higher value if for example you plan to perform a selection of various summaries afterwards.
length - You can choose between short, medium and long. short summaries are roughly up to two sentences long, medium between three and five, and long might have more six or more sentences.
format - You can choose between paragraph and bullets. Paragraph generates a coherent sequence of sentences, while bullets outputs the summary in bullet points.
extractiveness - This parameter can be set at low, medium, high values.
"""

def ai_summrization(text):
    try:
        response = co.summarize(
        text=text,
        model='command',
        length='short',
        format="bullets",
        extractiveness='medium'
        )
        summary = response.summary
        print(summary,"\n")
        return summary
    except Exception:
       pass


def summrize(documnet):  
  # Calling the split function to split text
  chunks = split_text(documnet)
  
  summaries = []
  for chunk in chunks:
    summary = ai_summrization(chunk)
    summaries.append(summary)
  
  return summaries


# Pass summary to TTS AI
def text_to_speech(name, text, language='en'):
    tts = gTTS(text=text, lang=language, slow=False, tld="us")
    tts.save(f"static\{name}.mp3")
    return f"static/{name}.mp3"

"""
Routes
"""

# Define a sample route
@app.get("/")
async def welcome(q: Optional[str] = None):
    return {"message": "Hello, FastAPI!", "q":q}

#create route to upload pdf
@app.post("/upload")
async def upload(file: UploadFile, request: Request):
    async with aiofiles.open(file.filename, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
    r = file.filename
    #read the pdf file
    document = read_pdf(r)
    # Call the summrize function with the document as input
    result = summrize(document)
    fname = gen_fname()
    url = text_to_speech(fname, str(result))

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"url":f"{request.base_url}{url}"}
        )

app.mount("/static", StaticFiles(directory="static"), name="static")


#run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)