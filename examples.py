# This file contains examples of how to use the tools provided

# Import statments
from getWeatherProducts import *
from metarDecoder import *
from tafDecoder import *

print(getMETAR("KEWR")) # gets the latest weather (METAR) at Newark Int'l Airport
print(getDecodedMETAR("KEWR")) # decodes the METAR for Newark Int'l Airport
print(getTAF("KEWR")) # gets the forecasted weather (TAF) at Newark Int'l Airport
print(getDecodedTAF("KEWR")) # decodes the TAF for Newark Int'l Airport