
import requests
from datetime import datetime,timedelta
import time, sys
TOTAL_DAYS = 7
MIN_AGE_LIMIT = 45
PIN = ["562157", "560063"]
STATE = ["Karnataka"]
DISTRICT =["Bangalore Urban"]
STATES = [
    {"state_id":1,"state_name":"Andaman and Nicobar Islands"},
    {"state_id":2,"state_name":"Andhra Pradesh"},
    {"state_id":3,"state_name":"Arunachal Pradesh"},
    {"state_id":4,"state_name":"Assam"},
    {"state_id":5,"state_name":"Bihar"},
    {"state_id":6,"state_name":"Chandigarh"},{"state_id":7,"state_name":"Chhattisgarh"},{"state_id":8,"state_name":"Dadra and Nagar Haveli"},{"state_id":37,"state_name":"Daman and Diu"},{"state_id":9,"state_name":"Delhi"},{"state_id":10,"state_name":"Goa"},{"state_id":11,"state_name":"Gujarat"},{"state_id":12,"state_name":"Haryana"},{"state_id":13,"state_name":"Himachal Pradesh"},{"state_id":14,"state_name":"Jammu and Kashmir"},{"state_id":15,"state_name":"Jharkhand"},{"state_id":16,"state_name":"Karnataka"},{"state_id":17,"state_name":"Kerala"},{"state_id":18,"state_name":"Ladakh"},{"state_id":19,"state_name":"Lakshadweep"},{"state_id":20,"state_name":"Madhya Pradesh"},{"state_id":21,"state_name":"Maharashtra"},{"state_id":22,"state_name":"Manipur"},{"state_id":23,"state_name":"Meghalaya"},{"state_id":24,"state_name":"Mizoram"},{"state_id":25,"state_name":"Nagaland"},{"state_id":26,"state_name":"Odisha"},{"state_id":27,"state_name":"Puducherry"},{"state_id":28,"state_name":"Punjab"},{"state_id":29,"state_name":"Rajasthan"},{"state_id":30,"state_name":"Sikkim"},{"state_id":31,"state_name":"Tamil Nadu"},{"state_id":32,"state_name":"Telangana"},{"state_id":33,"state_name":"Tripura"},{"state_id":34,"state_name":"Uttar Pradesh"},{"state_id":35,"state_name":"Uttarakhand"},{"state_id":36,"state_name":"West Bengal"}
]
print(STATES["state_name"] == "Karnataka")
sys.exit()
def get_district_id():
    ## get state id
    URL = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    statesData = get_url_data_helper(URL)
    for state in statesData:
        print(state)
        
def calculate_days():
    days_total = []
    final_dates = []
    for i in range(TOTAL_DAYS):
        days_total.append(datetime.today() +timedelta(i))
    for i in days_total:
        final_dates.append(i.strftime("%d%m%y"))


def get_url_data_helper(URL):
    result=requests.get(URL)
    print(result)
    json_result=result.json() 
    return json_result

def findByPin(date):
    for pin in PIN:
        try:
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}".format(pin,date)
            json_result=get_url_data_helper(URL)
            
            if json_result["sessions"]:
                for sess_idx, session in enumerate(json_result["sessions"]):
                    if session["min_age_limit"] == MIN_AGE_LIMIT:
                        if session["available_capacity"]>0:
                            print("Date Available: " +  session["date"] +", "+ session["from"] + " to " + str(session["to"]))
                            print(str(sess_idx+1) + ". " + session["name"] + ", " + str(session["center_id"]) )
                            print("Dose1:" + str(session["available_capacity_dose1"])) 
                            print("Dose2:" + str(session["available_capacity_dose2"]))
        except Exception as e:
            print(e)

def findByDistrict(date):
    for dist in DISTRICT:
        try:
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}".format(dist,date)
            json_result = get_url_data_helper(URL)
            print(json_result)                
        except Exception as e:
            print(e)

if __name__=="__main__":
    STATE = "Karnataka"
    DISTRICT = []
    get_district_id()