# This file decodes METARs in an easy-to-read dictionary format

from getWeatherProducts import *
from metarDecoder import *

# TAF decoder - returns decoded TAF as dictionary
def tafStrDecoder(tafStr):
    splitTAF = tafStr.split()
    
    if 'TAF' in splitTAF: # take out 'TAF' from the TAF
        splitTAF.pop(0)
    
    # DECODING TAF!!!
    decodedTAF = {}
    

    # station name
    decodedTAF['station'] = splitTAF[0]
    splitTAF.pop(0)
    
    
    # remove AUTO/COR/RTD/AMD
    if (splitTAF[2] == 'AUTO'):
        splitTAF.pop(2)
    if (splitTAF[2] == 'COR'):
        splitTAF.pop(2)
    if (splitTAF[2] == 'RTD'):
        splitTAF.pop(2)
    if (splitTAF[2] == 'AMD'):
        splitTAF.pop(2)
    
    
    # TAF date/time
    decodedTAF['issueDate'] = splitTAF[0][0:2]
    decodedTAF['issueTime'] = splitTAF[0][2:]
    splitTAF.pop(0)
    
    
    # TAF validity period
    decodedTAF['validStartDate'] = splitTAF[0][0:2]
    decodedTAF['validStartTime'] = splitTAF[0][2:4]
    decodedTAF['validEndDate'] = splitTAF[0][5:7]
    decodedTAF['validEndTime'] = splitTAF[0][7:]
    splitTAF.pop(0)
    
    splitTAF.insert(0, "FM" + decodedTAF['validStartDate'] + decodedTAF['validStartTime'] + "00" )
    
    # Split the TAF into its components
    blockIdxs = [s for s in range(len(splitTAF)) if
                 ("FM" in splitTAF[s] or "TEMPO" in splitTAF[s] or "BECMG" in splitTAF[s] or "PROB" in splitTAF[s])] # TAF block indices
    blockIdxs.append(len(splitTAF)) # add end of TAF
    
    tafBlocks = [] # contains all TAF blocks
    for i in range(len(blockIdxs) - 1):
        tafBlocks.append(splitTAF[blockIdxs[i] : blockIdxs[i+1]])

    for block in tafBlocks: # for each block of time in the TAF
        blockIdStr = tafBlocks.index(block) # assign an ID to the block
        
        # BLOCK TYPE AND TIMES
        decodedTAF[blockIdStr] = {}
        fmInBlock = [string[2:] for string in block if 'FM' in string] # check if from block
        if fmInBlock != []:
            decodedTAF[blockIdStr]['group'] = 'from'
            decodedTAF[blockIdStr]['startDate'] = fmInBlock[0][:2]
            decodedTAF[blockIdStr]['startTime'] = fmInBlock[0][2:]
            decodedTAF[blockIdStr]['endDate'] = ''
            decodedTAF[blockIdStr]['endTime'] = ''
        
        elif 'TEMPO' in block: # check if tempo block
            decodedTAF[blockIdStr]['group'] = 'temporary'
        
        elif 'BECMG' in block: # check if becoming block
            decodedTAF[blockIdStr]['group'] = 'becoming'
        
        probInBlock = [string[4:] for string in block if 'PROB' in string] # check if probability block
        if probInBlock != []:
            decodedTAF[blockIdStr]['group'] = 'probability ' + probInBlock[0]
        
        slashInBlock = [string for string in block if '/' in string] # if not from block, check for start and end times using this
        if slashInBlock != [] and fmInBlock == []:
            decodedTAF[blockIdStr]['startDate'] = slashInBlock[0][:2]
            decodedTAF[blockIdStr]['startTime'] = slashInBlock[0][2:4] + '00'
            decodedTAF[blockIdStr]['endDate'] = slashInBlock[0][5:7]
            decodedTAF[blockIdStr]['endTime'] = slashInBlock[0][7:] + '00'
        
        if tafBlocks.index(block) != 0: # make sure that previous block has an end date and time
            #print(tafBlocks.index(block))
            prevBlockId = tafBlocks.index(block) - 1
            if decodedTAF[prevBlockId]['endDate'] == '':
                decodedTAF[prevBlockId]['endDate'] = decodedTAF[blockIdStr]['startDate']
            if decodedTAF[prevBlockId]['endTime'] == '':
                decodedTAF[prevBlockId]['endTime'] = decodedTAF[blockIdStr]['startTime']
        
        if tafBlocks.index(block) == len(tafBlocks) - 1: # if this is the last TAF block, end observation at valid end time
            decodedTAF[blockIdStr]['endDate'] = decodedTAF['validEndDate'] + '00'
            decodedTAF[blockIdStr]['endTime'] = decodedTAF['validEndTime'] + '00'

            
        # WINDS
        windInBlock = [string for string in block if ('KT' in string and '/' not in string)] # check if wind predicted (look for knots)
        if windInBlock != []:
            winds = windInBlock[0]
            decodedTAF[blockIdStr]['windDir'] = winds[0:3]
            if not winds[5].isnumeric():
                decodedTAF[blockIdStr]['windSpeed'] = winds[3:5] + 'KT'
            else:
                decodedTAF[blockIdStr]['windSpeed'] = winds[3:6] + 'KT'
            if ("G" in winds):
                gIndex = winds.index('G')
                decodedTAF[blockIdStr]['windGusts'] = winds[gIndex + 1:]
            else:
                decodedTAF[blockIdStr]['windGusts'] = None
        else:
            decodedTAF[blockIdStr].update(dict.fromkeys(['windDir', 'windSpeed', 'windGusts'], None))
        
        
        # WIND SHEAR
        windShearInBlock = [string for string in block if 'WS' in string] # check if wind shear predicted (look for WS)
        if windShearInBlock != []:
            windShear = windShearInBlock[0][2:]
            decodedTAF[blockIdStr]['windShearHeight'] = windShear[0:3]
            decodedTAF[blockIdStr]['windShearDir'] = windShear[4:7]
            decodedTAF[blockIdStr]['windShearSpeed'] = windShear[7:]
        else:
            decodedTAF[blockIdStr].update(dict.fromkeys(['windShearHeight', 'windShearDir', 'windShearSpeed'], None))
        
        
        # VISIBILITY
        visIdx = [v for v in block if "SM" in v]
        if visIdx != []:
            decodedTAF[blockIdStr]['vis'] = visIdx[0]
            if (not "SM" in decodedTAF[blockIdStr]['vis']):
                decodedTAF[blockIdStr]['vis'] + " " + block[block.index(decodedTAF['vis']) + 1]
        else:
            decodedTAF[blockIdStr]['vis'] = None

            
        # CLOUDS
        if 'CLR' in block:
            decodedTAF[blockIdStr]['clouds'] = ['clear below 12000']
        elif 'SKC' in block:
            decodedTAF[blockIdStr]['clouds'] = ['clear']
        else:
            decodedTAF[blockIdStr]['clouds'] = []
            skyConds = ['FEW', 'SCT', 'OVC', 'BKN']
            for cond in skyConds:
                condAlt = [w[3:] for w in block if cond in w]
                if(condAlt != []):
                    for i in range(len(condAlt)):
                        if "CB" in condAlt[i]:
                            decodedTAF[blockIdStr]['clouds'].append(cond.lower() + " " + str(int(condAlt[i][:-2]) * 100) + " cumulonimbus")
                        else:
                            decodedTAF[blockIdStr]['clouds'].append(cond.lower() + " " + str(int(condAlt[i]) * 100))

            decodedTAF[blockIdStr]['clouds'].sort(key = lambda x: int(x.split()[1])) # sort by cloud heights
        
        # WEATHER
        str4Block = ' '.join(block)
        wx4Block = weatherStrDecoded(str4Block)
        if 'NSW' in block:
            decodedTAF[blockIdStr]['weather'] = 'No significant weather'
        elif wx4Block != []:
            decodedTAF[blockIdStr]['weather'] = wx4Block
        else:
            decodedTAF[blockIdStr]['weather'] = None
        
        # LOCAL ALTIMETER
        qnhInBlock = [blk for blk in block if 'QNH' in blk]
        if qnhInBlock != []:
            decodedTAF[blockIdStr]['localAlt'] = qnhInBlock[0][3:-3]
        else:
            decodedTAF[blockIdStr]['localAlt'] = None

        
    return decodedTAF

def getDecodedTAF(stationCode):
    return tafStrDecoder(getTAF(stationCode)) # get the decoded TAF