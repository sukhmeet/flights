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
import urllib.parse
import urllib.request
def init():
    global base_url
    base_url = """https://www.google.com/async/flights/calendar?ei=JlsZW7agE6SO5wLykYLoAg&yv=3&async=data:%5B%5B%5B%5B%5B%5Bnull%2C%5B%5B%22departture_airport%22%2C0%5D%5D%5D%2C%5Bnull%2C%5B%5B%22destination_airport%22%2C0%5D%5D%5D%2C%5B%222017-06-23%22%5D%2Cnull%5D%2C%5B%5Bnull%2C%5B%5B%22destination_airport%22%2C0%5D%5D%5D%2C%5Bnull%2C%5B%5B%22departture_airport%22%2C0%5D%5D%5D%2C%5B%222017-07-03%22%5D%2Cnull%5D%5D%2Cnull%2C%5B1%5D%2Cnull%2Cnull%2Cnull%2Cnull%2C1%2Cnull%2C2%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C0%5D%2C%5B%5B%5Bnull%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2Cnull%2C%5B%5D%2C%5B%5D%5D%2C%5Bnull%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2Cnull%2C%5B%5D%2C%5B%5D%2Cnull%2Cnull%5D%5D%5D%2Cnull%2C%22USD%22%2C3%2C%5B%5D%5D%2C0%2C%5B%222017-06-16%22%5D%2C%5B%222017-08-18%22%5D%2C3%5D,s:s,tfg-bgr:%5B%22!4eKl4sNCCK7AmFJBCKhE-P2LclJsZeICAAAASlIAAAAKmQFWqwocDRQucOJ2VR3OIsqxf5dE3kiEUZT3z7Y1gRniHwxCFJq4e-5LWB6otcE8dWwIxLZCH8lhYrL1iw8FunVUGPpybkNUHbV8DPMAoCJ9uGqcMHEJ9xI9q02TbNZfYB5_k5ykalJf74fz2nXv0lMtjuICMLZ1HAjaXOHmtoLhhh79r7nNCm5bKCERA6xQ_bEo5CqUTXpHbyuO75j_vYodwaMe19PQQubDJJWGtvEAsn7c16B4IqiDI8EQxvHKtE5lpg5d6kFguaJlqQYROf7NIn7wflGptGLVo3jAvr5bYoRHEoKENlo319RTvb16i83Ea-ICCgdv1zFUgkm11uIP8dMPrnVQ7CKQ-KHk6hdi4Idw_5b3KWPmXsiCMCVdMDXK7qJFoJLgcZuFuccRnlkFbEE91dpD5W9mp-gPSDCewvqSRS7LQTmg-Uu4sQOoWn_Ghzuz4GNB%22%2Cnull%2Cnull%2C10%2Cnull%2Cnull%2Cnull%2C0%5D,_fmt:jspb"""

def main():
    global base_url
    requests.packages.urllib3.disable_warnings()
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="start date ( or end date is required ) " , action="store")
    parser.add_argument("-e", help="end date ( or start date is required ) ", action="store")
    parser.add_argument("-d", help="trip duration in days ( default 9 )", action="store", type=int , default=9)
    parser.add_argument("-p", help="search period in days ( default 60 )", action="store", type=int ,
    default=60)
    parser.add_argument("-ws", help="filter by weekday of start date (Mon, Tue etc)", action="store")
    parser.add_argument("-we", help="filter by weekday of end date", action="store")
    args = parser.parse_args()
    init()
    with open('airports.json') as f:
        airports = json.load(f)

    start_dt_str = args.s
    end_dt_str = args.e
    trip_duration = args.d
    max_search_days = args.p
    weekday_start_date = args.ws
    weekday_end_date = args.we

    if start_dt_str is None and end_dt_str is None:
        print("Start or End date must be provided")
        exit(1)

    if start_dt_str is None:
        end_dt = datetime.strptime(end_dt_str, "%Y-%m-%d")
        start_dt = end_dt - timedelta(days=max_search_days)
        start_dt_str = start_dt.strftime("%Y-%m-%d")
    else:
        start_dt = datetime.strptime(start_dt_str, "%Y-%m-%d")

    if end_dt_str is None:
        start_dt = datetime.strptime(start_dt_str, "%Y-%m-%d")
        end_dt = start_dt + timedelta(days=max_search_days)
        end_dt_str = end_dt.strftime("%Y-%m-%d")
    else:
        end_dt = datetime.strptime(end_dt_str, "%Y-%m-%d")


    s = "departture_airport"
    #pprint(airports)
    code = airports['departure_airport']['code']
    r = urllib.parse.quote_plus(code)
    #print("r is " + r + "code is " + code)
    base_url = base_url.replace(s, r)

    s = "destination_airport"
    code = airports['destination_airport']['code']
    r = urllib.parse.quote_plus(code)
    #print("r is " + r + "code is " + code)
    base_url = base_url.replace(s, r)


    base_url = base_url.replace("2017-06-23", start_dt_str)
    interval_dt = start_dt + timedelta(days=trip_duration)
    interval_dt_str = interval_dt.strftime("%Y-%m-%d")
    base_url=base_url.replace("2017-07-03", interval_dt_str)
    base_url=base_url.replace("2017-06-16", start_dt_str)
    base_url=base_url.replace("2017-08-18", end_dt_str)
    #print(start_dt_str , interval_dt_str , end_dt_str)
    #print(base_url)
    response = requests.get(base_url, verify=False, stream=True)
    #print(response.text)
    response = response.text.replace("google.sbox.p50 && google.sbox.p50(", "")
    response = response.replace(")]}'", "")


    data = json.loads(response)

    datalist = data['_r'][0]
    print("\nShowing data for : " + airports['departure_airport']['name'] + " to " + airports['destination_airport']['name']+ "\n")
    for data in datalist:
        res_start_dt_str = data[0][0]
        res_end_dt_str = data[1][0]
        res_start_dt = datetime.strptime(res_start_dt_str, "%Y-%m-%d")
        res_end_dt = datetime.strptime(res_end_dt_str, "%Y-%m-%d")
        price = round(data[3], 0)
        res_start_dt_str = res_start_dt.strftime("%a %d-%b")
        res_end_dt_str = res_end_dt.strftime("%a %d-%b")
        bPrint = True
        if weekday_start_date is not None:
            if not weekday_start_date in res_start_dt_str:
                bPrint = False
        if weekday_end_date is not None:
            if not weekday_end_date in res_end_dt_str:
                bPrint = False
        if bPrint:
            print(res_start_dt_str, " " , res_end_dt_str , " " , str(price))

main()
