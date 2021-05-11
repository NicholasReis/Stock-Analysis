

class Stock:
	yearlyData = dict()
	
	stock_symbol = ""
	def __init__(self, stock_symbol):
		self.stock_symbol = stock_symbol
		#self.loadFromFile()
	
	def loadFromFile(self):
		lines =[]
		with open('temporaryData') as tempData:
			lines =tempData.read().splitlines()
		#print(lines)
		year = 0
		for line in lines:
			#print("Newline")
			if(line != ""):
				values = str(line).split(":")
				#print(values)
				if(values[0] == "year"):
					year = values[1]
					self.yearlyData[year] = dict()
					#print(yearlyData)
				else:
					#print(values)
					self.yearlyData[year][values[0]] = values[1]

		print(self.yearlyData["2020"]["net_income"])

	def getYears(self):
		trackedYears = []
		currentYear = 2021
		years = len(self.yearlyData)
		while(years > 0):
			trackedYears.append(currentYear-(years))
			years -=1
		return trackedYears

	def getAnnualRevenue(self, year):
		return self.yearlyData[str(year)]["annual_revenue"]
		#I need to break these all down into each year
		#So with some fandangling I can use year as an
		#Identifier of sorts and the labels below as the
		#Key I want returned

		#pe
		#annual_revenue
		#profit_margin #(Net income / Total Revenue)
		#shares_issued
		#current_assets
		#current_liabilities
		#cash_flow
		#capital_expenditures
		#price #price to free cash flow < 15%
