# modules/schedule.py
# Study Scheduler Module - SIMPLE VERSION
# Created by Soza

import datetime

# ========================
# SIMPLE DATA STORAGE
# ========================

# Just use a dictionary - simple!
schedule = {}

# ========================
# CORE FUNCTIONS - SIMPLE
# ========================

def get_todays_schedule():
    """Show today's schedule - SIMPLE"""
    today = datetime.datetime.now().strftime("%A")  # "Monday"
    
    if today not in schedule:
        return "📅 No schedule for today.\nAdd with: /add_session"
    
    result = f"📅 Today ({today}):\n"
    for i, item in enumerate(schedule[today], 1):
        result += f"{i}. {item}\n"
    
    return result


def add_session(day, time, subject):
    """Add one session - SIMPLE"""
    day = day.capitalize()
    
    # Check day is valid
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", 
            "Friday", "Saturday", "Sunday"]
    
    if day not in days:
        return f"❌ Use: Monday, Tuesday, etc."
    
    # Add to schedule
    if day not in schedule:
        schedule[day] = []
    
    session = f"{time} - {subject}"
    schedule[day].append(session)
    
    # Sort by time
    schedule[day].sort()
    
    return f"✅ Added: {session}"


def show_week():
    """Show whole week - SIMPLE"""
    if not schedule:
        return "📅 Schedule empty.\nAdd with: /add_session"
    
    result = "📅 Weekly Schedule:\n"
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", 
                "Friday", "Saturday", "Sunday"]:
        if day in schedule and schedule[day]:
            result += f"\n{day}:\n"
            for session in schedule[day]:
                result += f"  • {session}\n"
    
    return result


def clear_day(day):
    """Clear one day - SIMPLE"""
    day = day.capitalize()
    
    if day in schedule:
        schedule[day] = []
        return f"✅ Cleared {day}"
    else:
        return f"📅 {day} already empty"


def count_sessions():
    """Count total sessions - SIMPLE"""
    total = sum(len(sessions) for sessions in schedule.values())
    return f"📊 Total sessions: {total}"


