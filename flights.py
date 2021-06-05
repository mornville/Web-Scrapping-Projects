"""
Requirements
pip install webdriver-manager
pip install selenium
pip insall webdriver
pip install pandas
python flights.py
"""

from selenium import webdriver
import time, csv, datetime
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

OPTS = webdriver.ChromeOptions()
OPTS.add_argument("--log-level=3") 
OPTS.headless = True
ATTRIBUTES = ['SNo.', 'Flight Name', 'Start Time', 'Source', 'Destination', 'Price']
MAX_NO_OF_TRIES = 6
NO_OF_ROW = 1
class Scraper:
    def __init__(self, source, dest, startDate):
        self.source = source    
        self.dest = dest
        self.startDate = startDate        
        self.search_url="https://www.ixigo.com/search/result/flight?from="+ self.source + "&to=" + self.dest + "&date="+self.startDate+"&returnDate=&adults=2&children=0&infants=0&class=e&source=Search%20Form"
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=OPTS)
        self.data = {}
        self.findClassTry = 0


    def waitForElementToLoad(self, className):
        try:
            self.driver.find_element_by_class_name(className)
            self.findClassTry = 0
            return
        except:
            self.findClassTry += 1
            if(self.findClassTry > MAX_NO_OF_TRIES):
                return
            else:
                print("Waiting for the webpage..")
                time.sleep(2)
            self.waitForElementToLoad(className)
            

    def searchByUrl(self, fileName):
        self.driver.get(self.search_url)
        ## Get number of pages
        try:
            self.waitForElementToLoad('page-num')
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
                index, flightData  = (self.searchForFlights(index, flightData))                    
        ## Writing data extracted into csv
        self.writeIntoCsv(flightData, fileName)

    def searchForFlights(self, index, flightData):
        self.waitForElementToLoad('c-flight-listing-row-v2')
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
            if flightType.lower()=='non-stop':
                if(index != 1):                    
                    flightData.append(None)

                flightData.append(flightNo)
                flightData.append(startTime)
                flightData.append(sourceName)
                flightData.append(destName)
                flightData.append(price)
                index+=1
        return index, flightData

    def writeIntoCsv(self, flightData, fileName):
        if len(flightData) ==  0:
            print("Couldn't find any data.")
            return
        
        with open(fileName, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(NO_OF_ROW, flightData)
            print("Data saved in " + fileName)
if __name__ == "__main__":
    try:        
        print("Enter INPUT filename without format: ")
        inpFile = input() + ".csv"
        df = pd.read_csv(inpFile)
        df.columns = range(df.shape[1])
        source = df[0]
        dest = df[1]
 
        print("Enter date in format(dd-mm-yyyy): ")
        startDate = input()
        datetime.datetime.strptime(startDate, "%d-%m-%Y")
        startDate.replace("/", "")

        print("Enter OUTPUT filename without format: ")
        outFile = input() + ".csv"

        with open(outFile,'w') as file:
            writer = csv.writer(file)
            writer.writerow(ATTRIBUTES)

        for i in range(0, len(source)):
            print(source[i], dest[i])
            NO_OF_ROW+=1
            a = Scraper(source[i], dest[i], startDate)
            a.searchByUrl(outFile)
        
    except Exception as e:
        print(e)
        print("Try Again")
