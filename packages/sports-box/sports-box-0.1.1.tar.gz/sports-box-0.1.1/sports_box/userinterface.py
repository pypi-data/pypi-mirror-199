# functions to display various data
from .getplayerstuff import playerNextNGames

import matplotlib.pyplot as plt


def showUpcomingGames(player, n):  # displays figure to show upcoming games
    df = playerNextNGames(player, n)
    df_new = df[['GAME_DATE', 'HOME_TEAM_NICKNAME', 'VISITOR_TEAM_NICKNAME', 'GAME_TIME']]

    fig = plt.figure(figsize=(7, 3.5))
    ax = fig.add_subplot(111)
    ax.table(cellText=df_new.values, colLabels=df_new.columns, loc='center')

    s = player + "'s Upcoming 3 Games"
    ax.set_title(s, fontdict={'fontweight': 'bold'}, loc='center')
    ax.axis('off')

    plt.show()


# showUpcomingGames("Lebron James", 3)
