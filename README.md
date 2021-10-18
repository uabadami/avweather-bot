# avweather-bot
Uses Python to get aviation weather products. Functions to retrieve and decode METAR, TAF, and winds aloft information.

METARs and TAFs are two crucial pieces of information that pilots around the world use to get the weather. METARs (METeorological Aerodrome Reports) give pilots the most recent hourly weather report at a given airport or reporting station, while TAFs (Terminal Aerodrome Forecasts) provide meteorological predictions for periods of up to 24 hours. 

These products can be computer-generated or human-generated, and in the United States, are published by the National Weather Service's Aviation Weather Center via a computerized system. Examples of both METARs and TAFs are shown below.

```
METAR KABC 101234Z 12015G24KT 4SM +TSRA HZ FEW004 SCT011 OVC019 19/14 3002
TAF: KJFK 172336Z 1800/1906 28012G19KT P6SM FEW060 FM180600 29010KT P6SM FEW060...
```

Neither of these products are easily human-readable. 