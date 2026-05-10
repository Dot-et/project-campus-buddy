# bot.py - Campus Buddy Bot (SECURE VERSION)
import os

TOKEN = os.getenv("BOT_TOKEN")
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# Import ALL modules
from modules import schedule, assignments
from modules.calculator import start_calculator, calculator_buttons  # FIXED IMPORTS
from modules.gpa_calculator import GPAManager
from modules import citation, pomodoro_timer, exam_countdown, quotes, dictionary




# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Initialize GPAManager
gpa_manager = GPAManager()

# ========================
# CORE COMMANDS
# ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message - /start"""
    welcome_text = """

     Welcome to 🎓 Campus Buddy Assistant
     This bot is developed by 
• Yeshi Geleta
• Soza Tamirat
• Sara Hailemariam

━━━━━━━━━━━━━━
✨ Smart Learning Bot
━━━━━━━━━━━━━━

📚 Features:
• Notes & Study Materials
• Schedule Manager
• AI Assistance

👇 Type a command to begin!

📋 **AVAILABLE COMMANDS:**

📅 **SCHEDULE:**
• /schedule - Today's study plan
• /add_session [day] [time] [subject] - Add session
• /week - Weekly schedule
• /clear_day [day] - Clear day's schedule
• /count - Count total sessions

📚 **ASSIGNMENTS:**
• /add [task] [date] - Add assignment
• /deadlines - View all assignments
• /delete [number] - Delete assignment
• /edit [number] [new_task] [new_date] - Edit assignment
• /done [number] - Mark as done
• /search [keyword] - Search assignments
• /upcoming - Upcoming assignments
• /stats - Assignment statistics

🧮 **CALCULATOR:**
• /calc - Open scientific calculator with advanced functions
• /calculate [expression] - Quick calculation

🎓 **GPA/CGPA:**
• /add_course [name] [score] [credit] - Add course to current semester
• /semester_gpa - Calculate current semester GPA
• /cgpa - Calculate cumulative GPA
• /new_semester - Start a new semester (moves current to history)

⏰ **STUDY TOOLS:**
• /pomodoro - Start 25-min focus timer
• /pomodoro_pause - Pause timer
• /pomodoro_resume - Resume timer
• /pomodoro_stop - Stop timer

📅 **EXAM TRACKER:**
• /addexam [name] [date] [time] - Add exam
• /exams - View your exams
• /deleteexam [name] - Delete exam

📚 **DICTIONARY:**
• /define [word] - Get word definition

💫 **MOTIVATION:**
• /quote - Today's motivational quote
• /motivate - Get random encouragement

📖 **CITATIONS:**
• /citations - View academic references

🛠️ **OTHER:**
• /clear_day [day] - Clear schedule for a day
• /count - Count your study sessions
"""
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command - /help"""
    await start(update, context)

# ========================
# SCHEDULE COMMANDS (UPDATED)
# ========================
async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show today's schedule - /schedule"""
    user_id = update.effective_user.id
    result = schedule.get_todays_schedule(user_id)
    await update.message.reply_text(result)

async def add_session_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add study session - /add_session [day] [time] [subject]"""
    if len(context.args) < 3:
        await update.message.reply_text(
            "❌ Usage: /add_session [day] [HH:MM] [subject]\n"
            "Example: /add_session Monday 08:00 Mathematics"
        )
        return
    
    user_id = update.effective_user.id
    day, time, *subject_words = context.args
    subject = " ".join(subject_words)
    result = schedule.add_session(user_id, day, time, subject)
    await update.message.reply_text(result)

async def week_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show weekly schedule - /week"""
    user_id = update.effective_user.id
    result = schedule.show_week(user_id)
    await update.message.reply_text(result)

async def clear_day_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear day's schedule - /clear_day [day]"""
    if not context.args:
        await update.message.reply_text(
            "❌ Usage: /clear_day [day]\n"
            "Example: /clear_day Monday"
        )
        return
    
    user_id = update.effective_user.id
    day = context.args[0]
    result = schedule.clear_day(user_id, day)
    await update.message.reply_text(result)

async def count_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Count total sessions - /count"""
    user_id = update.effective_user.id
    result = schedule.count_sessions(user_id)
    await update.message.reply_text(result)

# ========================
# ASSIGNMENT COMMANDS (UPDATED)
# ========================
async def add_assignment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add assignment - /add [task] [date]"""
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Usage: /add [task] [yyyy-mm-dd]\n"
            "Example: /add \"Math Homework\" 2024-03-20"
        )
        return
    
    user_id = update.effective_user.id
    task = " ".join(context.args[:-1])
    date = context.args[-1]
    result = assignments.add_assignment(user_id, task, date)
    await update.message.reply_text(result)

