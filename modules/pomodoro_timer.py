# modules/pomodoro_timer.py
# Campus Buddy - Pomodoro Timer

import asyncio

timers = {}


def get_timer(user_id):
    return timers.get(user_id)


def start_timer(user_id, minutes=25):
    try:
        minutes = int(minutes)
    except (ValueError, TypeError):
        return "❌ Minutes must be a number."

    if minutes <= 0:
        return "❌ Minutes must be greater than 0."

    timers[user_id] = {
        "minutes": minutes,
        "remaining": minutes * 60,
        "running": True
    }

    return (
        "🍅 POMODORO STARTED!\n\n"
        f"⏱️ Focus time: {minutes} minutes\n"
        "📚 Stay focused and avoid distractions!"
    )


def stop_timer(user_id):
    if user_id not in timers:
        return "❌ No active Pomodoro timer."

    timers[user_id]["running"] = False
    del timers[user_id]

    return "🛑 Pomodoro timer stopped."


def timer_status(user_id):
    if user_id not in timers:
        return "🍅 No active Pomodoro timer."

    data = timers[user_id]

    remaining = data["remaining"]

    minutes = remaining // 60
    seconds = remaining % 60

    status = "▶️ Running" if data["running"] else "⏸️ Paused"

    return (
        "🍅 POMODORO STATUS\n\n"
        f"⏱️ Remaining: {minutes:02d}:{seconds:02d}\n"
        f"📊 Status: {status}"
    )


def reset_timer(user_id):
    if user_id in timers:
        del timers[user_id]

    return "🔄 Pomodoro timer reset."


def get_presets():
    return (
        "🍅 POMODORO PRESETS\n\n"
        "⚡ Quick Focus — 15 minutes\n"
        "📚 Standard Focus — 25 minutes\n"
        "🔥 Deep Focus — 50 minutes\n"
        "☕ Long Break — 15 minutes"
    )


async def run_timer(user_id, callback=None):
    """
    Background countdown.

    callback should be an async function that accepts
    the user_id when the timer finishes.
    """

    if user_id not in timers:
        return

    while user_id in timers:

        if not timers[user_id]["running"]:
            break

        if timers[user_id]["remaining"] <= 0:
            break

        await asyncio.sleep(1)

        if user_id not in timers:
            break

        timers[user_id]["remaining"] -= 1

    if user_id in timers:
        del timers[user_id]

        if callback:
            await callback(user_id)


def pause_timer(user_id):
    if user_id not in timers:
        return "❌ No active timer."

    timers[user_id]["running"] = False

    return "⏸️ Pomodoro paused."


def resume_timer(user_id):
    if user_id not in timers:
        return "❌ No active timer."

    timers[user_id]["running"] = True

    return "▶️ Pomodoro resumed."
