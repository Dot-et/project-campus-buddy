# modules/assignments.py
# Campus Buddy - Assignment Manager

import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "assignments.txt")


def _read_assignments():
    if not os.path.exists(DATA_FILE):
        return []

    assignments = []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = line.split("|")

            if len(parts) == 4:
                user_id, task, date, status = parts
                assignments.append({
                    "user_id": user_id,
                    "task": task,
                    "date": date,
                    "status": status
                })

    return assignments


def _save_assignments(assignments):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        for item in assignments:
            file.write(
                f"{item['user_id']}|"
                f"{item['task']}|"
                f"{item['date']}|"
                f"{item['status']}\n"
            )


def add_assignment(user_id, task, date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return "❌ Invalid date.\nUse: YYYY-MM-DD"

    assignments = _read_assignments()

    assignments.append({
        "user_id": str(user_id),
        "task": task,
        "date": date,
        "status": "Pending"
    })

    _save_assignments(assignments)

    return (
        "✅ Assignment Added!\n\n"
        f"📘 {task}\n"
        f"📅 {date}\n"
        "⏳ Pending"
    )


def get_assignments(user_id):
    assignments = _read_assignments()

    user_items = [
        item for item in assignments
        if item["user_id"] == str(user_id)
    ]

    if not user_items:
        return "📭 You have no assignments."


    message = "📋 Your Assignments\n\n"

    for i, item in enumerate(user_items, 1):
        status_icon = "✅" if item["status"] == "Done" else "⏳"

        message += (
            f"{i}. 📘 {item['task']}\n"
            f"   📅 {item['date']}\n"
            f"   {status_icon} {item['status']}\n\n"
        )

    return message


def delete_assignment(user_id, number):
    assignments = _read_assignments()

    user_items = [
        item for item in assignments
        if item["user_id"] == str(user_id)
    ]

    if number < 1 or number > len(user_items):
        return "❌ Invalid assignment number."

    target = user_items[number - 1]

    assignments.remove(target)
    _save_assignments(assignments)

    return (
        "🗑️ Assignment Deleted!\n\n"
        f"📘 {target['task']}\n"
        f"📅 {target['date']}"
    )


def mark_done(user_id, number):
    assignments = _read_assignments()

    user_items = [
        item for item in assignments
        if item["user_id"] == str(user_id)
    ]

    if number < 1 or number > len(user_items):
        return "❌ Invalid assignment number."

    target = user_items[number - 1]
    target["status"] = "Done"

    _save_assignments(assignments)

    return (
        "✅ Assignment Completed!\n\n"
        f"📘 {target['task']}"
    )


def upcoming_assignments(user_id):
    assignments = _read_assignments()

    today = datetime.now().date()

    upcoming = []

    for item in assignments:
        if item["user_id"] != str(user_id):
            continue

        if item["status"] != "Pending":
            continue

        try:
            due_date = datetime.strptime(
                item["date"], "%Y-%m-%d"
            ).date()
        except ValueError:
            continue

        if due_date >= today:
            upcoming.append(item)

    if not upcoming:
        return "🎉 No upcoming assignments!"

    upcoming.sort(key=lambda x: x["date"])

    message = "⏳ Upcoming Assignments\n\n"

    for i, item in enumerate(upcoming, 1):
        message += (
            f"{i}. 📘 {item['task']}\n"
            f"   📅 {item['date']}\n\n"
        )

    return message


def assignment_stats(user_id):
    assignments = _read_assignments()

    user_items = [
        item for item in assignments
        if item["user_id"] == str(user_id)
    ]

    if not user_items:
        return "📊 No assignment statistics yet."

    total = len(user_items)
    done = sum(
        1 for item in user_items
        if item["status"] == "Done"
    )
    pending = total - done

    return (
        "📊 Assignment Statistics\n\n"
        f"📘 Total: {total}\n"
        f"✅ Completed: {done}\n"
        f"⏳ Pending: {pending}"
    )

