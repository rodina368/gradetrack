"""
Student Grade Manager
----------------------
A simple command-line tool for teachers and teaching assistants to record
students, log grades per subject, and instantly see averages, letter grades,
and class performance summaries — all stored in a local SQLite database.

Run with: python main.py
"""

import database
import grades_utils


def print_header(title: str):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


def menu():
    print_header("STUDENT GRADE MANAGER")
    print("1. Add a new student")
    print("2. Add a grade for a student")
    print("3. View a student's report card")
    print("4. View all students")
    print("5. View class average (all subjects or one subject)")
    print("6. Delete a student")
    print("0. Exit")
    return input("\nChoose an option: ").strip()


def add_student_flow():
    print_header("Add New Student")
    name = input("Student name: ").strip()
    student_number = input("Student number/ID: ").strip()
    if not name or not student_number:
        print("⚠️  Name and student number are required.")
        return
    try:
        database.add_student(name, student_number)
        print(f"✅ Added student '{name}' ({student_number}).")
    except Exception as e:
        print(f"⚠️  Could not add student (duplicate ID?). Details: {e}")


def add_grade_flow():
    print_header("Add Grade")
    student_number = input("Student number/ID: ").strip()
    student = database.find_student_by_number(student_number)
    if not student:
        print("⚠️  No student found with that ID.")
        return
    student_id, name, _ = student
    subject = input("Subject: ").strip()
    try:
        score = float(input("Score (0-100): ").strip())
    except ValueError:
        print("⚠️  Score must be a number.")
        return
    if not (0 <= score <= 100):
        print("⚠️  Score must be between 0 and 100.")
        return

    database.add_grade(student_id, subject, score)
    print(f"✅ Recorded {subject} = {score} for {name}.")


def view_report_card():
    print_header("Student Report Card")
    student_number = input("Student number/ID: ").strip()
    student = database.find_student_by_number(student_number)
    if not student:
        print("⚠️  No student found with that ID.")
        return

    student_id, name, number = student
    grades = database.get_grades_for_student(student_id)

    print(f"\nName: {name}")
    print(f"ID: {number}")

    if not grades:
        print("No grades recorded yet.")
        return

    print("\n{:<20} {:>8} {:>8}".format("Subject", "Score", "Grade"))
    print("-" * 38)
    for subject, score in grades:
        print("{:<20} {:>8.1f} {:>8}".format(subject, score, grades_utils.letter_grade(score)))

    scores = [s for _, s in grades]
    avg = grades_utils.average(scores)
    top = grades_utils.highest_score(grades)
    low = grades_utils.lowest_score(grades)

    print("-" * 38)
    print(f"Average: {avg}  ({grades_utils.letter_grade(avg)})")
    print(f"Highest: {top[0]} ({top[1]})")
    print(f"Lowest:  {low[0]} ({low[1]})")


def view_all_students():
    print_header("All Students")
    students = database.get_all_students()
    if not students:
        print("No students found.")
        return
    print("{:<5} {:<25} {:<15}".format("ID", "Name", "Student Number"))
    print("-" * 45)
    for sid, name, number in students:
        print("{:<5} {:<25} {:<15}".format(sid, name, number))


def view_class_average():
    print_header("Class Average")
    subject = input("Subject (leave blank for overall average): ").strip()
    avg = database.get_class_average(subject if subject else None)
    if avg is None:
        print("No grades recorded yet.")
        return
    label = f"'{subject}'" if subject else "all subjects"
    print(f"Class average for {label}: {avg} ({grades_utils.letter_grade(avg)})")


def delete_student_flow():
    print_header("Delete Student")
    student_number = input("Student number/ID to delete: ").strip()
    student = database.find_student_by_number(student_number)
    if not student:
        print("⚠️  No student found with that ID.")
        return
    student_id, name, _ = student
    confirm = input(f"Type 'yes' to confirm deleting {name}: ").strip().lower()
    if confirm == "yes":
        database.delete_student(student_id)
        print(f"🗑️  Deleted {name}.")
    else:
        print("Cancelled.")


def main():
    database.init_db()
    actions = {
        "1": add_student_flow,
        "2": add_grade_flow,
        "3": view_report_card,
        "4": view_all_students,
        "5": view_class_average,
        "6": delete_student_flow,
    }

    while True:
        choice = menu()
        if choice == "0":
            print("Goodbye! 👋")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("⚠️  Invalid option, try again.")


if __name__ == "__main__":
    main()
