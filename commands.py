"""
Discord's commands
"""
from client import fetch_offers
from utils import format_offer

from discord.ext import commands
from discord import Intents, Embed


intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)




@bot.event
async def on_ready():
    print(intents.message_content)
    print(f"{bot.user.name} est connecté !")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(f"Message reçu : {message.content}")
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong !")

@bot.command()
async def offres(ctx):

    offers = fetch_offers().get("result", [])
    embed = Embed(
        title="Liste des Offres VIE",
        description="Voici les offres disponibles actuellement :",
        color=0x1abc9c
    )
    print(offers)
    for offer in offers:
        print(offer)
        embed.add_field(
            name=offer["missionTitle"],
            value=f"Entreprise : {offer['organizationName']}\nLieu : {offer['cityName']}",
            inline=False
        )

    embed.set_footer(text="Bot VIE • Généré automatiquement")
    await ctx.send(embed=embed)
    