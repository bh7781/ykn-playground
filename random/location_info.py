"""
This script uses the Google Maps API to retrieve ratings and number of reviews places, and stores the information in a Pandas dataframe.
"""

import googlemaps
import pandas as pd

def get_hospital_ratings(api_key, hospitals):
    
    gmaps = googlemaps.Client(key=api_key)
    
    results = []
    
    for hospital in hospitals:
        geocode_result = gmaps.geocode(hospital + ', Pune, India')[0]['geometry']['location']
        lat = geocode_result['lat']
        lng = geocode_result['lng']

        places_result = gmaps.places_nearby(location=(lat, lng), radius=5000, type='hospital', name=hospital)['results'][0]
        place_id = places_result['place_id']

        details_result = gmaps.place(place_id=place_id, fields=['rating', 'user_ratings_total'])
        rating = details_result['result'].get('rating', 'Not available')
        num_reviews = details_result['result'].get('user_ratings_total', 'Not available')
        results.append({'Hospital': hospital, 'Rating': rating, 'Number of Reviews': num_reviews})
    
    return results


def get_place_details(api_key, places):
    # Create Google Maps client
    gmaps = googlemaps.Client(key=api_key)

    # Initialize empty lists to store results
    names = []
    ratings = []
    num_reviews = []
    cities = []
    states = []
    countries = []
    postal_codes = []

    for place in places:
        # Geocode the place name to get its latitude and longitude
        geocode_result = gmaps.geocode(place)[0]['geometry']['location']
        lat = geocode_result['lat']
        lng = geocode_result['lng']

        # Reverse geocode the latitude and longitude to get the address components
        reverse_geocode_result = gmaps.reverse_geocode((lat, lng))[0]
        address_components = reverse_geocode_result['address_components']

        # Extract the city, state, country, and postal code from the address components
        city = next((comp['long_name'] for comp in address_components if 'locality' in comp['types']), '')
        state = next((comp['long_name'] for comp in address_components if 'administrative_area_level_1' in comp['types']), '')
        country = next((comp['long_name'] for comp in address_components if 'country' in comp['types']), '')
        postal_code = next((comp['long_name'] for comp in address_components if 'postal_code' in comp['types']), '')

        # Search for the place near the latitude and longitude and get its place ID
        places_result = gmaps.places_nearby(location=(lat, lng), radius=5000, name=place)['results'][0]
        place_id = places_result['place_id']

        # Fetch the details of the place using its place ID and print its rating and number of reviews
        details_result = gmaps.place(place_id=place_id, fields=['rating', 'user_ratings_total'])
        rating = details_result['result'].get('rating', 'Not available')
        num_review = details_result['result'].get('user_ratings_total', 'Not available')

        # Append the results to the corresponding lists
        names.append(place)
        ratings.append(rating)
        num_reviews.append(num_review)
        cities.append(city)
        states.append(state)
        countries.append(country)
        postal_codes.append(postal_code)

    # Create a Pandas dataframe with the results
    df = pd.DataFrame({
        'place': names,
        'rating': ratings,
        'num_reviews': num_reviews,
        'city': cities,
        'state': states,
        'country': countries,
        'postal_code': postal_codes
    })

    return df


api_key = 'YOUR_API_KEY'

hospitals = [
    "Paranjpe Eye Clinic & Surgery Centre",
    "Patil Hospital General & Eye Hospital",
    "Patil Eye Hospital",
    "Vijayshree Day Care Eye Clinic",
    "Contacare Eye Hospital",
    "Hi Tech Eye Surgery And Laser Centre",
    "Axis Eye Clinic",
    "Jeevan Sparsh Eye Hospital",
    "Deshpande Eye Hospital and Laser Cer",
    "Dr Agarwal's Eye Hospital Ltd.",
    "Neo Vision Eye Care And Laser Center",
    "PBMAS HV Desai Eye Hospital"
]

results = get_hospital_ratings(api_key, hospitals)
df = pd.DataFrame(results)

print(df)

# api_key = 'YOUR_API_KEY'
# places = ['Eiffel Tower', 'Statue of Liberty', 'Taj Mahal']
# df = get_place_details(api_key, places)
# print(df)