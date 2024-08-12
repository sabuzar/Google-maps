import googlemaps


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


def get_businesses(api_key, keyword, location):
    # Get the coordinates (latitude and longitude) of the location
    latitude, longitude = get_coordinates(api_key, location)
    if latitude is None or longitude is None:
        return

    # Initialize the Google Maps client
    gmaps = googlemaps.Client(key=api_key)

    # Perform a text search based on the keyword and location
    places = gmaps.places(query=keyword, location=(latitude, longitude))

    # Extract the first 10 businesses' details
    businesses = places['results'][:10]

    # Extract image URLs from each business
    image_urls = []
    for business in businesses:
        # Get place details for each business
        place_details = gmaps.place(place_id=business['place_id'])
        # Extract image URLs if available
        photos = place_details['result'].get('photos', [])
        for photo in photos:
            photo_reference = photo['photo_reference']
            # Construct the URL using the photo reference
            url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
            image_urls.append(url)


    return image_urls


# Enter your Google Maps API key here
api_key = 'AIzaSyDnKCD2RxoPNQZyq9kLFpEWLHnEKacHAUo'

# Ensure your API key is authenticated
try:
    gmaps = googlemaps.Client(key=api_key)
except googlemaps.exceptions.ApiError as e:
    print("Error:", e)
    print("Please check your API key and ensure it is authenticated.")
else:
    # Enter the keyword you want to search for
    keyword = 'restaurants'

    # Enter the location where you want to search
    location = 'San Francisco'

    # Get image URLs of the top 10 businesses
    image_urls = get_businesses(api_key, keyword, location)


