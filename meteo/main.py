from genericpath import exists
from rich import print
import platform
import typer
import json
import os.path
import os
from pathlib import Path
from Weather import Weather

app = typer.Typer()
weather = Weather()


# the main command for the meteo app
def main(
    C: str = typer.Option(None, "--city", "-C",
                          help="City that you want to get weather data for."),
    A: str = typer.Option(None, "--api-key", "-A",
                          help="Changes the API key for the weather API."),
    B: str = typer.Option(None, "--change-city", "-B",
                          help="Change the city in the config file."),
) -> None:
    # checks if city is None
    if C:
        print(weather.getFormatedWeather(C))
    # planned to check if a config file exists and if not than it will output this
    elif A or B:
        configDir = Path.home()
      
        if Path(f"{configDir}\\meteo\\config.json").is_file():
            with open(f"{configDir}\\meteo\\config.json", "r+") as f:
                  configFile = f
                  configJson = json.load(configFile)
            
            configFile = open(f"{configDir}\\meteo\\config.json", "w")

            if A:
                # changes the API key in the config file
                city = configJson["CITY"]
                configFile.write('{\n"API_KEY": "' + A + '",\n"CITY": "' + city + '"\n}')
                
            elif B:
                # changes the city in the config file
                api_key = configJson["API_KEY"]
                configFile.write('{\n"API_KEY": "' + api_key + '",\n"CITY": "' + B + '"\n}')
                 
            configFile.close()
                
            
        # creates the config file if it doesn't exist  
        else:
            # checks if the meteo directory exists
            if not os.path.exists(f"{configDir}\\meteo"):
                os.mkdir(f"{configDir}\\meteo")

            # creates the config file with specified API key and/or city
            with open(f"{configDir}\\meteo\\config.json", "w") as f:
                if A:
                    f.write('{\n"API_KEY": "' + A + '",\n"CITY": ""\n}')
                elif B:
                    f.write('{\n"API_KEY": "",\n"CITY": "' + B + '"\n}')


if __name__ == "__main__":
    typer.run(main)
