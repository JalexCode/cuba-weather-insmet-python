from cuba_weather_insmet import CubaWeatherInsMet


api = CubaWeatherInsMet()

# extended weather
print("Pronóstico extendido")
weather = api.get_extended_weather('Santiago')
print(weather)
print("==================================================")

# all temperature values
print("Mapa de temperaturas")
tmp_general = api.get_temperatures_map()
print(tmp_general)
tmp_cmg = api.get_temperature("Camagüey")
print(tmp_cmg)
print("==================================================")

# get national weather
print("Clima en todo el país")
national_weather = api.get_weather_values_map()
for i in national_weather.keys():
    print(i)
    print(national_weather[i])
print("==================================================")

# get weather state
print("Estado del clima en el territorio nacional")
state = api.get_weather_state_map()
for i in state.keys():
    print(i)
    for j in state[i]:
        print(j)
        print(state[i][j])
