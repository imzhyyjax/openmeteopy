# Import necessary classes from the openmeteopy library
from openmeteopy import OpenMeteo
from openmeteopy.options import ForecastOptions
from openmeteopy.daily import DailyForecast
import json

# --- Configuration ---
# Set the latitude and longitude for the location you want the weather for.
# Here, we use Shanghai's coordinates as an example.
LATITUDE = 31.2304
LONGITUDE = 121.4737
# Set the number of days for the forecast. 3 days means today, tomorrow, and the day after.
FORECAST_DAYS = 3

# --- Weather Code Mapping ---
# This dictionary maps WMO weather codes to human-readable descriptions.
# You can pass this to an LLM to help it understand the weather conditions.
WMO_WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

# --- Main script ---
def get_daily_weather_forecast():
    """
    Fetches and returns the daily weather forecast for a specific location.
    """
    # 1. Set up the options for the weather API call.
    options = ForecastOptions(
        latitude=LATITUDE,
        longitude=LONGITUDE,
        forecast_days=FORECAST_DAYS
    )

    # 2. Specify which daily weather variables you want to retrieve.
    daily = DailyForecast()
    daily = daily.temperature_2m_max()
    daily = daily.temperature_2m_min()
    daily = daily.weathercode()
    daily = daily.precipitation_sum()
    daily = daily.windspeed_10m_max()

    # 3. Create the OpenMeteo client and fetch the data.
    client = OpenMeteo(options, daily=daily)
    forecast_data = client.get_dict()

    return forecast_data

def translate_daily_weather_codes(forecast_data):
    """
    Translates the weather codes in the daily forecast data to their descriptions.
    """
    if 'daily' in forecast_data and 'weathercode' in forecast_data['daily']:
        weather_descriptions = [WMO_WEATHER_CODES.get(code, "Unknown code") for code in forecast_data['daily']['weathercode']]
        forecast_data['daily']['weather_description'] = weather_descriptions
    return forecast_data

def trim_forecast_to_days(forecast_data, days):
    """
    Trims the forecast data to the specified number of days as a workaround.
    """
    if 'daily' in forecast_data:
        for key in forecast_data['daily']:
            forecast_data['daily'][key] = forecast_data['daily'][key][:days]
    return forecast_data

if __name__ == "__main__":
    # Fetch the raw daily weather data
    weather_data = get_daily_weather_forecast()

    # Add the human-readable weather descriptions
    weather_data_with_descriptions = translate_daily_weather_codes(weather_data)

    # Trim the forecast to the desired number of days
    trimmed_weather_data = trim_forecast_to_days(weather_data_with_descriptions, FORECAST_DAYS)

    # Print the final JSON output
    print("--- Daily Weather Forecast Data with Descriptions (JSON format) ---")
    print(json.dumps(trimmed_weather_data, indent=4))
    print("-----------------------------------------------------------------")
    print(f"Successfully fetched and trimmed {FORECAST_DAYS}-day daily weather forecast for Shanghai.")
    print("This concise daily data is ideal for LLM processing.")
