import pandas as pd
import folium

# Comparison
def union_and_comparison(process_hotelscom_hotel_df, process_priceline_hotel_df):
    process_hotelscom_hotel_df.rename(columns={"name":"HotelName","starRating":"StarRating","price":"HotelPrice","coordinate.lat":"Lat","coordinate.lon":"Lon"},inplace=True)
    process_priceline_hotel_df.rename(columns={"name":"HotelName","starRating":"StarRating","price":"HotelPrice","location.latitude":"Lat","location.longitude":"Lon"},inplace=True)
    process_priceline_hotel_df = process_priceline_hotel_df[0:100]
    process_priceline_hotel_df.reset_index(inplace=True,drop=True)

    all_hotels_df = pd.DataFrame()
    all_hotels_df = all_hotels_df.append([process_priceline_hotel_df, process_hotelscom_hotel_df])
    all_hotels_df.reset_index(inplace=True,drop=True)
    all_hotels_df["HotelPrice"] = all_hotels_df["HotelPrice"].astype(str)
    all_hotels_df['HotelPrice'] = all_hotels_df.HotelPrice.str.replace(",", '')
    all_hotels_df["HotelPrice"] = all_hotels_df["HotelPrice"].astype(float)
    all_hotels_df['HotelName'] = all_hotels_df.HotelName.str.replace(" Hotel", '')
    all_hotels_df['HotelName'] = all_hotels_df.HotelName.str.replace("Hotel ", '')
    all_hotels_df['HotelName'] = all_hotels_df['HotelName'].str.upper()

    all_hotels_df = all_hotels_df.groupby("HotelName", group_keys=False).apply(lambda x: x.loc[x["HotelPrice"].idxmin()])
    all_hotels_df.reset_index(drop=True , inplace=True)
    return all_hotels_df


# create map
def create_interactive_map(all_hotels_df, path):
    m = folium.Map(location=[all_hotels_df["Lat"].mean(),
    all_hotels_df.Lon.mean()], zoom_start=12.4, control_scale=True )
    tooltip = "Click here for hotel name"
    for index, location_info in all_hotels_df.iterrows():
        folium.Marker([location_info["Lat"], location_info["Lon"]],
                      popup="Hotel name- "+location_info["HotelName"]+"<br>"+
                      "Hotel Price- "+str(location_info["HotelPrice"])+"$"+"<br>"+
                      "Website -"+location_info['Website'],
                      tooltip=tooltip).add_to(m)
    try:
        m.save(path)
        print("Map saved in your path")
    except:
        print("Got a problem")