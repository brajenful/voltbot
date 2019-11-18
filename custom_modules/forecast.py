from forecastiopy import *
import geopy

class Weather(object):

	def __init__(self, address:str):
		self.darksky_api_key = 'dd1473466769051ef1c08eb24e7946fd'
		self.geopy_username = 'brajenful'

		self.address = address
		self.output = {}

		self.geocoder = geopy.geocoders.GeoNames(username = self.geopy_username)

		self.__geolocate()
		self.__get_forecast()

	def __get_forecast(self):
		self.forecast = ForecastIO.ForecastIO(self.darksky_api_key, latitude = self.coordinates[0], longitude = self.coordinates[1])

	def __geolocate(self):
		self.coordinates = self.geocoder.geocode(self.address)[1]

	def current(self):
		self.current = FIOCurrently.FIOCurrently(self.forecast)
		self.output['Time'] = self.current.time
		self.output['Summary'] = self.current.summary
		self.output['Precipitation'] = self.current.precipIntensity
		self.output['Temperature'] = self.current.temperature
		self.output['Humidity'] = self.current.humidity
		self.output['Wind'] = self.current.windSpeed

		return self.output

current = Weather('Kadafalva').current()
print(current)
