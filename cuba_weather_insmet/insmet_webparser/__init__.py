# Keep It Simple
from urllib.request import urlopen
import requests

LOCATIONS = [
    ('Pinar del Río', 1),
    ('La Habana', 7),
    ('Varadero', 13),
    ('Cienfuegos', 19),
    ('Cayo Coco', 25),
    ('Camagüey', 31),
    ('Holguín', 37),
    ('Santiago de Cuba', 43)
]

# insmet api url
GENESIS = 'http://www.insmet.cu/asp/genesis.asp?'

# insmet icons url
#ICONS_PATH = "http://www.insmet.cu/imagenes/iconos/"

# Rosa Nautica
RN = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSO", "SO", "OSO", "O", "ONO", "NO", "NNO", "N"]

# actually useless
# municipalities_prefix = ["pr", "ch", "ar", "my", "ij", "mz", "vc", "cf", "sp", "ca", "cm", "lt", "hg", "gm", "sc",
#                          "gt"]

# Cuba provinces
MUNICIPALITIES = ["Pinar del Río", "Ciudad de La Habana", "Artemisa", "Mayabeque", "Isla de la Juventud",
                  "Matanzas", "Villa Clara", "Cienfuegos", "Sancti Spíritus", "Ciego de Ávila", "Camagüey",
                  "Las Tunas", "Holguín", "Granma", "Santiago de Cuba", "Guantánamo"]

# Cuba zones
ZONAS= ["occ", "cen", "orn", "ors"]

# classes

class WeatherJSONModel():
    def __init__(self, date, data):
        self.date = date
        self.data = data

    def __str__(self):
        result = ''

        result += 'Date: {}\n'.format(self.date)

        for l in LOCATIONS:
            result += '{}:\n'.format(l[0])

            for day in self.data[l[0]]:
                result += str(day)

            result += '\n'

        return result


class WeatherDayModel():
    def __init__(self, day, data: str):
        self.day = day

        temps = data[0:5]

        self.tmax, self.tmin = temps.split(' ')

        self.description = data[6:]

    def __str__(self):
        return '''
            Day: {}, 
            Maximum Temperature: {}°C, 
            Minimum Temperature: {}°C, 
            Description: {}
        '''.format(self.day, self.tmax, self.tmin, self.description)


# added by @JalexCode
class TemperatureMap:
    ''' Class to storage all provinces temperatures map '''
    def __init__(self, temperatures):
        self.temperatures: dict = temperatures

    def get_temperatures_map(self) -> dict:
        return self.temperatures

    def get_temperature(self, city) -> tuple:
        try:
            return self.temperatures[city]
        except KeyError:
            raise Exception(f"[error] No existe la ciudad {city}")

    def __str__(self) -> str:
        text = ''
        for i in range(len(MUNICIPALITIES)):
            text += MUNICIPALITIES[i] + "\n"
            text += f"Máximas: {self.temperatures[MUNICIPALITIES[i]][0]}\n"
            text += f"Mínimas: {self.temperatures[MUNICIPALITIES[i]][1]}\n\n"
        return text

# added by @JalexCode
class CityWeather:
    ''' Class to storage INSMET weather info '''
    def __init__(self, city, tmax, tmin, tactual, humidity, wind, rain_3_hours, rain_24_hours):
        self.city = city
        self.tmax = tmax
        self.tmin = tmin
        self.tactual = tactual
        self.humidity = humidity
        self.wind = wind
        self.rain_3_hours = rain_3_hours
        self.rain_24_hours = rain_24_hours

    def __str__(self) -> str:
        return f"""Ciudad: {self.city}
Temperatura máxima: {self.tmax} ºC
Temperatura mínima: {self.tmin} ºC
Temperatura actual: {self.tactual} ºC
Humedad: {self.humidity} %
Viento: {self.wind}
Lluvias en 3 horas: {self.rain_3_hours} mm
Lluvias en 24 horas: {self.rain_24_hours} mm
"""


