# avweather-bot

METARs and TAFs are two crucial pieces of information that pilots around the world use to get the weather. METARs (METeorological Aerodrome Reports) give pilots the most recent hourly weather report at a given airport or reporting station, while TAFs (Terminal Aerodrome Forecasts) provide meteorological predictions for periods of up to 24 hours. They inform pilots of meteorological conditions including wind, visibility, cloud height and type, adverse weather conditions, temperature, and more.

In the United States, these products are published by the National Weather Service's Aviation Weather Center via a computerized system. Examples of both METARs and TAFs are shown below.

```
METAR KEWR 101234Z 12015G24KT 4SM +TSRA HZ FEW004 SCT011 OVC019 19/14 3002
TAF: KJFK 172336Z 1800/1906 28012G19KT P6SM FEW060 FM180600 29010KT P6SM FEW060...
```

As shown above, neither of these crucial products are easily human-readable. This project uses Python to both retrieve and decode METARs and TAFs. Examples of how to do this are shown in ```examples.py```, and below (where "KABC" can be replaced by any valid airport code).

Get a raw METAR: ```getMETAR("KABC")```
Get a raw TAF: ```getTAF("KABC")```
Get a decoded METAR: ```getDecodedMETAR("KABC")```
Get a decoded TAF: ```getDecodedTAF("KABC")```

Future work on this bot will include a "remarks" section decoder.