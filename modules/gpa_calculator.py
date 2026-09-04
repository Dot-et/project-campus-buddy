# modules/gpa_calculator.py
# Campus Buddy - Ethiopian GPA Calculator

GRADE_POINTS = {
    "A+": 4.0,
    "A": 4.0,
    "A-": 3.75,
    "B+": 3.5,
    "B": 3.0,
    "B-": 2.75,
    "C+": 2.5,
    "C": 2.0,
    "C-": 1.75,
    "D": 1.0,
    "F": 0.0,
}


def calculate_gpa(courses):
    """
    courses format:
    [
        ("Software Engineering", 3, "A"),
        ("Database", 3, "B+")
    ]
    """

    if not courses:
        return "❌ No courses provided."

    total_points = 0
    total_credits = 0

    for course in courses:
        if len(course) != 3:
            return "❌ Invalid course format."

        name, credit, grade = course

        try:
            credit = float(credit)
        except ValueError:
            return f"❌ Invalid credit for {name}."

        grade = grade.upper().strip()

        if grade not in GRADE_POINTS:
            return f"❌ Invalid grade: {grade}"

        total_points += credit * GRADE_POINTS[grade]
        total_credits += credit

    if total_credits == 0:
        return "❌ Total credit cannot be zero."

    gpa = total_points / total_credits

    return (
        "🎓 GPA RESULT\n\n"
        f"📚 Total Credits: {total_credits:g}\n"
        f"📊 GPA: {gpa:.2f} / 4.00\n\n"
        f"{gpa_message(gpa)}"
    )


def gpa_message(gpa):
    if gpa >= 3.75:
        return "🏆 Excellent performance!"
    elif gpa >= 3.00:
        return "🌟 Very good performance!"
    elif gpa >= 2.50:
        return "👍 Good performance!"
    elif gpa >= 2.00:
        return "📖 Keep working hard."
    else:
        return "💪 Don't give up. You can improve!"


def grade_point(grade):
    grade = grade.upper().strip()

    if grade not in GRADE_POINTS:
        return None

    return GRADE_POINTS[grade]


def show_grade_scale():
    message = "🎓 GPA GRADE SCALE\n\n"

    for grade, point in GRADE_POINTS.items():
        message += f"{grade} → {point:.2f}\n"

    return message


def calculate_single_course(credit, grade):
    try:
        credit = float(credit)
    except ValueError:
        return "❌ Credit must be a number."

    point = grade_point(grade)

    if point is None:
        return "❌ Invalid grade."

    return (
        f"📘 Grade: {grade.upper()}\n"
        f"📚 Credit: {credit:g}\n"
        f"⭐ Grade Point: {point:.2f}\n"
        f"📊 Quality Point: {credit * point:.2f}"
    )


def calculate_cumulative_gpa(previous_gpa, previous_credits, new_courses):
    try:
        previous_gpa = float(previous_gpa)
        previous_credits = float(previous_credits)
    except ValueError:
        return "❌ Invalid previous GPA or credits."

    if previous_credits < 0:
        return "❌ Credits cannot be negative."

    if previous_gpa < 0 or previous_gpa > 4:
        return "❌ GPA must be between 0 and 4."

    if not new_courses:
        return "❌ No new courses provided."

    new_points = 0
    new_credits = 0

    for course in new_courses:
        name, credit, grade = course

        try:
            credit = float(credit)
        except ValueError:
            return f"❌ Invalid credit for {name}."

        point = grade_point(grade)

        if point is None:
            return f"❌ Invalid grade for {name}: {grade}"

        new_points += credit * point
        new_credits += credit

    old_points = previous_gpa * previous_credits

    total_credits = previous_credits + new_credits

    if total_credits == 0:
        return "❌ Total credits cannot be zero."

    cumulative_gpa = (
        old_points + new_points
    ) / total_credits

    return (
        "🎓 CUMULATIVE GPA\n\n"
        f"📊 Previous GPA: {previous_gpa:.2f}\n"
        f"📚 Previous Credits: {previous_credits:g}\n"
        f"➕ New Credits: {new_credits:g}\n"
        f"📈 New Cumulative GPA: {cumulative_gpa:.2f} / 4.00\n\n"
        f"{gpa_message(cumulative_gpa)}"
    )
