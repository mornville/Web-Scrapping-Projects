"""
Requirements
pip install webdriver-manager
pip install selenium
pip insall webdriver
python flights.py
"""

from selenium import webdriver
import time, csv
import pandas as pd
import datetime
from webdriver_manager.chrome import ChromeDriverManager

OPTS = webdriver.ChromeOptions()
OPTS.add_argument("--log-level=3")
OPTS.headless = True
ATTRIBUTES = ['SNo.', 'Flight Name', 'Flight No.', 'Source', 'Destination', 'Source Name','Destination Name','Start Time','End Time', 'Total Time', 'Stops', 'Price']
MAX_NO_OF_TRIES = 10
FOUND_DATA = False
DRIVER =  webdriver.Chrome(ChromeDriverManager().install(), options=OPTS)


class Scraper:
    def __init__(self, source, dest, startDate, count=0):
        self.source = source    
        self.dest = dest
        self.startDate = startDate        
        self.search_url="https://www.ixigo.com/search/result/flight?from="+ self.source + "&to=" + self.dest + "&date="+self.startDate+"&returnDate=&adults=2&children=0&infants=0&class=e&source=Search%20Form"
        self.findClassTry = 0
        self.count = count


    def waitForElementToLoad(self, className):
        try:
            DRIVER.find_element_by_class_name(className)
            self.findClassTry = 0
            return
        except:
            self.findClassTry += 1
            if(self.findClassTry > MAX_NO_OF_TRIES):
                return
            else:
                print("Waiting for the webpage..")
                time.sleep(3)
            self.waitForElementToLoad(className)
            

    def searchByUrl(self, fileName):
        DRIVER.get(self.search_url)
        ## Get number of pages
        try:
            self.waitForElementToLoad('page-num')
            pagesFound = (DRIVER.find_elements_by_class_name("page-num"))
        except:
            pagesFound = []
      
        flightData = []
        flag = 1
        if(pagesFound == []):
            flightData  = (self.searchForFlights(flightData))
        else:
            for page in pagesFound:
                if flag == 1:
                    flag = 0
                    pass
                else:
                    page.click()
                flightData  = (self.searchForFlights(flightData))                    
        ## Writing data extracted into csv
        self.writeIntoCsv(flightData, fileName)
        return self.count

    def searchForFlights(self, flightData):
        self.waitForElementToLoad('c-flight-listing-row-v2')
        flightList = DRIVER.find_elements_by_class_name("c-flight-listing-row-v2")
        for flight in flightList:  
            airlineInfo = flight.find_element_by_class_name("airline-info")
            flightName, flightNo = airlineInfo.text.split("\n")
            ## Get source information
            sourceInfo = flight.find_element_by_class_name("left-wing")
            sourceCode, startTime, startDate, sourceName = sourceInfo.text.split("\n")

            ## Get destination information
            destInfo = flight.find_element_by_class_name("right-wing")
            destCode, endTime, endDate, destName = destInfo.text.split("\n")

            ## journeyInfo
            journeyInfo = flight.find_element_by_class_name("timeline-widget")
            totalTime, flightType = journeyInfo.text.split("\n")
            price = flight.find_element_by_class_name("c-price-display").text
            
            flightData.append([flightName, flightNo, sourceCode, destCode, sourceName, destName,  startTime, endTime, totalTime, flightType, price])
        return flightData

    def writeIntoCsv(self, flightData, fileName):
        if len(flightData) ==  0:
            print("Couldn't find any data.")
            return       
        print("\n" + str(len(flightData)) + " number of flights found, writing into " + fileName + "....") 
        with open(fileName, 'a') as file:
            writer = csv.writer(file)
            for row in flightData:
                self.count+=1
                row.insert(0, self.count)
                writer.writerow(row)
            print("Data saved in " + fileName)

if __name__=="__main__":
    try:
        print('\n' + '*'*50)
        inpFile = input("Enter INPUT filename without format: ") + ".csv"
        df = pd.read_csv(inpFile)
        df.columns = range(df.shape[1])
        source = df[0]
        dest = df[1]

        startDate = input("Enter date in format(dd/mm/yyyy): ")
        datetime.datetime.strptime(startDate, "%d/%m/%Y")
        startDate = startDate.replace("/", "")

        outFile = input("Enter OUTPUT filename without format: ") + ".csv"

        print('\n' + '*'*50)

        with open(outFile,'w') as file:
            writer = csv.writer(file)
            writer.writerow(ATTRIBUTES)
        
        count = 0
        for i in range(0, len(source)):  
            try:          
                print('\n' + '-'*50)
                print("Finding Flights for : " + source[i] + " to " + dest[i])
                a = Scraper(source[i], dest[i], startDate, count)
                count = a.searchByUrl(outFile)
            except Exception as e:
                print(e)
                pass
        print('\n' + '-'*50)
   
        print("Total " + str(count) + " number of flights found.")

    except Exception as e:
        print(e)
        print("Try Again")

