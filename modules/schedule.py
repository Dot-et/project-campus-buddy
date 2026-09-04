# modules/schedule.py
# Campus Buddy - Schedule Manager

DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

user_schedules = {}


def _get_user_schedule(user_id):
    if user_id not in user_schedules:
        user_schedules[user_id] = {}
    return user_schedules[user_id]


def add_session(user_id, day, time, subject):
    day = day.capitalize()

    if day not in DAYS:
        return "❌ Invalid day. Use Monday-Sunday."

    schedule = _get_user_schedule(user_id)

    if day not in schedule:
        schedule[day] = []

    schedule[day].append((time, subject))
    schedule[day].sort()

    return (
        "✅ Session Added!\n\n"
        f"📅 {day}\n"
        f"⏰ {time}\n"
        f"📚 {subject}"
    )


def get_day_schedule(user_id, day):
    day = day.capitalize()
    schedule = _get_user_schedule(user_id)

    if day not in schedule or not schedule[day]:
        return f"📅 No sessions on {day}."

    message = f"📅 {day.upper()}\n\n"

    for i, (time, subject) in enumerate(schedule[day], 1):
        message += f"{i}. ⏰ {time} — 📚 {subject}\n"

    return message


def get_todays_schedule(user_id):
    from datetime import datetime

    today = datetime.now().strftime("%A")

    return get_day_schedule(user_id, today)


def show_week(user_id):
    schedule = _get_user_schedule(user_id)

    if not schedule:
        return "📅 Your weekly schedule is empty."

    message = "📅 WEEKLY SCHEDULE\n"

    for day in DAYS:
        if day in schedule and schedule[day]:
            message += f"\n📌 {day}\n"

            for time, subject in schedule[day]:
                message += f"   ⏰ {time} — 📚 {subject}\n"

    return message


def clear_day(user_id, day):
    day = day.capitalize()
    schedule = _get_user_schedule(user_id)

    if day not in schedule or not schedule[day]:
        return f"📅 {day} is already empty."

    schedule[day] = []

    return f"🗑️ {day} schedule cleared."


def clear_all(user_id):
    if user_id in user_schedules:
        user_schedules[user_id] = {}

    return "🗑️ Your entire schedule has been cleared."


def count_sessions(user_id):
    schedule = _get_user_schedule(user_id)

    total = sum(
        len(sessions)
        for sessions in schedule.values()
    )

    return f"📊 Total scheduled sessions: {total}"
