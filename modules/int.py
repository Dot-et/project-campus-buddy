# modules/int.py
# Campus Buddy - Integration Calculator

import sympy as sp


def integrate(expression):
    """Calculate the indefinite integral of an expression."""

    try:
        expression = expression.strip()

        if not expression:
            return "❌ Please enter an expression."

        x = sp.symbols("x")

        expression = expression.replace("^", "**")

        expr = sp.sympify(expression)

        result = sp.integrate(expr, x)

        return (
            "∫ INTEGRATION RESULT\n\n"
            f"📐 ∫ {expression} dx\n\n"
            f"✅ Result:\n{result} + C"
        )

    except Exception:
        return (
            "❌ Integration error.\n\n"
            "Use x as the variable.\n"
            "Example: x^2 + 2*x"
        )


def definite_integral(expression, lower, upper):
    """Calculate a definite integral."""

    try:
        expression = expression.strip()

        x = sp.symbols("x")

        expression = expression.replace("^", "**")

        expr = sp.sympify(expression)

        lower = float(lower)
        upper = float(upper)

        result = sp.integrate(
            expr,
            (x, lower, upper)
        )

        return (
            "∫ DEFINITE INTEGRAL\n\n"
            f"📐 Expression: {expression}\n"
            f"🔽 Lower: {lower:g}\n"
            f"🔼 Upper: {upper:g}\n\n"
            f"✅ Result: {result}"
        )

    except Exception:
        return "❌ Could not calculate the definite integral."


def integration_help():
    return (
        "∫ INTEGRATION CALCULATOR\n\n"
        "Enter an expression using x.\n\n"
        "Examples:\n"
        "• x^2\n"
        "• 2*x + 5\n"
        "• sin(x)\n"
        "• x^3 + 4*x\n\n"
        "The result is returned with + C."
    )
