# AI Interview Assistant ✨

This project is an AI-powered interview assistant that generates and evaluates technical interview questions and answers. It leverages Google Gemini AI and Streamlit to provide an interactive interview experience.

This project idea has been on my mind for a while. The education program I attended, UP School AI First Developer program, encuraged me during this time to bring the idea into the world.
I successfully deployed its live version for the first time as a capstone project for AIFD program. 💃🆙

See project presentation [[Link]](https://docs.google.com/presentation/d/1_EYQUjhAnyn5pkf9DV9o1Hr80Y2xIfR6/edit?usp=drive_link&ouid=116767463502226715354&rtpof=true&sd=true)

## Features

- **Interactive UI**: Built with Streamlit for a user-friendly interface.
- **AI-Powered**: Utilizes Google Gemini AI for generating interview questions and evaluating answers.
- **Customizable**: Users can input their job title, experience level, and specific topics to tailor the interview questions.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/ezgicinan/upschool-aifd-capstone-project.git
    cd upschool-aifd-capstone-project
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate` or `.\.venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file and add your Gemini API key:
    ```plaintext
    GEMINI_API_KEY=your_gemini_api_key_here
    ```

## Usage

1. Run the Streamlit app:
    ```sh
    streamlit run ./app.py
    ```

2. Open your browser and go to `http://localhost:8501`.

3. Fill in your user information, job title, experience level, and topics in the sidebar.

4. Click "Start Interview" to begin the interview process.

## Configuration

The Streamlit server configuration is set in the `.streamlit/config.toml` file:
```toml
[server]
runOnSave = false
