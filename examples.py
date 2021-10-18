# This file contains examples of how to use the tools provided

# Import statments
from getWeatherProducts import *
from metarDecoder import *
from tafDecoder import *

print(getDecodedMETAR("KEWR")) # gets the latest weather (METAR) at Newark Int'l Airport
print(getDecodedTAF("KEWR")) # gets the forecasted weather (TAF) at Newark Int'l Airport