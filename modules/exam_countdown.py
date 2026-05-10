import json
import os
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

# =========================
# CONFIG
# =========================
DB_FILE = "exam_db.json"
DAILY_SECONDS = 24 * 60 * 60

# =========================
# DATABASE FUNCTIONS
# =========================
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# =========================
# ADD EXAM (DATE + TIME)
# /addexam Name YYYY-MM-DD HH:MM
# =========================
async def add_exam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if len(context.args) != 3:
        await update.message.reply_text(
            "Usage:\n/addexam Math 2025-03-15 09:00"
        )
        return

    exam_name = context.args[0]
    dt_string = f"{context.args[1]} {context.args[2]}"

    try:
        exam_time = datetime.strptime(dt_string, "%Y-%m-%d %H:%M")
    except ValueError:
        await update.message.reply_text("❌ Format must be YYYY-MM-DD HH:MM")
        return

    db = load_db()
    db.setdefault(user_id, {})
    db[user_id][exam_name] = exam_time.isoformat()
    save_db(db)

    await update.message.reply_text(
        f"✅ Exam added\n📘 {exam_name}\n🕒 {exam_time}"
    )

# =========================
# VIEW OWN EXAMS
# /exams
# =========================
async def view_exams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    db = load_db()

    if user_id not in db or not db[user_id]:
        await update.message.reply_text("❌ No exams found.")
        return

    now = datetime.now()
    msg = "📚 Your Exams:\n\n"

    for name, t in db[user_id].items():
        exam_time = datetime.fromisoformat(t)
        delta = exam_time - now

        if delta.total_seconds() > 0:
            days = delta.days
            hours, rem = divmod(delta.seconds, 3600)
            minutes = rem // 60
            status = f"⏳ {days}d {hours}h {minutes}m left"
        else:
            status = "📕 Passed"

        msg += f"• {name}\n🕒 {exam_time}\n{status}\n\n"

    await update.message.reply_text(msg)

# =========================
# UPDATE EXAM
# /updateexam Name YYYY-MM-DD HH:MM
# =========================
async def update_exam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if len(context.args) != 3:
        await update.message.reply_text(
            "Usage:\n/updateexam Math 2025-04-01 10:00"
        )
        return

    exam_name = context.args[0]
    dt_string = f"{context.args[1]} {context.args[2]}"

    try:
        new_time = datetime.strptime(dt_string, "%Y-%m-%d %H:%M")
    except ValueError:
        await update.message.reply_text("❌ Invalid date/time format")
        return

    db = load_db()

    if user_id not in db or exam_name not in db[user_id]:
        await update.message.reply_text("❌ Exam not found.")
        return

    db[user_id][exam_name] = new_time.isoformat()
    save_db(db)

    await update.message.reply_text(
        f"🔄 Exam updated\n📘 {exam_name}\n🕒 {new_time}"
    )

# =========================
# DELETE EXAM
# /deleteexam Name
# =========================
async def delete_exam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if len(context.args) != 1:
        await update.message.reply_text(
            "Usage:\n/deleteexam Math"
        )
        return

    exam_name = context.args[0]
    db = load_db()

    if user_id in db and exam_name in db[user_id]:
        del db[user_id][exam_name]
        save_db(db)
        await update.message.reply_text("🗑 Exam deleted.")
    else:
        await update.message.reply_text("❌ Exam not found.")

# =========================
# AUTO DAILY NOTIFICATION
# (RUNS BY ITSELF)
# =========================
async def exam_notifier(context: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    now = datetime.now()

    for user_id, exams in db.items():
        for name, t in exams.items():
            exam_time = datetime.fromisoformat(t)
            delta = exam_time - now

            if delta.total_seconds() > 0:
                days = delta.days
                hours, rem = divmod(delta.seconds, 3600)
                minutes = rem // 60

                await context.bot.send_message(
                    chat_id=int(user_id),
                    text=(
                        f"📘 Exam Reminder\n"
                        f"📝 {name}\n"
                        f"⏳ Time left: {days}d {hours}h {minutes}m"
                    )
                )
