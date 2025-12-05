# Configuration File for Campus_budd_bot

**Branch:** Yeshi_Dot-et  
**Developer:** Yeshi  

## About This File
This file (`config.py`) contains all the settings needed for the Campus Buddy Bot.  
Instead of writing these values directly in the code, we keep them here so it is easier to manage and update the bot.

## What It Contains

### Bot Information
- **BOT_NAME** – Name of the bot  
- **BOT_VERSION** – Version of the bot  
- **BOT_DEVELOPER** – Developer’s name  
- **BOT_BRANCH** – Branch name

### Database Information
- **DB_NAME** – Name of the database file  
- **DB_TABLE** – Table used for storing assignments

### Priority Levels
- **PRIORITIES** – Assignment priority levels: High, Medium, Low

### Status Options
- **STATUS_OPTIONS** – Whether an assignment is Pending or Completed

### Date Format
- **DATE_FORMAT** – How dates are displayed (`YYYY-MM-DD`)

### Default Values
- **DEFAULT_SUBJECT** – Default subject if none is specified  
- **DEFAULT_PRIORITY** – Default priority if none is set

### Logging
- **LOG_LEVEL** – Logging level for debugging or info messages  
- **LOG_FORMAT** – Format of the log messages

## How to Use
To use the settings in your Python code, just import the file:

```python
import config

# Example usage
print(config.BOT_NAME)
print(config.PRIORITIES["high"])
