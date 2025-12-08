# modules/assignments.py

import os
from datetime import datetime

DATA_FILE = "assignments.txt"


# -------------------------------
# ADD ASSIGNMENT
# -------------------------------
def add_assignment(task, date):
    try:
        datetime.strptime(date, "%Y-%m-%d")  # Validate date

        with open(DATA_FILE, "a") as file:
            file.write(f"{task}|{date}\n")

        return f"✅ Assignment added!\n📘 {task}\n📅 {date}"

    except ValueError:
        return "❌ Invalid date format! Use yyyy-mm-dd."
    except Exception as e:
        return f"❌ Error: {e}"


# -------------------------------
# GET ALL ASSIGNMENTS
# -------------------------------
def get_assignments():
    if not os.path.exists(DATA_FILE):
        return "📭 No assignments found."

    with open(DATA_FILE, "r") as file:
        lines = file.readlines()

    if not lines:
        return "📭 No assignments found."

    message = "📋 Your Assignments:\n\n"
    for i, line in enumerate(lines, start=1):
        task, date = line.strip().split("|")
        message += f"{i}. 📘 {task} — 📅 {date}\n"

    return message


# -------------------------------
# DELETE ASSIGNMENT
# -------------------------------
def delete_assignment(number):
    if not os.path.exists(DATA_FILE):
        return "❌ No assignments to delete."

    with open(DATA_FILE, "r") as file:
        lines = file.readlines()

    if number < 1 or number > len(lines):
        return "❌ Invalid assignment number."

    deleted = lines.pop(number - 1)

    with open(DATA_FILE, "w") as file:
        file.writelines(lines)

    task, date = deleted.strip().split("|")
    return f"🗑️ Deleted:\n📘 {task}\n📅 {date}"


# -------------------------------
# EDIT ASSIGNMENT
# -------------------------------
def edit_assignment(number, new_task, new_date):
    try:
        datetime.strptime(new_date, "%Y-%m-%d")

        if not os.path.exists(DATA_FILE):
            return "❌ No assignments found."

        with open(DATA_FILE, "r") as file:
            lines = file.readlines()

        if number < 1 or number > len(lines):
            return "❌ Invalid assignment number."

        lines[number - 1] = f"{new_task}|{new_date}\n"

        with open(DATA_FILE, "w") as file:
            file.writelines(lines)

        return f"✏️ Assignment updated!\n📘 {new_task}\n📅 {new_date}"

    except ValueError:
        return "❌ Invalid date format! Use yyyy-mm-dd."
    except Exception as e:
        return f"❌ Error: {e}"
