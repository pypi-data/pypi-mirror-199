import pytest
# from mo_osrs_highscores.highscores import Highscores
from mo_osrs_highscores import Highscores
from mo_osrs_highscores.pageparser import ParsePage


def test_lookup():
    stats = Highscores.getHighScores("rsb perpdoom")

    print(stats.HighScores)
    #ParsePage().request_page("safdsafdaf")

