# modules/calculator.py
# Campus Buddy - Scientific Calculator

import math
import sympy as sp

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


user_calc = {}


def safe_eval(expr, mode="DEG"):
    try:
        expr = expr.replace("÷", "/")
        expr = expr.replace("×", "*")
        expr = expr.replace("^", "**")

        if not expr.strip():
            return 0

        if mode == "DEG":
            sin = lambda x: math.sin(math.radians(x))
            cos = lambda x: math.cos(math.radians(x))
            tan = lambda x: math.tan(math.radians(x))
        else:
            sin = math.sin
            cos = math.cos
            tan = math.tan

        def factorial(x):
            if not float(x).is_integer() or x < 0:
                raise ValueError("Factorial requires a non-negative whole number")
            return math.factorial(int(x))

        safe_dict = {
            "sin": sin,
            "cos": cos,
            "tan": tan,
            "asin": math.asin,
            "acos": math.acos,
            "atan": math.atan,
            "sqrt": math.sqrt,
            "log": math.log10,
            "ln": math.log,
            "pi": math.pi,
            "e": math.e,
            "factorial": factorial,
            "abs": abs,
        }

        return eval(
            expr,
            {"__builtins__": {}},
            safe_dict
        )

    except ZeroDivisionError:
        return "❌ Division by zero"

    except ValueError as e:
        return f"❌ {e}"

    except SyntaxError:
        return "❌ Invalid expression"

    except Exception:
        return "❌ Calculation error"


def real_integration(expression):
    try:
        x = sp.symbols("x")

        expression = expression.replace("^", "**")

        expr = sp.sympify(expression)

        result = sp.integrate(expr, x)

        return f"∫ {expression} dx = {result}"

    except Exception:
        return "❌ Integration error\nUse x as the variable."


def calculator_keyboard():

    keys = [
        [
            ("RAD", "calc_rad"),
            ("DEG", "calc_deg"),
            ("⌫", "calc_back"),
            ("C", "calc_clear")
        ],

        [
            ("sin", "sin("),
            ("cos", "cos("),
            ("tan", "tan("),
            ("√", "sqrt(")
        ],

        [
            ("sin⁻¹", "asin("),
            ("cos⁻¹", "acos("),
            ("tan⁻¹", "atan("),
            ("!", "factorial(")
        ],

        [
            ("log", "log("),
            ("ln", "ln("),
            ("π", "pi"),
            ("e", "e")
        ],

        [
            ("(", "("),
            (")", ")"),
            ("^", "^"),
            ("%", "%")
        ],

        [
            ("7", "7"),
            ("8", "8"),
            ("9", "9"),
            ("÷", "÷")
        ],

        [
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("×", "×")
        ],

        [
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("−", "-")
        ],

        [
            ("0", "0"),
            (".", "."),
            ("=", "calc_equals"),
            ("+", "+")
        ],

        [
            ("M+", "calc_mplus"),
            ("MR", "calc_mr"),
            ("∫", "calc_integral"),
            ("History", "calc_history")
        ],

        [
            ("Exit", "calc_exit")
        ]
    ]

    keyboard = []

    for row in keys:
        keyboard.append([
            InlineKeyboardButton(
                text=text,
                callback_data=data
            )
            for text, data in row
        ])

    return InlineKeyboardMarkup(keyboard)


def calculator_text(data):

    expression = data["expr"]

    return (
        "🧮 SCIENTIFIC CALCULATOR\n\n"
        f"Mode: {data['mode']}\n"
        f"Expression:\n{expression or '0'}"
    )


async def start_calculator(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    user_calc[user_id] = {
        "expr": "",
        "mode": "DEG",
        "history": [],
        "memory": 0
    }

    await update.effective_message.reply_text(
        calculator_text(user_calc[user_id]),
        reply_markup=calculator_keyboard()
    )


async def calculator_buttons(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    user_id = query.from_user.id

    if user_id not in user_calc:
        user_calc[user_id] = {
            "expr": "",
            "mode": "DEG",
            "history": [],
            "memory": 0
        }

    data = user_calc[user_id]
    key = query.data

    # Clear
    if key == "calc_clear":
        data["expr"] = ""

    # Backspace
    elif key == "calc_back":
        data["expr"] = data["expr"][:-1]

    # Degree mode
    elif key == "calc_deg":
        data["mode"] = "DEG"

    # Radian mode
    elif key == "calc_rad":
        data["mode"] = "RAD"

    # Equals
    elif key == "calc_equals":

        if not data["expr"]:
            result = "0"

        else:
            result = safe_eval(
                data["expr"],
                data["mode"]
            )

        data["history"].append(
            f"{data['expr']} = {result}"
        )

        data["expr"] = str(result)

    # Memory plus
    elif key == "calc_mplus":

        result = safe_eval(
            data["expr"],
            data["mode"]
        )

        if isinstance(result, (int, float)):

            data["memory"] += result

            data["expr"] = str(
                data["memory"]
            )

    # Memory recall
    elif key == "calc_mr":

        data["expr"] = str(
            data["memory"]
        )

    # Integration
    elif key == "calc_integral":

        if not data["expr"]:

            result = "❌ Enter an expression first."

        else:

            result = real_integration(
                data["expr"]
            )

            data["history"].append(result)

        await query.message.edit_text(
            result,
            reply_markup=calculator_keyboard()
        )

        return

    # History
    elif key == "calc_history":

        history = data["history"]

        if history:
            history_text = "\n".join(
                f"{i}. {item}"
                for i, item in enumerate(history, 1)
            )
        else:
            history_text = "No calculations yet."

        await query.message.edit_text(
            "📜 CALCULATOR HISTORY\n\n"
            + history_text,
            reply_markup=calculator_keyboard()
        )

        return

    # Exit
    elif key == "calc_exit":

        user_calc.pop(user_id, None)

        await query.message.edit_text(
            "✅ Calculator closed.\n\n"
            "Use the main menu to open it again."
        )

        return

    # Normal calculator button
    else:

        data["expr"] += key

    await query.message.edit_text(
        calculator_text(data),
        reply_markup=calculator_keyboard()
    )


def calculate_start_handler():
    return start_calculator


def calculate_button_handler():
    return calculator_buttons
