import requests
import pandas as pd
import json
# hotels.com
CITY_ID_URL = "https://hotels-com-provider.p.rapidapi.com/v1/destinations/search"
HOTEL_INFO_URL = "https://hotels-com-provider.p.rapidapi.com/v1/hotels/search"

def get_city_id_hotels(city, rapid_api_key):
    """Return city id of specific city from RapidAPI

    :param city: city name
    :param rapid_api_key: RapidAPI key
    :return: city id from RapidAPI
    """

    querystring = {"query": city, "currency": "USD", "locale": "en_US"}
    headers = {"X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com"}
    response = requests.request("GET", CITY_ID_URL, headers=headers, params=querystring)
    response_json = json.loads(response.text)
    hotels_city_id = pd.json_normalize(response_json["suggestions"]).entities[0][0]['destinationId']
    return hotels_city_id


def get_hotel_info_hotels(hotels_city_id, check_in, check_out, rapid_api_key):
    """Returns information about the available hotels according to the function parameters

    :param hotels_city_id: city id
    :param check_in: date for check in
    :param check_out: date for check out
    :param rapid_api_key: RapidAPI key
    :return: dataframe with information about the available hotels
    """

    all_df = pd.DataFrame()
    headers = {"X-RapidAPI-Key": rapid_api_key,
               "X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com"}
    for i in range(4):
        page_num = str(i + 1)
        querystring = {"checkin_date": check_in, "checkout_date": check_out,
                       "sort_order": "STAR_RATING_HIGHEST_FIRST",
                       "destination_id": hotels_city_id,
                       "adults_number": "1", "locale": "en_US",
                       "currency": "USD", "page_number": page_num}

        response = requests.request("GET", HOTEL_INFO_URL, headers=headers, params=querystring)
        response_json = json.loads(response.text)
        df = pd.json_normalize(response_json)
        df = pd.json_normalize(df["searchResults.results"][0])
        all_df = all_df.append(df)
        all_df.reset_index(inplace=True, drop=True)
    hotelscom_hotel_df = all_df[["name", "starRating", "coordinate.lon", "coordinate.lat", 'ratePlan.price.current']]
    return hotelscom_hotel_df


# hotels processing data
def process_hotels_data(hotelscom_hotel_df):
    hotelscom_hotel_df['price'] = 0
    hotelscom_hotel_df = hotelscom_hotel_df.apply(lambda row: fix_price(row), axis=1)
    hotelscom_hotel_df['Website'] = 'Hotels.com'
    del hotelscom_hotel_df["ratePlan.price.current"]
    return hotelscom_hotel_df
def fix_price(row):
    row['price'] = row['ratePlan.price.current']
    row['price'] = row['price'].replace("$", "")
    try:
        row['price'] = int(row['price'])
    except:
        pass
    return row