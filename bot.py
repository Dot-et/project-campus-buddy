# Campus Buddy Bot (SECURE VERSION)

import os
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

# ========================
# BOT TOKEN
# ========================
TOKEN = os.getenv("BOT_TOKEN")

# ========================
# IMPORT ALL MODULES
# ========================
from modules import schedule, assignments
from modules.calculator import start_calculator, calculator_buttons
from modules.gpa_calculator import GPAManager
from modules import citation, pomodoro_timer, exam_countdown, quotes, dictionary

# ========================
# ENABLE LOGGING
# ========================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ========================
# GPA MANAGER
# ========================
gpa_manager = GPAManager()

# ========================
# START COMMAND
# ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
╔══════════════════════════════╗
║       🎓 CAMPUS BUDDY       ║
║   Your Smart Academic Mate  ║
╚══════════════════════════════╝

✨ Welcome to Campus Buddy!

Your all-in-one academic assistant
for managing university life.

📚 Assignments
🎓 GPA & CGPA
📅 Schedule
🧮 Calculator
⏰ Study Tools
📝 Exam Tracker
📖 Learning Tools
💫 Motivation

👇 Choose a feature below:
"""

    keyboard = [
        ["📚 Assignments", "🎓 GPA & CGPA"],
        ["📅 Schedule", "🧮 Calculator"],
        ["⏰ Study Tools", "📝 Exam Tracker"],
        ["📖 Learning Tools", "💫 Motivation"],
        ["❓ Help & Commands"],
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup
    )


# ========================
# HELP COMMAND
# ========================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

# ========================
# SCHEDULE COMMANDS
# ========================
async def s# ========================
# CLICKABLE MENU
# ========================
async def menu_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the main clickable Campus Buddy menu."""
    choice = update.message.text

    if choice == "📚 Assignments":
        await update.message.reply_text(
            """📚 ASSIGNMENTS

Choose an action:

➕ Add: /add [task] [date]
📋 Deadlines: /deadlines
🔎 Search: /search [keyword]
⬆️ Upcoming: /upcoming
📊 Statistics: /stats
✅ Done: /done [number]
✏️ Edit: /edit [number] [task] [date]
🗑️ Delete: /delete [number]""",
            reply_markup=ReplyKeyboardMarkup(
                [["🏠 Main Menu", "🎓 GPA & CGPA"],
                 ["📅 Schedule", "⏰ Study Tools"]],
                resize_keyboard=True
            )
        )

    elif choice == "🎓 GPA & CGPA":
        await update.message.reply_text(
            """🎓 GPA & CGPA

➕ Add Course
Use: /add_course [name] [score] [credit]

📊 Semester GPA
Use: /semester_gpa

🏆 CGPA
Use: /cgpa

🔄 New Semester
Use: /new_semester""",
            reply_markup=ReplyKeyboardMarkup(
                [["🏠 Main Menu", "📚 Assignments"],
                 ["📅 Schedule", "🧮 Calculator"]],
                resize_keyboard=True
            )
        )

    elif choice == "📅 Schedule":
        await update.message.reply_text(
            """📅 SMART SCHEDULE

📖 Today's Schedule
/schedule

➕ Add Class
/add_session [day] [time] [subject]

📆 Weekly Schedule
/week

🗑️ Clear Day
/clear_day [day]

🔢 Count Sessions
/count""",
            reply_markup=ReplyKeyboardMarkup(
                [["🏠 Main Menu", "📚 Assignments"],
                 ["🎓 GPA & CGPA", "📝 Exam Tracker"]],
                resize_keyboard=True
            )
        )

    elif choice == "🧮 Calculator":
        await update.message.reply_text(
            """🧮 CALCULATOR

🔢 Quick Calculation
/calculate 2+2*3

⚡ Scientific Calculator
/calc

Example:
 /calculate 15*4+20""",
            reply_markup=ReplyKeyboardMarkup(
                [["🏠 Main Menu", "🎓 GPA & CGPA"],
                 ["📖 Learning Tools", "⏰ Study Tools"]],
                resize_keyboard=True
            )
        )

    elif choice == "⏰ Study Tools":
        await update.message.reply_text(
            """⏰ STUDY TOOLS

🍅 Start Pomodoro
/pomodoro

⏸️ Pause
/pomodoro_pause

▶️ Resume
/pomodoro_resume

⏹️ Stop
/pomodoro_stop""",
            reply_markup=ReplyKeyboardMarkup(
                [["🏠 Main Menu", "📚 Assignments"],
                 ["📝 Exam Tracker", "💫 Motivation"]],
                resize_keyboard=True
            )
        )

    elif choice == "📝 Exam Tracker":
        await update.message.reply_text(
            """📝 EXAM TRACKER

➕ Add Exam
/addexam [name] [date] [time]

📋 View Exams
/exams

🗑️ Delete Exam
/deleteexam [name]""",
            reply_markup=ReplyKeyboardMarkup(
                [["🏠 Main Menu", "📅 Schedule"],
                 ["🎓 GPA & CGPA", "⏰ Study Tools"]],
                resize_keyboard=True
            )
        )

    elif choice == "📖 Learning Tools":
        await update.message.reply_text(
            """📖 LEARNING TOOLS

🔤 Dictionary
/define [word]

📚 Citation Manager
/citations

Example:
 /define algorithm""",
            reply_markup=ReplyKeyboardMarkup(
                [["🏠 Main Menu", "🧮 Calculator"],
                 ["💫 Motivation", "📚 Assignments"]],
                resize_keyboard=True
            )
        )

    elif choice == "💫 Motivation":
        await update.message.reply_text(
            """💫 MOTIVATION

💬 Daily Quote
/quote

✨ Get Motivated
/motivate

Keep learning. Keep building. 🚀""",
            reply_markup=ReplyKeyboardMarkup(
                [["🏠 Main Menu", "⏰ Study Tools"],
                 ["📖 Learning Tools", "📚 Assignments"]],
                resize_keyboard=True
            )
        )

    elif choice == "❓ Help & Commands":
        await update.message.reply_text(
            """❓ CAMPUS BUDDY HELP

Use the buttons to explore Campus Buddy,
or type /help to see all available commands.

🏠 /start — Main menu
❓ /help — Commands

🚀 Happy learning!"""
        )

    elif choice == "🏠 Main Menu":
        await start(update, context)


chedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    result = schedule.get_todays_schedule(user_id)
    await update.message.reply_text(result)

async def add_session_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 3:
        await update.message.reply_text(
            "Usage:\n/add_session Monday 08:00 Mathematics"
        )
        return

    user_id = update.effective_user.id
    day, time, *subject_words = context.args
    subject = " ".join(subject_words)

    result = schedule.add_session(user_id, day, time, subject)

    await update.message.reply_text(result)

async def week_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    result = schedule.show_week(user_id)
    await update.message.reply_text(result)

async def clear_day_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Usage:\n/clear_day Monday"
        )
        return

    user_id = update.effective_user.id
    day = context.args[0]

    result = schedule.clear_day(user_id, day)

    await update.message.reply_text(result)

async def count_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    result = schedule.count_sessions(user_id)
    await update.message.reply_text(result)

# ========================
# ASSIGNMENT COMMANDS
# ========================
async def add_assignment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage:\n/add Math Homework 2026-05-20"
        )
        return

    user_id = update.effective_user.id

    task = " ".join(context.args[:-1])
    date = context.args[-1]

    result = assignments.add_assignment(user_id, task, date)

    await update.message.reply_text(result)

async def deadlines_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    result = assignments.get_assignments(user_id)

    await update.message.reply_text(result)

async def delete_assignment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Usage:\n/delete 1")
        return

    try:
        user_id = update.effective_user.id
        number = int(context.args[0])

        result = assignments.delete_assignment(user_id, number)

        await update.message.reply_text(result)

    except:
        await update.message.reply_text("Invalid number")

async def edit_assignment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 3:
        await update.message.reply_text(
            "Usage:\n/edit 1 NewTask 2026-05-30"
        )
        return

    try:
        user_id = update.effective_user.id
        number = int(context.args[0])

        new_task = " ".join(context.args[1:-1])
        new_date = context.args[-1]

        result = assignments.edit_assignment(
            user_id,
            number,
            new_task,
            new_date
        )

        await update.message.reply_text(result)

    except:
        await update.message.reply_text("Invalid input")

async def done_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Usage:\n/done 1")
        return

    try:
        user_id = update.effective_user.id
        number = int(context.args[0])

        result = assignments.mark_done(user_id, number)

        await update.message.reply_text(result)

    except:
        await update.message.reply_text("Invalid number")

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Usage:\n/search math")
        return

    user_id = update.effective_user.id
    keyword = " ".join(context.args)

    result = assignments.search_assignment(user_id, keyword)

    await update.message.reply_text(result)

async def upcoming_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    result = assignments.upcoming_assignments(user_id)

    await update.message.reply_text(result)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    result = assignments.assignment_stats(user_id)

    await update.message.reply_text(result)

# ========================
# GPA COMMANDS
# ========================
async def add_course_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) != 3:
        await update.message.reply_text(
            "Usage:\n/add_course Mathematics 85 3"
        )
        return

    try:
        user_id = update.effective_user.id

        name = context.args[0]
        score = int(context.args[1])
        credit = int(context.args[2])

        result = gpa_manager.add_course(
            user_id,
            name,
            score,
            credit
        )

        await update.message.reply_text(result)

    except:
        await update.message.reply_text("Invalid input")