async def deadlines_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View assignments - /deadlines"""
    user_id = update.effective_user.id
    result = assignments.get_assignments(user_id)
    await update.message.reply_text(result)

async def delete_assignment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete assignment - /delete [number]"""
    if not context.args:
        await update.message.reply_text(
            "❌ Usage: /delete [number]\n"
            "Example: /delete 1"
        )
        return
    
    try:
        user_id = update.effective_user.id
        number = int(context.args[0])
        result = assignments.delete_assignment(user_id, number)
        await update.message.reply_text(result)
    except ValueError:
        await update.message.reply_text("❌ Please enter a valid number")

async def edit_assignment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Edit assignment - /edit [number] [new_task] [new_date]"""
    if len(context.args) < 3:
        await update.message.reply_text(
            "❌ Usage: /edit [number] [new_task] [new_date]\n"
            "Example: /edit 1 \"Science Project\" 2024-03-25"
        )
        return
    
    try:
        user_id = update.effective_user.id
        number = int(context.args[0])
        new_task = " ".join(context.args[1:-1])
        new_date = context.args[-1]
        result = assignments.edit_assignment(user_id, number, new_task, new_date)
        await update.message.reply_text(result)
    except ValueError:
        await update.message.reply_text("❌ Please enter a valid number")

async def done_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mark assignment as done - /done [number]"""
    if not context.args:
        await update.message.reply_text(
            "❌ Usage: /done [number]\n"
            "Example: /done 1"
        )
        return
    
    try:
        user_id = update.effective_user.id
        number = int(context.args[0])
        result = assignments.mark_done(user_id, number)
        await update.message.reply_text(result)
    except ValueError:
        await update.message.reply_text("❌ Please enter a valid number")

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Search assignments - /search [keyword]"""
    if not context.args:
        await update.message.reply_text(
            "❌ Usage: /search [keyword]\n"
            "Example: /search math"
        )
        return
    
    user_id = update.effective_user.id
    keyword = " ".join(context.args)
    result = assignments.search_assignment(user_id, keyword)
    await update.message.reply_text(result)

async def upcoming_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show upcoming assignments - /upcoming"""
    user_id = update.effective_user.id
    result = assignments.upcoming_assignments(user_id)
    await update.message.reply_text(result)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Assignment statistics - /stats"""
    user_id = update.effective_user.id
    result = assignments.assignment_stats(user_id)
    await update.message.reply_text(result)

# ========================
# GPA MODULE COMMANDS (FIXED)
# ========================

async def add_course_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add course - /add_course [name] [score] [credit]"""
    if len(context.args) != 3:
        await update.message.reply_text(
            "❌ Usage: /add_course [name] [score] [credit]\n"
            "Example: /add_course Mathematics 85 3"
        )
        return
    
    try:
        user_id = update.effective_user.id
        name = context.args[0]
        score = int(context.args[1])
        credit = int(context.args[2])
        
        # Use the GPAManager
        result = gpa_manager.add_course(user_id, name, score, credit)
        await update.message.reply_text(result)
        
    except ValueError:
        await update.message.reply_text("❌ Please enter valid numbers for score and credit")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def semester_gpa_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculate semester GPA - /semester_gpa"""
    user_id = update.effective_user.id
    
    # Use the GPAManager
    result = gpa_manager.get_semester_gpa(user_id)
    await update.message.reply_text(result, parse_mode='Markdown')

async def cgpa_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculate CGPA - /cgpa"""
    user_id = update.effective_user.id
    
    # Use the GPAManager
    result = gpa_manager.get_cgpa(user_id)
    await update.message.reply_text(result, parse_mode='Markdown')

async def new_semester_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start new semester - /new_semester"""
    user_id = update.effective_user.id
    result = gpa_manager.new_semester(user_id)
    await update.message.reply_text(result)

# ========================
# DICTIONARY COMMANDS
# ========================
async def define_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Define word - /define [word]"""
    if not context.args:
        await update.message.reply_text("Usage: /define algorithm")
        return
    
    word = " ".join(context.args)
    result = dictionary.define(word)
    await update.message.reply_text(result)

# ========================
# QUOTES COMMANDS
# ========================
async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get today's quote - /quote"""
    quote = quotes.get_todays_quote()
    await update.message.reply_text(f"💫 {quote}")

