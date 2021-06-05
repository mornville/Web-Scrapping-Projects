"""
Requirements
pip install webdriver-manager
pip install selenium
pip insall webdriver
python flights.py
"""

from selenium import webdriver
import time, csv
from webdriver_manager.chrome import ChromeDriverManager

OPTS = webdriver.ChromeOptions()
OPTS.headless = False
ATTRIBUTES = ['SNo.', 'Flight Name', 'Flight No.', 'Source','Start Time', 'Start Date', 'Source Name', 'Destination', 'End Time', 'End Date', 'Destination Name', 'Total Time', 'Flight Type', 'Price']

class Scraper:
    def __init__(self, source, dest, startDate):
        self.source = source
        self.dest = dest
        self.startDate = startDate        
        self.search_url="https://www.ixigo.com/search/result/flight?from="+ self.source + "&to=" + self.dest + "&date="+self.startDate+"&returnDate=&adults=2&children=0&infants=0&class=e&source=Search%20Form"
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=OPTS)
        self.data = {}

    def searchByUrl(self, fileName):
        self.driver.get(self.search_url)
        time.sleep(5)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        ## Get number of pages
        try:
            pagesFound = (self.driver.find_elements_by_class_name("page-num"))
        except:
            pagesFound = []
      
        index, flightData = 1, []
        if(pagesFound == []):
            index, flightData  = (self.searchForFlights(index, flightData))
        else:
            for page in pagesFound:
                if index == 1:
                    pass
                else:
                    page.click()
                    time.sleep(3)                
                index, flightData  = (self.searchForFlights(index, flightData))                    
        ## Writing data extracted into csv
        self.writeIntoCsv(flightData, fileName)

    def searchForFlights(self, index, flightData):
        flightList = self.driver.find_elements_by_class_name("c-flight-listing-row-v2")
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
            
            flightData.append([index, flightName, flightNo, sourceCode, startTime, startDate, sourceName, destCode, endTime, endDate, destName, totalTime, flightType, price])
            index+=1
        return index, flightData

    def writeIntoCsv(self, flightData, fileName):
        fileName+=".csv"
        with open(fileName, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(ATTRIBUTES)
            for row in flightData:
                writer.writerow(row)

while(True):
    try:
        print("Enter Source Airport Code: ")
        sourceCode = input()
        print("Enter Destination Airport Code: ")
        destCode = input()
        print("Enter Travelling date (dd/mm/yyyy format): ")
        startDate = input()
        print("Enter File name without any format: ")
        fileName = input()
        startDate = startDate.replace("/", "")
        a = Scraper(sourceCode, destCode, startDate)
        a.searchByUrl(fileName)
        print('\n============================================================')
        print('DATA SAVED IN ' + fileName + ".csv")
        print('============================================================\n')
    except Exception as e:
        print(e)
        print('\n============================================================')
        print("Try Again")
        print('============================================================\n')

    