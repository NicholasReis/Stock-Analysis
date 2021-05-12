import requests
import json
import os

class DataGrabber:
	#Creates a global dictionary to hold all the yearly data
	yearly_data = dict()
	minYear = 5000
	maxYear = 0
	def __init__(self, stock_symbol):
		#Assigns stock symbol to a non-existent global variable
		#I need to investigate this, but I suspect it's just a quirk of python
		self.stock_symbol = stock_symbol
		
		#Commented out since it's not needed during testing
		self.write_to_file()
		
		#Assigns a shortened segment from the file gnerated from the online resource
		shortened_segment = self.read_from_file()
		print("Files found!")
		#print(shortened_segment) #Temporary diagnostic info for parsing JSON element

		#Creates a smaller segment of JSON regarding just the cashflow
		cashflow_statement = self.process_segment(shortened_segment, '"cashflowStatementHistory"')
		#print(cashflow_statement)

		#Creates a smaller segment of JSON regarding just the income_statement	This stupid-ass ":{" changes the quartly vs annual
		income_statement = self.process_segment(shortened_segment, '"incomeStatementHistory":{')
		#print(income_statement)
		

		#Creates a smaller segment of JSON regarding just the balance_sheet
		balance_history = self.process_segment(shortened_segment, '"balanceSheetHistory"')
		#print(balance_history)

		#converts the JSON string into accessible data for yearly_data[]
		self.process_income_statement(income_statement)
		#
		#converts the JSON string into accessible data for yearly_data[]
		self.process_balance_sheet(balance_history)
		#converts the JSON string into accessible data for yearly_data[]
		self.process_cashflow(cashflow_statement)
		
		#self.delete_files()
		
	#Function to grab online resource
	def write_to_file(self):
		#Assigns the shortened version of the webpage
		shortened_segment = self.grabResource('https://finance.yahoo.com/quote/'+ self.stock_symbol +'/financials?p='+ self.stock_symbol)

		#Opens/Creates a file with the ticker symbol of the stock to store data
		#I am going to have to handle overwriting data or deleting the file later
		with open(self.stock_symbol+".txt", "w") as output_file:
			#Writes the shortened pieces to the file (Though this will later be formatted into a dictionary entry)
			output_file.write(shortened_segment)

	#Function to parse the <stockname> file
	def read_from_file(self):
		#Opens the file which in the future will have the formatted stock information
		with open(self.stock_symbol + ".txt") as input_file:
			#Reads the file and assigns it to a string
			text_from_file = input_file.read()
		#Returns the text from the file
		return text_from_file

	#Function to grab the webpage and isolate the relevant data
	def grabResource(self, webPage):
		#Assigns html as the page request
		html = requests.get(webPage)
		#Sets the beginning index of the relevant info
		begin = html.text.index('"QuoteSummaryStore"')
		#Sets the ending index of the relevant info
		end = html.text.index('"FinanceConfigStore"')
		#Isolates the relevant info
		shortened_segment = html.text[begin:end]
		#Returns relevant info
		return shortened_segment

	#Takes the chunk of relevant data and breaks it down further into the segment of relevant
	#data (ie. CashFlow data, Balance Sheet data, and Income Statement data)
	def process_segment(self, segment, label):
		#Beings at the respective data label
		begin = segment.index(label)
		#Finds the ']' and then from there the nearest '}}' which in this dataset denotes
		#the end of the JSON data designated to the respective label
		end = segment.index(']', begin)
		end = segment.index('}', end)
		#Returns the data of the respective label in a JSON format
		return segment[begin:end+1]

	#Function to process the information specific to the income statement
	def process_income_statement(self, statement):
		#Creates an array for storing the data associated with each year (Though currently quarter)
		income_data = []
		#Checks that there is another element (researchDevelopment is the first label in the data)
		while('researchDevelopment' in statement):
			#If there is it will take the index of the first quotation mark
			begin = statement.index('"researchDevelopment"')-1
			#It will then take the index of the end of the data
			end = statement.index('}}', begin)+2
			#And input that string of data into the array
			income_data.append(statement[begin:end])
			#Chops off the segment we processed so that instance of researchDevelopment wont come up again
			statement = statement[end:]

		#Takes each string of data and loads it into a JSON object
		for data in income_data:
			#Loads data as JSON
			data_as_json = json.loads(data)
			
			#Yes this is sloppy, but I desperately don't want to import OS-------------------
			#Assigns the largest year with recorded data
			if(int(data_as_json["endDate"]["fmt"][0:4]) > self.maxYear):
				self.maxYear = int(data_as_json["endDate"]["fmt"][0:4])

			#Assigns the smallest year with recorded data
			if(int(data_as_json["endDate"]["fmt"][0:4]) < self.minYear):
				self.minYear = int(data_as_json["endDate"]["fmt"][0:4])
			#Because if I do I will have to make adjustments for mac and windows-------------

			#Loads the data into a file
			with open(self.stock_symbol+str(data_as_json["endDate"]["fmt"][0:4])+".txt", "w") as output_file:
				output_file.write("research_development>"+str(data_as_json["researchDevelopment"])+'\n')
				output_file.write("pretax_income>"+str(data_as_json["incomeBeforeTax"])+'\n')
				output_file.write("minority_interest>"+str(data_as_json["minorityInterest"])+'\n')
				output_file.write("net_income>"+str(data_as_json["netIncome"])+'\n')
				output_file.write("sellingGeneralAdministrative>"+str(data_as_json["sellingGeneralAdministrative"])+'\n')
				output_file.write("grossProfit>"+str(data_as_json["grossProfit"])+'\n')
				output_file.write("earnings_before_income_taxes>"+str(data_as_json["ebit"])+'\n') #earnings I think
				output_file.write("operating_income>"+str(data_as_json["operatingIncome"])+'\n')
				output_file.write("otherOperatingExpenses>"+str(data_as_json["otherOperatingExpenses"])+'\n')
				output_file.write("interest_expense>"+str(data_as_json["interestExpense"])+'\n')
				output_file.write("extraordinary_items>"+str(data_as_json["extraordinaryItems"])+'\n')
				output_file.write("non_recurring>"+str(data_as_json["nonRecurring"])+'\n')				
				output_file.write("other_items>"+str(data_as_json["otherItems"])+'\n')
				output_file.write("income_tax_expense>"+str(data_as_json["incomeTaxExpense"])+'\n')
				output_file.write("total_revenue>"+str(data_as_json["totalRevenue"])+'\n')
				output_file.write("total_operating_expenses>"+str(data_as_json["totalOperatingExpenses"])+'\n')				
				output_file.write("cost_of_revenue>"+str(data_as_json["costOfRevenue"])+'\n')
				output_file.write("total_other_income_expense_net>"+str(data_as_json["totalOtherIncomeExpenseNet"])+'\n')
				output_file.write("discontinued_operations>"+str(data_as_json["discontinuedOperations"])+'\n')
				output_file.write("net_income_from_continuing_ops>"+str(data_as_json["netIncomeFromContinuingOps"])+'\n')				
				output_file.write("net_income_applicable_to_common_shares>"+str(data_as_json["netIncomeApplicableToCommonShares"])+'\n')
				
	#Function to process the information specific to the balance sheet
	def process_balance_sheet(self, statement):
		#Creates an array for storing the data associated with each year (Though currently quarter)
		income_data = []
		#Checks that there is another element (intangibleAssets is the first label in the data)
		while('intangibleAssets' in statement):
			#If there is it will take the index of the first quotation mark
			begin = statement.index('"intangibleAssets"')-1
			#It will then take the index of the end of the data
			end = statement.index('}}', begin)+2
			#And input that string of data into the array
			income_data.append(statement[begin:end])
			#Chops off the segment we processed so that instance of intangibleAssets wont come up again
			statement = statement[end:]

		#Takes each string of data and loads it into a JSON object
		for data in income_data:
			#Loads data as JSON
			data_as_json = json.loads(data)
			
			#Loads the data into a file
			with open(self.stock_symbol+str(data_as_json["endDate"]["fmt"][0:4])+".txt", "a") as output_file:
				output_file.write("intangible_assets>"+str(data_as_json["intangibleAssets"])+'\n')
				output_file.write("capital_surplus>"+str(data_as_json["capitalSurplus"])+'\n')
				output_file.write("total_liab>"+str(data_as_json["totalLiab"])+'\n')
				output_file.write("total_stockholder_equity>"+str(data_as_json["totalStockholderEquity"])+'\n')
				output_file.write("deferred_long_term_liabilities>"+str(data_as_json["deferredLongTermLiab"])+'\n')
				output_file.write("other_current_liabilities>"+str(data_as_json["otherCurrentLiab"])+'\n')
				output_file.write("total_assets>"+str(data_as_json["totalAssets"])+'\n')
				output_file.write("common_stock>"+str(data_as_json["commonStock"])+'\n')
				output_file.write("other_current_assets>"+str(data_as_json["otherCurrentAssets"])+'\n')
				output_file.write("retained_earnings>"+str(data_as_json["retainedEarnings"])+'\n')
				output_file.write("other_liabilities>"+str(data_as_json["otherLiab"])+'\n')
				output_file.write("good_will>"+str(data_as_json["goodWill"])+'\n')
				output_file.write("treasury_stock>"+str(data_as_json["treasuryStock"])+'\n')
				output_file.write("other_assets>"+str(data_as_json["otherAssets"])+'\n')
				output_file.write("cash>"+str(data_as_json["cash"])+'\n')
				output_file.write("total_current_liabilities>"+str(data_as_json["totalCurrentLiabilities"])+'\n')
				output_file.write("deferred_long_term_asset_charges>"+str(data_as_json["deferredLongTermAssetCharges"])+'\n')
				output_file.write("short_long_term_debt>"+str(data_as_json["shortLongTermDebt"])+'\n')
				output_file.write("other_stockholder_equity>"+str(data_as_json["otherStockholderEquity"])+'\n')
				output_file.write("property_plant_equipment>"+str(data_as_json["propertyPlantEquipment"])+'\n')
				output_file.write("total_current_assets>"+str(data_as_json["totalCurrentAssets"])+'\n')
				output_file.write("long_term_investments>"+str(data_as_json["longTermInvestments"])+'\n')
				output_file.write("net_tangible_assets>"+str(data_as_json["netTangibleAssets"])+'\n')
				output_file.write("net_receivables>"+str(data_as_json["netReceivables"])+'\n')
				output_file.write("long_term_debt>"+str(data_as_json["longTermDebt"])+'\n')
				output_file.write("inventory>"+str(data_as_json["inventory"])+'\n')
				output_file.write("accounts_payable>"+str(data_as_json["accountsPayable"])+'\n')

	#Function to process the information specific to the cashflow
	def process_cashflow(self, statement):
		#Creates an array for storing the data associated with each year (Though currently quarter)
		income_data = []
		#Checks that there is another element (investments is the first label in the data)
		while('investments' in statement):
			#If there is it will take the index of the first quotation mark
			begin = statement.index('"investments"')-1
			#It will then take the index of the end of the data
			end = statement.index('}}', begin)+2
			#And input that string of data into the array
			income_data.append(statement[begin:end])
			#Chops off the segment we processed so that instance of investments wont come up again
			statement = statement[end:]

		#Takes each string of data and loads it into a JSON object
		for data in income_data:
			#Loads data as JSON
			data_as_json = json.loads(data)
			
			#Loads the data into a file
			with open(self.stock_symbol+str(data_as_json["endDate"]["fmt"][0:4])+".txt", "a") as output_file:
				output_file.write("investments>"+str(data_as_json["investments"])+'\n')
				output_file.write("change_to_liabilities>"+str(data_as_json["changeToLiabilities"])+'\n')
				output_file.write("total_cashflows_from_investing_activities>"+str(data_as_json["totalCashflowsFromInvestingActivities"])+'\n')
				output_file.write("net_borrowings>"+str(data_as_json["netBorrowings"])+'\n')
				output_file.write("total_cash_from_financing_activities>"+str(data_as_json["totalCashFromFinancingActivities"])+'\n')
				output_file.write("change_to_operating_activities>"+str(data_as_json["changeToOperatingActivities"])+'\n')
				output_file.write("issuance_of_stock>"+str(data_as_json["issuanceOfStock"])+'\n')
				output_file.write("change_in_cash>"+str(data_as_json["changeInCash"])+'\n')
				output_file.write("repurchase_of_stock>"+str(data_as_json["repurchaseOfStock"])+'\n')
				output_file.write("effect_of_exchange_rate>"+str(data_as_json["effectOfExchangeRate"])+'\n')
				output_file.write("total_cash_from_operating_activities>"+str(data_as_json["totalCashFromOperatingActivities"])+'\n')
				output_file.write("depreciation>"+str(data_as_json["depreciation"])+'\n')
				output_file.write("other_cashflows_from_investing_activities>"+str(data_as_json["otherCashflowsFromInvestingActivities"])+'\n')
				output_file.write("dividends_paid>"+str(data_as_json["dividendsPaid"])+'\n')
				output_file.write("change_to_account_receivables>"+str(data_as_json["changeToAccountReceivables"])+'\n')
				output_file.write("other_cashflows_from_financing_activities>"+str(data_as_json["otherCashflowsFromFinancingActivities"])+'\n')
				output_file.write("change_to_net_income>"+str(data_as_json["changeToNetincome"])+'\n')
				output_file.write("capital_expenditures>"+str(data_as_json["capitalExpenditures"])+'\n')

	#Returns the recorded years of data
	def getYears(self):
		return range(self.minYear, self.maxYear)

#	def delete_files(self):
#		years = self.getYears()
#		print(years)
#		for year in years:
#			try:
#				print(self.stock_symbol+str(year)+".txt")
#				os.remove(self.stock_symbol+str(year)+".txt")
#			except OSError:
#				pass
