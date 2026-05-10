# modules/assignments.py - USER-SPECIFIC VERSION
import os
import json
from datetime import datetime

# -------------------------------
# USER-SPECIFIC DATA MANAGEMENT
# -------------------------------
def get_user_file(user_id):
    """Get user-specific assignments file"""
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Each user gets their own file
    return os.path.join(data_dir, f"assignments_{user_id}.json")

def load_user_assignments(user_id):
    """Load assignments for specific user"""
    user_file = get_user_file(user_id)
    if os.path.exists(user_file):
        with open(user_file, "r") as file:
            return json.load(file)
    return []

def save_user_assignments(user_id, assignments):
    """Save assignments for specific user"""
    user_file = get_user_file(user_id)
    with open(user_file, "w") as file:
        json.dump(assignments, file, indent=2)

# -------------------------------
# ADD ASSIGNMENT (USER-SPECIFIC)
# -------------------------------
def add_assignment(user_id, task, date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        
        # Load user's assignments
        assignments = load_user_assignments(user_id)
        
        # Add new assignment
        assignments.append({
            "task": task,
            "date": date,
            "status": "Pending"
        })
        
        # Save back
        save_user_assignments(user_id, assignments)
        
        return f"✅ Assignment added!\n📘 {task}\n📅 {date}\n⏳ Status: Pending"
        
    except ValueError:
        return "❌ Invalid date format! Use yyyy-mm-dd."
    except Exception as e:
        return f"❌ Error: {e}"

# -------------------------------
# GET ALL ASSIGNMENTS (USER-SPECIFIC)
# -------------------------------
def get_assignments(user_id):
    assignments = load_user_assignments(user_id)
    
    if not assignments:
        return "📭 No assignments found."
    
    message = "📋 Your Assignments:\n\n"
    for i, assignment in enumerate(assignments, start=1):
        message += f"{i}. 📘 {assignment['task']}\n"
        message += f"   📅 {assignment['date']} | ✅ {assignment['status']}\n\n"
    
    return message

# -------------------------------
# DELETE ASSIGNMENT (USER-SPECIFIC)
# -------------------------------
def delete_assignment(user_id, number):
    assignments = load_user_assignments(user_id)
    
    if not assignments:
        return "❌ No assignments to delete."
    
    if number < 1 or number > len(assignments):
        return "❌ Invalid assignment number."
    
    deleted = assignments.pop(number - 1)
    save_user_assignments(user_id, assignments)
    
    return f"🗑️ Deleted:\n📘 {deleted['task']}\n📅 {deleted['date']}\n✅ {deleted['status']}"

# -------------------------------
# EDIT ASSIGNMENT (USER-SPECIFIC)
# -------------------------------
def edit_assignment(user_id, number, new_task, new_date):
    try:
        datetime.strptime(new_date, "%Y-%m-%d")
        
        assignments = load_user_assignments(user_id)
        
        if not assignments:
            return "❌ No assignments found."
        
        if number < 1 or number > len(assignments):
            return "❌ Invalid assignment number."
        
        # Update assignment
        assignments[number - 1]["task"] = new_task
        assignments[number - 1]["date"] = new_date
        
        save_user_assignments(user_id, assignments)
        
        return f"✏️ Updated!\n📘 {new_task}\n📅 {new_date}\n✅ {assignments[number-1]['status']}"
        
    except ValueError:
        return "❌ Invalid date format! Use yyyy-mm-dd."
    except Exception as e:
        return f"❌ Error: {e}"

# -------------------------------
# MARK AS DONE (USER-SPECIFIC)
# -------------------------------
def mark_done(user_id, number):
    assignments = load_user_assignments(user_id)
    
    if not assignments:
        return "❌ No assignments found."
    
    if number < 1 or number > len(assignments):
        return "❌ Invalid assignment number."
    
    assignments[number - 1]["status"] = "Done"
    save_user_assignments(user_id, assignments)
    
    return f"✅ Marked as Done:\n📘 {assignments[number-1]['task']}"

# -------------------------------
# SEARCH ASSIGNMENT (USER-SPECIFIC)
# -------------------------------
def search_assignment(user_id, keyword):
    assignments = load_user_assignments(user_id)
    
    if not assignments:
        return "❌ No assignments found."
    
    results = []
    for i, assignment in enumerate(assignments, start=1):
        if keyword.lower() in assignment["task"].lower():
            results.append(f"{i}. 📘 {assignment['task']} | 📅 {assignment['date']} | ✅ {assignment['status']}")
    
    if not results:
        return "🔍 No matching assignments found."
    
    return "🔍 Search Results:\n\n" + "\n".join(results)

# -------------------------------
# SHOW UPCOMING ASSIGNMENTS (USER-SPECIFIC)
# -------------------------------
def upcoming_assignments(user_id):
    assignments = load_user_assignments(user_id)
    
    if not assignments:
        return "❌ No assignments found."
    
    today = datetime.now().date()
    upcoming = []
    
    for i, assignment in enumerate(assignments, start=1):
        due_date = datetime.strptime(assignment["date"], "%Y-%m-%d").date()
        
        if due_date >= today and assignment["status"] == "Pending":
            upcoming.append(f"{i}. 📘 {assignment['task']} — 📅 {assignment['date']}")
    
    if not upcoming:
        return "✅ No upcoming assignments!"
    
    return "⏳ Upcoming Assignments:\n\n" + "\n".join(upcoming)

# -------------------------------
# ASSIGNMENT STATISTICS (USER-SPECIFIC)
# -------------------------------
def assignment_stats(user_id):
    assignments = load_user_assignments(user_id)
    
    if not assignments:
        return "❌ No assignments found."
    
    total = len(assignments)
    done = sum(1 for a in assignments if a["status"] == "Done")
    pending = total - done
    
    return (
        "📊 Your Assignment Statistics:\n\n"
        f"📘 Total: {total}\n"
        f"✅ Done: {done}\n"
        f"⏳ Pending: {pending}"
    )



