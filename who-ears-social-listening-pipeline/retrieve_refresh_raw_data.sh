#!/bin/sh
cd data/01_raw
curl -O -L https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv
git clone https://github.com/citibeats-labs/who-ears
cd who-ears
git pull
cd ..