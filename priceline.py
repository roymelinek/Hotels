import requests
import pandas as pd
import json
# priceline
# priceline city id location query
CityID_url = "https://priceline-com-provider.p.rapidapi.com/v1/hotels/locations"
HotelInfo_url = "https://priceline-com-provider.p.rapidapi.com/v1/hotels/search"

def get_city_id_priceline(city,RapidAPI_key):
    querystring = {"name":city,"search_type":"CITY"}
    headers = {"X-RapidAPI-Key": RapidAPI_key,
    "X-RapidAPI-Host": "priceline-com-provider.p.rapidapi.com"}
    response = requests.request("GET", CityID_url, headers=headers, params=querystring)
    response_json = json.loads(response.text)
    priceline_city_id = pd.json_normalize(response_json).cityID[0]
    return priceline_city_id

# priceline hotels info query
def get_hotel_info_priceline(priceline_city_id, check_in, check_out, RapidAPI_key):
    all_df = pd.DataFrame()
    headers = {"X-RapidAPI-Key": RapidAPI_key,
    "X-RapidAPI-Host": "priceline-com-provider.p.rapidapi.com"}
    for i in range(2):
        page_num = str(i)
        querystring = {"sort_order":"STAR","location_id":priceline_city_id,
                       "date_checkout":check_out,"date_checkin":check_in,
                       "rooms_number":"1","page_number":page_num}
        response = requests.request("GET", HotelInfo_url, headers=headers, params=querystring)
        response_json = json.loads(response.text)
        df = pd.json_normalize(response_json)
        df = pd.json_normalize(df["hotels"][0])
        all_df = all_df.append(df)
        all_df.reset_index(inplace = True ,drop = True)
    priceline_hotel_df = all_df[["name","starRating","location.longitude","location.latitude","ratesSummary.minStrikePrice","ratesSummary.minPrice"]]
    priceline_hotel_df.name = priceline_hotel_df.name.astype(str)
    priceline_hotel_df["ratesSummary.minStrikePrice"] = priceline_hotel_df["ratesSummary.minStrikePrice"].astype(str)
    priceline_hotel_df = priceline_hotel_df[priceline_hotel_df.name!='nan']
    return priceline_hotel_df

# priceline processing data
def process_priceline_data(priceline_hotel_df):
    priceline_hotel_df['price'] = None
    priceline_hotel_df = priceline_hotel_df.apply(lambda row: correct_price(row), axis=1)
    priceline_hotel_df.drop(['ratesSummary.minStrikePrice','ratesSummary.minPrice' ], axis=1 , inplace=True)
    priceline_hotel_df['Website'] = 'Priceline'
    return priceline_hotel_df
def correct_price(row):
    if row["ratesSummary.minStrikePrice"] == 'nan':
        row['price'] = row['ratesSummary.minPrice']
    else:
        row['price'] = row['ratesSummary.minStrikePrice']
    row['price'] = float(row['price'])
    row['price'] = round(row['price'])
    row['price'] = int(row['price'])
    return row