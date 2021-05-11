import requests
import json

#Flag for deletion------------------------
import time
import array
#-----------------------------------------

class DataGrabber:

	#Creates a global dictionary that stores all the yearly information of the stock
	yearly_data = dict()

	#Constructor requires the stock symbol to search
	def __init__(self, stock_symbol):
		
		#Assigns stock symbol to a global variable that no longer exists, but this still works.
		#Will investigate, but it is probably just a quirk of python
		self.stock_symbol = stock_symbol
		
		#Calls write to file
		#self.write_to_file()
		
		#I probably dont actually need to shorten this segment
		#The idea is that if there is a significantly (10%-30%) it will be able to run a modicum faster and also organizes the data a bit better
		shortened_segment = self.read_from_file()
		#This print is just here to validate that the resource was loaded properly
		print("Income Statement found!")

		#print(shortened_segment) #Here to read data manually. Will delete when done.

		
		cashflow_statement = self.process_segment(shortened_segment, '"cashflowStatementHistory"')
		#print(cashflow_statement) #Here to read data manually. Will delete when done.

		income_statement = self.process_segment(shortened_segment, '"incomeStatementHistory"')
		print(income_statement) #Here to read data manually. Will delete when done.
		self.process_income_statement(income_statement)
		balance_history = self.process_segment(shortened_segment, '"balanceSheetHistory"')
		#print(balance_history)

	#write_to_file (should take the stock symbol, but doesn't need it for some reason) and 
	def write_to_file(self):
		shortened_segment = self.grabResource('https://finance.yahoo.com/quote/'+ self.stock_symbol +'/financials?p='+ self.stock_symbol)
		#I am going to have to handle overwriting data or deleting the file later		
		with open(self.stock_symbol+".txt", "w") as output_file:
			output_file.write(shortened_segment)

	def read_from_file(self):
		with open(self.stock_symbol + ".txt") as input_file:
			text_from_file = input_file.read()
		return text_from_file

	def grabResource(self, webPage):
		html = requests.get(webPage)
		begin = html.text.index('"QuoteSummaryStore"')
		end = html.text.index('"FinanceConfigStore"')
		shortened_segment = html.text[begin:end]
		return shortened_segment

	def process_segment(self, segment, label):
		begin = segment.index(label)
		end = segment.index(']', begin)
		end = segment.index('}', end)
		return segment[begin:end]

	def process_income_statement(self, statement):
		income_data = []
		while('researchDevelopment' in statement):
			begin = statement.index('"researchDevelopment"')-1
			end = statement.index('}}', begin)+2
			income_data.append(statement[begin:end])
			statement = statement[end:]
		for data in income_data:
			data_as_json = json.loads(data)
			print(data_as_json["endDate"]["fmt"])
	
	#def process_balance_sheet(self):
		

	#def process_cash_flow(self):
		
	#TODO------------------------------------------------------------------------------
	#Need to export relevant data into a file once I accurately 
