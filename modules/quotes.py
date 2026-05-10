# modules/quotes.py - 30 DAYS, AUTO-SEND
import datetime

QUOTES = [
    "Day 1: 📚 Small daily improvements = stunning results.",
    "Day 2: 🚀 Start now. Perfect later.",
    "Day 3: 💪 Discipline > motivation.",
    "Day 4: 🎯 Focus on the process.",
    "Day 5: 🔥 Don't watch the clock.",
    "Day 6: 🌟 Believe you can.",
    "Day 7: ⚡ Start small, stay consistent.",
    "Day 8: 📖 Read. Learn. Grow.",
    "Day 9: 🧠 Knowledge is power.",
    "Day 10: 🎓 Education changes everything.",
    "Day 11: 💡 Ideas need action.",
    "Day 12: ✨ You're capable of amazing things.",
    "Day 13: 📈 Progress, not perfection.",
    "Day 14: 🌱 Grow daily.",
    "Day 15: 🏆 Champions keep going.",
    "Day 16: 🌅 Today matters.",
    "Day 17: 💼 Hard work pays.",
    "Day 18: 🧩 Every piece matters.",
    "Day 19: 🌊 Ride the waves.",
    "Day 20: 🎨 Create your future.",
    "Day 21: 🌟 Shine bright.",
    "Day 22: 📝 Write your story.",
    "Day 23: 🧭 Stay on course.",
    "Day 24: 💎 You're a diamond.",
    "Day 25: 🌳 Strong roots, strong future.",
    "Day 26: 🚤 Keep moving forward.",
    "Day 27: 🔑 Consistency is key.",
    "Day 28: 🎪 Life is your classroom.",
    "Day 29: 🌌 Dream big, act now.",
    "Day 30: 🏁 Finish strong!"
]

def get_todays_quote():
    """Get today's unique quote (cycles every 30 days)"""
    day_of_month = datetime.datetime.now().day  # 1-31
    quote_index = (day_of_month - 1) % 30  # 0-29
    return QUOTES[quote_index]