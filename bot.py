
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import config  
from modules import assignments  
from modules import calculator   
from modules import schedule     

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = """
🎓 **Campus Buddy Bot - Ready to Help!**

📋 **Commands:**
/add [task] [date]  - Add assignment
/deadlines         - View assignments
/calc [math]       - Calculator
/schedule          - Today's plan
/help              - Show commands
    """
    await update.message.reply_text(message)


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    
    task = " ".join(context.args[:-1])
    date = context.args[-1]
    result = assignments.add_assignment(task, date)
    await update.message.reply_text(result)


async def calc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
   
    
    math_expression = " ".join(context.args)
    result = calculator.calculate(math_expression)
    await update.message.reply_text(result)


async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    
    result = schedule.get_todays_schedule()
    await update.message.reply_text(result)


def main():
   
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_command))
    application.add_handler(CommandHandler("deadlines", assignments.get_assignments))
    application.add_handler(CommandHandler("calc", calc_command))
    application.add_handler(CommandHandler("schedule", schedule_command))
    application.add_handler(CommandHandler("help", start))
    

    print("🤖 Waiter (bot.py) is ready to take orders!")
    application.run_polling()


if __name__ == "__main__":
    main()