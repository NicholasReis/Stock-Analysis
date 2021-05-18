from DataGrabber import *

class Stock:
	#Creates a global dictionary
	yearlyData = dict()
	years = []
	#Creates a global stock symbol variable
	stock_symbol = ""
	def __init__(self, stock_symbol):
		#Assigns the stock symbol to the variable
		self.stock_symbol = stock_symbol
		#self.loadFromFile(years)
		dg = DataGrabber(stock_symbol)
		self.years = dg.get_years()
		self.yearlyData = dg.get_data()
		print(self.yearlyData["2018"])
	
	#Using the keys given by getYears they can be sent here to get the Annual Revenue for that year
	#This will likey become getData and accept a label as another argument, I'm not sure why I did it this way
	#Though I suspect it's because of the way the data was separated by DataGrabber, but if I output it in a nice
	#Way that shouldn't end up mattering too much.
	def getData(self, year, label):
		#Returns the annual revenue from the associated year
		return self.yearlyData[str(year)][label]

	def get_years(self):
		return self.years
