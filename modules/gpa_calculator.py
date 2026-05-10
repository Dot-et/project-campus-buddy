# gpa_calculator.py
import json
import os

# =========================
# ORIGINAL CLASS DEFINITIONS
# =========================

class Course:
    """Represents a single course"""
    
    # Grading scale
    GRADE_SCALE = {
        90: ("A", 4.0),
        85: ("A-", 3.7),
        80: ("B+", 3.3),
        75: ("B", 3.0),
        70: ("B-", 2.7),
        65: ("C+", 2.3),
        60: ("C", 2.0),
        55: ("C-", 1.7),
        50: ("D+", 1.3),
        45: ("D", 1.0),
        40: ("D-", 0.7),
        0: ("F", 0.0)
    }
    
    def __init__(self, name: str, score: int, credit: int):
        self.name = name
        self.score = score
        self.credit = credit
        self.letter, self.point = self._calculate_grade()
    
    def _calculate_grade(self):
        """Convert score to letter grade and grade point"""
        for min_score, (letter, point) in self.GRADE_SCALE.items():
            if self.score >= min_score:
                return letter, point
        return "F", 0.0
    
    def __str__(self):
        return f"{self.name}: {self.score}% ({self.letter}, {self.point})"


class Semester:
    """Represents a semester with multiple courses"""
    
    def __init__(self):
        self.courses = []
    
    def add_course(self, course: Course):
        """Add a course to this semester"""
        self.courses.append(course)
    
    def calculate_gpa(self) -> float:
        """Calculate GPA for this semester"""
        if not self.courses:
            return 0.0
        
        total_points = 0
        total_credits = 0
        
        for course in self.courses:
            total_points += course.point * course.credit
            total_credits += course.credit
        
        if total_credits == 0:
            return 0.0
        
        return round(total_points / total_credits, 2)
    
    def summary(self) -> str:
        """Formatted summary of the semester"""
        if not self.courses:
            return "No courses added yet."
        
        text = ""
        for i, course in enumerate(self.courses, 1):
            text += f"{i}. {course.name}\n"
            text += f"   Score: {course.score}/100\n"
            text += f"   Grade: {course.letter}\n"
            text += f"   Credit: {course.credit}\n"
            text += f"   Point: {course.point}\n\n"
        
        text += f"📊 **Semester GPA:** {self.calculate_gpa()}"
        return text

# =========================
# USER-SPECIFIC STORAGE
# =========================

def get_user_file(user_id):
    """Get user-specific GPA data file"""
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, f"gpa_{user_id}.json")

def load_user_semesters(user_id):
    """Load semesters for specific user"""
    user_file = get_user_file(user_id)
    if os.path.exists(user_file):
        with open(user_file, "r") as f:
            return json.load(f)
    return []  # Returns list of semesters

def save_user_semesters(user_id, semesters):
    """Save semesters for specific user"""
    user_file = get_user_file(user_id)
    
    # Convert to serializable format
    serializable = []
    for semester in semesters:
        # Convert Semester object to dict
        semester_dict = {
            "courses": [
                {
                    "name": course.name,
                    "score": course.score,
                    "credit": course.credit,
                    "letter": course.letter,
                    "point": course.point
                }
                for course in semester.courses
            ]
        }
        serializable.append(semester_dict)
    
    with open(user_file, "w") as f:
        json.dump(serializable, f, indent=2)

# =========================
# UPDATED STUDENTGPA CLASS
# =========================

class StudentGPA:
    """Stores semesters and calculates CGPA - USER-SPECIFIC"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.semesters = []  # List of Semester objects
        self.load_from_disk()
    
    def load_from_disk(self):
        """Load semesters from user's file"""
        data = load_user_semesters(self.user_id)
        
        # Convert loaded data back to Semester objects
        for semester_data in data:
            semester = Semester()
            for course_data in semester_data.get("courses", []):
                # Recreate Course objects
                course = Course(
                    name=course_data["name"],
                    score=course_data["score"],
                    credit=course_data["credit"]
                )
                semester.add_course(course)
            self.semesters.append(semester)
    
    def save_to_disk(self):
        """Save semesters to user's file"""
        save_user_semesters(self.user_id, self.semesters)
    
    def add_semester(self, semester: Semester):
        """Add a semester"""
        self.semesters.append(semester)
        self.save_to_disk()
    
    def get_current_semester(self):
        """Get or create current semester"""
        # Always use the last semester as "current"
        if not self.semesters:
            self.semesters.append(Semester())
        return self.semesters[-1]
    
    def calculate_cgpa(self) -> float:
        """Calculate cumulative GPA"""
        total_points = 0
        total_credits = 0

        for semester in self.semesters:
            for course in semester.courses:
                total_points += course.point * course.credit
                total_credits += course.credit

        if total_credits == 0:
            return 0.0

        return round(total_points / total_credits, 2)
    
    def summary(self) -> str:
        """Formatted summary of all semesters"""
        if not self.semesters:
            return "📚 No GPA data yet.\nAdd courses with: /add_course"
        
        text = "🎓 **Your Academic Record**\n"
        text += "━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for i, semester in enumerate(self.semesters, 1):
            text += f"**Semester {i}:**\n"
            text += semester.summary() + "\n\n"
        
        text += "━━━━━━━━━━━━━━━━━━━━\n"
        text += f"📊 **Overall CGPA:** {self.calculate_cgpa()}"
        
        return text

# =========================
# GPA MANAGER (For bot.py)
# =========================

class GPAManager:
    """Manages GPA for all users"""
    
    def __init__(self):
        self.user_gpas = {}  # {user_id: StudentGPA instance}
    
    def get_user_gpa(self, user_id):
        """Get or create GPA calculator for user"""
        if user_id not in self.user_gpas:
            self.user_gpas[user_id] = StudentGPA(user_id)
        return self.user_gpas[user_id]
    
    def add_course(self, user_id, name, score, credit):
        """Add course to user's current semester"""
        gpa_calc = self.get_user_gpa(user_id)
        current_semester = gpa_calc.get_current_semester()
        
        # Create and add course
        course = Course(name, score, credit)
        current_semester.add_course(course)
        
        # Save to disk
        gpa_calc.save_to_disk()
        
        return f"✅ Added: {name} ({score}%, {credit} credits)"
    
    def get_semester_gpa(self, user_id):
        """Get current semester GPA"""
        gpa_calc = self.get_user_gpa(user_id)
        current_semester = gpa_calc.get_current_semester()
        
        if not current_semester.courses:
            return "❌ No courses in current semester."
        
        gpa = current_semester.calculate_gpa()
        return current_semester.summary()
    
    def get_cgpa(self, user_id):
        """Get CGPA"""
        gpa_calc = self.get_user_gpa(user_id)
        cgpa = gpa_calc.calculate_cgpa()
        return f"🎓 **Your CGPA:** {cgpa}"
    
    def new_semester(self, user_id):
        """Start a new semester"""
        gpa_calc = self.get_user_gpa(user_id)
        gpa_calc.semesters.append(Semester())
        gpa_calc.save_to_disk()
        return "📚 New semester started!"