import os 
import httpx
from dotenv import load_dotenv
from datetime import datetime
from pprint import pprint


class Weather:
    def __init__(self, city=""):
        load_dotenv("../.env")
        self.city = city
        self.api_key = os.environ["API_KEY"]
    
    def getLatLon(self, city):
        res = httpx.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city.title()}&limit=5&appid={self.api_key}").json()
        lat = res[0]["lat"]
        lon = res[0]["lon"]
        
        return (lat, lon)
    
    def getWeather(self, city):
        lat, lon = self.getLatLon(city)
        res = httpx.get(f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=hourly,minutely&units=metric&appid={self.api_key}").json()
        return res
    
    def getFormatedWeather(self, city):
        res = self.getWeather(city)
        
        return {
            "temp": res["current"]["temp"],
            "feels_like": res["current"]["feels_like"],
            "wind_speed": res["current"]["wind_speed"],
            "wind_deg": res["current"]["wind_deg"],
            "description": res["current"]["weather"][0]["description"],
            "prcpChance": res["daily"][0]["pop"],
            "humidity": res["current"]["humidity"],
            "uvIndex": res["current"]["uvi"],
            "sunrise": res["current"]["sunrise"],
            "sunset": res["current"]["sunset"],
            "timezone": res["timezone"],
            "timezone_offset": res["timezone_offset"],
        }
        
    def changeCity(self, city: str):
        self.city = city
        

if __name__ == "__main__":
    weather = Weather("London")
    
    data = weather.getFormatedWeather("London")
    
    print(f"Sunrise is at {datetime.fromtimestamp(data['sunrise'])}, Sunset is at {datetime.fromtimestamp(data['sunset'])}")
    
    
    {datetime.fromtimestamp(data['sunrise'] + data["timezone_offset"])}