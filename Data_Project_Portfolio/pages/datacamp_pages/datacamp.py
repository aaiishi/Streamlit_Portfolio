import streamlit as st
from datetime import datetime
from pages.datacamp_pages.functions import *  # Import the functions from your previous code

# ---- WELCOME PART ----
#st.markdown("<h1 style='text-align: center;'>FastMyTrip</h1>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1.5, 1])  # Adjust column ratios to center the image
with col2:
    st.image("assets/FastMyTrip.png", width=250)

# ---- USER PART ----
st.write("**Select the variables for your trip :**")
st.write("")

# Inputs
col1, col2 = st.columns(2)
with col1:
    city_input = st.text_input('**🏙️ Your city :**')
    current_city = get_closest_city(city_input)  # Get the closest city based on user input
    origin = get_country_code(current_city)  # Get the airport code for the current city
with col2:
    weather_preference = st.selectbox('**🌦️ Weather :**', ['', 'Clear Conditions', 'Cloudy Conditions', 'Fog and Haze', 'Precipitation', 'Snow', 'Sleet'])

col3, col4 = st.columns(2)
with col3:
    temperature = st.slider('**🌡️ Temperature in °C :**', -30, 30, value=0)
with col4:
    travel_date = st.date_input('**🗓️ Departure date :**', value=datetime.today())

st.write("")

# Expander for reviewing selections and confirming the trip
with st.expander("Review Your Selections"):
    st.write("")
    
    # Create four columns to separate each piece of information
    col1, col2, col3, col4 = st.columns(4)
    
    # Left-most column for City
    with col1:
        st.write(f"🏙️ {current_city}")
    
    # Second column for Weather
    with col2:
        st.write(f"🌦️ {weather_preference}")
    
    # Third column for Temperature
    with col3:
        st.write(f"🗓️ {travel_date}")
    
    # Right-most column for Departure Date
    with col4:
        st.write(f"🌡️ {temperature}°C")

    st.write("")

    # ---- Button to confirm and process the trip ----
    if st.button("Find my trip"):
        st.success("Your trip is processing...")

        # ---- VALIDATION ----
        validation_errors = False

        # Validate that the city is not empty
        if not city_input:
            st.error("Please enter your city.")
            validation_errors = True

        # Validate weather selection (it should not be the placeholder '')
        if weather_preference == '':
            st.error("Please select a valid weather condition.")
            validation_errors = True

        # Validate the travel date (it should not be before today)
        if travel_date < datetime.today().date():
            st.error("The departure date cannot be in the past.")
            validation_errors = True

        # If there are no validation errors, process the trip
        if not validation_errors:
            # ---- PROCESS TRIP LOGIC ----
            travel_date_str = travel_date.strftime('%Y-%m-%d')
            found_flights = []  # Store results for display
            matching_cities = False  # Variable to know if matching cities were found
            city_list = list(city_codes.items())
            random.shuffle(city_list)

            # Loop to check the weather of the cities
            for city, code in city_codes.items():
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_WEATHER}&units=metric'
                temperature_data, weather_description = get_weather_data(url)
                print(f'In {city}, the temp is {temperature_data}, and the condition are {weather_description}')

                # Check temperature and weather conditions
                if temperature - 5 <= temperature_data <= temperature + 5:
                    if matches_weather_family(weather_description, weather_preference) and city != current_city:
                        city_name = city.split(',')[0].strip()
                        st.success(f"🎉 {city_name} is a match!")
                        matching_cities = True
                        st.markdown(f"### ✈️ Trip to {city_name}")
                        st.write(f"**Temperature** : {temperature_data}°C")
                        st.write(f"**Weather** : {weather_description}")

                        # Show information about the city
                        Information = get_all_infos_about(city_name)
                        st.write(f"🗺️ **Description** : {Information['Description']}")
                        st.write(f"ℹ️ **Information** : {Information['Information']}")

                        # ---- Show Flights ----
                        flights_info = search_flights(origin, code, travel_date_str, adults=1)
                        if flights_info:
                            st.markdown(f"## ✈️ Flights to {city_name}")

                            for i, flight in enumerate(flights_info, 1):
                                price = flight['price']
                                currency = flight['currency']

                                # Create a box for each flight
                                st.markdown(f"""
                                <div style="border: 1px solid #4CAF50; padding: 10px; margin-bottom: 10px; border-radius: 10px;">
                                    <h4 style="color: #4CAF50;">Flight {i}: {price} {currency}</h4>
                                """, unsafe_allow_html=True)

                                # Show each flight segment
                                for segment_num, segment in enumerate(flight['segments'], 1):
                                    departure_time = segment['departure_time']
                                    datetime_obj = datetime.strptime(departure_time, "%Y-%m-%dT%H:%M:%S")
                                    readable_format = datetime_obj.strftime("%B %d, %Y at %I:%M %p")
                                    departure_location = segment['departure_location']
                                    arrival_location = segment['arrival_location']
                                    airline = segment['airline']
                                    flight_number = segment['flight_number']
                                    arrival_city = get_city_by_code(arrival_location)
                                    departure_city = get_city_by_code(departure_location)

                                    st.markdown(f"""
                                    <div style="margin-left: 20px; padding: 5px;">
                                        <strong>Segment {segment_num}</strong> <br>
                                        🛫 <strong>Departure</strong>: {departure_location} | {departure_city} | {readable_format} <br>
                                        🛬 <strong>Arrival</strong>: {arrival_location} | {arrival_city}<br>
                                        ✈️ <strong>Airline</strong>: {airline} (Flight {flight_number}) <br>
                                        <hr>
                                    </div>
                                    """, unsafe_allow_html=True)

                                st.markdown("</div>", unsafe_allow_html=True)

                        else:
                            st.warning(f"No flights found to {city_name}.")

                        # ---- Show Hotels ----
                        city_code = from_airport_to_city(code)
                        hotels_info = search_hotels(city_code, 10, ratings=5)
                        if hotels_info:
                            st.markdown(f"## 🏨 Hotels in {city_name}")

                            for i, hotel in enumerate(hotels_info, 1):
                                # Show each hotel as a card
                                st.markdown(f"""
                                <div style="border: 1px solid #4CAF50; padding: 10px; margin-bottom: 10px; border-radius: 10px;">
                                    <h4>🏨 Hotel {i}: {hotel}</h4>
                                </div>
                                """, unsafe_allow_html=True)

                        else:
                            st.warning(f"No hotels found in {city_name}.")
                        
                        break
            if not matching_cities:
                st.warning("No matching cities found for your preferences.")