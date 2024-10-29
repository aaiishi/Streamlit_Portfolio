import requests
from datetime import datetime, timedelta
import time
from fuzzywuzzy import process
import random

city_codes = {
    "New York City, USA": "JFK",
    "Los Angeles, USA": "LAX",
    "Chicago, USA": "ORD",
    "London, UK": "LHR",
    "Paris, France": "CDG",
    "Tokyo, Japan": "HND",
    "Dubai, UAE": "DXB",
    "Hong Kong": "HKG",
    "Singapore": "SIN",
    "Sydney, Australia": "SYD",
    "Frankfurt, Germany": "FRA",
    "Toronto, Canada": "YYZ",
    "Mexico City, Mexico": "MEX",
    "Amsterdam, Netherlands": "AMS",
    "São Paulo, Brazil": "GRU",
    "Beijing, China": "PEK",
    "Mumbai, India": "BOM",
    "Bangkok, Thailand": "BKK",
    "Istanbul, Turkey": "IST",
    "Seoul, South Korea": "ICN",
    "Moscow, Russia": "SVO",
    "Rome, Italy": "FCO",
    "Madrid, Spain": "MAD",
    "Zurich, Switzerland": "ZRH",
    "Johannesburg, South Africa": "JNB",
    "Vienna, Austria": "VIE",
    "Brussels, Belgium": "BRU",
    "Cairo, Egypt": "CAI",
    "Delhi, India": "DEL",
    "Kuala Lumpur, Malaysia": "KUL",
    "Doha, Qatar": "DOH",
    "Athens, Greece": "ATH",
    "Copenhagen, Denmark": "CPH",
    "Manila, Philippines": "MNL",
    "Stockholm, Sweden": "ARN",
    "Dublin, Ireland": "DUB",
    "Miami, USA": "MIA",
    "Buenos Aires, Argentina": "EZE",
    "Santiago, Chile": "SCL",
    "Lisbon, Portugal": "LIS",
    "Rio de Janeiro, Brazil": "GIG",
    "Oslo, Norway": "OSL",
    "Auckland, New Zealand": "AKL",
    "Lima, Peru": "LIM",
    "Helsinki, Finland": "HEL",
    "Vancouver, Canada": "YVR",
    "Munich, Germany": "MUC",
    "Bangalore, India": "BLR",
    "Karachi, Pakistan": "KHI",
    "Jakarta, Indonesia": "CGK",
    "Tehran, Iran": "IKA",
    "Algiers, Algeria": "ALG",
    "Casablanca, Morocco": "CMN",
    "Lagos, Nigeria": "LOS",
    "Nairobi, Kenya": "NBO",
    "Beirut, Lebanon": "BEY",
    "Tel Aviv, Israel": "TLV",
    "Panama City, Panama": "PTY",
    "Havana, Cuba": "HAV",
    "Ho Chi Minh City, Vietnam": "SGN",
    "Guangzhou, China": "CAN",
    "Shenzhen, China": "SZX",
    "Shanghai, China": "PVG",
    "Melbourne, Australia": "MEL",
    "Perth, Australia": "PER",
    "Montreal, Canada": "YUL",
    "Manchester, UK": "MAN",
    "Edinburgh, UK": "EDI",
    "Birmingham, UK": "BHX",
    "Atlanta, USA": "ATL",
    "Dallas, USA": "DFW",
    "Houston, USA": "IAH",
    "San Francisco, USA": "SFO",
    "Las Vegas, USA": "LAS",
    "Seattle, USA": "SEA",
    "Washington D.C., USA": "IAD",
    "Orlando, USA": "MCO",
    "Boston, USA": "BOS",
    "Charlotte, USA": "CLT",
    "Philadelphia, USA": "PHL",
    "Denver, USA": "DEN",
    "San Diego, USA": "SAN",
    "Minneapolis, USA": "MSP",
    "Phoenix, USA": "PHX",
    "Detroit, USA": "DTW",
    "St. Louis, USA": "STL",
    "Kansas City, USA": "MCI",
    "Salt Lake City, USA": "SLC",
    "Tampa, USA": "TPA",
    "New Orleans, USA": "MSY",
    "Pittsburgh, USA": "PIT",
    "Cleveland, USA": "CLE",
    "Cincinnati, USA": "CVG",
    "Columbus, USA": "CMH",
    "Portland, USA": "PDX",
    "Indianapolis, USA": "IND",
    "Raleigh, USA": "RDU",
    "Austin, USA": "AUS",
    "San Antonio, USA": "SAT",
    "Memphis, USA": "MEM",
    "Florence, Italy": "FLR",
    "Reykjavik, Iceland": "KEF",
    "Nice, France": "NCE",
    "Malé, Maldives": "MLE",
    "Phuket, Thailand": "HKT",
    "Marrakech, Morocco": "RAK",
    "Kyoto, Japan": "UKY",
    "Barcelona, Spain": "BCN",
    "Venice, Italy": "VCE",
    "Bali, Indonesia": "DPS",
    "Cancún, Mexico": "CUN"
}


