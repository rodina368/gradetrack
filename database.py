"""
database.py
Handles all SQLite database operations for the Student Grade Manager.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "grades.db"


def get_connection():
    """Create (if needed) and return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create the students and grades tables if they don't already exist."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_number TEXT UNIQUE NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            score REAL NOT NULL CHECK (score >= 0 AND score <= 100),
            FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def add_student(name: str, student_number: str) -> int:
    """Insert a new student. Returns the new student's id."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, student_number) VALUES (?, ?)",
        (name, student_number),
    )
    conn.commit()
    student_id = cur.lastrowid
    conn.close()
    return student_id


def get_all_students():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, student_number FROM students ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return rows


def find_student_by_number(student_number: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, student_number FROM students WHERE student_number = ?",
        (student_number,),
    )
    row = cur.fetchone()
    conn.close()
    return row


def add_grade(student_id: int, subject: str, score: float) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO grades (student_id, subject, score) VALUES (?, ?, ?)",
        (student_id, subject, score),
    )
    conn.commit()
    grade_id = cur.lastrowid
    conn.close()
    return grade_id


def get_grades_for_student(student_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT subject, score FROM grades WHERE student_id = ? ORDER BY subject",
        (student_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_class_average(subject: str = None):
    """Return the average score, optionally filtered by subject."""
    conn = get_connection()
    cur = conn.cursor()
    if subject:
        cur.execute("SELECT AVG(score) FROM grades WHERE subject = ?", (subject,))
    else:
        cur.execute("SELECT AVG(score) FROM grades")
    result = cur.fetchone()[0]
    conn.close()
    return round(result, 2) if result is not None else None


def delete_student(student_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
