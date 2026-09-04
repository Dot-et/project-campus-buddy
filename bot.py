# ============================================================
# CAMPUS BUDDY BOT
# Professional Student Productivity Assistant
# ============================================================

import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import BOT_TOKEN

from modules import schedule
from modules import assignments
from modules import calculator
from modules import gpa_calculator
from modules import citation
from modules import dictionary
from modules import pomodoro_timer
from modules import quotes
from modules import exam_countdown
from modules import int as integration


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ============================================================
# USER STATE
# ============================================================

user_state = {}


def get_state(user_id):
    if user_id not in user_state:
        user_state[user_id] = {
            "action": None,
            "data": {},
        }

    return user_state[user_id]


def clear_action(user_id):
    state = get_state(user_id)
    state["action"] = None
    state["data"] = {}


# ============================================================
# MAIN MENU
# ============================================================

def main_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "📚 Assignments",
                callback_data="menu_assignments"
            ),
            InlineKeyboardButton(
                "📅 Schedule",
                callback_data="menu_schedule"
            ),
        ],

        [
            InlineKeyboardButton(
                "🎓 GPA Calculator",
                callback_data="menu_gpa"
            ),
            InlineKeyboardButton(
                "🧮 Calculator",
                callback_data="menu_calculator"
            ),
        ],

        [
            InlineKeyboardButton(
                "📖 Dictionary",
                callback_data="menu_dictionary"
            ),
            InlineKeyboardButton(
                "📑 Citations",
                callback_data="menu_citation"
            ),
        ],

        [
            InlineKeyboardButton(
                "🍅 Pomodoro",
                callback_data="menu_pomodoro"
            ),
            InlineKeyboardButton(
                "⏳ Exam Countdown",
                callback_data="menu_exam"
            ),
        ],

        [
            InlineKeyboardButton(
                "∫ Integration",
                callback_data="menu_integration"
            ),
            InlineKeyboardButton(
                "💡 Motivation",
                callback_data="menu_motivation"
            ),
        ],

        [
            InlineKeyboardButton(
                "📊 My Dashboard",
                callback_data="menu_dashboard"
            ),
        ],

        [
            InlineKeyboardButton(
                "ℹ️ Help",
                callback_data="menu_help"
            ),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def back_button():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🏠 Main Menu",
                callback_data="back_home"
            )
        ]
    ])


# ============================================================
# START
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    clear_action(user.id)

    text = (
        "🎓 <b>WELCOME TO CAMPUS BUDDY</b>\n\n"
        f"Hello <b>{user.first_name}</b>! 👋\n\n"

        "Your personal academic productivity assistant.\n\n"

        "🚀 <b>What can I help you with?</b>\n\n"

        "📚 Manage assignments\n"
        "📅 Organize your schedule\n"
        "🎓 Calculate your GPA\n"
        "🧮 Scientific calculations\n"
        "📖 Look up English words\n"
        "📑 Generate citations\n"
        "🍅 Focus with Pomodoro\n"
        "⏳ Track your exams\n"
        "∫ Calculate integrations\n"
        "💡 Get study motivation\n\n"

        "<i>Select a feature below to get started.</i>"
    )

    await update.effective_message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_menu()
    )


# ============================================================
# HOME
# ============================================================

async def show_home(query):

    text = (
        "🎓 <b>CAMPUS BUDDY</b>\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🧠 <b>YOUR ACADEMIC ASSISTANT</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"

        "📚 Study smarter.\n"
        "📅 Stay organized.\n"
        "🎯 Reach your goals.\n\n"

        "Choose a tool below:"
    )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=main_menu()
    )


# ============================================================
# ASSIGNMENTS
# ============================================================

