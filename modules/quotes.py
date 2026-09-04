# modules/quotes.py
# Campus Buddy - Quotes & Study Tips

import random


QUOTES = [
    "Success is the sum of small efforts, repeated day in and day out.",
    "The secret of getting ahead is getting started.",
    "Don't watch the clock; do what it does. Keep going.",
    "Believe you can and you're halfway there.",
    "Great things are done by a series of small things brought together.",
    "Success doesn't come from what you do occasionally. It comes from what you do consistently.",
    "The future depends on what you do today.",
    "Every expert was once a beginner.",
    "Small progress is still progress.",
    "Your only limit is your determination."
]


STUDY_TIPS = [
    "📚 Study in short focused sessions and take regular breaks.",
    "📝 Write down the most important points after each study session.",
    "🔕 Turn off unnecessary notifications while studying.",
    "🧠 Try to explain what you learned without looking at your notes.",
    "⏰ Create a realistic study schedule and follow it consistently.",
    "💧 Stay hydrated and get enough sleep before an exam.",
    "🔄 Review difficult topics regularly instead of studying them only once.",
    "🎯 Set one clear goal before starting each study session.",
    "📖 Practice with questions instead of only reading your notes.",
    "💪 Don't be discouraged by difficult subjects. Practice improves understanding."
]


def get_random_quote():
    quote = random.choice(QUOTES)

    return (
        "💬 DAILY MOTIVATION\n\n"
        f"“{quote}”\n\n"
        "— Campus Buddy"
    )


def get_random_tip():
    tip = random.choice(STUDY_TIPS)

    return (
        "💡 STUDY TIP\n\n"
        f"{tip}"
    )


def get_quote():
    return get_random_quote()


def get_tip():
    return get_random_tip()


def get_all_quotes():
    message = "💬 MOTIVATIONAL QUOTES\n\n"

    for i, quote in enumerate(QUOTES, 1):
        message += f"{i}. “{quote}”\n\n"

    return message


def get_all_tips():
    message = "💡 STUDY TIPS\n\n"

    for i, tip in enumerate(STUDY_TIPS, 1):
        message += f"{i}. {tip}\n\n"

    return message
