import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Grade Calculator",
    page_icon="🎓",
    layout="centered",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- Page ---------- */

    .stApp {
        background-color: #f6f8fb;
    }

    .block-container {
        max-width: 650px;
        padding-top: 45px;
        padding-bottom: 40px;
    }


    /* ---------- Header ---------- */

    .app-title {
        text-align: center;
        font-size: 42px;
        font-weight: 750;
        color: #172033;
        margin-bottom: 8px;
    }

    .app-subtitle {
        text-align: center;
        font-size: 18px;
        color: #667085;
        margin-bottom: 40px;
    }


    /* ---------- Input label ---------- */

    .input-label {
        font-size: 20px;
        font-weight: 700;
        color: #172033;
        margin-bottom: 8px;
    }


    /* ---------- Result card ---------- */

    .result-card {
        background-color: #ffffff;
        border: 1px solid #e1e6ed;
        border-radius: 16px;
        padding: 30px;
        margin-top: 28px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
    }

    .result-label {
        font-size: 17px;
        color: #667085;
        margin-bottom: 10px;
    }

    .grade {
        font-size: 82px;
        font-weight: 800;
        line-height: 1;
        color: #2563eb;
    }

    .result-message {
        font-size: 20px;
        font-weight: 650;
        color: #172033;
        margin-top: 18px;
    }

    .result-score {
        font-size: 16px;
        color: #667085;
        margin-top: 8px;
    }


    /* ---------- Grading scale ---------- */

    .scale-title {
        font-size: 20px;
        font-weight: 700;
        color: #172033;
        margin-top: 32px;
        margin-bottom: 12px;
    }


    /* ---------- Button ---------- */

    .stButton > button {
        height: 48px;
        border-radius: 10px;
        font-size: 17px;
        font-weight: 650;
    }


    /* ---------- Footer ---------- */

    .footer {
        text-align: center;
        color: #98a2b3;
        font-size: 14px;
        margin-top: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# FUNCTIONS
# =========================================================

def calculate_grade(mark: int) -> str:
    """Calculate the letter grade for a mark between 0 and 100."""

    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "E"


def get_grade_message(grade: str) -> str:
    """Return a friendly message for the calculated grade."""

    messages = {
        "A": "Excellent performance! 🎉",
        "B": "Great job! Keep it up! 👏",
        "C": "Good effort! Keep improving. 👍",
        "D": "You passed. Keep working to improve. 📚",
        "E": "Keep practicing. You can do better! 💪",
    }

    return messages[grade]


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="app-title">🎓 Grade Calculator</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="app-subtitle">'
    'Enter your mark between 0 and 100 to calculate your grade.'
    '</div>',
    unsafe_allow_html=True,
)


# =========================================================
# INPUT
# =========================================================

st.markdown(
    '<div class="input-label">Enter Your Mark</div>',
    unsafe_allow_html=True,
)

mark = st.number_input(
    "Mark",
    min_value=0,
    max_value=100,
    value=0,
    step=1,
    format="%d",
    label_visibility="collapsed",
)

st.progress(
    mark / 100,
    text=f"{mark} / 100",
)

calculate = st.button(
    "Calculate Grade",
    type="primary",
    use_container_width=True,
)


# =========================================================
# RESULT
# =========================================================

if calculate:

    grade = calculate_grade(mark)
    message = get_grade_message(grade)

    st.markdown(
        f"""
<div class="result-card">
    <div class="result-label">Your Grade</div>
    <div class="grade">{grade}</div>
    <div class="result-message">{message}</div>
    <div class="result-score">Mark: <strong>{mark}</strong> / 100</div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Additional status message
    if grade == "A":
        st.success("Outstanding result!")

    elif grade == "B":
        st.success("Very good result!")

    elif grade == "C":
        st.info("Good result. Keep improving!")

    elif grade == "D":
        st.warning("You passed. Focus on improving your score.")

    else:
        st.error("Below the passing range. Keep practicing!")


# =========================================================
# GRADING SCALE
# =========================================================

st.markdown(
    '<div class="scale-title">Grading Scale</div>',
    unsafe_allow_html=True,
)

grading_scale = {
    "Mark Range": [
        "90 – 100",
        "80 – 89",
        "70 – 79",
        "60 – 69",
        "0 – 59",
    ],
    "Grade": [
        "A",
        "B",
        "C",
        "D",
        "E",
    ],
}

st.table(grading_scale)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">Grade Calculator</div>',
    unsafe_allow_html=True,
)
