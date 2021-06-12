
from typing_extensions import Final
import requests
from datetime import datetime,timedelta
import json
TOTAL_DAYS = 7
MIN_AGE_LIMIT = 45
PIN = ["562157", "560063"]
days_total = []
final_dates = []
for i in range(TOTAL_DAYS):
    days_total.append(datetime.today() +timedelta(i))

for i in days_total:
    final_dates.append(i.strftime("%d%m%y"))

for pin in PIN:
    try:
        for date in final_dates:
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pin,date)
            result=requests.get(URL)
            json_result=result.json()
            if json_result["centers"]:
                for center_idx, center in enumerate(json_result["centers"]):
                    for sess_idx, session in enumerate(center["sessions"]):
                        if session["min_age_limit"] == MIN_AGE_LIMIT:
                            if session["available_capacity"]>0:
                                ("Date Available: " +  date)
                                print(str(center_idx+1) + ". " + center["name"] + ", " + str(center["center_id"]) )
                                print("Dose1:" + str(session["available_capacity_dose1"])) 
                                print("Dose2:" + str(session["available_capacity_dose2"]))
    except Exception as e:
        print(e)
