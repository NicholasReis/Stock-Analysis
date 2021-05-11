import requests
import json
import time
import array

class DataGrabber:

	yearly_data = dict()

	def __init__(self, stock_symbol):
		self.stock_symbol = stock_symbol
		
		#self.write_to_file()
		
		shortened_segment = self.read_from_file()
		print("Income Statement found!")
		print(shortened_segment)

		cashflow_statement = self.process_segment(shortened_segment, '"cashflowStatementHistory"')
		#print(cashflow_statement)

		income_statement = self.process_segment(shortened_segment, '"incomeStatementHistory"')
		print(income_statement)
		self.process_income_statement(income_statement)

		balance_history = self.process_segment(shortened_segment, '"balanceSheetHistory"')
		#print(balance_history)
		

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
		return segment[begin:end+1]

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
		
