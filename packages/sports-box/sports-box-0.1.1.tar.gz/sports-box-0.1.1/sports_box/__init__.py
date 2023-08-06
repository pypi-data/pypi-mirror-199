from ._version import __version__

# from .fantasydata import getMyTeam, myRoster
from .getplayerstuff import (
    getPID,
    getPlayer,
    playerStats,
    playerNextNGames,
    PlayerInfo,
    PlayerStats,
    PlayerGames,
    PlayerId,
)
from .getteamstuff import getTeam, TeamId
from .teamcolors import getTName, getTColor1
from .getnews import getNBANews, getNFLNews
from .gettodayscores import getScores
from .userinterface import showUpcomingGames
