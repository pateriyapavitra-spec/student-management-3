import streamlit as st
import json
from pathlib import Path

DATABASE = "school_data.json"

# ---------------- Database ---------------- #

data = {"students": [], "teachers": []}

if Path(DATABASE).exists():
    with open(DATABASE, "r") as f:
        content = f.read()
        if content:
            data = json.loads(content)


def save():
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)


def valid_email(email):
    return "@" in email and "." in email


# ---------------- Page ---------------- #

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Management System")
st.markdown("---")

menu = st.sidebar.selectbox(
    "Choose Option",
    [
        "Dashboard",
        "Register Student",
        "Register Teacher",
        "Add Grades",
        "Student Details",
        "Teacher Details",
        "View Students",
        "View Teachers",
    ],
)

# ---------------- Dashboard ---------------- #

if menu == "Dashboard":

    c1, c2 = st.columns(2)

    c1.metric("Students", len(data["students"]))
    c2.metric("Teachers", len(data["teachers"]))

    st.success("Welcome to Student Management System")

# ---------------- Register Student ---------------- #

elif menu == "Register Student":

    st.header("👨‍🎓 Register Student")

    with st.form("student_form"):

        name = st.text_input("Student Name")

        age = st.number_input("Age", 1, 100)

        email = st.text_input("Email")

        roll = st.text_input("Roll Number")

        submit = st.form_submit_button("Register")

        if submit:

            if not valid_email(email):
                st.error("Invalid Email")

            elif any(s["roll_num"] == roll for s in data["students"]):
                st.warning("Student Already Exists")

            else:

                data["students"].append(
                    {
                        "name": name,
                        "age": age,
                        "email": email,
                        "roll_num": roll,
                        "grade": {},
                    }
                )

                save()

                st.success("Student Registered Successfully")

# ---------------- Register Teacher ---------------- #

elif menu == "Register Teacher":

    st.header("👩‍🏫 Register Teacher")

    with st.form("teacher_form"):

        name = st.text_input("Teacher Name")

        age = st.number_input("Age", 20, 100)

        email = st.text_input("Email")

        subject = st.text_input("Subject")

        emp = st.text_input("Employee ID")

        submit = st.form_submit_button("Register")

        if submit:

            if not valid_email(email):
                st.error("Invalid Email")

            elif any(t["empl_id"] == emp for t in data["teachers"]):
                st.warning("Teacher Already Exists")

            else:

                data["teachers"].append(
                    {
                        "name": name,
                        "age": age,
                        "email": email,
                        "empl_id": emp,
                        "subject": subject,
                    }
                )

                save()

                st.success("Teacher Registered Successfully")

# ---------------- Add Grades ---------------- #

elif menu == "Add Grades":

    st.header("📝 Add Student Grade")

    roll = st.text_input("Roll Number")

    subject = st.text_input("Subject")

    marks = st.number_input("Marks", 0.0, 100.0)

    if st.button("Add Grade"):

        found = False

        for s in data["students"]:

            if s["roll_num"] == roll:

                s["grade"][subject] = marks

                save()

                found = True

                st.success("Grade Added Successfully")

                break

        if not found:
            st.error("Student Not Found")

# ---------------- Student Details ---------------- #

elif menu == "Student Details":

    st.header("📊 Student Details")

    roll = st.text_input("Enter Roll Number")

    if st.button("Search Student"):

        found = False

        for s in data["students"]:

            if s["roll_num"] == roll:

                grades = s["grade"]

                avg = (
                    sum(grades.values()) / len(grades)
                    if grades
                    else 0
                )

                st.subheader(s["name"])

                st.write("**Age:**", s["age"])
                st.write("**Email:**", s["email"])
                st.write("**Roll Number:**", s["roll_num"])

                st.write("### Grades")

                if grades:
                    st.table(
                        {
                            "Subject": grades.keys(),
                            "Marks": grades.values(),
                        }
                    )
                else:
                    st.info("No Grades Available")

                st.success(f"Average Marks : {avg:.2f}")

                found = True

                break

        if not found:
            st.error("Student Not Found")

# ---------------- Teacher Details ---------------- #

elif menu == "Teacher Details":

    st.header("👩‍🏫 Teacher Details")

    emp = st.text_input("Employee ID")

    if st.button("Search Teacher"):

        found = False

        for t in data["teachers"]:

            if t["empl_id"] == emp:

                st.subheader(t["name"])

                st.write("Subject :", t["subject"])
                st.write("Email :", t["email"])
                st.write("Employee ID :", t["empl_id"])

                found = True

                break

        if not found:
            st.error("Teacher Not Found")

# ---------------- View Students ---------------- #

elif menu == "View Students":

    st.header("📋 All Students")

    if len(data["students"]) == 0:
        st.info("No Students Found")

    else:

        table = []

        for s in data["students"]:

            table.append(
                {
                    "Name": s["name"],
                    "Age": s["age"],
                    "Roll": s["roll_num"],
                    "Email": s["email"],
                }
            )

        st.dataframe(table, use_container_width=True)

# ---------------- View Teachers ---------------- #

elif menu == "View Teachers":

    st.header("📋 All Teachers")

    if len(data["teachers"]) == 0:
        st.info("No Teachers Found")

    else:

        table = []

        for t in data["teachers"]:

            table.append(
                {
                    "Name": t["name"],
                    "Subject": t["subject"],
                    "Employee ID": t["empl_id"],
                    "Email": t["email"],
                }
            )

        st.dataframe(table, use_container_width=True)