weather_possible = {
    'Clear sky',
    'Few clouds',
    'Scattered clouds',
    'Broken clouds',
    'Overcast clouds',
    'Mist',
    'Smoke',
    'Haze',
    'Dust',
    'Fog',
    'Sand, dust whirls',
    'Squalls',
    'Tornado',
    'Snow',
    'Rain',
    'Drizzle',
    'Thunderstorm',
    'Thunderstorm with light rain',
    'Thunderstorm with rain',
    'Thunderstorm with heavy rain',
    'Thunderstorm with light drizzle',
    'Thunderstorm with drizzle',
    'Thunderstorm with heavy drizzle',
    'Thunderstorm with hail',
    'Sleet',
    'Shower rain',
    'Heavy intensity rain',
    'Very heavy rain',
    'Freezing rain',
    'Light rain and snow',
    'Rain and snow',
    'Light shower snow',
    'Shower snow',
    'Heavy shower snow'
}


# Amadeus API credentials
API_KEY = 'Hia3mrHL5Enqce1DBCUZAtnBCV5r3ZyZ'
API_SECRET = 'AmlLKKWM2cwmufrT'
# OpenWeather API key
API_WEATHER = '82bd0ac1ed6570afbf57976105eed6b9'

# Function to authenticate and get access token
def get_amadeus_access_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': API_KEY,
        'client_secret': API_SECRET
    }
    response = requests.post(url, headers=headers, data=data)
    token = response.json().get('access_token')
    return token

# Function to search for flights
# Function to search for flights
import requests

def search_flights(origin, destination, departure_date, adults):
    token = get_amadeus_access_token()
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": str(adults),
        "max": 5  # Limit results
    }

    '''# Print parameters for debugging
    print("Requesting flights with parameters:")
    print(f"Origin: {origin}, Destination: {destination}, Departure Date: {departure_date}, Adults: {adults}")'''

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        flights = response.json().get('data', [])
        #print(f"Found {len(flights)} flights.")

        # Create a list to hold structured flight information
        structured_flights = []
        for flight in flights:
            price = flight['price']['total']
            currency = flight['price']['currency']

            # Loop through all segments in the itinerary
            for itinerary in flight['itineraries']:
                segments_info = []
                for segment in itinerary['segments']:
                    departure_time = segment['departure']['at']
                    departure_location = segment['departure']['iataCode']
                    arrival_location = segment['arrival']['iataCode']
                    airline = segment['carrierCode']  # The operating airline
                    flight_number = segment['number']  # Flight number
                    aircraft_code = segment['aircraft']['code']  # Aircraft model code
       
                    # Collect segment information
                    segments_info.append({
                        "departure_time": departure_time,
                        "departure_location": departure_location,
                        "arrival_location": arrival_location,
                        "airline": airline,
                        "flight_number": flight_number,
                        "aircraft": aircraft_code,
                    })

                structured_flights.append({
                    "price": price,
                    "currency": currency,
                    "segments": segments_info
                })

        return structured_flights
    else:
        print(f"Error fetching flights: {response.status_code}")
        print(response.json())  # Print the response body for more details
        return []  # Return an empty list on error



