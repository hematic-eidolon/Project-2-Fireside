import datetime # NOQA
import json
import os
import requests

class currencyHandler():
  def __init__(self):
    # load settings and read the last date
    self.jsonDict = dict(json.load(open("settings.json"))) # NOQA
    self.UKtoAUD = 0
    self.UKtoUSD = 0

    # check if a day or more since last update.
    cT = datetime.datetime.now(datetime.timezone.utc) 
    pT = self.jsonDict["settings"]["last-updated-currency"]
    cStrFormat = f"{cT.day}:{cT.month}:{cT.year}"
    if cStrFormat != pT:
      # this code has not been run since yesterday, so refresh the currency conversion.
      self.reloadCurrencies()


  # wrappers for the conversion as functions
  def GBPtoAUD(self,value:float) -> float:
    return self.UKtoAUD * value
  def GBPtoUSD(self,value:float) -> float:
    return self.UKtoUSD * value

  # private method actually calls the API.
  def __currencyConvert(self,cFrom:str,cTo:str,value:float=1):
    parameters = {
      "api_key":os.getenv("API_KEY"),
      "format":"json",
      "from":cFrom,
      "to":cTo,
      "amount":value
    }
    url = "https://api.getgeoapi.com/v2/currency/convert"
    return requests.get(url, parameters).json()

  # get new values for currency conversion
  def reloadCurrencies(self) -> bool:
    s = True
    dt = datetime.datetime.now(datetime.timezone.utc) 
    AUDResponse = self.__currencyConvert("GBP","AUD")
    if AUDResponse["status"] == "success":
      self.UKtoAUD = AUDResponse["rates"]["AUD"]["rate"]
    else:
      print("ERROR: COULD NOT CALCULATE GBP TO AUD!!!")
      s = False
    
    USDResponse = self.__currencyConvert("GBP","USD")
    if USDResponse["status"] == "success":
      self.UKtoUSD = USDResponse["rates"]["USD"]["rate"]
    else:
      print("ERROR: COULD NOT CALCULATE GBP TO USD!!!")
      s = False

    # reset time since last refresh
    self.jsonDict["settings"]["last-updated-currency"] = \
    f"{dt.day}:{dt.month}:{dt.year}"
    self.jsonDict["settings"]["UKtoUSD"] = self.UKtoUSD
    self.jsonDict["settings"]["UKtoAUD"] = self.UKtoAUD
    
    # Reload the dictionary
    json.dump(self.jsonDict, open("settings.json","w"), indent=4)
    self.jsonDict = dict(json.load(open("settings.json")))

    # return success status 
    return s
    
    