def assignments_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "➕ Add Assignment",
                callback_data="assignment_add"
            )
        ],

        [
            InlineKeyboardButton(
                "📋 View Assignments",
                callback_data="assignment_view"
            )
        ],

        [
            InlineKeyboardButton(
                "⏳ Upcoming",
                callback_data="assignment_upcoming"
            ),
            InlineKeyboardButton(
                "📊 Statistics",
                callback_data="assignment_stats"
            ),
        ],

        [
            InlineKeyboardButton(
                "✅ Mark Done",
                callback_data="assignment_done"
            ),
            InlineKeyboardButton(
                "🗑️ Delete",
                callback_data="assignment_delete"
            ),
        ],

        [
            InlineKeyboardButton(
                "🏠 Main Menu",
                callback_data="back_home"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


async def show_assignments_menu(query):

    text = (
        "📚 <b>ASSIGNMENT MANAGER</b>\n\n"

        "Keep track of your academic tasks.\n\n"

        "➕ Add new work\n"
        "📋 View your assignments\n"
        "⏳ Check upcoming deadlines\n"
        "✅ Mark completed work\n"
        "📊 Track your progress"
    )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=assignments_menu()
    )


# ============================================================
# SCHEDULE
# ============================================================

def schedule_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "➕ Add Session",
                callback_data="schedule_add"
            )
        ],

        [
            InlineKeyboardButton(
                "📅 Today",
                callback_data="schedule_today"
            ),
            InlineKeyboardButton(
                "🗓️ This Week",
                callback_data="schedule_week"
            ),
        ],

        [
            InlineKeyboardButton(
                "📊 Count Sessions",
                callback_data="schedule_count"
            )
        ],

        [
            InlineKeyboardButton(
                "🗑️ Clear Schedule",
                callback_data="schedule_clear"
            )
        ],

        [
            InlineKeyboardButton(
                "🏠 Main Menu",
                callback_data="back_home"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


async def show_schedule_menu(query):

    text = (
        "📅 <b>SCHEDULE MANAGER</b>\n\n"

        "Plan your academic life with ease.\n\n"

        "➕ Add study sessions\n"
        "📅 View today's schedule\n"
        "🗓️ View your weekly schedule\n"
        "📊 Count study sessions\n"
        "🗑️ Clear your schedule"
    )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=schedule_menu()
    )


# ============================================================
# GPA
# ============================================================

def gpa_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🎓 Grade Scale",
                callback_data="gpa_scale"
            )
        ],

        [
            InlineKeyboardButton(
                "🧮 Calculate GPA",
                callback_data="gpa_calculate"
            )
        ],

        [
            InlineKeyboardButton(
                "📈 Cumulative GPA",
                callback_data="gpa_cumulative"
            )
        ],

        [
            InlineKeyboardButton(
                "🏠 Main Menu",
                callback_data="back_home"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


async def show_gpa_menu(query):

    text = (
        "🎓 <b>ETHIOPIAN GPA CALCULATOR</b>\n\n"

        "Calculate your academic performance quickly.\n\n"

        "⭐ Supports A+ to F\n"
        "📚 Credit-based calculation\n"
        "📈 Cumulative GPA calculation\n\n"

        "Choose an option:"
    )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=gpa_menu()
    )


# ============================================================
# POMODORO
# ============================================================

def pomodoro_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "⚡ 15 Minutes",
                callback_data="pomo_15"
            ),
            InlineKeyboardButton(
                "🍅 25 Minutes",
                callback_data="pomo_25"
            ),
        ],

        [
            InlineKeyboardButton(
                "🔥 50 Minutes",
                callback_data="pomo_50"
            )
        ],

        [
            InlineKeyboardButton(
                "📊 Status",
                callback_data="pomo_status"
            ),
            InlineKeyboardButton(
                "🛑 Stop",
                callback_data="pomo_stop"
            ),
        ],

        [
            InlineKeyboardButton(
                "🏠 Main Menu",
                callback_data="back_home"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


async def show_pomodoro_menu(query):

    text = (
        "🍅 <b>POMODORO FOCUS</b>\n\n"

        "Turn your study time into focused sessions.\n\n"

        "⚡ 15 min — Quick focus\n"
        "🍅 25 min — Classic Pomodoro\n"
        "🔥 50 min — Deep focus\n\n"

        "Choose your focus session:"
    )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=pomodoro_menu()
    )


# ============================================================
# MOTIVATION
# ============================================================

def motivation_menu():

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "💬 Motivation",
                callback_data="mot_quote"
            ),

            InlineKeyboardButton(
                "💡 Study Tip",
                callback_data="mot_tip"
            )
        ],

        [
            InlineKeyboardButton(
                "📚 All Tips",
                callback_data="mot_all_tips"
            )
        ],

        [
            InlineKeyboardButton(
                "🏠 Main Menu",
                callback_data="back_home"
            )
        ]

    ])