# Function to search for hotels
def search_hotels(city_code, radius=5, ratings="5"):
    token = get_amadeus_access_token() 
    url = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "cityCode": city_code,
        "radius": radius,
        "ratings": ratings        
    }

    response = requests.get(url, headers=headers, params=params)
    hotels_list = []  # Initialize a list to store hotel names

    if response.status_code == 200:
        hotels = response.json().get('data', [])
        #print(f"Found {len(hotels)} hotels:")
        
        for nb, hotel in enumerate(hotels):
            if nb < 5:  # Limit to the first 5 hotels
                name = hotel['name']
                hotels_list.append(name)  # Add the hotel name to the list

        return hotels_list  # Return the list of hotel names
    else:
        print(f"Error fetching hotels: {response.status_code}")
        return []  # Return an empty list in case of an error

#Function to search for weather
def get_weather_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temperature = data['main']['temp']
            weather_description = data['weather'][0]['description'].capitalize()
            return temperature, weather_description
        else:
            print(f"Error fetching weather data: {response.status_code}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None
    
# Function to check if the weather description matches the expected family
def matches_weather_family(weather_description, weather_preference):
    # Define weather family mapping
    weather_families = {
    "Clear Conditions": [
        "Clear sky",
        "Few clouds"
    ],
    "Cloudy Conditions": [
        "Scattered clouds",
        "Broken clouds",
        "Overcast clouds"
    ],
    "Fog and Haze": [
        "Mist",
        "Smoke",
        "Haze",
        "Fog",
        "Dust",
        "Sand, dust whirls"
    ],
    "Precipitation": {
        "Rain": [
            "Rain",
            "Drizzle",
            "Shower rain",
            "Heavy intensity rain",
            "Very heavy rain",
            "Freezing rain",
            "Light rain and snow",
            "Rain and snow"
        ],
        "Snow": [
            "Snow",
            "Light shower snow",
            "Shower snow",
            "Heavy shower snow"
        ],
        "Sleet": [
            "Sleet"
        ]
    },
    "Storms": {
        "Thunderstorm": [
            "Thunderstorm",
            "Thunderstorm with light rain",
            "Thunderstorm with rain",
            "Thunderstorm with heavy rain",
            "Thunderstorm with light drizzle",
            "Thunderstorm with drizzle",
            "Thunderstorm with heavy drizzle",
            "Thunderstorm with hail"
        ]
    },
    "Extreme Weather": [
        "Squalls",
        "Tornado"
    ]
}

    # Check if the provided weather description is in the selected weather family
    for family, conditions in weather_families.items():
        if weather_preference == family:
            if weather_description in conditions:
                return True
    return False

def get_country_code(city_name):
    # Look up the city name in the city_codes dictionary
    airport_code = city_codes.get(city_name)
    
    # Return the airport code if found, otherwise return a not found message
    if airport_code:
        return airport_code
    else:
        return "City not found in the database."
    
def get_closest_city(user_input):
    # Extract the city names from the city_codes dictionary
    cities = list(city_codes.keys())
    
    # Use fuzzy matching to find the closest city
    closest_match = process.extractOne(user_input, cities)
    
    # Return the closest city name
    return closest_match[0] if closest_match else "No close match found."
    
def from_airport_to_city(airport_code):
    # Dictionary mapping of airport codes to city codes
    airport_to_city_map = {
    "JFK": "NYC",
    "LAX": "LAX",
    "CHI": "CHI",
    "LHR": "LON",
    "CDG": "PAR",
    "HND": "TYO",
    "DXB": "DXB",
    "HKG": "HKG",
    "SIN": "SIN",
    "SYD": "SYD",
    "FRA": "FRA",
    "YYZ": "TOR",
    "MEX": "MEX",
    "AMS": "AMS",
    "GRU": "SAO",
    "PEK": "BJS",
    "BOM": "BOM",
    "BKK": "BKK",
    "IST": "IST",
    "ICN": "SEL",
    "SVO": "MOW",
    "FCO": "ROM",
    "MAD": "MAD",
    "ZRH": "ZRH",
    "JNB": "JNB",
    "VIE": "VIE",
    "BRU": "BRU",
    "CAI": "CAI",
    "DEL": "DEL",
    "KUL": "KUL",
    "DOH": "DOH",
    "ATH": "ATH",
    "CPH": "CPH",
    "MNL": "MNL",
    "ARN": "STO",
    "DUB": "DUB",
    "MIA": "MIA",
    "EZE": "BUE",
    "SCL": "SCL",
    "LIS": "LIS",
    "GIG": "RIO",
    "OSL": "OSL",
    "AKL": "AKL",
    "LIM": "LIM",
    "HEL": "HEL",
    "YVR": "VAN",
    "MUC": "MUC",
    "BLR": "BLR",
    "KHI": "KHI",
    "CGK": "JKT",
    "IKA": "THR",
    "ALG": "ALG",
    "CMN": "CAS",
    "LOS": "LOS",
    "NBO": "NBO",
    "BEY": "BEY",
    "TLV": "TLV",
    "PTY": "PTY",
    "HAV": "HAV",
    "SGN": "SGN",
    "CAN": "CAN",
    "SZX": "SZX",
    "PVG": "SHA",
    "MEL": "MEL",
    "PER": "PER",
    "YUL": "YMQ",
    "MAN": "MAN",
    "EDI": "EDI",
    "BHX": "BHX",
    "ATL": "ATL",
    "DFW": "DFW",
    "IAH": "HOU",
    "SFO": "SFO",
    "LAS": "LAS",
    "SEA": "SEA",
    "IAD": "WAS",
    "MCO": "ORL",
    "BOS": "BOS",
    "CLT": "CLT",
    "PHL": "PHL",
    "DEN": "DEN",
    "SAN": "SAN",
    "MSP": "MSP",
    "PHX": "PHX",
    "DTW": "DET",
    "STL": "STL",
    "MCI": "MKC",
    "SLC": "SLC",
    "TPA": "TPA",
    "MSY": "MSY",
    "PIT": "PIT",
    "CLE": "CLE",
    "CVG": "CIN",
    "CMH": "CMH",
    "PDX": "PDX",
    "IND": "IND",
    "RDU": "RAL",
    "AUS": "AUS",
    "SAT": "SAT",
    "MEM": "MEM",
    "BCN": "BCN",  # Barcelona, Spain
    "VCE": "VCE",  # Venice, Italy
    "MUC": "MUC",  # Munich, Germany
    "NAP": "NAP",  # Naples, Italy
    "FLR": "FLR",  # Florence, Italy
    "NCE": "NCE",  # Nice, France
    "CPT": "CPT",  # Cape Town, South Africa
    "PRG": "PRG",  # Prague, Czech Republic
    "BUD": "BUD",  # Budapest, Hungary
    "KRK": "KRK",  # Krakow, Poland
    "VNO": "VNO",  # Vilnius, Lithuania
    "WAW": "WAW",  # Warsaw, Poland
    "MLA": "MLA",  # Malta
    "TPE": "TPE",  # Taipei, Taiwan
    "KIX": "OSA",  # Osaka, Japan
    "HNL": "HNL"   # Honolulu, Hawaii
}

    
    # Lookup the city code based on the airport code
    return airport_to_city_map.get(airport_code, "Unknown city code")


def get_city_by_code(code):
    # Reverse the dictionary: Keys will be airport codes, values will be city names
    reversed_city_codes = {v: k for k, v in city_codes.items()}
    
    # Look up the city using the code
    city = reversed_city_codes.get(code.upper())  # Ensure the code is in uppercase for uniformity
    
    if city:
        return city
    else:
        return "City not found for the given code."
    
import requests

def get_all_infos_about(city):
    language_code = 'en'
    base_url = f'https://{language_code}.wikipedia.org/api/rest_v1/page/summary/'
    
    # Construct the URL for the summary of the city
    url = base_url + city.replace(" ", "_")  # Replace spaces in the city name with underscores
    
    headers = {
        'User-Agent': 'YourAppName (your.email@example.com)'  # Adjust this to your own app details
    }

    response = requests.get(url, headers=headers)

    # Convert response to JSON
    data = response.json()

    # Check if the response contains the expected data
    if response.status_code == 200 and 'title' in data:
        full_info = {}
        title = data.get('title', 'No title available')
        description = data.get('description', 'No description available')
        extract = data.get('extract', 'No extract available')
        
        full_info['Title'] = title
        full_info['Description'] = description
        full_info['Information'] = extract
        
        return full_info
    else:
        return "No results found."

