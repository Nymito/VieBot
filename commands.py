"""
Discord's commands
"""
from client import fetch_offers, set_filters, get_filters
from utils import format_offer, build_filters, Filters

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
    user_id = ctx.author.id
    filters = get_filters(user_id) or None
    offers = fetch_offers(filters=filters).get("result", [])
    embed = Embed(
        title="Liste des Offres VIE",
        description="Voici les offres disponibles actuellement :",
        color=0x1abc9c
    )

    for offer in offers:
        print(offer)
        embed.add_field(
            name=offer["missionTitle"],
            value=f"Entreprise : {offer['organizationName']}\nLieu : {offer['cityName']}",
            inline=False
        )

    embed.set_footer(text="Bot VIE • Généré automatiquement")
    await ctx.send(embed=embed)

    
@bot.command()
async def filtres(ctx, *args):
    if not(filters:=build_filters(ctx,*args)):
        await aide(ctx)
    else:
        print("author "+str(ctx.author.id)+" setting filters: {query "+filters["query"]+ " location "+str(filters["location"])+"}")
        set_filters(ctx.author.id, query=filters["query"], location=filters["location"])


@bot.command()
async def mes_filtres(ctx):
    user_id = ctx.author.id
    filters = get_filters(user_id)

    if filters:
        await ctx.send(f'Vos filtres actuels sont :\n- Mots-clés : {filters["query"]}\n- Localisation : {filters["location"]}')
    else:
        await ctx.send("Vous n'avez pas encore défini de filtres.")

@bot.command()
async def aide(ctx):
    """Affiche une aide détaillée sur les commandes disponibles."""
    embed = Embed(
        title="📜 Aide des commandes",
        description="Voici la liste des commandes disponibles et leur fonctionnement :",
        color=0x3498db
    )

    embed.add_field(
        name="!ping",
        value="Test la connexion avec le bot. Répond par 'Pong !'.",
        inline=False
    )

    embed.add_field(
        name="!offres",
        value="Affiche la liste des offres VIE disponibles.\n"
              "Les offres sont récupérées et affichées avec des détails tels que le titre, l'entreprise et la localisation.",
        inline=False
    )

    embed.add_field(
        name="!filtres",
        value="Permet de définir vos filtres de recherche.\n"
              "Syntaxe : `!filtres <mots-clés> à <localisation>`\n"
              "avec localisation = Pays ou Région\n"
              "Exemples :\n"
              "• `!filtres developpeur backend à Montreal`\n"
              "• `!filtres developpeur backend` (sans localisation)",
        inline=False
    )

    embed.add_field(
        name="!mes_filtres",
        value="Affiche les filtres que vous avez définis.\n"
              "Si aucun filtre n'est défini, une invitation à les définir sera affichée.",
        inline=False
    )

    embed.set_footer(text="Bot VIE • Commande d'aide")
    await ctx.send(embed=embed)