async def show_motivation_menu(query):

    text = (
        "💡 <b>MOTIVATION CENTER</b>\n\n"

        "A little motivation can change your study session.\n\n"

        "💬 Get motivation\n"
        "💡 Get study tips\n"
        "📚 View all study tips"
    )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=motivation_menu()
    )


# ============================================================
# DASHBOARD
# ============================================================

async def show_dashboard(query):

    user_id = query.from_user.id

    assignment_text = assignments.get_assignments(user_id)

    assignment_count = assignment_text.count("📘")

    session_text = schedule.count_sessions(user_id)

    try:
        session_count = int(
            session_text.split(":")[-1].strip()
        )
    except Exception:
        session_count = 0

    exam_text = exam_countdown.get_exam(user_id)

    if "No exam" in exam_text:
        exam_status = "📭 No exam countdown"
    else:
        exam_status = "⏳ Exam countdown active"

    text = (
        "📊 <b>MY CAMPUS DASHBOARD</b>\n\n"

        "━━━━━━━━━━━━━━━━━━\n"
        "📚 <b>STUDY OVERVIEW</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"

        f"📝 Assignments: <b>{assignment_count}</b>\n"
        f"📅 Study Sessions: <b>{session_count}</b>\n"
        f"{exam_status}\n\n"

        "🎯 <b>Keep moving forward!</b>\n"
        "Every small study session counts."
    )

    keyboard = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "🔄 Refresh",
                callback_data="menu_dashboard"
            )
        ],

        [
            InlineKeyboardButton(
                "🏠 Main Menu",
                callback_data="back_home"
            )
        ]

    ])

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=keyboard
    )


# ============================================================
# HELP
# ============================================================

async def show_help(query):

    text = (
        "ℹ️ <b>CAMPUS BUDDY HELP</b>\n\n"

        "🎓 Campus Buddy helps students manage "
        "their academic life from one place.\n\n"

        "<b>Available tools:</b>\n\n"

        "📚 Assignment Manager\n"
        "📅 Schedule Manager\n"
        "🎓 GPA Calculator\n"
        "🧮 Scientific Calculator\n"
        "📖 Dictionary\n"
        "📑 Citation Manager\n"
        "🍅 Pomodoro Timer\n"
        "⏳ Exam Countdown\n"
        "∫ Integration Calculator\n"
        "💡 Motivation Center\n\n"

        "Use the buttons to navigate through Campus Buddy."
    )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=back_button()
    )


