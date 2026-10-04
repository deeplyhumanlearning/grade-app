import streamlit as st

st.set_page_config(
    page_title="Student Grade Manager",
    page_icon="📊",
    layout="centered",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 900px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    .title {
        text-align: center;
        margin-bottom: 2rem;
    }

    .title h1 {
        margin-bottom: 0.25rem;
    }

    .title p {
        color: #6b7280;
        margin-top: 0;
    }

    div[data-testid="stMetric"] {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        background: #ffffff;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    div[data-testid="stMetricLabel"] {
        color: #6b7280;
    }

    div[data-testid="stForm"] {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.25rem;
        background: #fafafa;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="title">
        <h1>Student Grade Manager</h1>
        <p>Track student performance and class statistics</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if "students" not in st.session_state:
    st.session_state.students = []

if "student_name" not in st.session_state:
    st.session_state.student_name = ""

if "student_mark" not in st.session_state:
    st.session_state.student_mark = 0.0

if "form_error" not in st.session_state:
    st.session_state.form_error = ""


def get_grade(mark):
    if mark >= 90:
        return "A"
    if mark >= 80:
        return "B"
    if mark >= 70:
        return "C"
    if mark >= 60:
        return "D"
    return "E"


def add_student():
    name = st.session_state.student_name.strip()
    mark = st.session_state.student_mark

    if not name:
        st.session_state.form_error = "Please enter a student name."
        return

    st.session_state.students.append(
        {
            "Name": name,
            "Mark": mark,
            "Grade": get_grade(mark),
        }
    )

    st.session_state.student_name = ""
    st.session_state.student_mark = 0.0
    st.session_state.form_error = ""


with st.form("add_student"):
    col1, col2 = st.columns([2, 1])

    with col1:
        st.text_input(
            "Student Name",
            placeholder="Enter student name",
            key="student_name",
        )

    with col2:
        st.number_input(
            "Mark",
            min_value=0.0,
            max_value=100.0,
            step=1.0,
            key="student_mark",
        )

    st.form_submit_button(
        "Add Student",
        use_container_width=True,
        on_click=add_student,
    )

if st.session_state.form_error:
    st.error(st.session_state.form_error)

if st.session_state.students:
    st.subheader("Students")
    st.table(st.session_state.students)

    marks = [student["Mark"] for student in st.session_state.students]
    average = sum(marks) / len(marks)

    st.subheader("Class Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Average", f"{average:.1f}")

    with col2:
        st.metric("Highest", f"{max(marks):g}")

    with col3:
        st.metric("Lowest", f"{min(marks):g}")
