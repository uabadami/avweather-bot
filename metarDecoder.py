# This file contains functions to decode METARs in an easy-to-read dictionary format

from getWeatherProducts import *

# Decode weather events from within a METAR
def weatherStrDecoded(wxString):
    wxList = wxString.split() # split weather string into individual phenomena
    
    # weather phenomena
    # sources: https://www.weather.gov/media/wrh/mesowest/metar_decode_key.pdf and https://www.la.utexas.edu/users/kimmel/GRG301K/grg301kmetars.html
    intensity = {'-': 'light', '+': 'heavy'}
    precipitation = {'RA': 'rain', 'DZ': 'drizzle', 'SN': 'snow', 'SG': 'snow grains',
               'IC': 'ice crystals', 'PL': 'ice pellets', 'UP': 'unknown precip',
               'GR': 'hail', 'GS': 'small hail'}
    descriptors = {'MI': 'shallow', 'PR': 'partial', 'BC': 'patches', 'DR': 'low drifting',
             'BL': 'blowing', 'SH': 'showers', 'TS': 'thunderstorm', 'FZ': 'freezing', 'VC': 'vicinity'}
    obscurations ={'FG': 'fog', 'BR': 'mist', 'HZ': 'haze', 'FU': 'smoke', 'DU': 'widespread dust',
                  'SA': 'sand', 'PY': 'spray', 'VA': 'volcanic ash'}
    miscs = {'SQ': 'squall', 'DS': 'duststorm', 'SS': 'sandstorm', 'PO': 'dust/sand whirls', 
            'FC': 'funnel cloud'}
    weatherCodeDict = [intensity, precipitation, descriptors, obscurations, miscs]
    
    if len(wxString) == 0: # if no weather, return
        return None
    
    decodedWeatherStr = [] # list containing all decoded weather events
    for weather in wxList:
        weatherDesc = ''
        for weatherCodeType in weatherCodeDict:
            intensityCode = [intensity[tens] for tens in intensity.keys() if tens in weather] # get intensity
            if (intensityCode != []):
                weatherDesc = weatherDesc + intensityCode[0] + " "
                weather = weather[1:]
            weatherCodes = [weatherCodeType[c] for c in weatherCodeType.keys() if c in weather and weather.index(c) % 2 == 0] # get all the non-intensity stuff
            if (weatherCodes != []):
                weatherDesc = weatherDesc + " ".join(weatherCodes) + " "
        if(weatherDesc != ''):
            decodedWeatherStr.append(weatherDesc[:-1]) # adds weather to the weather list if weather exists
    
    return decodedWeatherStr