# added by @JalexCode
class Wind:
    ''' Class to storage wind info '''
    def __init__(self, velocity, direction_angle, direction):
        self.velocity = velocity
        self.direction_angle = direction_angle
        self.direction = direction

    def __str__(self) -> str:
        text = f"{self.velocity} Km/h ({self.direction_angle}º) {self.direction}"
        if 'NE' in self.direction:
            text += " ↗"
        elif 'SE' in self.direction:
            text += " ↗"
        elif 'NO' in self.direction:
            text += " ↖"
        elif 'SO' in self.direction:
            text += " ↙"
        elif 'N' == self.direction:
            text += " ↑"
        elif 'S' == self.direction:
            text += " ↓"
        elif 'E' == self.direction:
            text += " →"
        elif 'O' == self.direction:
            text += " ←"
        return text

# added by @JalexCode
class WeatherMap:
    ''' Class to storage Cuba's zones weather state '''
    def __init__(self, image, state):
        self.image = image
        self.state = state

    def __str__(self) -> str:
        return f"Estado: {self.state}\nImagen: {self.image}\n"

# methods
def get_forecast():
    url = GENESIS + 'TB0=PLANTILLAS&TB1=PT5'

    res = urlopen(url)

    content = str(res.read())

    fecha = content[content.find('fecha5'):content.find(';  //fecha del pronostico para 5 dias')]
    fecha = fecha.split('=')[1].replace('"', '')

    content = content[content.find('pdia'):content.find('ndia')]
    content = content[content.find('(') + 1:content.find(')')]
    content = content.replace("\\'", '')

    adata = content.split(',')

    data = dict()

    for l in LOCATIONS:
        data[l[0]] = []

        d = 1

        for i in range(l[1], l[1] + 5):
            data[l[0]].append(WeatherDayModel(d, adata[i]))
            d += 1

    return WeatherJSONModel(fecha, data)


# added by @JalexCode
def get_temperatures_map() -> TemperatureMap:
    """Returns a dict with all provinces max and min temperatures
    Returns
    -------
    TemperatureMap
        {"province_name":(max temperature, min temperature), ...}
    """
    url = GENESIS + 'TB0=PLANTILLAS&TB1=PTM&TB2=/Pronostico/pth.txt'
    # temperatures dict
    temperatures = {}
    # getting data
    with requests.get(url) as res:
        if res.status_code == 200:
            # getting temps array
            content = res.text
            raw_temps = content[content.find("var tempx=new Array("):content.find(";\nvar estax=new Array")]
            raw_temps = raw_temps.replace("var tempx=new Array(", "")
            raw_temps = raw_temps.replace(")", "")
            raw_temps = raw_temps.replace("'", "")
            # mapping tempertaures string
            for i, pairs in enumerate(raw_temps.split(",")):
                temperatures[MUNICIPALITIES[i]] = tuple(map(lambda i: int(i), pairs.split()))
    return TemperatureMap(temperatures)

