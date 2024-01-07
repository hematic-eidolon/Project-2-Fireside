import currencyHandler as _c  # NOQA
import datetime
import json

class Fixture:

    def __init__(self, ID, currencyHandlerRef: _c.currencyHandler, **kwargs):
        self.__ID = ID
        self.__name = kwargs.get("name", "Unnamed Game")
        self.__date = kwargs.get("date", "Date TBC")
        self.__players = kwargs.get("players", "Players TBC")
        self.__entryFee = kwargs.get("entryFee", "£TBC")
        self.__prizeMoney = kwargs.get("prizeMoney", "£TBC")
        self.__currencyRef = currencyHandlerRef

    def __repr__(self) -> str:
        return f"Fixture ID: {self.__ID}, Name: {self.__name}"

    # =============== GETTERS =============== #
    def getID(self) -> int:
        return self.__ID

    def getName(self) -> str:
        return self.__name

    def getDate(self) -> datetime.datetime:
        return self.__date

    def getPlayers(self) -> list:
        return self.__players

    def getFee(self) -> float:
        return self.__entryFee

    def getPrizeMoney(self) -> float:
        return self.__prizeMoney

    # ============== SETTERS ============== #
    def setID(self, ID):
        self.__ID = ID

    def setName(self, name: str):
        self.__name = name

    def setDate(self, date: datetime.datetime):
        self.__date = date

    def setPlayers(self, players: list):
        self.__players = players

    def setFee(self, entryFee: float):
        self.__entryFee = entryFee

    def setPrizeMoney(self, prizeMoney: float):
        self.__prizeMoney = prizeMoney

    # ============== METHODS ================ #
    def getDatePretty(self) -> str:
        return self.__date.strftime("%d/%m/%y")

    def getCostForCountry(self, country: str):
        if country == "USA":
            return f"${self.__currencyRef.GBPtoUSD(self.__entryFee)}"
        elif country == "AUS":
            return f"${self.__currencyRef.GBPtoAUD(self.__entryFee)}"
        else:
            pass


def loadFixturesFromJSON():
    jsonFixtures = dict(json.load(open("settings.json")))
    for fixture in jsonFixtures:
        print(fixture)
