import asyncio
from telegram import Update
from telegram.ext import ContextTypes

# ==========================
# CONFIGURATION
# ==========================
READ_TIME = 25 * 60
BREAK_TIME = 5 * 60

# ==========================
# USER STATES STORAGE
# ==========================
pomodoro_users = {}
# user_id: {
#   state: "reading" / "break" / "paused"
#   remaining: seconds left
#   task: asyncio.Task
#   sound_mode: "normal" / "silent"
# }

# ==========================
# MESSAGES
# ==========================
MSG_START = "📚 Pomodoro started! Focus for 25 minutes."
MSG_PAUSE = "⏸ Pomodoro paused."
MSG_RESUME = "▶ Pomodoro resumed."
MSG_STOP = "⏹ Pomodoro stopped."
MSG_READ_END = "✅ Break time! Refresh your mind."
MSG_BREAK_END = "🔔 Time to focus again!"

# ==========================
# CUSTOM BREAK ACTIONS
# ==========================
BREAK_ACTIONS = ["💧 Drink water", "🤸 Stretch", "🧘‍♀️ Relax eyes"]

# ==========================
# SOUND SETTINGS
# ==========================
async def sound_normal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    pomodoro_users.setdefault(user_id, {})['sound_mode'] = 'normal'
    await update.message.reply_text("🔊 Notifications set to NORMAL")

async def sound_silent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    pomodoro_users.setdefault(user_id, {})['sound_mode'] = 'silent'
    await update.message.reply_text("🔕 Notifications set to SILENT")

# ==========================
# TIMER LOGIC
# ==========================
async def run_timer(user_id, chat_id, context, duration, next_state):
    while pomodoro_users[user_id]["remaining"] > 0:
        await asyncio.sleep(1)
        if pomodoro_users[user_id]["state"] == "paused":
            continue
        pomodoro_users[user_id]["remaining"] -= 1

    # Determine message
    message = MSG_READ_END if next_state == "break" else MSG_BREAK_END
    sound_mode = pomodoro_users[user_id].get("sound_mode", "normal")
    disable = True if sound_mode == "silent" else False
    await context.bot.send_message(chat_id=chat_id, text=message, disable_notification=disable)

    # Send break actions
    if next_state == "break":
        actions = "\n".join(BREAK_ACTIONS)
        await context.bot.send_message(chat_id=chat_id, text=f"Take a short break:\n{actions}", disable_notification=disable)

    # Auto-repeat
    if next_state == "break":
        pomodoro_users[user_id]["state"] = "break"
        pomodoro_users[user_id]["remaining"] = BREAK_TIME
        pomodoro_users[user_id]["task"] = asyncio.create_task(run_timer(user_id, chat_id, context, BREAK_TIME, "reading"))
    else:
        pomodoro_users[user_id]["state"] = "reading"
        pomodoro_users[user_id]["remaining"] = READ_TIME
        pomodoro_users[user_id]["task"] = asyncio.create_task(run_timer(user_id, chat_id, context, READ_TIME, "break"))

# ==========================
# COMMANDS / HANDLERS
# ==========================
async def pomodoro_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    pomodoro_users.setdefault(user_id, {})
    pomodoro_users[user_id]["state"] = "reading"
    pomodoro_users[user_id]["remaining"] = READ_TIME

    sound_mode = pomodoro_users[user_id].get("sound_mode", "normal")
    disable = True if sound_mode == "silent" else False
    await context.bot.send_message(chat_id=chat_id, text=MSG_START, disable_notification=disable)

    pomodoro_users[user_id]["task"] = asyncio.create_task(run_timer(user_id, chat_id, context, READ_TIME, "break"))

async def pomodoro_pause(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in pomodoro_users:
        pomodoro_users[user_id]["state"] = "paused"
        await update.message.reply_text(MSG_PAUSE)

async def pomodoro_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in pomodoro_users:
        pomodoro_users[user_id]["state"] = "reading" if pomodoro_users[user_id]["remaining"] > BREAK_TIME else "break"
        await update.message.reply_text(MSG_RESUME)

async def pomodoro_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in pomodoro_users:
        if "task" in pomodoro_users[user_id]:
            pomodoro_users[user_id]["task"].cancel()
        del pomodoro_users[user_id]
        await update.message.reply_text(MSG_STOP)



