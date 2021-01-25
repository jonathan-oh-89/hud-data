# hud-data


This repo pulls together FHA mortgage foreclosure and delinquency data from HUD. It also, pulls median home values from
zillow and calculates the quarterly change. The three data sets are joined on the county fips id and quarterly date.


# Motivation
This project was created to generate data for this dashboard:
https://public.tableau.com/profile/jonathan.oh2482#!/vizhome/Mortgagedelinquenciesandrisinghomeprices/Dashboard1

# Directions
- Clone repo to your computer.
- Download list of County FIPS Ids from: https://www.census.gov/geographies/reference-files/2018/demo/popest/2018-fips.html
- Download the most recent data for Counties from https://www.zillow.com/research/data/.
- Download FHA 90 day default data from https://hudgis-hud.opendata.arcgis.com/datasets/single-family-fha-90-day-defaults-by-tract
- Download FHA foreclosure data from https://hudgis-hud.opendata.arcgis.com/datasets/single-family-fha-mortgages-in-active-foreclosure-by-tract
- Run hud_data.py
- The result will be stored in data.csv

# What's in the csv files
- data.csv
  - Number of FHA loans in 90 day default territory. Aggregates updated on quarterly basis.
  - Number of FHA loans in active foreclosure. Aggregates updated on quarterly basis.
  - Change in median home values by county on quarterly basis.





