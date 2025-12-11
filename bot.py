
# bot.py - Campus Buddy Bot MVP Interface
# Connects: Schedule (Soza), Calculator (Sara), Assignments (Yeshi)

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# Import team modules
from modules import schedule    # Soza's module
from modules import assignments # Yeshi's module  
from modules import calculator  # Sara's module

# Import config (local token)
import config

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ========================
# CORE COMMANDS
# ========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message - /start"""
    welcome_text = """
🎓 **CAMPUS BUDDY BOT - MVP READY!**

🤖 **YOUR STUDY ASSISTANT IS HERE!**

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
• /calc - Open scientific calculator
• /calculate [expression] - Quick calculation

❓ **HELP:**
• /help - Show commands
• /about - About this bot

📌 **Examples:**
• /add_session Monday 08:00 Mathematics
• /add "Math HW" 2024-03-20
• /calculate 5 + 3 * 2
    """
    await update.message.reply_text(welcome_text)  # Remove parse_mode


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command - /help"""
    await start(update, context)


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """About this bot - /about"""
    about_text = """
🤖 **Campus Buddy Bot - MVP Phase 1**

📚 **Project:** Python Group Project
🎓 **University:** Debre Birhan University
👥 **Team:** Soza, Sara, Yeshi
📅 **Phase:** 1 - Minimum Viable Product

🔧 **Features:**
• Study Schedule Manager
• Assignment Tracker  
• Scientific Calculator
• Clean Bot Interface

🚀 **Built with:** Python, Telegram Bot API
✨ **For:** Students by Students
    """
    await update.message.reply_text(about_text, parse_mode='Markdown')


# ========================
# SCHEDULE MODULE COMMANDS (Soza)
# ========================

async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show today's schedule - /schedule"""
    result = schedule.get_todays_schedule()
    await update.message.reply_text(result)


async def add_session_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add study session - /add_session [day] [time] [subject]"""
    if len(context.args) < 3:
        await update.message.reply_text(
            "❌ Usage: /add_session [day] [HH:MM] [subject]\n"
            "Example: /add_session Monday 08:00 Mathematics\n"
            "Valid days: Monday to Sunday"
        )
        return
    
    day, time, *subject_words = context.args
    subject = " ".join(subject_words)
    result = schedule.add_session(day, time, subject)
    await update.message.reply_text(result)


async def week_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show weekly schedule - /week"""
    result = schedule.show_week()
    await update.message.reply_text(result)


async def clear_day_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear day's schedule - /clear_day [day]"""
    if not context.args:
        await update.message.reply_text(
            "❌ Usage: /clear_day [day]\n"
            "Example: /clear_day Monday\n"
            "⚠️ This removes ALL sessions for that day!"
        )
        return
    
    day = context.args[0]
    result = schedule.clear_day(day)
    await update.message.reply_text(result)


async def count_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Count total sessions - /count"""
    result = schedule.count_sessions()
    await update.message.reply_text(result)


# ========================
# ASSIGNMENT MODULE COMMANDS (Yeshi)
# ========================

async def add_assignment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add assignment - /add [task] [date]"""
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Usage: /add [task] [yyyy-mm-dd]\n"
            "Example: /add \"Math Homework\" 2024-03-20\n"
            "📌 Use quotes for multi-word tasks"
        )
        return
    
    task = " ".join(context.args[:-1])
    date = context.args[-1]
    result = assignments.add_assignment(task, date)
    await update.message.reply_text(result)


async def deadlines_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View assignments - /deadlines"""
    result = assignments.get_assignments()
    await update.message.reply_text(result)


async def delete_assignment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete assignment - /delete [number]"""
    if not context.args:
        await update.message.reply_text(
            "❌ Usage: /delete [number]\n"
            "Example: /delete 1\n"
            "📌 First view assignments with /deadlines"
        )
        return
    
    try:
        number = int(context.args[0])
        result = assignments.delete_assignment(number)
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
        number = int(context.args[0])
        new_task = " ".join(context.args[1:-1])
        new_date = context.args[-1]
        result = assignments.edit_assignment(number, new_task, new_date)
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
        number = int(context.args[0])
        result = assignments.mark_done(number)
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
    
    keyword = " ".join(context.args)
    result = assignments.search_assignment(keyword)
    await update.message.reply_text(result)


async def upcoming_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show upcoming assignments - /upcoming"""
    result = assignments.upcoming_assignments()
    await update.message.reply_text(result)


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Assignment statistics - /stats"""
    result = assignments.assignment_stats()
    await update.message.reply_text(result)


# ========================
# CALCULATOR MODULE COMMANDS (Sara)
# ========================

async def calc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Open calculator - /calc"""
    await calculator.start_calculator(update, context)


async def calculate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Quick calculation - /calculate [expression]"""
    if not context.args:
        await update.message.reply_text(
            "❌ Usage: /calculate [expression]\n"
            "Example: /calculate 5 + 3 * 2\n"
            "For full calculator: /calc"
        )
        return
    
    expression = " ".join(context.args)
    
    # Simple calculation (basic safety)
    try:
        # Very basic safe eval for MVP
        allowed_chars = set("0123456789+-*/(). ")
        if all(c in allowed_chars for c in expression):
            result = eval(expression)
            await update.message.reply_text(f"🧮 {expression} = {result}")
        else:
            await update.message.reply_text("❌ Use /calc for advanced calculations")
    except:
        await update.message.reply_text("❌ Calculation error. Try /calc for full calculator")


# ========================
# ERROR HANDLING
# ========================

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle unknown commands"""
    await update.message.reply_text(
        "❌ Unknown command.\n"
        "Try /help to see available commands."
    )


# ========================
# MAIN BOT SETUP
# ========================

def main():
    """Start the bot"""
    
    # Create bot application
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    # ========================
    # REGISTER ALL COMMANDS
    # ========================
    
    # Core commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    
    # Schedule commands (Soza)
    application.add_handler(CommandHandler("schedule", schedule_command))
    application.add_handler(CommandHandler("add_session", add_session_command))
    application.add_handler(CommandHandler("week", week_command))
    application.add_handler(CommandHandler("clear_day", clear_day_command))
    application.add_handler(CommandHandler("count", count_command))
    
    # Assignment commands (Yeshi)
    application.add_handler(CommandHandler("add", add_assignment_command))
    application.add_handler(CommandHandler("deadlines", deadlines_command))
    application.add_handler(CommandHandler("delete", delete_assignment_command))
    application.add_handler(CommandHandler("edit", edit_assignment_command))
    application.add_handler(CommandHandler("done", done_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("upcoming", upcoming_command))
    application.add_handler(CommandHandler("stats", stats_command))
    
    # Calculator commands (Sara)
    application.add_handler(CommandHandler("calc", calc_command))
    application.add_handler(CommandHandler("calculate", calculate_command))
    application.add_handler(CallbackQueryHandler(calculator.calculator_buttons))
    
    # Error handler (MUST BE LAST!)
    from telegram.ext import MessageHandler, filters
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    
    # Start the bot
    print("=" * 50)
    print("🤖 CAMPUS BUDDY BOT - MVP PHASE 1")
    print("=" * 50)
    print("✅ Schedule Module: READY (Soza)")
    print("✅ Assignment Module: READY (Yeshi)")
    print("✅ Calculator Module: READY (Sara)")
    print("✅ Bot Interface: READY")
    print("=" * 50)
    print("🚀 Bot starting...")
    print("👉 Test commands: /start, /schedule, /add, /calc")
    print("=" * 50)
    
    application.run_polling()


if __name__ == "__main__":
    main()


    