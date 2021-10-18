# This file gets raw METAR and TAF data from aviationweather.gov and transforms it into a more Python-friendly format.

# import area
import csv
import requests
import pandas as pd
import urllib


# Access METARs and TAFs as CSV files
weatherFiles = 'https://www.aviationweather.gov/adds/dataserver_current/current/' # location of all avwx current data
mostRecentMETARs = weatherFiles + 'metars.cache.csv' # location of METARs csv
mostRecentTAFs = weatherFiles + 'tafs.cache.csv' # location of TAFs csv


# Access METAR + all other info provided with a METAR for a given airport/reporting station
# Note: overhaul this method once we get an actual FAA METAR API.
def getMETARwData(stationCode):
    stationCode = ''.join(stationCode.split()).upper() # format the code properly

    if len(stationCode) < 3: # if not a valid code, return empty dataframe
        print('Input too short, must be 3 or 4 characters')
        return pd.DataFrame()
    elif len(stationCode) == 3 and stationCode.isalpha(): # if it's part of a K- airport
        stationCode = 'K' + stationCode # makes code into US airport code - TEMPORARY FIX
    
    
    metarDF = pd.read_csv(mostRecentMETARs, skiprows = 5) # csv --> dataframe
    metarStations = metarDF['station_id'].unique().tolist()
        
    if stationCode not in metarStations: # if METAR not found, return empty dataframe
        print('METAR not found for ' + stationCode)
        return pd.DataFrame()

    allWxData = metarDF.loc[metarDF['station_id'] == stationCode] # get all weather data
    return allWxData

# Only retrieve the full METAR for an airport
def getMETAR(stationCode):
    fullMetar = getMETARwData(stationCode)
    if not fullMetar.empty: # if a METAR exists for the airport
        return list(getMETARwData(stationCode)['raw_text'])[0] # return the text of the METAR (henceforth referred to as the METAR)
    return ""

# Only get weather string from METAR
def getWxStr(stationCode):
    fullMetar = getMETARwData(stationCode)
    if fullMetar.empty: # if no metar exists, return empty string
        return ""
    elif not fullMetar['wx_string'].dropna().empty: # if adverse weather exists at the airport
        return list(getMETARwData(stationCode)['wx_string'])[0]
    return ""

# Get flight category of an airport (VFR, MVFR, IFR, LIFR)
def getFlightCat(stationCode):
    fullMetar = getMETARwData(stationCode)
    if fullMetar.empty: # if no metar exists, return empty string
        return ""
    elif not fullMetar['flight_category'].dropna().empty: # if no flight category exists for the airport
        return list(getMETARwData(stationCode)['flight_category'])[0]
    return ""

# Get remarks section of a METAR
def getRemarks(stationCode):
    fullMetar = getMETARwData(stationCode)
    if fullMetar.empty: # if no metar exists, return empty string
        return ""
    else: # if a METAR exists for the airport
        metarText = list(fullMetar['raw_text'])[0]
        if "RMK" in metarText: # if there are remarks, return them
            rmkIdx = metarText.index("RMK")
            return metarText[rmkIdx + 4:]
        return "" # if not, return blank




# Access TAF + all other info provided with a TAF for a given airport/reporting station
# Note: overhaul this method once we get an actual FAA METAR API.

# Gets the TAF for an airport
def getTAF (stationCode):
    stationCode = ''.join(stationCode.split()).upper() # format the code properly
    if len(stationCode) < 3:
        print('Input too short, must be 3 or 4 characters')
        return
    elif len(stationCode) == 3 and stationCode.isalpha(): # if it's part of a K- airport
        stationCode = 'K' + stationCode # makes code into US airport code - TEMPORARY FIX

    response = urllib.request.urlopen(mostRecentTAFs) # access the TAF csv
    lines = [l.decode('utf-8') for l in response.readlines()] # gets the lines of the csv
    cr = csv.reader(lines) # sets up a csv reader

    for i in range(5): # skips first 5 lines
        next(cr)
    
    tafListMeanings = next(cr) # gets the headers for each item in the TAF + everything-else
    #print (tafListMeanings)

    tafList = [] # create a list where each row is a TAF and all the data associated with it
    for row in cr:
        tafList.append(row)

    tafDesired = [row[0] for row in tafList if stationCode in row[1]] # get the TAF for stationCode

    if tafDesired != []: # if there is a TAF, return it
        return tafDesired[0]
    
    else: # return blank
        print('TAF not found for ' + stationCode)
        return ""  
