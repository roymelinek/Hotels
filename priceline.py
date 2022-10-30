import pandas as pd


def get_city_id_priceline(city, priceline):
    """Return city id of specific city from RapidAPI

    :param city: city name
    :param priceline: Priceline RapidAPI object
    :return: city id from RapidAPI
    """

    querystring = {"name": city, "search_type": "CITY"}
    headers = {
        "X-RapidAPI-Key": priceline.key,
        "X-RapidAPI-Host": priceline.host
    }
    response_json = priceline.city_id(priceline.city_id_url, headers, querystring)
    priceline_city_id = pd.json_normalize(response_json).cityID[0]
    return priceline_city_id


def get_hotel_info_priceline(priceline_city_id, check_in, check_out, priceline):
    """Returns information about the available hotels according to the function parameters

    :param priceline_city_id: city id
    :param check_in: date for check in
    :param check_out: date for check out
    :param priceline: Priceline RapidAPI object
    :return: dataframe with information about the available hotels
    """

    all_df = pd.DataFrame()
    headers = {
        "X-RapidAPI-Key": priceline.key,
        "X-RapidAPI-Host": priceline.host
    }
    for i in range(2):
        page_num = str(i)
        querystring = {
            "sort_order": "STAR", "location_id": priceline_city_id,
            "date_checkout": check_out, "date_checkin": check_in,
            "rooms_number": "1", "page_number": page_num
        }
        response_json = priceline.hotel_info(priceline.hotel_info_url, headers, querystring)
        df = pd.json_normalize(response_json)
        try:
            df = pd.json_normalize(df["hotels"][0])
            all_df = all_df.append(df)
            all_df.reset_index(inplace=True, drop=True)
        except:
            pass

    priceline_hotel_df = all_df[[
        "name", "starRating", "location.longitude", "location.latitude",
        "ratesSummary.minStrikePrice", "ratesSummary.minPrice"
    ]]
    priceline_hotel_df.name = priceline_hotel_df.name.astype(str)
    priceline_hotel_df["ratesSummary.minStrikePrice"] = priceline_hotel_df["ratesSummary.minStrikePrice"].astype(str)
    priceline_hotel_df = priceline_hotel_df[priceline_hotel_df.name != 'nan']
    return priceline_hotel_df


def process_priceline_data(priceline_hotel_df):
    priceline_hotel_df['price'] = None
    priceline_hotel_df = priceline_hotel_df.apply(lambda row: correct_price(row), axis=1)
    priceline_hotel_df.drop(['ratesSummary.minStrikePrice', 'ratesSummary.minPrice'], axis=1, inplace=True)
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
