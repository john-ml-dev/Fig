import scrapy
import json
from time import sleep
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class FlightSpider(scrapy.Spider):
    name = "flight"
        
    def start_requests(self):
        # start_urls = "https://www.flightradar24.com/data/airports"
        countries_url = "https://www.flightradar24.com/airports/country-list"
        yield scrapy.Request(url=countries_url, callback=self.parse_country)

                
    def parse_country(self,response):
        """Parsing Countries into JSON File"""

        country_details = json.loads(response.body)
        country_code = country_details.keys()
        codes = [country for country in country_code]
        countries = []
        for num, country in enumerate(country_details.values()):
            country["url"] = "https://www.flightradar24.com/data/airports/" + country["url"]
            country["code"] = codes[num]
            countries.append(country)
        # country_data = {"countries": countries}
        with open("countries.json",'w') as f:
            json.dump(countries,f, indent=2)
    
        airport_url = "https://www.flightradar24.com/airports/list"
        yield scrapy.Request(url=airport_url, callback= self.parse_airport)
       
        
    def parse_airport(self,response):
        """Parsing Airport into JSON File"""
        airport_details = json.loads(response.body)
        keys = ["icao", "iata", "name", "lat", "lon", "url","num_x","city", "code"]
        airports = []
        for airport in airport_details.values():
            airports.append({key:value for key,value in zip(keys,airport)})

        
        with open("airports.json", 'w') as f:
            json.dump(airports, f, indent=2)
        airlines_url = "https://www.flightradar24.com/mobile/airlines"
        yield scrapy.Request(url=airlines_url, callback=self.parse_airline)
        
    def parse_airline(self,response):
        """Parsing Airlines into JSON File"""
        airline_details = json.loads(response.body)
        airlines = airline_details["rows"]
        # airlines = {"airlines": airlines}
        with open("airlines.json", 'w') as f:
            json.dump(airlines, f, indent=2)


        

# https://www.flightradar24.com/webapi/v1/airport-disruptions?continent=0&period=live&type=both&indices=false
# https://data-live.flightradar24.com/clickhandler/?version=1.5&flight=352b26f8
# https://data-live.flightradar24.com/clickhandler/?version=1.5&flight=352b1036
# https://www.flightradar24.com/airports/list?version=0
# https://www.flightradar24.com/airports/traffic-stats/?airport=kms
# https://www.flightradar24.com/airports/traffic-stats/?airport=tkd

# pinned flights
# https://www.flightradar24.com/flights/pinned?limit
# country list
# https://www.flightradar24.com/airports/country-list
# airlines 
# https://www.flightradar24.com/mobile/airlines?format=2&version=0