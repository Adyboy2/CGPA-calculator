import pandas as pd
import streamlit as st

st.set_page_config(page_title="CGPA Calculator", page_icon="🎓", layout="centered")

GRADE_POINTS = {
    "A": 10.0,
    "A-": 9.0,
    "B": 8.0,
    "B-": 7.0,
    "C": 6.0,
    "C-": 5.0,
    "D": 4.0,
    "E": 2.0,
    "NC": 0.0,
}
CREDIT_OPTIONS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 16, 20]

def four_one(courses):
    return pd.DataFrame(
        {
            "Course": courses,
            "Credits": [3] * len(courses),
            "Grade": ["A"] * len(courses),
        }
    )


PROFILES = {
    "Advay": {
        "cgpa": 8.87,
        "credits": 117,
        "four_one": four_one(["AI", "ML", "ASM", "MPC", "DOP"]),
    },
    "Anoushka": {
        "cgpa": 8.66,
        "credits": 117,
        "four_one": four_one(["AI", "ML", "ASM", "MPC", "TP", "LOP", "DOP"]),
    },
}
FOUR_TWO_COURSES = pd.DataFrame(
    {"Course": ["PS-2"], "Credits": [20], "Grade": ["A"]}
)


def calculator(prefix, courses_df, default_cgpa, default_credits, default_course_credits):
    """Render one semester calculator; returns (new_cgpa, total_credits)."""
    col1, col2 = st.columns(2)
    current_cgpa = col1.number_input(
        "Current CGPA",
        min_value=0.0,
        max_value=10.0,
        **({} if f"{prefix}_cgpa" in st.session_state else {"value": float(default_cgpa)}),
        step=0.01,
        format="%.2f",
        key=f"{prefix}_cgpa",
    )
    credits_done = col2.number_input(
        "Credits completed",
        min_value=0,
        **({} if f"{prefix}_credits" in st.session_state else {"value": int(default_credits)}),
        step=1,
        key=f"{prefix}_credits",
    )

    st.subheader("This semester's courses")
    st.caption(
        "Edit grades and credits using the dropdowns. Use the + row at the bottom "
        "to add a course; select a row and press Delete to remove it."
    )
    courses = st.data_editor(
        courses_df,
        num_rows="dynamic",
        width="stretch",
        hide_index=True,
        column_config={
            "Course": st.column_config.TextColumn("Course", required=True),
            "Credits": st.column_config.SelectboxColumn(
                "Credits",
                options=CREDIT_OPTIONS,
                required=True,
                default=default_course_credits,
            ),
            "Grade": st.column_config.SelectboxColumn(
                "Grade", options=list(GRADE_POINTS), required=True, default="A"
            ),
        },
        key=f"{prefix}_courses",
    )

    valid = courses.dropna(subset=["Credits", "Grade"])
    sem_credits = float(valid["Credits"].sum())
    sem_points = float((valid["Credits"] * valid["Grade"].map(GRADE_POINTS)).sum())

    sgpa = sem_points / sem_credits if sem_credits else 0.0
    total_credits = credits_done + sem_credits
    new_cgpa = (
        (current_cgpa * credits_done + sem_points) / total_credits if total_credits else 0.0
    )

    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("SGPA", f"{sgpa:.2f}")
    m2.metric("New CGPA", f"{new_cgpa:.2f}", delta=f"{new_cgpa - current_cgpa:+.2f}")
    m3.metric("Total credits", f"{total_credits:g}")
    return new_cgpa, total_credits


st.title("🎓 CGPA Calculator")

name = st.radio("Student", list(PROFILES), horizontal=True)
profile = PROFILES[name]
pid = name.lower()

tab41, tab42 = st.tabs(["4-1 CGPA", "4-2 / Graduation CGPA"])

with tab41:
    cgpa_41, credits_41 = calculator(
        f"{pid}_s41", profile["four_one"], profile["cgpa"], profile["credits"], 3
    )

with tab42:
    st.info("Starts from your 4-1 result. You can still edit these two fields.")
    p42 = f"{pid}_s42"
    seed = (round(cgpa_41, 2), int(credits_41))
    if st.session_state.get(f"{p42}_seed") != seed:  # 4-1 changed: refresh the start values
        st.session_state[f"{p42}_seed"] = seed
        st.session_state[f"{p42}_cgpa"], st.session_state[f"{p42}_credits"] = seed
    calculator(p42, FOUR_TWO_COURSES, seed[0], seed[1], 20)
