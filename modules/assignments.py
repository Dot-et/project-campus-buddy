






# modules/assignments.py

import os
from datetime import datetime

DATA_FILE =os.path.join(os.path.dirname(__file__), "assignments.txt"

# -------------------------------
# ADD ASSIGNMENT
# -------------------------------
def add_assignment(task, date):
    try:
        datetime.strptime(date, "%Y-%m-%d")

        with open(DATA_FILE, "a") as file:
            file.write(f"{task}|{date}|Pending\n")

        return f"✅ Assignment added!\n📘 {task}\n📅 {date}\n⏳ Status: Pending"

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
        task, date, status = line.strip().split("|")
        message += f"{i}. 📘 {task}\n   📅 {date} | ✅ {status}\n\n"

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

    task, date, status = deleted.strip().split("|")
    return f"🗑️ Deleted:\n📘 {task}\n📅 {date}\n✅ {status}"


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

        task, date, status = lines[number - 1].strip().split("|")
        lines[number - 1] = f"{new_task}|{new_date}|{status}\n"

        with open(DATA_FILE, "w") as file:
            file.writelines(lines)

        return f"✏️ Updated!\n📘 {new_task}\n📅 {new_date}\n✅ {status}"

    except ValueError:
        return "❌ Invalid date format! Use yyyy-mm-dd."
    except Exception as e:
        return f"❌ Error: {e}"


# -------------------------------
# MARK AS DONE
# -------------------------------
def mark_done(number):
    if not os.path.exists(DATA_FILE):
        return "❌ No assignments found."

    with open(DATA_FILE, "r") as file:
        lines = file.readlines()

    if number < 1 or number > len(lines):
        return "❌ Invalid assignment number."

    task, date, status = lines[number - 1].strip().split("|")
    lines[number - 1] = f"{task}|{date}|Done\n"

    with open(DATA_FILE, "w") as file:
        file.writelines(lines)

    return f"✅ Marked as Done:\n📘 {task}"


# -------------------------------
# SEARCH ASSIGNMENT
# -------------------------------
def search_assignment(keyword):
    if not os.path.exists(DATA_FILE):
        return "❌ No assignments found."

    with open(DATA_FILE, "r") as file:
        lines = file.readlines()

    results = []
    for i, line in enumerate(lines, start=1):
        if keyword.lower() in line.lower():
            task, date, status = line.strip().split("|")
            results.append(f"{i}. 📘 {task} | 📅 {date} | ✅ {status}")

    if not results:
        return "🔍 No matching assignments found."

    return "🔍 Search Results:\n\n" + "\n".join(results)


# -------------------------------
# SHOW UPCOMING ASSIGNMENTS
# -------------------------------
def upcoming_assignments():
    if not os.path.exists(DATA_FILE):
        return "❌ No assignments found."

    today = datetime.now().date()
    upcoming = []

    with open(DATA_FILE, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines, start=1):
        task, date, status = line.strip().split("|")
        due_date = datetime.strptime(date, "%Y-%m-%d").date()

        if due_date >= today and status == "Pending":
            upcoming.append(f"{i}. 📘 {task} — 📅 {date}")

    if not upcoming:
        return "✅ No upcoming assignments!"

    return "⏳ Upcoming Assignments:\n\n" + "\n".join(upcoming)


# -------------------------------
# ASSIGNMENT STATISTICS
# -------------------------------
def assignment_stats():
    if not os.path.exists(DATA_FILE):
        return "❌ No assignments found."

    with open(DATA_FILE, "r") as file:
        lines = file.readlines()

    total = len(lines)
    done = 0
    pending = 0

    for line in lines:
        task, date, status = line.strip().split("|")
        if status == "Done":
            done += 1
        else:
            pending += 1

    return (
        "📊 Assignment Statistics:\n\n"
        f"📘 Total: {total}\n"
        f"✅ Done: {done}\n"
        f"⏳ Pending: {pending}"
    )




