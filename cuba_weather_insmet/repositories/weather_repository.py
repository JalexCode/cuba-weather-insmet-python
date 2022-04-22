from cuba_weather_insmet.insmet_webparser import get_weather_values_map, get_temperatures_map

from ..insmet_webparser import get_forecast, get_weather_values_map, get_weather_state_map

class WeatherRepository:
  '''
    Class to provide the functionality of obtaining weather data
  '''
  def __init__(self):
    pass

  def get_extended_weather(self, source):
    weatherdata = get_forecast()
    return WeatherModel(
      date = weatherdata.date,
      cityName=source.name,
      data= weatherdata.data[source.name]
    )

  # added by @JalexCode
  def get_weather_values_map(self):
    return get_weather_values_map()

  # added by @JalexCode
  def get_temperatures_map(self):
    return get_temperatures_map()

  # added by @JalexCode
  def get_weather_state_map(self):
    return get_weather_state_map()

class WeatherModel():
  def __init__(self, date, cityName, data):
    self.date = date
    self.cityName = cityName
    self.days = data

  def __str__(self):
    result: str = ''
    result += 'City Name: {}\n'.format(self.cityName)
    result += 'Datetime Update: {}\n'.format(self.date)

    for i in range(0, len(self.days)):
      result += '{}\n'.format(self.days[i])

    #result += 'Today\'s Weather Forecast: ${}\n'.format(self.weatherForecast)
    #result += 'Drought Status: {}'.format(self.droughtStatus)
    
    return result