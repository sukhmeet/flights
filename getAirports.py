import sys
import os
import argparse
import json
from pprint import pprint
from datetime import datetime
from datetime import timedelta
import subprocess
import requests
import shutil
import ssl
import urllib.request


def getAirports():

    url_airport_ref="https://clients1.google.com/complete/search?client=flights&hl=en&gl=us&gs_rn=64&gs_ri=flights&requiredfields=regions_enabled%3Afalse%7Ctrains_enabled%3Atrue%7Cdeduplicate_cities_enabled%3Afalse%7Cairportless_locations_enabled%3Atrue&ds=flights&cp=4&gs_id=57&q=airport_to_search&callback=google.sbox.p50&gs_gbg=ubZgH31ccdKzlj7cm87O59vyZs"

    departure_search_str = input('Enter Departure Airport: ')
    url_airport = url_airport_ref.replace("airport_to_search", departure_search_str)
    url_airport1 = url_airport
    response = requests.get(url_airport, verify=False, stream=True)
    response = response.text.replace("google.sbox.p50 && google.sbox.p50(", "")
    response = response.replace("])", "]")


    data = json.loads(response)

    dict_airports_out = {}
    dict_airports_out['departure_airport']={}
    dict_airports_out['destination_airport']={}
    print("Select Airport # from the list below ")
    i = 0
    data_airports = data[1]
    for l in data_airports:
        dict = l[3]
        i += 1
        print("#" + str(i) +" : " + dict['a'], dict['d'], dict['f'])

    j = int(input('Enter your choice : '))
    d = data_airports[j-1]
    dict = d[3]
    dict_airports_out['departure_airport']['name']= dict['a'] + "," + dict['d'] + "," + dict['f']
    dict_airports_out['departure_airport']['code']= dict['a']


    # search for 2nd Airport


    destination_search_str = input('Enter Destination Airport: ')

    url_airport = url_airport_ref.replace("airport_to_search", destination_search_str)

    response = requests.get(url_airport, verify=False, stream=True)
    response = response.text.replace("google.sbox.p50 && google.sbox.p50(", "")
    response = response.replace("])", "]")


    data = json.loads(response)

    print("Select Airport # from the list below ")
    i = 0
    data_airports = data[1]
    for l in data_airports:
        dict = l[3]
        i += 1
        print("#" + str(i) +" : " + dict['a'], dict['d'], dict['f'])
    j = int(input('Enter your choice : '))
    d = data_airports[j-1]
    dict = d[3]


    dict_airports_out['destination_airport']['name']= dict['a'] + "," + dict['d'] + "," + dict['f']
    dict_airports_out['destination_airport']['code']= dict['a']

    # write to file
    with open('airports.json', 'w') as fp:
        json.dump(dict_airports_out, fp)

    print("Saved Airport Data \n")
    pprint(dict_airports_out)


def main():
    global cmd
    requests.packages.urllib3.disable_warnings()
    getAirports()
    print("\nDone\n")

main()