# ============================================================
# TEXT INPUT HANDLER
# ============================================================

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    text = update.message.text.strip()

    state = get_state(user_id)
    action = state["action"]


    # --------------------------------------------------------
    # ASSIGNMENT ADD
    # --------------------------------------------------------

    if action == "assignment_add":

        parts = text.split("|")

        if len(parts) != 2:

            await update.message.reply_text(
                "❌ <b>Invalid format.</b>\n\n"
                "Use:\n"
                "<code>Assignment name | YYYY-MM-DD</code>",
                parse_mode="HTML"
            )

            return

        task = parts[0].strip()
        date = parts[1].strip()

        result = assignments.add_assignment(
            user_id,
            task,
            date
        )

        clear_action(user_id)

        await update.message.reply_text(
            result,
            reply_markup=assignments_menu()
        )

        return


    # --------------------------------------------------------
    # ASSIGNMENT DELETE
    # --------------------------------------------------------

    if action == "assignment_delete":

        try:
            number = int(text)

        except ValueError:

            await update.message.reply_text(
                "❌ Enter a valid assignment number."
            )

            return

        result = assignments.delete_assignment(
            user_id,
            number
        )

        clear_action(user_id)

        await update.message.reply_text(
            result,
            reply_markup=assignments_menu()
        )

        return


    # --------------------------------------------------------
    # ASSIGNMENT DONE
    # --------------------------------------------------------

    if action == "assignment_done":

        try:
            number = int(text)

        except ValueError:

            await update.message.reply_text(
                "❌ Enter a valid assignment number."
            )

            return

        result = assignments.mark_done(
            user_id,
            number
        )

        clear_action(user_id)

        await update.message.reply_text(
            result,
            reply_markup=assignments_menu()
        )

        return


    # --------------------------------------------------------
    # SCHEDULE ADD
    # --------------------------------------------------------

    if action == "schedule_add":

        parts = text.split("|")

        if len(parts) != 3:

            await update.message.reply_text(
                "❌ <b>Invalid format.</b>\n\n"
                "Use:\n"
                "<code>Monday | 10:00 | Database</code>",
                parse_mode="HTML"
            )

            return

        day = parts[0].strip()
        time = parts[1].strip()
        subject = parts[2].strip()

        result = schedule.add_session(
            user_id,
            day,
            time,
            subject
        )

        clear_action(user_id)

        await update.message.reply_text(
            result,
            reply_markup=schedule_menu()
        )

        return


    # --------------------------------------------------------
    # DICTIONARY
    # --------------------------------------------------------

    if action == "dictionary":

        result = await dictionary.lookup_word(text)

        clear_action(user_id)

        await update.message.reply_text(
            result,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([

                [
                    InlineKeyboardButton(
                        "🔎 Search Again",
                        callback_data="dictionary_search"
                    )
                ],

                [
                    InlineKeyboardButton(
                        "🏠 Main Menu",
                        callback_data="back_home"
                    )
                ]

            ])
        )

        return


    # --------------------------------------------------------
    # INTEGRATION
    # --------------------------------------------------------

    if action == "integration":

        result = integration.integrate(text)

        clear_action(user_id)

        await update.message.reply_text(
            result,
            reply_markup=back_button()
        )

        return


    # --------------------------------------------------------
    # GPA CALCULATOR
    # --------------------------------------------------------

    if action == "gpa_calculate":

        if text.lower() == "done":

            courses = state["data"].get(
                "courses",
                []
            )

            result = gpa_calculator.calculate_gpa(
                courses
            )

            clear_action(user_id)

            await update.message.reply_text(
                result,
                reply_markup=gpa_menu()
            )

            return


        parts = text.split("|")

        if len(parts) != 3:

            await update.message.reply_text(
                "❌ Invalid format.\n\n"
                "Use:\n"
                "<code>Database | 3 | A</code>\n\n"
                "When finished, send:\n"
                "<code>done</code>",
                parse_mode="HTML"
            )

            return


        name = parts[0].strip()
        credit = parts[1].strip()
        grade = parts[2].strip().upper()


        try:
            float(credit)

        except ValueError:

            await update.message.reply_text(
                "❌ Credit must be a number."
            )

            return


        if gpa_calculator.grade_point(grade) is None:

            await update.message.reply_text(
                "❌ Invalid grade.\n\n"
                "Use grades such as:\n"
                "A+, A, A-, B+, B, B-, C+, C, C-, D, F"
            )

            return


        state["data"]["courses"].append(
            (
                name,
                credit,
                grade
            )
        )


        await update.message.reply_text(
            f"✅ Added: <b>{name}</b>\n"
            f"📚 Credit: {credit}\n"
            f"⭐ Grade: {grade}\n\n"
            "Add another course or send "
            "<code>done</code>.",
            parse_mode="HTML"
        )

        return


    # --------------------------------------------------------
    # CUMULATIVE GPA
    # --------------------------------------------------------

    if action == "gpa_cumulative":

        step = state["data"].get("step")

        if step == "previous_gpa":

            try:
                previous_gpa = float(text)

            except ValueError:

                await update.message.reply_text(
                    "❌ Enter a valid GPA."
                )

                return

            if previous_gpa < 0 or previous_gpa > 4:

                await update.message.reply_text(
                    "❌ GPA must be between 0 and 4."
                )

                return

            state["data"]["previous_gpa"] = previous_gpa
            state["data"]["step"] = "previous_credits"

            await update.message.reply_text(
                "📚 Now enter your previous total credits.\n\n"
                "Example: <code>60</code>",
                parse_mode="HTML"
            )

            return


        if step == "previous_credits":

            try:
                previous_credits = float(text)

            except ValueError:

                await update.message.reply_text(
                    "❌ Enter a valid number of credits."
                )

                return

            if previous_credits < 0:

                await update.message.reply_text(
                    "❌ Credits cannot be negative."
                )

                return

            state["data"]["previous_credits"] = previous_credits
            state["data"]["step"] = "new_courses"

            await update.message.reply_text(
                "📚 Add your new courses.\n\n"
                "Use:\n"
                "<code>Database | 3 | A</code>\n\n"
                "Send <code>done</code> when finished.",
                parse_mode="HTML"
            )

            return


        if step == "new_courses":

            if text.lower() == "done":

                courses = state["data"].get(
                    "courses",
                    []
                )

                if not courses:

                    await update.message.reply_text(
                        "❌ Add at least one new course."
                    )

                    return

                result = gpa_calculator.calculate_cumulative_gpa(

                    state["data"]["previous_gpa"],

                    state["data"]["previous_credits"],

                    courses
                )

                clear_action(user_id)

                await update.message.reply_text(
                    result,
                    reply_markup=gpa_menu()
                )

                return


            parts = text.split("|")

            if len(parts) != 3:

                await update.message.reply_text(
                    "❌ Use:\n"
                    "<code>Database | 3 | A</code>",
                    parse_mode="HTML"
                )

                return


            name = parts[0].strip()
            credit = parts[1].strip()
            grade = parts[2].strip().upper()


            if gpa_calculator.grade_point(grade) is None:

                await update.message.reply_text(
                    "❌ Invalid grade."
                )

                return


            try:
                float(credit)

            except ValueError:

                await update.message.reply_text(
                    "❌ Credit must be a number."
                )

                return


            state["data"]["courses"].append(
                (
                    name,
                    credit,
                    grade
                )
            )


            await update.message.reply_text(
                f"✅ Added: <b>{name}</b>\n"
                f"📚 Credit: {credit}\n"
                f"⭐ Grade: {grade}\n\n"
                "Add another course or send "
                "<code>done</code>.",
                parse_mode="HTML"
            )

            return


    # --------------------------------------------------------
    # EXAM COUNTDOWN
    # --------------------------------------------------------

    if action == "exam":

        parts = text.split("|")

        if len(parts) != 2:

            await update.message.reply_text(
                "❌ <b>Invalid format.</b>\n\n"
                "Use:\n"
                "<code>Database Exam | 2026-09-20</code>",
                parse_mode="HTML"
            )

            return


        exam_name = parts[0].strip()
        exam_date = parts[1].strip()

        result = exam_countdown.set_exam(
            user_id,
            exam_name,
            exam_date
        )

        clear_action(user_id)

        await update.message.reply_text(
            result,
            reply_markup=InlineKeyboardMarkup([

                [
                    InlineKeyboardButton(
                        "🔄 View Countdown",
                        callback_data="exam_view"
                    )
                ],

                [
                    InlineKeyboardButton(
                        "🗑️ Delete",
                        callback_data="exam_delete"
                    )
                ],

                [
                    InlineKeyboardButton(
                        "🏠 Main Menu",
                        callback_data="back_home"
                    )
                ]

            ])
        )

        return


    # --------------------------------------------------------
    # DEFAULT
    # --------------------------------------------------------

    await update.message.reply_text(
        "👋 Please use the buttons below "
        "to choose a feature.",
        reply_markup=main_menu()
    )


