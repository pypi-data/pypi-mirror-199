import requests

# import discord
# from discord.ext import commands


class Game:
    def __init__(self, gameStatus, gameStatusText, homeTeam, hWins, hLosses, hScore, awayTeam, aWins, aLosses, aScore):
        self.gameStatus = gameStatus
        self.gameStatusText = gameStatusText
        self.homeTeam = homeTeam
        self.hWins = hWins
        self.hLosses = hLosses
        self.hScore = hScore
        self.awayTeam = awayTeam
        self.aWins = aWins
        self.aLosses = aLosses
        self.aScore = aScore


url = 'https://nba-prod-us-east-1-mediaops-stats.s3.amazonaws.com/NBA/liveData/scoreboard/todaysScoreboard_00.json'
data = requests.get(url)
scores_data = data.json()
isGames = False

if data.ok:
    isGames = True


def getScores():
    games = list()
    games.clear()

    if isGames:
        scoreboard = scores_data.get('scoreboard')

        for s in scoreboard['games']:
            if s['gameStatus'] == 1:
                s['homeTeam']['score'] = ' '
                s['awayTeam']['score'] = ' '
            game = Game(
                s['gameStatus'],
                s['gameStatusText'],
                s['homeTeam']['teamTricode'],
                s['homeTeam']['wins'],
                s['homeTeam']['losses'],
                s['homeTeam']['score'],
                s['awayTeam']['teamTricode'],
                s['awayTeam']['wins'],
                s['awayTeam']['losses'],
                s['awayTeam']['score'],
            )
            games.append(game)

        # for g in games:
        # print("-----------------")
        # print(g.gameStatusText)
        # print(g.awayTeam + " " + str(g.aScore) + "  @  " + str(g.hScore) + " " + g.homeTeam)
        # print("-----------------")

        return games


# print(scores_data.get('scoreboard'))
# getScores()

"""
class Scores(commands.Cog, name="scores"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='nbascores')
    async def nflnews(ctx):
        #Shows todays NBA box scores
        games = getScores()

        embed = discord.Embed(title="NBA Box Scores")

        for g in games:
            score = g.awayTeam + " " + str(g.aScore) + "    @    " + str(g.hScore) + " " + g.homeTeam
            embed.add_field(name=score, value=g.gameStatusText, inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Scores(bot))

"""
