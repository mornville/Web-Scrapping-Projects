from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager

OPTS = webdriver.ChromeOptions()
OPTS.headless = True
class Scraper:
    def __init__(self, source, dest, startDate, returnDate="", noOfAdults=1, noOfChildren=0, noOfInfants=0, classType='e'):
        self.source = source
        self.dest = dest
        self.startDate = startDate
        self.returnDate = returnDate
        self.noOfAdults = str(noOfAdults)
        self.noOfChildren = str(noOfChildren)
        self.noOfInfants = str(noOfInfants)
        self.classType = classType
        self.search_url="https://www.ixigo.com/search/result/flight?from="+self.source + "&to="+self.dest + "&date=" + self.startDate + "&returnDate=" + self.returnDate + "&adults="+self.noOfAdults+"&children="+self.noOfChildren+"&infants="+self.noOfInfants+"&class="+self.classType+"&source=Search%20Form" 
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=OPTS)
    
    def searchByUrl(self):
        self.driver.get(self.search_url)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(5)
        flightList = self.driver.find_elements_by_class_name("c-flight-listing-row-v2")
        for flight in flightList:
            attributes = flight.text.split("\n")
            print(attributes)
            print(len(attributes))
            
a = Scraper('DEL', 'BOM', '11062021')
a.searchByUrl()
