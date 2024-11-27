"""
Sets everything up
"""

from config import TOKEN
from commands import bot, intents

if __name__ == "__main__":
    bot.run(TOKEN)
