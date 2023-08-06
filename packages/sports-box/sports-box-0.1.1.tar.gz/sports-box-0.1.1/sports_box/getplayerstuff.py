# favorite player data

# import userprofile
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import PlayerNextNGames

# from nbaHeadshots import getHeadshotById, getAllHeadshots


# MOCK CLASSES
########################################################
class PlayerId(object):
    def __init__(self, player_id):
        self.player_id = player_id

    def get_data(self):
        data = players.find_players_by_full_name("Lebron James")
        return data


class PlayerInfo(object):
    def __init__(self, player_id):
        self.player_id = player_id

    def get_data(self):
        data = commonplayerinfo.CommonPlayerInfo(2544).common_player_info
        return data


class PlayerStats(object):
    def __init__(self, player_id):
        self.player_id = player_id

    def get_data(self):
        data = playercareerstats.PlayerCareerStats(2544).career_totals_regular_season.get_dict()
        # data = playerStats("Lebron James")
        return data


class PlayerGames(object):
    def __init__(self, number_of_games, player_id, season_all, season_type_all_star):
        self.number_of_games = number_of_games
        self.player_id = player_id
        self.season_all = season_all
        self.season_type_all_star = season_type_all_star

    def get_data(self):
        data = PlayerNextNGames(
            number_of_games="3", player_id=2544, season_all="2021-22", season_type_all_star="Regular Season"
        ).next_n_games.get_dict()
        # data = playerNextNGames("Lebron James", 3)
        return data


#############################################################################


def getPID(player):  # helper function to get player ID
    p = players.find_players_by_full_name(player)
    d = p[0]
    id = list(d.items())[0][1]

    return id


def getPlayer(player):
    # getHeadshotById(id)
    id = getPID(player)
    load = commonplayerinfo.CommonPlayerInfo(id).common_player_info
    # load = commonplayerinfo.CommonPlayerInfo(id)
    playerinfo = load.common_player_info.get_data_frame()
    # playerinfo = load.get_dict()
    # playerinfo = load

    # display(playerinfo.loc[0])
    return playerinfo
    # print(playerinfo)


def playerStats(player):  # show career stats of player
    id = getPID(player)
    load = playercareerstats.PlayerCareerStats(id).career_totals_regular_season
    stats = load.get_data_frame()
    # stats = load.get_dict()
    # stats.style.set_caption(player + "'s Stats")

    # print(stats)
    return stats  # horizontal stats


def playerNextNGames(player, n):  # return next n games as data frame
    s = str(n)
    id = getPID(player)
    load = PlayerNextNGames(
        number_of_games=s, player_id=id, season_all="2022-23", season_type_all_star="Regular Season"
    )
    upcoming = load.next_n_games.get_data_frame()
    # upcoming = load.next_n_games.get_dict()
    # upcoming.style.set_caption(player + "'s Upcoming " + s + " Games")

    return upcoming
    # print(upcoming)


# getPlayer("Lebron James")
# playerStats("Lebron James")
# playerNextNGames("Lebron James", 3)
