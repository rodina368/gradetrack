# Student Grade Manager

A simple command-line application for teachers and teaching assistants to
record students, log grades per subject, and instantly see averages, letter
grades, and class performance — all stored locally in a SQLite database.

Built with Python's standard library only (`sqlite3`) — no external
dependencies required.

## Features

- Add students with a unique student ID
- Record grades for any subject
- View a full report card per student: scores, letter grades, average,
  highest/lowest subject
- View the whole class list
- Calculate the class average — overall or filtered by subject
- Delete a student (with confirmation)
- Data persists between runs in a local `grades.db` SQLite file

## Why this project

As a Teaching Assistant, I dealt with grade tracking and student records
first-hand. This tool automates the parts of that process that are normally
done manually in spreadsheets — recording scores, computing averages, and
generating a quick report per student — using a real relational database
instead of flat files.

## Tech stack

- Python 3
- SQLite (via the built-in `sqlite3` module)

## Getting started

```bash
git clone https://github.com/rodina368/student-grade-manager.git
cd student-grade-manager
python main.py
```

No installation step is needed — the database file is created automatically
on first run.

## Example usage

```
========================================
STUDENT GRADE MANAGER
========================================
1. Add a new student
2. Add a grade for a student
3. View a student's report card
4. View all students
5. View class average (all subjects or one subject)
6. Delete a student
0. Exit

Choose an option: 3
Student number/ID: S001

Name: Layla Ahmed
ID: S001

Subject                 Score    Grade
--------------------------------------
CS101                    88.0        B
Math                     92.0        A
--------------------------------------
Average: 90.0  (A)
Highest: Math (92.0)
Lowest:  CS101 (88.0)
```

## Project structure

```
student-grade-manager/
├── main.py           # CLI menu and application flow
├── database.py       # SQLite connection, schema, and queries
├── grades_utils.py   # Grade calculations (average, letter grade, etc.)
├── README.md
└── .gitignore
```

## Possible future improvements

- Export report cards to PDF or CSV
- Add a simple web interface (Flask)
- Support multiple classes/sections
- Add unit tests with `pytest`

## Author

**Rodaina Sailh**
Computer Science student, Libyan International Medical University (LIMU)
[github.com/rodina368](https://github.com/rodina368)
