from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, CallbackContext
import sympy as sp

# User sessions storage
user_sessions = {}

# Initialize user session
def init_user_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "expression": "",
            "history": [],
            "memory": 0,
            "deg": True  # Degree mode by default
        }

# /start command
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    init_user_session(user_id)
    update.message.reply_text(
        "Welcome to Campus Buddy Calculator!\nUse /keyboard to start calculating."
    )

# Build the calculator keyboard
def calculator_keyboard():
    keyboard = [
        # Numbers & basic operators
        [InlineKeyboardButton("7", callback_data="7"),
         InlineKeyboardButton("8", callback_data="8"),
         InlineKeyboardButton("9", callback_data="9"),
         InlineKeyboardButton("÷", callback_data="/")], #for divition

        [InlineKeyboardButton("4", callback_data="4"),
         InlineKeyboardButton("5", callback_data="5"),
         InlineKeyboardButton("6", callback_data="6"),
         InlineKeyboardButton("×", callback_data="*")],# for multiplication

        [InlineKeyboardButton("1", callback_data="1"),
         InlineKeyboardButton("2", callback_data="2"),
         InlineKeyboardButton("3", callback_data="3"),
         InlineKeyboardButton("-", callback_data="-")],# for substraction

        [InlineKeyboardButton("0", callback_data="0"),
         InlineKeyboardButton(".", callback_data="."),
         InlineKeyboardButton("(", callback_data="("),
         InlineKeyboardButton(")", callback_data=")")],

        [InlineKeyboardButton("=", callback_data="="),#for giving result
         InlineKeyboardButton("+", callback_data="+"),# for addition
         InlineKeyboardButton("C", callback_data="C"),#for clean
         InlineKeyboardButton("π", callback_data="pi"),
         InlineKeyboardButton("e", callback_data="E")],

        # Advanced functions
        [InlineKeyboardButton("√", callback_data="sqrt"),#for square root
         InlineKeyboardButton("^", callback_data="^"),# for power
         InlineKeyboardButton("%", callback_data="%"),#for percent
         InlineKeyboardButton("log", callback_data="log"),
         InlineKeyboardButton("ln", callback_data="ln")],

        [InlineKeyboardButton("Σ", callback_data="sum"),#for summition
         InlineKeyboardButton("mod", callback_data="mod"),
         InlineKeyboardButton("!", callback_data="factorial"),
         InlineKeyboardButton("∫", callback_data="integrate"),
         InlineKeyboardButton("deg/rad", callback_data="deg")],

        # Trigonometry
        [InlineKeyboardButton("sin", callback_data="sin"),
         InlineKeyboardButton("cos", callback_data="cos"),
         InlineKeyboardButton("tan", callback_data="tan")],

        [InlineKeyboardButton("asin", callback_data="asin"),
         InlineKeyboardButton("acos", callback_data="acos"),
         InlineKeyboardButton("atan", callback_data="atan")],

        # Control buttons
        [InlineKeyboardButton("History", callback_data="history"),#all prievieous calculation history after restart the bot 
         InlineKeyboardButton("Clear", callback_data="C"),#remove the number from adding,sutracting...)
         InlineKeyboardButton("Exist", callback_data="Exist"),#exist from keyboard(otherwise calculator)
         InlineKeyboardButton("Off", callback_data="off")]#reset the calculator
    ]
    return InlineKeyboardMarkup(keyboard)

# /keyboard command
def keyboard(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    init_user_session(user_id)
    update.message.reply_text(
        "Calculator Keyboard:", reply_markup=calculator_keyboard()
    )

# Placeholder for Campus Buddy main menu
def campus_buddy_main_menu():
    return InlineKeyboardMarkup([[InlineKeyboardButton("Feature1", callback_data="f1")],
                                 [InlineKeyboardButton("Feature2", callback_data="f2")]])

# Handle button clicks
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    init_user_session(user_id)
    session = user_sessions[user_id]
    data = query.data

    try:
        # Clear expression
        if data == "C" or data == "Clear":
            session["expression"] = ""

        # Evaluate expression
        elif data == "=":
            expr = session["expression"]
            if expr.strip() == "":
                query.edit_message_text(
                    text="Expression is empty", reply_markup=calculator_keyboard()
                )
                return

            # Replace user-friendly symbols with sympy equivalents
            expr = expr.replace("π", "pi").replace("e", "E").replace("^", "**")
            expr = expr.replace("×", "*").replace("÷", "/").replace("√", "sqrt")
            expr = expr.replace("%", "*0.01").replace("!", "factorial")

            # Degree/radian handling for trig
            if session["deg"]:
                expr = expr.replace("sin(", "sin(rad(")
                expr = expr.replace("cos(", "cos(rad(")
                expr = expr.replace("tan(", "tan(rad(")
                expr = expr.replace("asin(", "deg(asin(")
                expr = expr.replace("acos(", "deg(acos(")
                expr = expr.replace("atan(", "deg(atan(")

            try:
                result = sp.sympify(expr, evaluate=True)
                result_str = str(result)
                session["history"].append(f"{session['expression']} = {result_str}")
                session["expression"] = result_str
            except Exception as e:
                session["expression"] = ""
                query.edit_message_text(
                    text=f"Error evaluating expression: {e}\nCheck your syntax.",
                    reply_markup=calculator_keyboard()
                )
                return

        # Exist button → exit calculator
        elif data == "Exist":
            session["expression"] = ""
            query.edit_message_text(
                text="Exiting Calculator... Returning to main menu.",
                reply_markup=campus_buddy_main_menu()
            )
            return

        # Off → reset session
        elif data == "off":
            session["expression"] = ""
            session["history"] = []
            session["memory"] = 0

        # History → show last 10 calculations
        elif data == "history":
            if not session["history"]:
                query.edit_message_text(
                    text="No history yet.", reply_markup=calculator_keyboard()
                )
            else:
                hist_text = "\n".join(session["history"][-10:])
                query.edit_message_text(
                    text=f"Last calculations:\n{hist_text}", reply_markup=calculator_keyboard()
                )
            return

        # Toggle degrees/radians
        elif data == "deg":
            session["deg"] = not session["deg"]
            mode = "Degrees" if session["deg"] else "Radians"
            query.edit_message_text(
                text=f"Trig mode set to {mode}", reply_markup=calculator_keyboard()
            )
            return

        # Append functions / symbols
        else:
            if data in ["sqrt","log","ln","sin","cos","tan","asin","acos","atan","sum","mod","factorial","integrate"]:
                session["expression"] += f"{data}("
            else:
                session["expression"] += data

    except Exception as e:
        session["expression"] = ""
        query.edit_message_text(
            text=f"Unexpected Error: {e}\nCheck your input.", reply_markup=calculator_keyboard()
        )
        return

    # Update display
    query.edit_message_text(
        text=session["expression"], reply_markup=calculator_keyboard()
    )

# Main function
def main():
    TOKEN = "8069213963:AAE8y2qLfF39JaGJCAfU4ppLfOjNzVH2gL4"
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("keyboard", keyboard))
    dp.add_handler(CommandHandler("quick_calculator", keyboard))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
