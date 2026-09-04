# modules/exam_countdown.py
# Campus Buddy - Exam Countdown

from datetime import datetime


exam_dates = {}


def set_exam(user_id, exam_name, exam_date):
    try:
        date = datetime.strptime(exam_date, "%Y-%m-%d")
    except ValueError:
        return "❌ Invalid date.\nUse: YYYY-MM-DD"

    if date.date() < datetime.now().date():
        return "❌ Exam date cannot be in the past."

    exam_dates[user_id] = {
        "name": exam_name,
        "date": exam_date
    }

    return (
        "✅ EXAM COUNTDOWN SET!\n\n"
        f"📚 {exam_name}\n"
        f"📅 {exam_date}\n\n"
        f"{countdown(user_id)}"
    )


def countdown(user_id):
    if user_id not in exam_dates:
        return "📭 No exam countdown set."

    exam = exam_dates[user_id]

    try:
        exam_date = datetime.strptime(
            exam["date"], "%Y-%m-%d"
        ).date()
    except ValueError:
        return "❌ Invalid exam date."

    today = datetime.now().date()
    days = (exam_date - today).days

    if days == 0:
        return "🔥 YOUR EXAM IS TODAY!"

    if days == 1:
        return "⚠️ Your exam is tomorrow!"

    if days > 1:
        return f"⏳ {days} days remaining."

    return "❌ Exam date has passed."


def get_exam(user_id):
    if user_id not in exam_dates:
        return "📭 No exam countdown set."

    exam = exam_dates[user_id]

    return (
        "📚 YOUR EXAM\n\n"
        f"📝 {exam['name']}\n"
        f"📅 {exam['date']}\n\n"
        f"{countdown(user_id)}"
    )


def delete_exam(user_id):
    if user_id not in exam_dates:
        return "📭 No exam countdown to delete."

    del exam_dates[user_id]

    return "🗑️ Exam countdown deleted."
