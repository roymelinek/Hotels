# Hotels comparison

##### Project's target - 
comparing hotel prices between hotel reservation websites by city name and date of stay at the hotel.

##### Project's output -
interactive map with the hotels locations, the cheapest price for these dates and from which website it was taken.
<br />
<br />
<br />
###### Priceline - 
get_city_id_priceline : the function get city name and RapidAPI key, and return the cityID from Priceline API. <br />
get_hotel_info_priceline : the function get cityID, check-in&out dates, RapidAPI key, and return a dataframe with the information about the available hotels from Priceline API. <br />
process_priceline_data : the function get the dataframe from get_hotel_info_priceline and process the data. <br />

###### Hotels.com - 
get_city_id_hotels - the function get city name and RapidAPI key, and return the cityID from Hotels API. <br />
get_hotel_info_hotels - the function get cityID, check-in&out dates, RapidAPI key, and return a dataframe with the information about the available hotels from Hotels API. <br />
process_hotels_data - the function get the dataframe from get_hotel_info_priceline and process the data. <br />

###### HotelsClass -
creating a class of Hotel.

###### comparison - 
union_and_comparison : the function get the hotel dataframes, and union between the process hotel dataframes. <br />
create_interactive_map : the function get the union df and create an interactive map from the df, the map will save in the HTML_Path.

###### S3-
upload_file : the function get file path, S3 bucket name and S3 object name. <br />
the function upload the file from the path to the S3 bucket
