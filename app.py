from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Access and Configure the API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
GENERATION_CONFIG = os.getenv("GENERATION_CONFIG")

st.set_page_config(page_title="Interview--- Me",
                   page_icon=":robot:",
                   initial_sidebar_state="expanded")

st.sidebar.title("User Information")
st.title("Interview Me :)")

@st.cache_resource
def get_gemini_response(prompt):
    # Model Configuration
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        safety_settings=safety_settings,
        generation_config=GENERATION_CONFIG,
    )

    #response = model.generate_content(prompt)
    #response_content = response.text
    #print(response_content)
    response_content = "Q1:XXX; A1:YYY; Q2:XXX; A2:YYY; Q3:XXX; A3:YYY"
    st.markdown(response_content) #response.text

    return response_content

# Sidebar
username = st.sidebar.text_input("Enter your username")
job_title = st.sidebar.text_input("Enter job title", placeholder="Software Engineer")
experience_level = st.sidebar.selectbox("Experience Level", ["Junior", "Mid", "Senior"])
topics = st.sidebar.text_area("Enter topics (e.g., Java, SpringBoot, MySQL)", placeholder="Java, SpringBoot, Backend")
start_interview = st.sidebar.button("Start Interview")

# Main Page
# When user clicks on the "Start Interview" button
isEmpty = not username or not job_title or not experience_level or not topics
if start_interview and not isEmpty:
    st.write(f"Hello, {username}! Let's start your interview for a {experience_level} level {job_title } position. Topics selected: {topics}")
    st.write("Generating your interview questions...")

    questions = ["What is polymorphism in Java?", 
                "How does Spring Boot handle dependency injection?", 
                "What is a primary key in MySQL?"]
    
    ai_answers = ["Polymorphism in Java is a concept by which we can perform a single action in different ways. It is one of the four pillars of Object-Oriented Programming (OOP).", 
                "Spring Boot handles dependency injection by using the @Autowired annotation to inject dependencies into a Spring Bean.", 
                "A primary key in MySQL is a unique identifier for each row in a table. It ensures that each row is uniquely identified and can be used to enforce data integrity."]

    for i, question in enumerate(questions, start=1):
        st.subheader(f"Question {i}: {question}")
        user_answer = st.text_area(f"Your Answer for Question {i}", key=f"answer_{i}")
        send_answer = st.button(f"Send Answer for Question {i}", key=f"send_{i}")
        show_your_score = st.button(f"Show Your Score for Question {i}", key=f"score_{i}")
        user_scores = [3, 1, 5]

        print("KOD BURDAMA 85 . SATIR")


        # Placeholder for user responses
        if f"user_response_{i}" not in st.session_state:
            print("KOD BURDAMA 85 . SATIR 1")

            st.session_state[f"user_response_{i}"] = None

        if send_answer:
            print("KOD BURDAMA 85 . SATIR 2")
            st.session_state[f"user_response_{i}"] = user_answer
        
        if st.session_state[f"user_response_{i}"]:
            st.write(f"Your Answer: {st.session_state[f'user_response_{i}']}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Show AI Response for Question {i}", key=f"ai_response_{i}"):
                    st.write(f"AI Response: {ai_answers[i - 1]}")
            with col2:
                if st.button(f"Show Your Score for Question {i}", key=f"score_{i}"):
                    st.write(f"Your Score: {user_scores[i - 1]}")

        if user_answer:
            st.write(f"User Answer for Question {i}: {user_answer}")
            show_ai_response = st.button(f"Show AI Response for Question {i}", key=f"ai_response_{i}")
            st.write(f"Your Answer: {user_answer}")

            #Enables buttons
            if show_ai_response: 
                ai_response = get_gemini_response(question)
                st.write(f"AI Response: {ai_response}")

            if show_your_score:
                # Placeholder for scoring logic
                st.write("Your Score: [Score Placeholder]")
elif start_interview and isEmpty:
    st.warning('Please fill in all the fields to start the interview.', icon="⚠️")

prompt = "Create interview questions at most 3."
model = genai.GenerativeModel(model_name="gemini-1.5-flash-lates")
#user_prompt=st.text_input("Please enter the job title you are applying for", key='message')

def generate_response(prompt):
    #response = genai.language.create(prompt, model="text-interview-questions")
    #response = model.generate_content(prompt, max_tokens=200)
    response = "Dummy response"
    return response

#if st.button("Get Questions"):
#    response = generate_response(user_prompt)
#    #if(response): st.write(response) kontrolü eklenebilir
#    st.write(response)
