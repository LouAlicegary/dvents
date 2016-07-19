from bs4 import BeautifulSoup
import requests
import time
import pprint
import re
import json
import math


class Scraper(object):
    
    """
    Returns an array of all the games found at the specified URL
    """
    def getEventDetails(self):

        date = "2016-07-22"
        page = 1
        maxPage = 1
        url = "http://www.metrotimes.com/detroit/EventSearch?narrowByDate=" + date + "&page=" + str(page)

        eventList = []

        while page <= maxPage:

            # Get search results from page
            soup = self.__getSoupFromURL(url)
            resultsObj = soup.find("div", id="searchResults")
            
            # Get result metrics
            resultsCountText = resultsObj.find("div", "listingsResultCount").text
            resultsCount = int(re.findall('\d+', resultsCountText)[0])            
            maxPage = int(math.ceil(resultsCount / 15.0))
            
            # Logging
            print "\n=== Scraping " + url + " ===\n"
            print "\n=== " + str(resultsCount) + " total results / " + str(maxPage) + " pages ===\n"

            # Add results to master list
            eventsOnPage = resultsObj.find_all("div", "EventListing")
            newEvents = self.__parseEvents(eventsOnPage, page)
            eventList.append(newEvents)

            # Incrment page counter and prep for next search
            page = page + 1
            url = "http://www.metrotimes.com/detroit/EventSearch?narrowByDate=" + date + "&page=" + str(page)

        return eventList


    """
    Grabs the HTML at the specified URL and returns a BeautifulSoup object
    """
    def __getSoupFromURL(self, url):

        try:
            r = requests.get(url)
        except:
            return None

        return BeautifulSoup(r.text, "html.parser")


    """

    """
    def __parseEvents(self, eventsOnPage, page):

        count = 1

        eventList = []

        for event in eventsOnPage:
            
            # Get source objects from page
            listing = event.find("div", "listing")
            jsonObj = json.loads(event.find("script").text)
            listingLocation = event.find("div", "listingLocation")
            
            eventObj = {}

            # Get required Fields (Name, Time, Description, Location Name, Location Address)
            try:
                eventObj["event_name"] = jsonObj[u"name"]
                eventObj["time"] = listing.find("h3").next_sibling.strip(' \t\n\r')
                eventObj["event_description"] = listing.find("p", "descripTxt").find(text=True, recursive=False).strip(' \t\n\r')
                eventObj["location_name"] = jsonObj[u"location"][u"name"]
                eventObj["location_address"] = jsonObj[u"location"][u"address"]
            except (KeyError, AttributeError):
                eventObj = None

            # Get URL (optional)
            try:
                eventObj["event_url"] = jsonObj[u"url"]
            except:
                None

            # Get Price (optional)
            try: 
                price = listing.find("span", "price")
                eventObj["price"] = price.find(text=True, recursive=False).strip(' \t\n\r')
            except (KeyError, AttributeError, TypeError):
                None
            
            # Append object to internal list
            if eventObj is not None:
                eventList.append(eventObj)

            # Logging
            print "\n\n\n"
            print "\n=== Result "+ str((page-1)*15+count) + " ===\n"
            pp.pprint(eventObj)
            count += 1

        return eventList


"""
Do the thing.
"""
def main():

    eventDetailsList = Scraper().getEventDetails()

    print "\n\n\n\n\n\n\n=== main() finished. ===\n"


if __name__ == "__main__":
   pp = pprint.PrettyPrinter(indent=4)
   main()