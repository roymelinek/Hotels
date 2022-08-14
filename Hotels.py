from urllib.request import urlopen
import requests
import pandas as pd
import time
import json
import folium
from priceline import  get_city_id_priceline , get_hotel_info_priceline , process_priceline_data
from hotelscom import get_city_id_hotels, get_hotel_info_hotels , process_hotels_data
from comparison import union_and_comparison, create_interactive_map
from HotelsClass import HotelInfo

if __name__ == "__main__":
    City = input("Input city name")
    CheckIn_date = input("Input check in date yyyy-mm-dd")
    CheckOut_date = input("Input check out date yyyy-mm-dd")
    HTML_Path = input("input your html path for the map")
    RapidAPI_key = input("Input your RapidAPI key use the API")
    hotel = HotelInfo(City , CheckIn_date , CheckOut_date)


    Priceline_city_id = get_city_id_priceline(hotel.city, RapidAPI_key)
    priceline_hotel_df = get_hotel_info_priceline(Priceline_city_id, hotel.CheckIn_date, hotel.CheckOut_date, RapidAPI_key)
    process_priceline_hotel_df = process_priceline_data(priceline_hotel_df)


    hotels_city_id = get_city_id_hotels(hotel.city, RapidAPI_key)
    hotelscom_hotel_df = get_hotel_info_hotels(hotels_city_id, hotel.CheckIn_date, hotel.CheckOut_date, RapidAPI_key)
    process_hotelscom_hotel_df = process_hotels_data(hotelscom_hotel_df)


    all_hotels_df = union_and_comparison(process_hotelscom_hotel_df, process_priceline_hotel_df)
    create_interactive_map(all_hotels_df, HTML_Path)