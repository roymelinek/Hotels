from priceline import get_city_id_priceline, get_hotel_info_priceline, process_priceline_data
from hotelscom import get_city_id_hotels, get_hotel_info_hotels, process_hotels_data
from comparison import union_and_comparison, create_interactive_map
from HotelsClass import HotelInfo
from S3 import upload_file


def management(
        city: str, check_in_date: str, check_out_date: str, html_path: str,
        rapid_api_key: str, bucket_name: str, s3_object_name: str
):

    hotel = HotelInfo(city, check_in_date, check_out_date)
    priceline_city_id = get_city_id_priceline(hotel.city, rapid_api_key)
    priceline_hotel_df = get_hotel_info_priceline(
        priceline_city_id, hotel.check_in_date, hotel.check_out_date, rapid_api_key
    )
    process_priceline_hotel_df = process_priceline_data(priceline_hotel_df)

    hotels_city_id = get_city_id_hotels(hotel.city, rapid_api_key)
    hotelscom_hotel_df = get_hotel_info_hotels(hotels_city_id, hotel.check_in_date, hotel.check_out_date, rapid_api_key)
    process_hotelscom_hotel_df = process_hotels_data(hotelscom_hotel_df)

    all_hotels_df = union_and_comparison(process_hotelscom_hotel_df, process_priceline_hotel_df)

    assert create_interactive_map(all_hotels_df, html_path)
    assert upload_file(html_path, bucket_name, s3_object_name)
    return "Done!"