async def motivate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get motivation - /motivate"""
    import random
    all_quotes = quotes.QUOTES
    quote = random.choice(all_quotes)
    await update.message.reply_text(f"✨ {quote}")

# ========================
# CITATION COMMANDS
# ========================
citation_manager = citation.CitationManager()

async def citations_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View citations - /citations"""
    # Add default citations
    citation_manager.auto_add_dictionary_source()
    citation_manager.auto_add_gpa_source()
    citation_manager.auto_add_quotes_source()
    
    result = citation_manager.telegram_list()
    await update.message.reply_text(result, parse_mode='Markdown')

# ========================
# QUICK CALCULATION COMMAND
# ========================
async def calculate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Quick calculation - /calculate [expression]"""
    if not context.args:
        await update.message.reply_text("Usage: /calculate 2+2*3 or /calculate sin(30)")
        return
    
    try:
        from modules.calculator import safe_eval
        expression = " ".join(context.args)
        result = safe_eval(expression)
        await update.message.reply_text(f"🧮 {expression} = {result}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# ========================
# ERROR HANDLING
# ========================
async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Unknown command. Try /start")

# ========================
# MAIN BOT SETUP
# ========================
def main():
    """Start the bot"""
    # Create bot application with timeouts
    application = Application.builder() \
        .token(config.BOT_TOKEN) \
        .connect_timeout(30).read_timeout(30).write_timeout(30) \
        .build()
    
    # ========================
    # REGISTER ALL COMMANDS
    # ========================
    
    # Core commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Schedule commands (UPDATED)
    application.add_handler(CommandHandler("schedule", schedule_command))
    application.add_handler(CommandHandler("add_session", add_session_command))
    application.add_handler(CommandHandler("week", week_command))
    application.add_handler(CommandHandler("clear_day", clear_day_command))
    application.add_handler(CommandHandler("count", count_command))
    
    # Assignment commands (UPDATED)
    application.add_handler(CommandHandler("add", add_assignment_command))
    application.add_handler(CommandHandler("deadlines", deadlines_command))
    application.add_handler(CommandHandler("delete", delete_assignment_command))
    application.add_handler(CommandHandler("edit", edit_assignment_command))
    application.add_handler(CommandHandler("done", done_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("upcoming", upcoming_command))
    application.add_handler(CommandHandler("stats", stats_command))
    
    # Calculator commands - FIXED
    application.add_handler(CommandHandler("calc", start_calculator))  # CHANGED from calculator.calc_command
    application.add_handler(CommandHandler("calculate", calculate_command))  # Added quick calculation
    application.add_handler(CallbackQueryHandler(calculator_buttons))  # CHANGED from calculator.calculator_buttons
    
    # GPA commands (FIXED)
    application.add_handler(CommandHandler("add_course", add_course_command))
    application.add_handler(CommandHandler("semester_gpa", semester_gpa_command))
    application.add_handler(CommandHandler("cgpa", cgpa_command))
    application.add_handler(CommandHandler("new_semester", new_semester_command))
    
    # Dictionary commands
    application.add_handler(CommandHandler("define", define_command))
    
    # Quotes commands
    application.add_handler(CommandHandler("quote", quote_command))
    application.add_handler(CommandHandler("motivate", motivate_command))
    
    # Pomodoro commands
    application.add_handler(CommandHandler("pomodoro", pomodoro_timer.pomodoro_start))
    application.add_handler(CommandHandler("pomodoro_pause", pomodoro_timer.pomodoro_pause))
    application.add_handler(CommandHandler("pomodoro_resume", pomodoro_timer.pomodoro_resume))
    application.add_handler(CommandHandler("pomodoro_stop", pomodoro_timer.pomodoro_stop))
    
    # Exam tracker commands
    application.add_handler(CommandHandler("addexam", exam_countdown.add_exam))
    application.add_handler(CommandHandler("exams", exam_countdown.view_exams))
    application.add_handler(CommandHandler("deleteexam", exam_countdown.delete_exam))
    
    # Citation commands
    application.add_handler(CommandHandler("citations", citations_command))
    
    # Error handler (MUST BE LAST!)
    from telegram.ext import MessageHandler, filters
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    
    # Start bot
    print("=" * 50)
    print("🤖 CAMPUS BUDDY BOT - SECURE VERSION")
    print("=" * 50)
    print("✅ ALL MODULES WITH USER SEPARATION")
    print("✅ Schedule: User-specific")
    print("✅ Assignments: User-specific")
    print("✅ Calculator: User-specific with advanced functions")
    print("✅ GPA: User-specific with persistent storage")
    print("✅ Pomodoro: User-specific")
    print("✅ Exams: User-specific")
    print("=" * 50)
    print("🚀 Bot starting... Use /start to see all commands")
    print("=" * 50)
    
    application.run_polling()

if __name__ == "__main__":
    main()