async def semester_gpa_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    result = gpa_manager.get_semester_gpa(user_id)

    await update.message.reply_text(result)

async def cgpa_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    result = gpa_manager.get_cgpa(user_id)

    await update.message.reply_text(result)

async def new_semester_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    result = gpa_manager.new_semester(user_id)

    await update.message.reply_text(result)

# ========================
# DICTIONARY
# ========================
async def define_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Usage:\n/define algorithm")
        return

    word = " ".join(context.args)

    result = dictionary.define(word)

    await update.message.reply_text(result)

# ========================
# QUOTES
# ========================
async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    quote = quotes.get_todays_quote()

    await update.message.reply_text(f"💫 {quote}")

async def motivate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    import random

    quote = random.choice(quotes.QUOTES)

    await update.message.reply_text(f"✨ {quote}")

# ========================
# CITATIONS
# ========================
citation_manager = citation.CitationManager()

async def citations_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    citation_manager.auto_add_dictionary_source()
    citation_manager.auto_add_gpa_source()
    citation_manager.auto_add_quotes_source()

    result = citation_manager.telegram_list()

    await update.message.reply_text(result)

# ========================
# QUICK CALCULATOR
# ========================
async def calculate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Usage:\n/calculate 2+2*3"
        )
        return

    try:
        from modules.calculator import safe_eval

        expression = " ".join(context.args)

        result = safe_eval(expression)

        await update.message.reply_text(
            f"🧮 {expression} = {result}"
        )

    except Exception as e:
        await update.message.reply_text(
            f"❌ Error: {str(e)}"
        )

# ========================
# UNKNOWN COMMAND
# ========================
async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "❌ Unknown command. Try /start"
    )

# ========================
# MAIN FUNCTION
# ========================
def main():

    application = (
        Application.builder()
        .token(TOKEN)
        .connect_timeout(30)
        .read_timeout(30)
        .write_timeout(30)
        .build()
    )

    # Core
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Schedule
    application.add_handler(CommandHandler("schedule", schedule_command))
    application.add_handler(CommandHandler("add_session", add_session_command))
    application.add_handler(CommandHandler("week", week_command))
    application.add_handler(CommandHandler("clear_day", clear_day_command))
    application.add_handler(CommandHandler("count", count_command))

    # Assignments
    application.add_handler(CommandHandler("add", add_assignment_command))
    application.add_handler(CommandHandler("deadlines", deadlines_command))
    application.add_handler(CommandHandler("delete", delete_assignment_command))
    application.add_handler(CommandHandler("edit", edit_assignment_command))
    application.add_handler(CommandHandler("done", done_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("upcoming", upcoming_command))
    application.add_handler(CommandHandler("stats", stats_command))

    # Calculator
    application.add_handler(CommandHandler("calc", start_calculator))
    application.add_handler(CommandHandler("calculate", calculate_command))
    application.add_handler(CallbackQueryHandler(calculator_buttons))

    # GPA
    application.add_handler(CommandHandler("add_course", add_course_command))
    application.add_handler(CommandHandler("semester_gpa", semester_gpa_command))
    application.add_handler(CommandHandler("cgpa", cgpa_command))
    application.add_handler(CommandHandler("new_semester", new_semester_command))

    # Dictionary
    application.add_handler(CommandHandler("define", define_command))

    # Quotes
    application.add_handler(CommandHandler("quote", quote_command))
    application.add_handler(CommandHandler("motivate", motivate_command))

    # Pomodoro
    application.add_handler(CommandHandler("pomodoro", pomodoro_timer.pomodoro_start))
    application.add_handler(CommandHandler("pomodoro_pause", pomodoro_timer.pomodoro_pause))
    application.add_handler(CommandHandler("pomodoro_resume", pomodoro_timer.pomodoro_resume))
    application.add_handler(CommandHandler("pomodoro_stop", pomodoro_timer.pomodoro_stop))

    # Exams
    application.add_handler(CommandHandler("addexam", exam_countdown.add_exam))
    application.add_handler(CommandHandler("exams", exam_countdown.view_exams))
    application.add_handler(CommandHandler("deleteexam", exam_countdown.delete_exam))

    # Citations
    application.add_handler(CommandHandler("citations", citations_command))

    # Clickable menu
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_router))

    # Unknown commands
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    print("🚀 Campus Buddy Bot is running...")

    application.run_polling()

# ========================
# RUN BOT
# ========================
if __name__ == "__main__":
    main()
