from rich import print
import platform
import typer
import json
import os.path
import os
from pathlib import Path
import httpx
from datetime import datetime

# Weather class in in here because I can't figure out how to import it from meteo\Weather.py
class Weather:
    def __init__(self, city="", api_key="", units="metric"):
        self.city = city
        self.unit = units.lower()
        self.api_key = api_key
    
    def getLatLon(self, city):
        res = httpx.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city.title()}&limit=5&appid={self.api_key}").json()
        lat = res[0]["lat"]
        lon = res[0]["lon"]
        
        return (lat, lon)
    
    def getWeather(self, city):
        lat, lon = self.getLatLon(city)
        res = httpx.get(f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=hourly,minutely&units={self.unit}&appid={self.api_key}").json()
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
        
    def changeUnits(self, unit: str):
        self.unit = unit.lower()
        
    def changeApiKey(self, api_key: str):
        self.api_key = api_key


app = typer.Typer()


def createConfig() -> None:
    configDir = Path.home()
    if os.path.exists(f"{configDir}\\meteo"):
        with open(getConfigDir(), "w") as f:
            f.write('{\n"API_KEY": "",\n"CITY": "",\n"UNITS": ""\n}')
    else:
        os.mkdir(f"{configDir}\\meteo")
        createConfig()


def getConfigDir() -> Path:
    return Path.home() / "meteo" / "config.json"


def configExists() -> bool:
    return Path(getConfigDir()).is_file()


def changeCity(city: str) -> None:
    configDir = Path.home()
    with open(getConfigDir(), "r") as f:
        config = json.load(f)

    configFile = open(getConfigDir(), "w")
    configFile.write(
        '{\n"API_KEY": "' + config["API_KEY"] + '",\n"CITY": "' + city + '",\n"UNITS": "' + config["UNITS"] + '"\n}')
    configFile.close()


def changeApiKey(api_key: str) -> None:
    configDir = Path.home()
    with open(getConfigDir(), "r") as f:
        config = json.load(f)

    configFile = open(getConfigDir(), "w")
    configFile.write('{\n"API_KEY": "' + api_key +
                     '",\n"CITY": "' + config["CITY"] + '",\n"UNITS": "' + config["UNITS"] + '"\n}')
    configFile.close()


def changeUnits(units: str) -> None:
    configDir = Path.home()
    with open(getConfigDir(), "r") as f:
        config = json.load(f)

    configFile = open(getConfigDir(), "w")
    configFile.write('{\n"API_KEY": "' + config["API_KEY"] +
                     '",\n"CITY": "' + config["CITY"] + '",\n"UNITS": "' + units + '"\n}')
    configFile.close()


# the command for changing the config
@app.command()
def config(change=typer.Argument(None, help="The config you want to change(key, city, unit, all, current, reset).")):
    if change == None:
        print("You need to specify what you want to change.")
    else:
        configDir = Path.home()
        if configExists():
            if change == "key":
                newKey = input("Please enter the new API key: ")
                changeApiKey(newKey)
            elif change == "city":
                newCity = input("Please enter the new city: ")
                changeCity(newCity)
            elif change == "units":
                newUnit = input("Please enter the unit(metric, imperial): ").lower()
                changeUnits(newUnit)
            elif change == "all":
                newKey = input("Please enter the new API key: ")
                changeApiKey(newKey)
                newCity = input("Please enter the new city: ")
                changeCity(newCity)
                newUnit = input("Please enter the unit(metric, imperial): ").lower()
                changeUnits(newCity)
            elif change == "reset":
                createConfig()
            elif change == "current":
                configDir = Path.home()
                with open(getConfigDir(), "r") as f:
                    config = json.load(f)
                    print("API Key: " + config["API_KEY"])
                    print("City: " + config["CITY"])
                    print("Units: " + config["UNITS"])
            else:
                print("You need to specify what you want to change.")
        else:
            print("You need to create a config first with the init command.")      
          
# creates the config file if it doesn't exist
@app.command()
def init() -> None:
    configDir = Path.home()
    if not os.path.exists(f"{configDir}\\meteo"):
        os.mkdir(f"{configDir}\\meteo")
        createConfig()

    elif not configExists():
        createConfig()
    elif configExists():
        with open(getConfigDir(), "r") as f:
            config = f

            if config.read() == "":
                createConfig()
            else:
                print("Config already exists.")


# the main command for the meteo app
@app.command()
def weather(C: str = typer.Option(None, "--city", "-C", help="City that you want to get weather data for."),) -> None:
    # checks if city is None
    if configExists():
        config = json.load(open(getConfigDir()))

        if config["API_KEY"] != "":
            if C:
              weather = Weather(api_key=config["API_KEY"], units=config["UNITS"])
              print(weather.getFormatedWeather(C))
            
            else:
                weather = Weather(api_key=config["API_KEY"], city=config["CITY"], units=config["UNITS"])
                with open(getConfigDir(), "r") as f:
                    config = json.load(f)
                    print(weather.getFormatedWeather(config["CITY"]))
        else:
            print("You need to specify an API key in the config file first.")
    else:
        print("Config doesn't exist. Run the init command to create one.")


if __name__ == "__main__":
    app()
