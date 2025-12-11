import math
import sympy as sp
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# =========================
# USER DATA STORAGE
# =========================
user_calc = {}

# =========================
# SAFE MATH + REAL INTEGRATION
# =========================
def safe_eval(expr, mode="DEG"):
    try:
        expr = expr.replace("÷", "/").replace("×", "*").replace("^", "**")

        # DEG / RAD handling
        if mode == "DEG":
            sin = lambda x: math.sin(math.radians(x))
            cos = lambda x: math.cos(math.radians(x))
            tan = lambda x: math.tan(math.radians(x))
        else:
            sin = math.sin
            cos = math.cos
            tan = math.tan

        def safe_factorial(x):
            if not float(x).is_integer() or x < 0:
                raise ValueError("Factorial only for whole numbers")
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
            "factorial": safe_factorial,
            "abs": abs,
            "sum": sum
        }

        return eval(expr, {"__builtins__": None}, safe_dict)

    except ZeroDivisionError:
        return "Error: Division by zero happen undefined "
    except SyntaxError:
        return "Error: Wrong format or input"
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception:
        return "Calculation error"


# =========================
# REAL INTEGRATION ENGINE 
#for this integration uses this form x**2 Then presses the ∫ button BOT OUTPUT ∫ x**2 dx = x**3/3
# ==========================
def real_integration(expression):
    try:
        x = sp.symbols('x')
        expr = sp.sympify(expression)
        result = sp.integrate(expr, x)
        return f"∫ {expression} dx = {result}"
    except Exception:
        return "Integration error (use x as variable)"


# =========================
# KEYBOARD LAYOUT (MOBILE)
# =========================
def calculator_keyboard():
    keys = [
        [("Rad", "Rad"), ("Deg", "Deg"), ("⌫", "⌫"), ("C", "C")],
        [("sin", "sin("), ("cos", "cos("), ("tan", "tan("), ("√", "sqrt(")],
        [("sin⁻¹", "asin("), ("cos⁻¹", "acos("), ("tan⁻¹", "atan("), ("!", "factorial(")],
        [("log", "log("), ("ln", "ln("), ("π", "pi"), ("e", "e")],
        [("(", "("), (")", ")"), ("^", "^"), ("%", "%")],
        [("7", "7"), ("8", "8"), ("9", "÷")],
        [("4", "4"), ("5", "5"), ("6", "×")],
        [("1", "1"), ("2", "2"), ("3", "-")],
        [("0", "0"), (".", "."), ("=", "="), ("+", "+")],
        [("M+", "M+"), ("MR", "MR"), ("Σ", "SUM"), ("∫", "INT")],
        [("History", "HISTORY"), ("Exit", "EXIT")]
    ]

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text=t, callback_data=d) for t, d in row]
        for row in keys
    ])


# =========================
# START CALCULATOR
# =========================
async def start_calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    user_calc[user_id] = {
        "expr": "",
        "mode": "DEG",
        "history": [],
        "memory": 0
    }

    await update.message.reply_text(
        "Scientific Calculator\n\nExpression:\n0",
        reply_markup=calculator_keyboard()
    )


# =========================
# BUTTON HANDLER
# =========================
async def calculator_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    key = query.data

    if user_id not in user_calc:
        return

    data = user_calc[user_id]

    # CLEAR
    if key == "C":
        data["expr"] = ""

    # BACKSPACE
    elif key == "⌫":
        data["expr"] = data["expr"][:-1]

    # MODE
    elif key == "Deg":
        data["mode"] = "DEG"

    elif key == "Rad":
        data["mode"] = "RAD"

    # MEMORY ADD
    elif key == "M+":
        result = safe_eval(data["expr"], data["mode"])
        if isinstance(result, (int, float)):
            data["memory"] += result
            data["expr"] = str(data["memory"])

    # MEMORY READ
    elif key == "MR":
        data["expr"] = str(data["memory"])

    # SUMMATION HELP
    elif key == "SUM":
        await query.message.edit_text(
            "Use format:  sum([1,2,3,4])",
            reply_markup=calculator_keyboard()
        )
        return

    # REAL INTEGRATION
    elif key == "INT":
        result = real_integration(data["expr"])
        data["history"].append(result)
        data["expr"] = ""
        await query.message.edit_text(
            result,
            reply_markup=calculator_keyboard()
        )
        return

    # EQUAL
    elif key == "=":
        result = safe_eval(data["expr"], data["mode"])
        data["history"].append(f"{data['expr']} = {result}")
        data["expr"] = str(result)

    # HISTORY
    elif key == "HISTORY":
        history_text = "\n".join(data["history"]) or "No history yet."
        await query.message.edit_text(
            f"History:\n{history_text}",
            reply_markup=calculator_keyboard()
        )
        return

    # EXIT
    elif key == "EXIT":
        del user_calc[user_id]
        await query.message.edit_text("Calculator Closed")
        return

    # NORMAL KEYS
    else:
        data["expr"] += key

    text = f" Mode: {data['mode']}\n\nExpression:\n{data['expr'] or '0'}"
    await query.message.edit_text(text, reply_markup=calculator_keyboard())


# =========================
# EXPORT HANDLERS
# =========================
def calculate_start_handler():
    return start_calculator

def calculate_button_handler():
    return calculator_buttons