# added by @JalexCode
def get_weather_values_map() -> dict:
    """Returns a dict with all provinces and municipalities weather info
    Returns
    -------
    tuple
        {province_or_municipality:CityWeather(), ...}
    """
    url = GENESIS + 'TB0=PLANTILLAS&TB1=ESTACIONES&TB2=CUBA2&TB3=CUBA&TB4=/pronostico/est.csv&TB5=16'
    cities_weather = {}
    with requests.get(url) as res:
        if res.status_code == 200:
            content = res.text
            # getting values array
            raw = content[content.find("var valor= new Array("):content.find(");					   //?4")]
            raw = raw.replace("var valor= new Array(", "")
            raw = raw.replace(");					   //?4", "")
            raw = raw.replace("'", "")
            # mapping raw values
            results = raw.split(",")
            for values in results:
                j = 0
                city_name = ""
                weather = [0, 0, 0, 0, None, 0, 0]
                wind = [0, 0, ""]
                # test = ['Trinidad', '32.4', '23.0', '23.4', '92', '3.6', '90', '0.0', '2.3', '/', '78337']
                for i in values.split():
                    try:
                        if j == len(weather) + 1:
                            break
                        # if current value is a "null" string, just ignore it
                        if i == "/" or i == "NaN":
                            weather[j] = 0
                            j += 1
                            continue
                        # try to transform current string in float number
                        v = float(i)
                        # if current value is wind force
                        if j == 4:
                            wind[0] = v
                        # if current value is wind direction
                        elif j == 5:
                            wind[1] = v
                            # determine wind direction in Rosa Nautica
                            wind[2] = RN[int(v // 22.5)]
                        # if current value is rain info
                        elif j > 5:
                            weather[j - 1] = v
                        else:
                            weather[j] = v
                        j += 1
                    except:
                        i = i.strip()
                        # if current value is a not "null" string
                        # considere it as the city's name
                        if "/" not in i or i != "NaN":
                            city_name += i + " "
                        continue
                # removing symbols
                city_name = city_name.replace("/", "")
                # removing spaces
                city_name = city_name.strip()
                # init Wind class
                weather[4] = Wind(*wind)
                # adding CityWeather to the dict
                cities_weather[city_name] = CityWeather(city_name, *weather)
        else:
            raise Exception("[error] Fallo durante la conexion a https://insmet.cu")
    return cities_weather

# added by @JalexCode
def get_weather_state_map():
    """Returns a dict with all zones weather state
        Returns
        -------
        dict
            {"zone":WeatherMap(), ...}
        """
    insmet_url = GENESIS + 'TB0=PLANTILLAS&TB1=PTM&TB2=/Pronostico/pth.txt'
    pt_js_url = "http://www.insmet.cu/JLib/pt.js"
    # estax array [from genesis.asp]
    estax = []
    # ic array [from pt.js]
    ic = []
    # est array [from pt.js]
    est = []
    # getting data
    with requests.get(insmet_url) as res:
        if res.status_code == 200:
            # getting estax array
            content = res.text
            raw_estax = content[content.find("var estax=new Array("):content.find(";\nvar pronName")]
            raw_estax = raw_estax.replace("var estax=new Array(", "")
            raw_estax = raw_estax.replace(")", "")
            raw_estax = raw_estax.replace("'", "")
            # filling array
            for i in raw_estax.split(','):
                estax.append(i.strip())
            #print(estax)
    with requests.get(pt_js_url) as res:
        if res.status_code == 200:
            # getting est array
            content = res.text
            raw_est = content[content.find("est= new Array("):content.find(");\r\n\t\t\t \r\nic= new Array(")]
            raw_est = raw_est.replace("est= new Array(", "")
            raw_est = raw_est.replace(")", "")
            raw_est = raw_est.replace('"', "")
            # filling array
            for i in raw_est.split(','):
                est.append(i.strip())
            #print(est)
            # getting ic array
            raw_ic = content[content.find("ic= new Array("):content.find(");\t\t\t \r\n\r\nimgP=new Array(")]
            raw_ic = raw_ic.replace("ic= new Array(", "")
            raw_ic = raw_ic.replace(")", "")
            raw_ic = raw_ic.replace('"', "")
            # filling array
            for i in raw_ic.split(','):
                item = i.strip()
                if item not in ic:
                    ic.append(item)
            #print(ic)
    #
    weather_state = {"morning":{}, "night":{}}
    # estado() is a method written in JavaScript and its located in 'pt.js' file. This is my Python version
    def estado(pttn=True):
        # pttn => Pronostico del Tiempo para la Tarde-Noche
        result = {}
        # if arrays are full
        if estax and ic and est:
            weather_state=""
            for i in range(len(ZONAS)):
                zone=ZONAS[i]
                weather_state= estax[i*2+(1 if pttn else 0)]
                for j in range(len(est)):
                    if est[j] in weather_state:
                        result[zone] = WeatherMap(ic[j - 1], weather_state.capitalize())
                        break
                    if j == len(est)-1:
                        # following pt.js's logic
                        result[zone] = WeatherMap(ic[-1], "")
                        # a possible solution as last resource (it's not in pt.js file)
                        # for k in range(len(ic)):
                        #     icon = ic[k]
                        #     if weather_state in icon:
                        #         result[zone] = WeatherMap(ic[k], weather_state.capitalize())
                        #         break
                        #     if k == len(ic) - 1:
                        #         result[zone] = WeatherMap(ic[-1], "")
        return result
    #
    weather_state["morning"] = estado(False)
    weather_state["night"] = estado(True)
    #
    return weather_state

