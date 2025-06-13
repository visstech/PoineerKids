import streamlit as st
from streamlit_ace import st_ace
import io
import sys
import random
import math
import datetime

# ✅ MUST be first Streamlit command
st.set_page_config(page_title="Codey Python Playground", layout="wide")

# Now it's safe to use other Streamlit functions
st.markdown("<p style='font-size:12px; color:gray;'>Developed by Vi.S.Senthilkumar</p>", unsafe_allow_html=True)

avatar = st.sidebar.selectbox("Choose your avatar", ["🐍 Python", "🤖 Robot", "🐱 Cat", "🐼 Panda"])

avatar_dict = {
    "🐍 Python": "https://img.icons8.com/color/96/python.png",
    "🤖 Robot": "https://img.icons8.com/color/96/robot-2.png",
    "🐱 Cat": "https://img.icons8.com/color/96/cat.png",
    "🐼 Panda": "https://img.icons8.com/color/96/panda.png"
}

st.sidebar.image(avatar_dict[avatar], width=80)

st.image("https://media.giphy.com/media/KAq5w47R9rmTuvWOWa/giphy.gif", width=100)

st.title("🐍 Codey: Python Learning Playground for Kids")
st.markdown("<p style='font-size:16px; color:red;'>Developed by Vi.S.Senthilkumar</p>", unsafe_allow_html=True)



# --- Challenges ---
challenges = {
    "Print your name": {
        "description": "Write code that prints your name.",
        "starter_code": "# Type your code below to print your name\nname = 'YourName'\nprint('Hello', name)",
        "solution": "name = 'Alice'\nprint('Hello', name)"
    },
    "Number check": {
        "description": "Check if a number is 1 and print a message.",
        "starter_code": "Num = 1\nif Num == 1:\n    print('Welcome to Codey!')\nelse:\n    print('Try again!')",
        "solution": "Num = 1\nif Num == 1:\n    print('Welcome to Codey!')\nelse:\n    print('Try again!')"
    },
    "Simple loop": {
        "description": "Print numbers from 1 to 5 using a loop.",
        "starter_code": "# Use a for loop to print numbers 1 to 5\nfor i in range(1, 6):\n    print(i)",
        "solution": "for i in range(1, 6):\n    print(i)"
    }
}

# Sidebar for selecting challenge
st.sidebar.header("Select Challenge")
selected_challenge = st.sidebar.selectbox("Choose a challenge", list(challenges.keys()))

challenge_data = challenges[selected_challenge]
st.sidebar.markdown(f"### Challenge Description:\n{challenge_data['description']}")

# Sidebar to simulate inputs for kids if needed
st.sidebar.header("Input Simulator")
num_input = st.sidebar.number_input("Enter a number (Num):", min_value=0, max_value=100, step=1, value=1)
name_input = st.sidebar.text_input("Enter your name:", value="Alice")

# Load or initialize user code from session state for persistence
if "user_code" not in st.session_state:
    st.session_state.user_code = challenge_data["starter_code"]

# If challenge changes, reset code
if st.session_state.get("last_challenge") != selected_challenge:
    st.session_state.user_code = challenge_data["starter_code"]
    st.session_state.last_challenge = selected_challenge

# Code editor with syntax highlighting (no debounce argument)
code = st_ace(
    value=st.session_state.user_code,
    language='python',
    theme='chrome',
    keybinding='vscode',
    font_size=20,
    tab_size=4,
    show_gutter=True,
    wrap=True,
    auto_update=True,
    min_lines=10,
    key='ace'
)

# Save current code to session_state to keep it between reruns
st.session_state.user_code = code

# Buttons for Run and Show Solution
col1, col2 = st.columns(2)
with col1:
    run_pressed = st.button("▶️ Run Code")
with col2:
    show_solution_pressed = st.button("👀 Show Solution")

# Show solution
if show_solution_pressed:
    st.info("Solution:")
    st.code(challenge_data["solution"], language="python")

# Run code and capture output if run button pressed
if run_pressed:
    buffer = io.StringIO()
    sys.stdout = buffer

    try:
        # Build safe environment with simulated inputs
        SAFE_GLOBALS = {
            "__builtins__": {
                "print": print,
                "range": range,
                "len": len,
                "int": int,
                "str": str,
                "float": float,
                "bool": bool,
                "list": list,
                "dict": dict,
                "set": set,
                "tuple": tuple,
                "enumerate": enumerate,
                "zip": zip,
                "min": min,
                "max": max,
                "abs": abs,
                "sum": sum,
                "type":type,
            },
            "Num": num_input,
            "name": name_input,
            "random": random,
            "math": math,
            "datetime":datetime
        }
        exec(code, SAFE_GLOBALS)
        sys.stdout = sys.__stdout__
        output = buffer.getvalue()
        st.success("✅ Output:")
        st.code(output, language='python')
    except Exception as e:       
        # Friendly error message for kids
        st.error(f"Oops! There was a problem with your code: {e}")
        st.info("Try checking your spelling, punctuation, and indentation. Keep going—you'll get it!")

        sys.stdout = sys.__stdout__
        st.error(f"❌ Error: {e}")

# --- Simple Chatbot Assistant ---
st.sidebar.header("🤖 Codey Assistant")

question = st.sidebar.text_area("Ask me a Python question:", height=100)
if st.sidebar.button("Ask"):
    q = question.strip().lower()
    if "print" in q:
        answer = "The print() function outputs text or variables to the screen."
    elif "loop" in q:
        answer = "A loop repeats code multiple times. For example, 'for i in range(5):' runs 5 times."
    elif "variable" in q:
        answer = "A variable stores data. Example: x = 5 assigns 5 to variable x."
    elif "input" in q:
        answer = "In this app, input() is simulated via the sidebar input boxes."
    else:
        answer = "Sorry, I don't understand that question yet. Try asking about print, loops, or variables."
    st.sidebar.markdown(f"**Answer:** {answer}")

# --- Progress Tracking (Basic) ---
st.sidebar.header("📂 Progress Tracker")

# Store completed challenges in session_state
if "completed" not in st.session_state:
    st.session_state.completed = set()

if run_pressed:
    if output.strip():
        st.session_state.completed.add(selected_challenge)

st.sidebar.markdown("### Completed Challenges:")
for c in challenges.keys():
    mark = "✅" if c in st.session_state.completed else "❌"
    st.sidebar.markdown(f"{mark} {c}")
