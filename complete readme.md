# Campus Buddy Bot 🤖📚

## 🎯 Project Overview
Campus Buddy Bot is a comprehensive Telegram bot that helps students manage their academic life with features like assignment tracking, GPA calculation, study scheduling, and more.

## ✨ Features

### 📚 **Academic Management**
- **Assignment Tracker** - Add/edit/delete assignments with deadlines
- **Study Schedule** - Daily/weekly study plans
- **GPA Calculator** - Semester and cumulative GPA calculation
- **Exam Countdown** - Track days until exams

### ⚡ **Study Tools**
- **Scientific Calculator** - Advanced math with integration and trigonometry
- **English Dictionary** - Instant word definitions
- **Motivational Quotes** - Daily encouragement
- **Pomodoro Timer** - 25-minute focus sessions

### 🔒 **Security Features**
- User-specific JSON storage for data isolation
- Persistent data that survives bot restarts
- Complete privacy between users

## 👥 Team Members
| ID | Name | GitHub |
|----|------|--------|
| 1701061 | Soza Tamrat | [@silencesoza](https://github.com/silencesoza) |
| 1701006 | Sara Hailemariam | [@sara23halle](https://github.com/sara23halle) |
| 1701171 | Yeshi Geleta | [@dot-et](https://github.com/dot-et) |

## 🚀 Quick Start

### 1. **Get Bot Token**
1. Open Telegram, search for **@BotFather**
2. Send `/newbot` and follow instructions
3. Copy your bot token (looks like: `1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ`)

### 2. **Setup & Run**

# Clone repository
git clone https://github.com/Debre-birhan-university/project-campus-buddy.git
cd project-campus-buddy

# Install dependencies
pip install python-telegram-bot requests sympy

# Configure bot
cp config.example.py config.py
# Edit config.py and add your bot token

# Run the bot
python bot.py


## 📊 Available Commands

### 📅 **Schedule**
/schedule - Today's study plan
/add_session [day] [time] [subject] - Add session
/week - Weekly schedule
/clear_day [day] - Clear day's schedule



### 📚 **Assignments**
/add [task] [date] - Add assignment
/deadlines - View all assignments
/delete [number] - Delete assignment
/edit [number] [new] [date] - Edit assignment
/search [keyword] - Search assignments



### 🎓 **GPA**
/add_course [name] [score] [credit] - Add course
/semester_gpa - Calculate semester GPA
/cgpa - Calculate cumulative GPA
/new_semester - Start new semester



### 🧮 **Calculator & Tools**
/calc - Open scientific calculator
/calculate [expression] - Quick calculation
/define [word] - Get word definition
/quote - Today's motivational quote
/motivate - Random encouragement



### ⏰ **Study Timer**
/pomodoro - Start 25-min focus timer
/pomodoro_pause - Pause timer
/pomodoro_resume - Resume timer
/pomodoro_stop - Stop timer



### 📅 **Exams**
/addexam [name] [date] [time] - Add exam
/exams - View your exams
/deleteexam [name] - Delete exam



### 📖 **References**
/citations - View academic references
/start - Welcome message
/help - Help command



## 📁 Project Structure
project-campus-buddy/
```
├── bot.py # Main bot file
├── config.py # Bot configuration
├── requirements.txt # Dependencies
│
├── modules/ # All feature modules
│ ├── schedule.py # Study schedule
│ ├── assignments.py # Assignment tracker
│ ├── calculator.py # Scientific calculator
│ ├── gpa_calculator.py # GPA calculator
│ ├── dictionary.py # English dictionary
│ ├── quotes.py # Motivational quotes
│ ├── citation.py # Academic references
│ ├── pomodoro_timer.py # Pomodoro timer
│ └── exam_countdown.py # Exam tracker
│
└── data/ # User data storage
├── schedule_12345.json # User-specific data
├── assignments_12345.json
├── gpa_12345.json
└── exams_12345.json
```

## 🔒 Data Security
- Each user's data stored in separate JSON files
- Data persists locally only
- `.gitignore` prevents committing sensitive data
- No data sharing between users

## 📈 Development Progress

### ✅ **Completed**
- All core modules implemented
- User-specific data storage
- Advanced calculator with integration
- Pomodoro timer with pause/resume
- Assignment statistics and search

### 🔄 **Active Development**
- Testing and bug fixes
- Documentation
- Performance optimization

## 🤝 Contributing
1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add: Your feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Create Pull Request

## 📄 License
Academic project for Python Programming course at Debre Birhan University.

---

**🚀 Happy Studying with Campus Buddy Bot!**


