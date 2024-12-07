from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Access and Configure the API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Interview--- Me",
                   page_icon=":robot:",
                   initial_sidebar_state="expanded")

st.sidebar.title("User Information")
st.title("Interview Me :)")

@st.cache_resource
def get_gemini_response(prompt):
    # Model Configuration
    generation_config={
        "temperature": 1, 
        "top_p": 0.95, 
        "top_k": 40, 
        "max_output_tokens": 18192, 
        "response_mime_type": "text/plain"
        }

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
        generation_config=generation_config,
    )

    #response = model.generate_content(prompt)
    #response_content = response.text
    #print(response_content)

    questions = ["What is polymorphism in Java?", 
                "How does Spring Boot handle dependency injection?", 
                "What is a primary key in MySQL?"]
    
    ai_answers = ["Polymorphism in Java is a concept by which we can perform a single action in different ways. It is one of the four pillars of Object-Oriented Programming (OOP).", 
                "Spring Boot handles dependency injection by using the @Autowired annotation to inject dependencies into a Spring Bean.", 
                "A primary key in MySQL is a unique identifier for each row in a table. It ensures that each row is uniquely identified and can be used to enforce data integrity."]


    return questions, ai_answers


def get_user_score(user_answers, size):
    placeholder_value = 0
    score = [placeholder_value] * size
    score[1] = 5
    score[0] = 2
    return score

# Sidebar
username = st.sidebar.text_input("Enter your username")
job_title = st.sidebar.text_input("Enter job title", placeholder="Software Engineer")
experience_level = st.sidebar.selectbox("Experience Level", ["Junior", "Mid", "Senior"])
topics = st.sidebar.text_area("Enter topics (e.g., Java, SpringBoot, MySQL)", placeholder="Java, SpringBoot, Backend")
start_interview = st.sidebar.button("Start Interview")

# Ensure session state for form handling
#if 'submitted' not in st.session_state:
#    st.session_state['submitted'] = False
#if 'user_answers' not in st.session_state:
#    st.session_state['user_answers'] = {}

# Ensure session state for questions and user answers
if 'questions' not in st.session_state:
    st.session_state['questions'] = []
if 'user_answers' not in st.session_state:
    st.session_state['user_answers'] = {}
if 'ai_answers' not in st.session_state:
    st.session_state['ai_answers'] = []
# Main Page
# When user clicks on the "Start Interview" button
isEmpty = not username or not job_title or not experience_level or not topics
if start_interview and not isEmpty:
    st.write(f"Hello, {username}! Let's start your interview for a {experience_level} level {job_title } position. Topics selected: {topics}")
    st.write("Generating your interview questions...")
   
    # Generate questions and store them in session state
    questions, ai_answers = get_gemini_response(topics)
    st.session_state['questions'] = questions
    st.session_state['user_answers'] = {}
    st.session_state['ai_answers'] = ai_answers

elif start_interview and isEmpty:
    st.warning('Please fill in all the fields to start the interview.', icon="⚠️")

print("if else dışında.")
print("Questions in state: ", st.session_state['questions'])
# Post-submission actions
#if st.session_state['submitted']:
#    st.write("Form submitted successfully! 🚀")
#    st.write("Here are your answers:")
#    for i, (question, answer) in enumerate(st.session_state['user_answers'].items(), start=1):
#        st.subheader(f"Question {i}: {question}")
#        st.write(f"Your Answer: {answer}")

# Display questions and form if questions exist
if st.session_state['questions']:
    form = st.form(key='questions_form')
    form.write("Please provide your answers to the questions below.")
    user_answers = st.session_state['user_answers']
    ai_answers = st.session_state['ai_answers']
    for i, question in enumerate(st.session_state['questions']):
        form.write(f"Question {i + 1}: {question}")
        user_answers[question] = form.text_input(label="Answer", 
                                                 label_visibility="collapsed", 
                                                 placeholder=f"Your Answer to Question {i+1}", 
                                                 key=f"answer_{i}")
    
     # Handle form submission
    submitted = form.form_submit_button('Submit')
    print("user_answers in state:", st.session_state['user_answers'])
    print("user_answers in form:", user_answers)

    if submitted:
        st.write("Form submitted successfully! 🚀")
        st.write("Here are your answers:")
        ai_answers = st.session_state['ai_answers']
        user_score = get_user_score(user_answers, len(ai_answers))

        for i, (question, answer) in enumerate(user_answers.items(), start=1):
            #st.subheader(f"Question {i}: {question}")
            st.write(f"Your Answer: {answer}")
            st.write(f"AI Answer: {ai_answers[i-1]}")
            st.write(f"Score: {user_score[i-1]}")
        
        submitted = False

prompt = "Create interview questions at most 3."
model = genai.GenerativeModel(model_name="gemini-1.5-flash-lates")
#user_prompt=st.text_input("Please enter the job title you are applying for", key='message')
