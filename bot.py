
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import config  
from modules import assignments  
from modules import calculator   
from modules import schedule     


# CORE COMMANDS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message and command list"""
    message = """
🎓 **Campus Buddy Bot - MVP Ready!**

📋 **AVAILABLE COMMANDS:**

📅 **Assignment Management:**
• /add [task] [date] - Add new assignment
• /deadlines - View all assignments

🧮 **Study Tools:**
• /calc [expression] - Quick calculator
• /schedule - Today's study plan

❓ **Help:**
• /help - Show this menu
• /start - Welcome message

📌 *Example: /add "Math HW" 2024-03-20*
    """
    await update.message.reply_text(message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)  # Same as start


# ASSIGNMENT COMMANDS 

async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add new assignment with error handling"""
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Usage: /add [task] [yyyy-mm-dd]\n"
            "Example: /add \"Math homework\" 2024-03-20"
        )
        return
    
    task = " ".join(context.args[:-1])
    date = context.args[-1]
    
    # Basic date validation
    if len(date) != 10 or date[4] != '-' or date[7] != '-':
        await update.message.reply_text("❌ Date format: yyyy-mm-dd (e.g., 2024-03-20)")
        return
    
    result = assignments.add_assignment(task, date)
    await update.message.reply_text(result)

async def deadlines_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View all assignments - FIXED to work with CommandHandler"""
    # Call module function and send result
    result = assignments.get_assignments()
    await update.message.reply_text(result)
# it shows the one that was done 
async def done_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /done [assignment number]")
        return

    try:
        number = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Assignment number must be a number.")
        return

    result = assignments.mark_done(number)
    await update.message.reply_text(result)
#  searching the assignment 
async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /search [keyword]")
        return

    keyword = " ".join(context.args)
    result = assignments.search_assignment(keyword)
    await update.message.reply_text(result)
#   remendires the up_coming assignment 
async def upcoming_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = assignments.upcoming_assignments()
    await update.message.reply_text(result)
# assignment statics
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = assignments.assignment_stats()
    await update.message.reply_text(result)
    


# STUDY TOOLS COMMANDS

async def calc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculator with error handling"""
    if not context.args:
        await update.message.reply_text(
            "❌ Usage: /calc [expression]\n"
            "Example: /calc 5 + 3 * 2"
        )
        return
    
    math_expression = " ".join(context.args)
    result = calculator.calculate(math_expression)
    await update.message.reply_text(result)

async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show today's schedule"""
    result = schedule.get_todays_schedule()
    await update.message.reply_text(result)


# ERROR HANDLING

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle unknown commands"""
    await update.message.reply_text(
        "❌ I don't recognize that command.\n"
        "Try /help to see available commands."
    )


# MAIN BOT SETUP

def main():
    # Create bot application
    application = Application.builder().token(config.BOT_TOKEN).build()
    
 
    # COMMAND REGISTRATION
   
    
    # Core commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Assignment commands 
    application.add_handler(CommandHandler("add", add_command))
    application.add_handler(CommandHandler("deadlines", deadlines_command))  # FIXED!
    # New Assignment Commands
    application.add_handler(CommandHandler("done", done_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("upcoming", upcoming_command))plication.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("clear", clear_command))
    # Study tools commands
    application.add_handler(CommandHandler("calc", calc_command))
    application.add_handler(CommandHandler("schedule", schedule_command))
    
    # Error handling 
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    
    # Start the bot
    print("🤖 Campus Buddy Bot - MVP Interface Ready!")
    print("👉 Available commands: /start, /add, /deadlines, /calc, /schedule")
    application.run_polling()

if __name__ == "__main__":
    main()
