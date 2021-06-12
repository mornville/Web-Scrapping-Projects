
import requests
from datetime import datetime,timedelta
import time
TOTAL_DAYS = 7
MIN_AGE_LIMIT = 45
PIN = ["562157", "560063"]
days_total = []
final_dates = []
for i in range(TOTAL_DAYS):
    days_total.append(datetime.today() +timedelta(i))

for i in days_total:
    final_dates.append(i.strftime("%d%m%y"))
i = 0
for pin in PIN:
    try:
        for date in final_dates:
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}".format(pin,date)
            result=requests.get(URL)
            json_result=result.json()
            if json_result["sessions"]:
                for sess_idx, session in enumerate(json_result["sessions"]):
                    if session["min_age_limit"] == MIN_AGE_LIMIT:
                        if session["available_capacity"]>0:
                            ("Date Available: " +  date)
                            print(str(sess_idx+1) + ". " + session["name"] + ", " + str(session["center_id"]) )
                            print("Dose1:" + str(session["available_capacity_dose1"])) 
                            print("Dose2:" + str(session["available_capacity_dose2"]))
    except Exception as e:
        print(e)
