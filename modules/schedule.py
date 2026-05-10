# modules/schedule.py - USER-SPECIFIC VERSION
import datetime
import json
import os

# ========================
# USER-SPECIFIC DATA STORAGE
# ========================

# Dictionary of user schedules: {user_id: schedule_dict}
user_schedules = {}

def get_user_file(user_id):
    """Get user-specific schedule file"""
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, f"schedule_{user_id}.json")

def load_user_schedule(user_id):
    """Load schedule for specific user"""
    user_file = get_user_file(user_id)
    if os.path.exists(user_file):
        with open(user_file, "r") as f:
            return json.load(f)
    return {}

def save_user_schedule(user_id, schedule_data):
    """Save schedule for specific user"""
    user_file = get_user_file(user_id)
    with open(user_file, "w") as f:
        json.dump(schedule_data, f, indent=2)

# ========================
# CORE FUNCTIONS - USER-SPECIFIC
# ========================

def get_todays_schedule(user_id):
    """Show today's schedule for specific user"""
    schedule = load_user_schedule(user_id)
    today = datetime.datetime.now().strftime("%A")  # "Monday"
    
    if today not in schedule:
        return "📅 No schedule for today.\nAdd with: /add_session"
    
    result = f"📅 Today ({today}):\n"
    for i, session in enumerate(schedule[today], 1):
        result += f"{i}. {session}\n"
    
    return result


def add_session(user_id, day, time, subject):
    """Add one session for specific user"""
    day = day.capitalize()
    
    # Check day is valid
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", 
            "Friday", "Saturday", "Sunday"]
    
    if day not in days:
        return f"❌ Use: Monday, Tuesday, etc."
    
    # Load user's schedule
    schedule = load_user_schedule(user_id)
    
    # Add to schedule
    if day not in schedule:
        schedule[day] = []
    
    session = f"{time} - {subject}"
    schedule[day].append(session)
    
    # Sort by time
    schedule[day].sort()
    
    # Save back
    save_user_schedule(user_id, schedule)
    
    return f"✅ Added: {session}"


def show_week(user_id):
    """Show whole week for specific user"""
    schedule = load_user_schedule(user_id)
    
    if not schedule:
        return "📅 Schedule empty.\nAdd with: /add_session"
    
    result = "📅 Your Weekly Schedule:\n"
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", 
                "Friday", "Saturday", "Sunday"]:
        if day in schedule and schedule[day]:
            result += f"\n{day}:\n"
            for session in schedule[day]:
                result += f"  • {session}\n"
        else:
            result += f"\n{day}: No sessions\n"
    
    return result


def clear_day(user_id, day):
    """Clear one day for specific user"""
    day = day.capitalize()
    schedule = load_user_schedule(user_id)
    
    if day in schedule:
        schedule[day] = []
        save_user_schedule(user_id, schedule)
        return f"✅ Cleared {day}"
    else:
        return f"📅 {day} already empty"


def count_sessions(user_id):
    """Count total sessions for specific user"""
    schedule = load_user_schedule(user_id)
    total = sum(len(sessions) for sessions in schedule.values())
    return f"📊 Your total sessions: {total}"