__version__ = '0.0.1'

from cuba_weather_insmet.insmet_webparser import CityWeather, TemperatureMap
from cuba_weather_municipality import CubaWeatherMunicipality
from .repositories import SourceRepository, WeatherRepository
from .insmet_webparser import CityWeather

class CubaWeatherInsMet:
    def __init__(self):
        self._cubaWeatherMunicipality = CubaWeatherMunicipality()
        self._sourceRepository = SourceRepository()
        self._weatherRepository = WeatherRepository()

    def get_extended_weather(self, input: str):
        '''
            Method that given a municipality searches the cuban municipalities to find the best match and returns the weather information.
        '''
        municipality = self._cubaWeatherMunicipality.get(input, suggestion=True)    
        source = self._sourceRepository.getSource(municipality)
        weather = self._weatherRepository.get_extended_weather(source)
        weather.cityName = municipality.name

        return weather

    # added by @JalexCode
    def get_weather_values_map(self) -> dict:
        """Returns a dict with all provinces and municipalities weather info
            Returns
            -------
            dict
                {province_or_municipality:CityWeather(), ...}
            """
        return self._weatherRepository.get_weather_values_map()

    # added by @JalexCode
    def get_weather(self, input) -> CityWeather:
        """Returns a CityWeather object with a city weather info
            Returns
            -------
            CityWeather
            """
        weather = self._weatherRepository.get_weather_values_map()
        return weather[input]

    # added by @JalexCode
    def get_temperatures_map(self) -> TemperatureMap:
        """ Returns a TemperatureMap object
        Call get_temperatures_map() method in TemperatureMap object to get a dict with all provinces min and max temperatures
        Returns
        -------
        TemperatureMap
            {"province_name":(max temperature, min temperature), ...}
        """
        map = self._weatherRepository.get_temperatures_map()
        return map

    # added by @JalexCode
    def get_temperature(self, city) -> tuple:
        """Returns a tuple with max and min temperatures from a given city
            Parameters
            ----------
            city : str
                Name of a city
            Returns
            -------
            tuple
                (max temperature, min temperature)
            """
        map:TemperatureMap = self.get_temperatures_map()
        return map.get_temperature(city)
    
    # added by @JalexCode
    def get_weather_state_map(self) -> dict:
        """Returns a dict with all zones prognos
        Returns
        -------
        dict
            {"zone":WeatherImage(), ...}
        """
        map = self._weatherRepository.get_weather_state_map()
        return map