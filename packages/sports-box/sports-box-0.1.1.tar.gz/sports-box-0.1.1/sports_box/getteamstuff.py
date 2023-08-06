# team stuff

# import userprofile
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teaminfocommon


# MOCK CLASSES
########################################################


class TeamId(object):
    def __init__(self, team_id):
        self.team_id = team_id

    def get_data(self):
        data = teams.find_team_by_abbreviation("mil")
        return data


########################################################


def getTeam(team):
    t = teams.find_team_by_abbreviation(team)
    # get team logo
    id = list(t.items())[0][1]
    load = teaminfocommon.TeamInfoCommon(team_id=id, season_nullable="2022-23")
    # teaminfo = load.team_info_common.get_data_frame()
    teaminfo = load.team_info_common.get_dict()

    # return teaminfo.loc[0]
    return teaminfo
    # print(teaminfo)
    # print(t)


# getTeam("mil")
