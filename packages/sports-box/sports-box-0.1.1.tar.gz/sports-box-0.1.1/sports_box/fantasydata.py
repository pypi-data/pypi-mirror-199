# fantasy data
"""
from espn_api.football import League

# extra parameters to access my private fantasy football league
sw_id = '{B56FC65C-ACE9-4947-B210-B80FC1048043}'
espns2 = (
    'AEA7%2FBS88%2F6NAM3aQBFkMe6KdKr5EP0fKrrSYmT%2B00j'
    'veWNMKI9N4QEdHy%2BCeDaTTAIoNYI3k6KUzJ4n5iUgzVBdGm7'
    'EWBU0EyBnp3eYODO62jLanJ0%2FejXBjTmXUh%2BIS39sWPZSB7'
    '9R6I%2FwJotut0wX5Myk2Nfo7Q588tMS4PW6t8srpRIDvdj4jUF'
    'nQeGQCDHjWXOgqU8X4VMj0APRaMqY2AlwIWhIfwN0UfQ5Vu1O6n4'
    '7WccFmqNX8pPHp5iJyr%2B%2Ffdyo%2FBgxsIH9fLwDVV4BUDN3uK'
    'AM%2BGVL6gf0xRkcpA%3D%3D'
)


# Helper function to get user's fantasy team - case sensitive
def getMyTeam(teamname):
    lg = League(league_id=1088987341, year=2022, espn_s2=espns2, swid=sw_id)
    myteam = ""
    for t in lg.teams:
        if t.team_name == teamname:
            myteam = t
            break

    return myteam


# Get user's fantasy roster
def myRoster(teamname):
    myteam = getMyTeam(teamname)
    return myteam.roster


myRoster("Handoff Hu")
# print(getMyTeam("Handoff Hu"))

"""
