import discord
import os
from getnews import getNBANews, getNFLNews
from gettodayscores import getScores
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# client = discord.Client(intents=discord.Intents.default())

# @client.event
# async def on_ready():
# print(f'{client.user} has connected to Discord!')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command(name='nbanews')
async def nbanews(ctx):
    articles = getNBANews()

    embed = discord.Embed(title="NBA Recent News")

    for a in articles:
        desc = a.description + "  [Read]({})".format(a.link)
        embed.add_field(name=a.headline, value=desc, inline=False)

    await ctx.send(embed=embed)


@bot.command(name='nflnews')
async def nflnews(ctx):
    articles = getNFLNews()

    embed = discord.Embed(title="NFL Recent News")

    for a in articles:
        desc = a.description + "  [Read]({})".format(a.link)
        embed.add_field(name=a.headline, value=desc, inline=False)

    await ctx.send(embed=embed)


@bot.command(name='nbascores')
async def nbascores(ctx):
    games = getScores()

    embed = discord.Embed(title="NBA Box Scores")

    for g in games:
        score = g.awayTeam + " " + str(g.aScore) + "    @    " + str(g.hScore) + " " + g.homeTeam
        embed.add_field(name=score, value=g.gameStatusText, inline=False)

    await ctx.send(embed=embed)


# client.run(TOKEN)
bot.run(TOKEN)
