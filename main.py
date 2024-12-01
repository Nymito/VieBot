"""
Sets everything up
"""

import os


from commands import bot

TOKEN = os.getenv('DISCORD_TOKEN')
if __name__ == "__main__":
    bot.run(TOKEN)
