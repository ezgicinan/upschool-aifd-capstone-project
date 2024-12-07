from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit as st
import json

# Load environment variables from .env file
load_dotenv()

# Access and Configure the API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Interview--- Me",
                   page_icon=":robot:",
                   initial_sidebar_state="expanded")

st.sidebar.title("ℹ️ User Information")
st.title("Interview Me :) ✨")

def parse_score_response(response_text):
    start_index = response_text.find('[')
    end_index = response_text.rfind(']') + 1
    trimmed_text = response_text[start_index:end_index]

    char_list = list(trimmed_text)
    char_list.pop(0)
    char_list.pop(len(char_list)-1)

    modified_response = "".join(char_list)
    splittedScoreList = modified_response.split(",")

    scoreList = []
    for element in splittedScoreList:
        convertedScore = int(element)
        scoreList.append(convertedScore)

    return scoreList


def parse_interview_response(response_text):
    try:
        start_index = response_text.find('{')
        end_index = response_text.rfind('}') + 1
        json_str = response_text[start_index:end_index]
        
        #Parse JSON
        parsedData = json.loads(json_str)
            
        # Separate questions and answers
        questions = {key: value for key, value in parsedData.items() if key.startswith("Q")}
        answers = {key: value for key, value in parsedData.items() if key.startswith("A")}

        return questions, answers
    
    except json.JSONDecodeError as e:
        print(f"JSON read error: {str(e)}")
        return None
    except KeyError as e:
        print(f"Missing data error: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None
    
@st.cache_resource
def generate_score_response(user_answers):
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
        system_instruction="You’re an engineer from a software team.",
    )
    print("-------------------")
    print("Generating score response...")

    prompt = generate_rating_prompt(user_answers=user_answers)
    response = model.generate_content(prompt)
    response_content = response.text

    score_response = parse_score_response(response_content)
    return score_response

@st.cache_resource
def get_gemini_response(level, position_name, topics):
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
        system_instruction="You’re an engineer from a software team.",
    )

    prompt = generate_prompt(level=level, position_name=position_name, topics=topics)
    response = model.generate_content(prompt)
    response_content = response.text

    # Parse the response
    questions, ai_answers = parse_interview_response(response_content) or ({}, {})

    return questions, ai_answers

def generate_prompt(level, position_name, topics):
    prompt = (
        f"Generate common technical interview questions for a {level} "
        f"{position_name} position and suggest brief answers. "
        f"Questions must be about {topics}. Create 4 questions and their answers. "
        "Create a JSON response like expected answer below:\n"
        "{\n\"Q1\": \"What is the difference between == and .equals() in Java?\","
        "\n\"A1\": \"The difference is...\","
        "\n\"Q2\": \"In spring...\","
        "\n\"A2\": \"Springboot...\","
        "\n\"Q3\": \"Jvm vs...\","
        "\n\"A3\": \"library..\"\n}"
    )
    return prompt

def generate_rating_prompt(user_answers):
    prompt = (
        f"Rate the following answers on a scale of 0 to 5 (0 being the lowest and 5 being the highest). Keys are questions and values are answers to be rated: \n"
        f"{user_answers}\n"
        "Expected response: [1, 3, 5, 4]\n"
        "Give me just your answer as expected list of scores for each answer, no explanation no comments."
    )
    return prompt

# Sidebar
username = st.sidebar.text_input("Enter your username")
job_title = st.sidebar.text_input("Enter job title", placeholder="Software Engineer")
experience_level = st.sidebar.selectbox("Experience Level", ["Junior", "Mid", "Senior"])
topics = st.sidebar.text_area("Enter topics (e.g., Java, SpringBoot, MySQL)", placeholder="Java, SpringBoot, Backend")
start_interview = st.sidebar.button("Start Interview")


# Ensure session state for form handling
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

# Ensure session state for questions and user answers
if 'questions' not in st.session_state:
    st.session_state['questions'] = {}
if 'user_answers' not in st.session_state:
    st.session_state['user_answers'] = {}
if 'ai_answers' not in st.session_state:
    st.session_state['ai_answers'] = {}


# Main Page
# When user clicks on the "Start Interview" button

isEmpty = not username or not job_title or not experience_level or not topics
if start_interview and not isEmpty:
    print("----------START APP---------------------")
    # Clear cache to force a fresh call to the API (before generating new data)
    st.cache_resource.clear()  # Clear any cached resources like external API calls

    # Reset the session state to ensure fresh data
    st.session_state['questions'] = {}
    st.session_state['user_answers'] = {}
    st.session_state['ai_answers'] = {}
    st.session_state['submitted'] = False

    st.write(f"Hello, {username}! Let's start your interview for a {experience_level} level {job_title } position. Topics selected: {topics}")
    st.write("Generating your interview questions...")
    
    # Generate questions and ai answers and store them in session state
    questions, ai_answers = get_gemini_response(level=experience_level, position_name=job_title, topics=topics) or ({}, {})
    

    # Check if questions or ai_answers are empty
    if not questions or not ai_answers:
        st.warning("Gemini has some issues while generating data. Please start the interview again.", icon="⚠️")
        st.stop()
    else:
        st.session_state['questions'] = questions
        st.session_state['user_answers'] = {}
        st.session_state['ai_answers'] = ai_answers
        st.session_state['submitted'] = False
elif start_interview and isEmpty:
    st.warning('Please fill in all the fields to start the interview.', icon="⚠️")

print("-----------------------------------------")
print("START INTERVIEW PRESSED AND QUESTIONS GENERATED.")
print("-----------------------------------------")


# Display questions and form if questions exist
if st.session_state['questions'] and not st.session_state['submitted']:
    print("Question exist and not submitter")
    form = st.form(key='questions_form', clear_on_submit=True)
    form.write("Please provide your answers to the questions below.")
    user_answers = st.session_state['user_answers']
    ai_answers = st.session_state['ai_answers']

    for key, question in st.session_state['questions'].items():
        form.write(f"{key}: {question}")
        user_answers[question] = form.text_input(
            label="Answer",
            label_visibility="collapsed",
            placeholder=f"Your Answer to {key}",
            key=f"answer_{key}")
    
    # Handle form submission
    submitted = form.form_submit_button('Submit')
    print("USER-ANSWERS in state: ", st.session_state['user_answers'])
    print("USER_ANSWERS in form:", user_answers)
    print("-----------------------------------------")

    if submitted:
        st.session_state['submitted'] = True
        st.write("Form submitted successfully! 🚀  Here are your answers:")
        ai_answers = st.session_state['ai_answers']

        user_score = generate_score_response(user_answers)

        for i, (question, answer) in enumerate(user_answers.items(), start=1):
            ai_key = f"A{i}"
            ai_answer = ai_answers.get(ai_key, "No AI answer available")

            st.markdown(f"**Your Answer to #Q{i}:** {answer}")
            st.markdown(f"**AI's Answer:** {ai_answer}")
            st.markdown(f"**Score:** 🌟 {user_score[i-1]}/5")
            st.divider()  # Adds a thin line to separate sections

        st.session_state['questions'] = {}
        st.session_state['user_answers'] = {}
        st.session_state['ai_answers'] = {}
        st.session_state['submitted'] = False
        
print("-----------------------------------------")
print(" st.session_state['questions']=",  st.session_state['questions'])
print(" st.session_state['submitted']=",  st.session_state['submitted'])
print("st.session_state['user_answers']=", st.session_state['user_answers'])
print("st.session_state['ai_answers']=", st.session_state['ai_answers'])