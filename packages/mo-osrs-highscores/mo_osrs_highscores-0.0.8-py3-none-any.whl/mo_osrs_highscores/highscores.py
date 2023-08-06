from .pageparser import ParsePage
from .resources import BallsAndPenis


class Highscores:

    @staticmethod
    def getHighScores(playerName):
        ParsePage().request_page(playerName)
        BallsAndPenis.getMegaDic()
        return BallsAndPenis
