from datetime import datetime
import random
MORNING_MESSAGES = [
    "Hope you're ready for a productive day.",
    "Start today with confidence.",
    "Every great investment begins with one good decision."
]

AFTERNOON_MESSAGES = [
    "Hope you're having a productive day.",
    "Keep making smart financial choices.",
    "You're halfway through another successful day."
]

EVENING_MESSAGES = [
    "Take a moment to review today's finances.",
    "Every small saving counts.",
    "Consistency builds wealth."
]
FINANCIAL_QUOTES = [
    "Small savings today create financial freedom tomorrow.",
    "Spend intentionally. Save consistently.",
    "Financial discipline creates future opportunities.",
    "Every expense tells a story.",
    "Wealth grows through consistency, not luck.",
    "Track your money before your money tracks you."
]


NIGHT_MESSAGES = [
    "Great work today. Take a moment to reflect on your finances.",
    "A quick review today leads to better decisions tomorrow.",
    "Rest well—your financial goals are built one day at a time."
]


def get_dashboard_greeting():
    """Return a greeting, a time-based message, and a random financial quote."""

    hour = datetime.now().hour

    if 5 <= hour < 12:
        greeting = "Good Morning ☀️"
        message = random.choice(MORNING_MESSAGES)
    elif 12 <= hour < 17:
        greeting = "Good Afternoon 👋"
        message = random.choice(AFTERNOON_MESSAGES)
    elif 17 <= hour < 21:
        greeting = "Good Evening 🌇"
        message = random.choice(EVENING_MESSAGES)
    else:
        greeting = "Good Night 🌙"
        message = random.choice(NIGHT_MESSAGES)

    quote = random.choice(FINANCIAL_QUOTES)

    return {
        "greeting": greeting,
        "message": message,
        "quote": quote,
    }