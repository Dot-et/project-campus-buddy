"""
Campus Buddy Bot - Main File
Branch: Yeshi_Dot-et
Developer: Yeshi
"""

import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import config

# Load token
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Logging
logging.basicConfig(
    format=config.LOG_FORMAT,
    level=config.LOG_LEVEL
)

# ---------------- BASIC COMMANDS ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👋 Welcome to {config.BOT_NAME}!\n\n"
        "Use /help to see all commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Available Commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/about - About the bot\n"
        "/status - Bot status\n\n"
        "📚 Assignment Commands:\n"
        "/add - Add a new assignment\n"
        "/list - List all assignments\n"
        "/complete - Mark assignment as completed\n"
        "/delete - Delete an assignment"
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🤖 Bot Name: {config.BOT_NAME}\n"
        f"🔢 Version: {config.BOT_VERSION}\n"
        f"👨‍💻 Developer: {config.BOT_DEVELOPER}"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running successfully!")

# ---------------- ASSIGNMENT COMMANDS ----------------

# Temporary memory storage (will be replaced by database later)
assignments = []

async def add_assignment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Usage: /add Assignment Title")
        return

    title = " ".join(context.args)
    assignments.append({"title": title, "status": "pending"})

    await update.message.reply_text(f"✅ Assignment added:\n{title}")

async def list_assignments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not assignments:
        await update.message.reply_text("📭 No assignments found.")
        return

    message = "📋 Your Assignments:\n\n"
    for i, task in enumerate(assignments, start=1):
        message += f"{i}. {task['title']} - {task['status']}\n"

    await update.message.reply_text(message)

async def complete_assignment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Usage: /complete 1")
        return

    index = int(context.args[0]) - 1

    if index < 0 or index >= len(assignments):
        await update.message.reply_text("❌ Invalid assignment number.")
        return

    assignments[index]["status"] = "completed"
    await update.message.reply_text("✅ Assignment marked as completed.")

async def delete_assignment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Usage: /delete 1")
        return

    index = int(context.args[0]) - 1

    if index < 0 or index >= len(assignments):
        await update.message.reply_text("❌ Invalid assignment number.")
        return

    removed = assignments.pop(index)
    await update.message.reply_text(f"🗑️ Deleted: {removed['title']}")

# ---------------- MAIN FUNCTION ----------------

def main():
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not found. Check your .env file.")
        return

    print(f"Starting {config.BOT_NAME}...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Basic Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("status", status))

    # Assignment Commands
    app.add_handler(CommandHandler("add", add_assignment))
    app.add_handler(CommandHandler("list", list_assignments))
    app.add_handler(CommandHandler("complete", complete_assignment))
    app.add_handler(CommandHandler("delete", delete_assignment))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
