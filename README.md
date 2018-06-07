# flights

A simple set of scripts to find lowest priced flights from Google.

1. getAirports.py - Run this script to set departure and destination airports. 
   One you Select the airports the script write data to a json file. 
   If you are searching for the same pair then you need to do run it only once
2. flights.py - This script needs either start or end date as required parameters. It will search 
   for d days of trip within the period ( default 60 days ) and can filter on weekday of start or end date of the trip.

   usage: flights.py [-h] [-s S] [-e E] [-d D] [-p P] [-ws WS] [-we WE]

   optional arguments:
      -h, --help  show this help message and exit
      -s S        start date ( or end date is required )
      -e E        end date ( or start date is required )
      -d D        trip duration in days ( default 9 )
      -p P        search period in days
      -ws WS      filter by weekday of start date (Mon, Tue etc)
      -we WE      filter by weekday of end date
