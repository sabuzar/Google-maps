import csv
import googlemaps

City='Amsterdam'
Keyword='solar panels'




appending_data = [
    'Search term','Business Number','Business Name','Address','Phone Number','Website','Rating','Opening Hours','Photo url','Business Status',"Review"
]
storing_file = open(f'output/data.csv', 'a', newline="",encoding='utf-8')
writer = csv.writer(storing_file)
writer.writerow(appending_data)
storing_file.close()

def get_coordinates(api_key, location):
    gmaps = googlemaps.Client(key=api_key)
    geocode_result = gmaps.geocode(location)

    if geocode_result:
        latitude = geocode_result[0]['geometry']['location']['lat']
        longitude = geocode_result[0]['geometry']['location']['lng']
        return latitude, longitude
    else:
        print(f"Could not find coordinates for {location}.")
        return None, None
def remove_newlines(input_text):
    # Replace all newline characters with an empty string
    output_text = input_text.replace('\n', '')
    return output_text




def remove_commas(input_list):
    # Concatenate all elements of the list into a single string
    concatenated_string = ''.join(input_list)
    # Remove commas from the concatenated string
    output_string = concatenated_string.replace(',', '')
    return output_string
def search_businesses(api_key, keyword, location):
    # Get the coordinates (latitude and longitude) of the location
    latitude, longitude = get_coordinates(api_key, location)
    if latitude is None or longitude is None:
        return

    # Initialize the Google Maps client
    gmaps = googlemaps.Client(key=api_key)

    # Perform a text search based on the keyword and location
    places = gmaps.places(query=keyword, location=(latitude, longitude))
    businesses = places['results'][:10]
    for idx, business in enumerate(businesses, start=1):
        place_details = gmaps.place(place_id=business['place_id'],language='nl')

        phone_number = place_details['result'].get('formatted_phone_number', 'N/A')
        website_link = place_details['result'].get('website', 'N/A')
        rating = place_details['result'].get('rating', 'N/A')
        opening_hours = place_details['result'].get('opening_hours', {}).get('weekday_text', 'N/A')
        Address=business.get('formatted_address', 'N/A')
        reviews = place_details['result'].get('reviews', [])
        if reviews:
            last_review = reviews[-1]
            author_name = last_review['author_name']
            rating2 = last_review['rating']
            text = last_review['text']
        else:
            author_name=None
            rating2=None
            text=None
        image_urls = []
        photos = place_details['result'].get('photos', [])
        for photo in photos:
            photo_reference = photo['photo_reference']
            # Construct the URL using the photo reference
            url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
            image_urls.append(url)

        appending_data = [
            Keyword+" "+City,idx,business['name'],remove_commas(Address),phone_number,website_link,rating,remove_commas(opening_hours),remove_commas(image_urls), business.get('business_status', 'N/A'),f'Author: {author_name}'+' '+f"Rating: {rating2}"+' '+f"Text: {remove_newlines(str(text))}"
        ]
        storing_file = open('output/data.csv', 'a', newline="",encoding='utf-8')
        writer = csv.writer(storing_file)
        writer.writerow(appending_data)
        storing_file.close()
        


# Enter your Google Maps API key here
api_key = 'api key'

# Ensure your API key is authenticated
try:
    gmaps = googlemaps.Client(key=api_key)
    #gmaps.places('pizza')
except googlemaps.exceptions.ApiError as e:
    print("Error:", e)
    print("Please check your API key and ensure it is authenticated.")
else:
    # Enter the keyword you want to search for
    keyword = Keyword

    # Enter the location where you want to search
    location = City

    # Call the function to search for businesses
    search_businesses(api_key, keyword, location)
