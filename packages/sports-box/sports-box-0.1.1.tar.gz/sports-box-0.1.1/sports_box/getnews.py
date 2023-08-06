import requests
import random

# import discord
# from discord.ext import commands


class Article:
    def __init__(self, headline, description, link):
        self.headline = headline
        self.description = description
        self.link = link

    def __eq__(self, other):
        return self.headline == other.headline

    def __hash__(self):
        return hash((self.headline, self.description, self.link))


def getNBANews():  # get 5 random recent articles
    url = 'http://site.api.espn.com/apis/site/v2/sports/basketball/nba/news'
    data = requests.get(url)
    news_dict = data.json()
    nbaarticles = set()

    nbaarticles.clear()

    while len(nbaarticles) < 5:
        random_article = random.choice(news_dict.get('articles'))
        article = Article(
            random_article['headline'], random_article['description'], random_article['links']['web']['href']
        )
        # print(random_article['headline'])
        # print(random_article['description'])
        # print(random_article['links']['web']['href'])
        nbaarticles.add(article)

    # for i in nbaarticles:
    # print(i.headline)
    # print(i.link)

    return nbaarticles
    # print(data)


# getNBANews()


def getNFLNews():  # get 5 random recent articles
    url = 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/news'
    data = requests.get(url)
    news_dict = data.json()
    nflarticles = set()

    nflarticles.clear()

    while len(nflarticles) < 5:
        random_article = random.choice(news_dict.get('articles'))
        article = Article(
            random_article['headline'], random_article['description'], random_article['links']['web']['href']
        )
        nflarticles.add(article)

    # for i in nflarticles:
    # print(i.headline)

    return nflarticles


# getNFLNews()

"""
class News(commands.Cog, name="news"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='nbanews')
    async def nbanews(self, ctx):
        articles = getNBANews()

        embed = discord.Embed(title="NBA Recent News")

        for a in articles:
            embed.add_field(name="[a.headline](a.link)", value=a.description, inline=False)

        await ctx.send(embed)

    @commands.command(name='nflnews')
    async def nflnews(self, ctx):
        articles = getNFLNews()

        embed = discord.Embed(title="NFL Recent News")

        for a in articles:
            embed.add_field(name="[a.headline](a.link)", value=a.description, inline=False)

        await ctx.send(embed)


async def setup(bot):
    await bot.add_cog(News(bot))
"""
