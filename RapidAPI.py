import requests
import json


class API:
    def __init__(self, rapid_api_key):
        self.name = ""
        self.key = rapid_api_key
        self.host = "-com-provider.p.rapidapi.com"

    def city_id(self, city_id_url, headers, querystring):
        response = requests.request("GET", city_id_url, headers=headers, params=querystring)
        response_json = json.loads(response.text)
        return response_json

    def hotel_info(self, hotel_info_url, headers, querystring):
        response = requests.request("GET", hotel_info_url, headers=headers, params=querystring)
        response_json = json.loads(response.text)
        return response_json


class Priceline(API):
    def __init__(self, rapid_api_key):
        super().__init__(rapid_api_key)
        self.name = "priceline"
        self.host = self.name + self.host
        self.city_id_url = "https://priceline-com-provider.p.rapidapi.com/v1/hotels/locations"
        self.hotel_info_url = "https://priceline-com-provider.p.rapidapi.com/v1/hotels/search"


class HotelsCom(API):
    def __init__(self, rapid_api_key):
        super().__init__(rapid_api_key)
        self.name = "hotels"
        self.host = self.name + self.host
        self.city_id_url = "https://hotels-com-provider.p.rapidapi.com/v1/destinations/search"
        self.hotel_info_url = "https://hotels-com-provider.p.rapidapi.com/v1/hotels/search"