# ============================================================
# BUTTON HANDLER
# ============================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    user_id = query.from_user.id
    data = query.data

    state = get_state(user_id)


    # ========================================================
    # HOME
    # ========================================================

    if data == "back_home":

        clear_action(user_id)

        await show_home(query)

        return


    # ========================================================
    # ASSIGNMENTS MENU
    # ========================================================

    if data == "menu_assignments":

        clear_action(user_id)

        await show_assignments_menu(query)

        return


    # ========================================================
    # SCHEDULE MENU
    # ========================================================

    if data == "menu_schedule":

        clear_action(user_id)

        await show_schedule_menu(query)

        return


    # ========================================================
    # GPA MENU
    # ========================================================

    if data == "menu_gpa":

        clear_action(user_id)

        await show_gpa_menu(query)

        return


    # ========================================================
    # POMODORO MENU
    # ========================================================

    if data == "menu_pomodoro":

        clear_action(user_id)

        await show_pomodoro_menu(query)

        return


    # ========================================================
    # MOTIVATION MENU
    # ========================================================

    if data == "menu_motivation":

        clear_action(user_id)

        await show_motivation_menu(query)

        return


    # ========================================================
    # DASHBOARD
    # ========================================================

    if data == "menu_dashboard":

        clear_action(user_id)

        await show_dashboard(query)

        return


    # ========================================================
    # HELP
    # ========================================================

    if data == "menu_help":

        clear_action(user_id)

        await show_help(query)

        return


    # ========================================================
    # CALCULATOR
    # ========================================================

    if data == "menu_calculator":

        clear_action(user_id)

        await calculator.start_calculator(
            update,
            context
        )

        return


    if (
        data.startswith("calc_")
        or data in [
            "sin(",
            "cos(",
            "tan(",
            "sqrt(",
            "asin(",
            "acos(",
            "atan(",
            "factorial(",
            "log(",
            "ln(",
            "pi",
            "e",
            "(",
            ")",
            "^",
            "%",
            "7",
            "8",
            "9",
            "÷",
            "4",
            "5",
            "6",
            "×",
            "1",
            "2",
            "3",
            "-",
            "0",
            ".",
            "+"
        ]
    ):

        await calculator.calculator_buttons(
            update,
            context
        )

        return


    # ========================================================
    # ASSIGNMENT ADD
    # ========================================================

    if data == "assignment_add":

        state["action"] = "assignment_add"

        await query.edit_message_text(

            "➕ <b>ADD ASSIGNMENT</b>\n\n"

            "Send it in this format:\n\n"

            "<code>Database Project | 2026-09-15</code>\n\n"

            "📅 Date format: YYYY-MM-DD",

            parse_mode="HTML",

            reply_markup=back_button()
        )

        return


    # ========================================================
    # ASSIGNMENT VIEW
    # ========================================================

    if data == "assignment_view":

        result = assignments.get_assignments(
            user_id
        )

        await query.edit_message_text(
            result,
            reply_markup=assignments_menu()
        )

        return


    # ========================================================
    # UPCOMING ASSIGNMENTS
    # ========================================================

    if data == "assignment_upcoming":

        result = assignments.upcoming_assignments(
            user_id
        )

        await query.edit_message_text(
            result,
            reply_markup=assignments_menu()
        )

        return


    # ========================================================
    # ASSIGNMENT STATISTICS
    # ========================================================

    if data == "assignment_stats":

        result = assignments.assignment_stats(
            user_id
        )

        await query.edit_message_text(
            result,
            reply_markup=assignments_menu()
        )

        return


    # ========================================================
    # ASSIGNMENT DELETE
    # ========================================================

    if data == "assignment_delete":

        state["action"] = "assignment_delete"

        await query.edit_message_text(

            "🗑️ <b>DELETE ASSIGNMENT</b>\n\n"

            "Send the assignment number.\n\n"

            "Example: <code>2</code>",

            parse_mode="HTML",

            reply_markup=back_button()
        )

        return


    # ========================================================
    # ASSIGNMENT DONE
    # ========================================================

    if data == "assignment_done":

        state["action"] = "assignment_done"

        await query.edit_message_text(

            "✅ <b>MARK AS DONE</b>\n\n"

            "Send the assignment number.\n\n"

            "Example: <code>1</code>",

            parse_mode="HTML",

            reply_markup=back_button()
        )

        return


    # ========================================================
    # SCHEDULE ADD
    # ========================================================

    if data == "schedule_add":

        state["action"] = "schedule_add"

        await query.edit_message_text(

            "➕ <b>ADD STUDY SESSION</b>\n\n"

            "Send:\n\n"

            "<code>Monday | 10:00 | Database</code>",

            parse_mode="HTML",

            reply_markup=back_button()
        )

        return


    # ========================================================
    # TODAY'S SCHEDULE
    # ========================================================

    if data == "schedule_today":

        result = schedule.get_todays_schedule(
            user_id
        )

        await query.edit_message_text(
            result,
            reply_markup=schedule_menu()
        )

        return


    # ========================================================
    # WEEKLY SCHEDULE
    # ========================================================

    if data == "schedule_week":

        result = schedule.show_week(
            user_id
        )

        await query.edit_message_text(
            result,
            reply_markup=schedule_menu()
        )

        return


    # ========================================================
    # SESSION COUNT
    # ========================================================

    if data == "schedule_count":

        result = schedule.count_sessions(
            user_id
        )

        await query.edit_message_text(
            result,
            reply_markup=schedule_menu()
        )

        return


    # ========================================================
    # CLEAR SCHEDULE
    # ========================================================

    if data == "schedule_clear":

        result = schedule.clear_all(
            user_id
        )

        await query.edit_message_text(
            result,
            reply_markup=schedule_menu()
        )

        return


    # ========================================================
    # GPA SCALE
    # ========================================================

    if data == "gpa_scale":

        result = gpa_calculator.show_grade_scale()

        await query.edit_message_text(
            result,
            reply_markup=gpa_menu()
        )

        return


    # ========================================================
    # GPA CALCULATE
    # ========================================================

    if data == "gpa_calculate":

        state["action"] = "gpa_calculate"

        state["data"] = {
            "courses": []
        }

        await query.edit_message_text(

            "🎓 <b>GPA CALCULATOR</b>\n\n"

            "Send each course like this:\n\n"

            "<code>Database | 3 | A</code>\n\n"

            "Add all your courses.\n\n"

            "When finished send:\n"
            "<code>done</code>",

            parse_mode="HTML",

            reply_markup=back_button()
        )

        return


    # ========================================================
    # CUMULATIVE GPA
    # ========================================================

    if data == "gpa_cumulative":

        state["action"] = "gpa_cumulative"

        state["data"] = {
            "step": "previous_gpa",
            "courses": []
        }

        await query.edit_message_text(

            "📈 <b>CUMULATIVE GPA</b>\n\n"

            "First, enter your previous GPA.\n\n"

            "Example:\n"
            "<code>3.50</code>",

            parse_mode="HTML",

            reply_markup=back_button()
        )

        return


    # ========================================================
    # DICTIONARY
    # ========================================================

    if data == "menu_dictionary" or data == "dictionary_search":

        state["action"] = "dictionary"

        await query.edit_message_text(

            "📖 <b>DICTIONARY</b>\n\n"

            "Send an English word.\n\n"

            "Example:\n"
            "<code>programming</code>",

            parse_mode="HTML",

            reply_markup=back_button()
        )

        return


    # ========================================================
    # CITATION
    # ========================================================

    if data == "menu_citation":

        clear_action(user_id)

        await query.edit_message_text(

            citation.citation_help(),

            reply_markup=back_button()
        )

        return


    # ========================================================
    # INTEGRATION
    # ========================================================

    if data == "menu_integration":

        state["action"] = "integration"

        await query.edit_message_text(

            "∫ <b>INTEGRATION CALCULATOR</b>\n\n"

            "Send an expression using x.\n\n"

            "Examples:\n"
            "<code>x^2</code>\n"
            "<code>2*x + 5</code>\n"
            "<code>sin(x)</code>",

            parse_mode="HTML",

            reply_markup=back_button()
        )

        return


    # ========================================================
    # POMODORO
    # ========================================================

    if data.startswith("pomo_"):

        if data == "pomo_status":

            result = pomodoro_timer.timer_status(
                user_id
            )

        elif data == "pomo_stop":

            result = pomodoro_timer.stop_timer(
                user_id
            )

        else:

            minutes = int(
                data.replace("pomo_", "")
            )

            result = pomodoro_timer.start_timer(
                user_id,
                minutes
            )

        await query.edit_message_text(
            result,
            reply_markup=pomodoro_menu()
        )

        return


    # ========================================================
    # EXAM MENU
    # ========================================================

    if data == "menu_exam":

        state["action"] = "exam"

        await query.edit_message_text(

            "⏳ <b>EXAM COUNTDOWN</b>\n\n"

            "Send your exam like this:\n\n"

            "<code>Database Exam | 2026-09-20</code>\n\n"

            "📅 Date format: YYYY-MM-DD",

            parse_mode="HTML",

            reply_markup=back_button()
        )

        return


    # ========================================================
    # VIEW EXAM
    # ========================================================

    if data == "exam_view":

        result = exam_countdown.get_exam(
            user_id
        )

        await query.edit_message_text(

            result,

            reply_markup=InlineKeyboardMarkup([

                [
                    InlineKeyboardButton(
                        "🗑️ Delete",
                        callback_data="exam_delete"
                    )
                ],

                [
                    InlineKeyboardButton(
                        "🏠 Main Menu",
                        callback_data="back_home"
                    )
                ]

            ])
        )

        return


    # ========================================================
    # DELETE EXAM
    # ========================================================

    if data == "exam_delete":

        result = exam_countdown.delete_exam(
            user_id
        )

        await query.edit_message_text(

            result,

            reply_markup=back_button()
        )

        return


    # ========================================================
    # MOTIVATION QUOTE
    # ========================================================

    if data == "mot_quote":

        await query.edit_message_text(

            quotes.get_random_quote(),

            reply_markup=motivation_menu()
        )

        return


    # ========================================================
    # STUDY TIP
    # ========================================================

    if data == "mot_tip":

        await query.edit_message_text(

            quotes.get_random_tip(),

            reply_markup=motivation_menu()
        )

        return


    # ========================================================
    # ALL STUDY TIPS
    # ========================================================

    if data == "mot_all_tips":

        await query.edit_message_text(

            quotes.get_all_tips(),

            reply_markup=motivation_menu()
        )

        return


# ============================================================
# HELP COMMAND
# ============================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.effective_message.reply_text(

        "🎓 <b>Campus Buddy</b>\n\n"
        "Use /start to open the main menu.\n\n"
        "You can manage assignments, schedules, "
        "GPA, exams, dictionary, calculator and more.",

        parse_mode="HTML",

        reply_markup=main_menu()
    )


# ============================================================
# ERROR HANDLER
# ============================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    logger.error(
        "Exception while handling update:",
        exc_info=context.error
    )


# ============================================================
# MAIN
# ============================================================

def main():

    if not BOT_TOKEN:

        raise RuntimeError(
            "BOT_TOKEN is missing.\n"
            "Set it with:\n"
            "export BOT_TOKEN='YOUR_NEW_TOKEN'"
        )


    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )


    # Commands
    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        CommandHandler(
            "help",
            help_command
        )
    )


    # Buttons
    application.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )


    # Text input
    application.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            handle_text
        )
    )


    # Errors
    application.add_error_handler(
        error_handler
    )


    print("=" * 60)
    print("🎓 CAMPUS BUDDY BOT")
    print("🚀 Professional Student Productivity Assistant")
    print("🤖 Bot is running...")
    print("=" * 60)


    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":
    main()