# METAR decoder - returns decoded METAR as dictionary
def metarStrDecoder(metarStr):
    splitMETAR = metarStr.split()
    
    # obtain METAR without remarks section
    if 'RMK' in splitMETAR:
        rmkIndexList = splitMETAR.index('RMK')
        metarNoRMK = splitMETAR[:rmkIndexList]
    else:
        metarNoRMK = splitMETAR        
    
    # DECODING METAR!!!
    decodedMETAR = {}
    
    # remove AUTO/COR/RTD/AMD - 4 if statements due to chance of multiple codes included in the same METAR
    if (metarNoRMK[2] == 'AUTO'):
        metarNoRMK.pop(2)
    if (metarNoRMK[2] == 'COR'):
        metarNoRMK.pop(2)
    if (metarNoRMK[2] == 'RTD'):
        metarNoRMK.pop(2)
    if (metarNoRMK[2] == 'AMD'):
        metarNoRMK.pop(2)
    
    # station name
    decodedMETAR['station'] = metarNoRMK[0]
    metarNoRMK.pop(0)

    # observation date/time
    decodedMETAR['date'] = metarNoRMK[0][0:2]
    decodedMETAR['time'] = metarNoRMK[0][2:]
    metarNoRMK.pop(0)

    # winds
    windsInfo = [w for w in metarNoRMK if "KT" in w][0]

    decodedMETAR['windDir'] = metarNoRMK[0][0:3]
    if not metarNoRMK[0][5].isnumeric():
        decodedMETAR['windSpeed'] = metarNoRMK[0][3:5] + 'KT'
    else:
        decodedMETAR['windSpeed'] = metarNoRMK[0][3:6] + 'KT'
    
    if ("G" in windsInfo):
        gIndex = metarNoRMK[0].index('G')
        decodedMETAR['windGusts'] = metarNoRMK[0][gIndex + 1:]
    else:
        decodedMETAR['windGusts'] = None
    
    windVar = [w for w in metarNoRMK if ("V" in w and "VRB" not in w and len(w) == 7)] # check if wind dir changing
    if(windVar != []):
        decodedMETAR['windVar'] = windVar[0]
        metarNoRMK.pop(0)
    else:
        decodedMETAR['windVar'] = None
    
    metarNoRMK.pop(0)
    
    # visibility
    decodedMETAR['vis'] = metarNoRMK[0]
    metarNoRMK.pop(0)
    if (not "SM" in decodedMETAR['vis']):
        decodedMETAR['vis'] = decodedMETAR['vis'] + " " + [w for w in metarNoRMK if "SM" in w][0]
        metarNoRMK.pop(0)
    
    # runway visual range
    rvrInfo = [w for w in metarNoRMK if ("R" in w and "FT" in w)]
    if(rvrInfo != []):
        rvrData = rvrInfo[0][1:]
        slashLoc = rvrData.index('/')

        decodedMETAR['rvr'] = {'runway': rvrData[:slashLoc], 'runwayVis': rvrData[slashLoc + 1:]} # add RVR info if it exists
        metarNoRMK.pop(0)    
    else:
        decodedMETAR['rvr'] = None # otherwise, don't add it
    
    # sky condition
    if 'CLR' in metarNoRMK:
        decodedMETAR['clouds'] = 'clear below 12000'
        metarNoRMK.pop(metarNoRMK.index('CLR'))
    elif 'SKC' in metarNoRMK:
        decodedMETAR['clouds'] = 'clear'
        metarNoRMK.pop(metarNoRMK.index('SKC'))
    else:
        decodedMETAR['clouds'] = []
        skyConds = ['FEW', 'SCT', 'OVC', 'BKN']
        for cond in skyConds:
            condAlt = [int(w[3:]) * 100 for w in metarNoRMK if cond in w]
            if(condAlt != []):
                for i in range(len(condAlt)):
                    decodedMETAR['clouds'].append(cond.lower() + ' ' + str(condAlt[i]))
                metarNoRMK = [code for code in metarNoRMK if cond not in code]
        decodedMETAR['clouds'].sort(key = lambda x: int(x.split()[1])) # sort by cloud heights
        
    # vertical visibility
    vvData = [w[2:] for w in metarNoRMK if 'VV' in w]
    
    if vvData != []:
        decodedMETAR['vertVis'] = vvData[0]
    else:
        decodedMETAR['vertVis'] = None

    
    # temperature and dewpoint
    tempDewptInfo = [w for w in metarNoRMK if "/" in w][0]
    slashLoc = tempDewptInfo.index('/')
    decodedMETAR['temp'] = tempDewptInfo[:slashLoc]
    decodedMETAR['dewpoint'] = tempDewptInfo[slashLoc+1:]
    
    # altimeter
    altimeter = metarNoRMK[metarNoRMK.index(tempDewptInfo) + 1]
    decodedMETAR['alt'] = altimeter[1:3] + '.' + altimeter[3:]
    
    metarNoRMK.pop(metarNoRMK.index(tempDewptInfo))
    metarNoRMK.pop(metarNoRMK.index(altimeter))
    
    # weather
    if len(metarNoRMK) == 0: # if no weather, return
        decodedMETAR['weather'] = None
    else: # otherwise, add the weather
        decodedMETAR['weather'] = weatherStrDecoded(' '.join(metarNoRMK))
    
    return decodedMETAR

# returns decoded METAR for a specific airport
def getDecodedMETAR (stationCode):
    decodedMETAR = metarStrDecoder(getMETAR(stationCode)) # get the decoded METAR

    # flight category code
    decodedMETAR['flightCat'] = getFlightCat(stationCode) # append flight category (VFR, MVFR, IFR, LIFR)
    return decodedMETAR