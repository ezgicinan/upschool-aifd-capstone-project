from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit

# Load environment variables from .env file
load_dotenv()

# Access the Gemini API Key
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
GENERATION_CONFIG = os.getenv("GENERATION_CONFIG")

genai.configure(api_key=GOOGLE_API_KEY)
prompt = "Create interview questions at most 3."

#You’re an engineer from a software team. Generate common technical
#interview questions for a senior software developer position and
#suggest strong brief answers. Questions must be about Java, Java Core, Spring boot, backend and create 3 questions for each topic. Give answers as Json key-value like 
#"Java Core": [{"Q1": "1. What is the difference between == and .equals() in Java?", "A1":"Answer..."}, {"Q2":"...","A2":"...."}],
#"Spring Boot Question":[{"Q1":"...", "A1":"..."}]

''' 
chat_session = model.start_chat(
        history=[{
            "role": "user",
            "parts": [files_toBeUpload[0], files_toBeUpload[1]]}])
'''

# response = chat_session.send_message(prompt)
# print("RESPONSE: ", response)
# JSON parse
#analysis = response.text
#print("ANALYSIS: ", analysis)
