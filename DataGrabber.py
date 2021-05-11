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

		#time.sleep(5)
		
		#balance_statement = grabResource('https://finance.yahoo.com/quote/'+ stock_symbol +'/balance-sheet?p='+ stock_symbol)
		#print("Balance Sheet found!")
		#time.sleep(5)
		
		#cash_flow_statement = grabResource('https://finance.yahoo.com/quote/'+stock_symbol +'/cash-flow?p='+ stock_symbol)
		#print("Cash Flow found!")

		#Unfortunately the keys to the data must be found in the source manually
		#annualRevenue = self.pullInfo(income_statement, "annualTotalRevenue")
		#totalAssets = self.pullInfo(income_statement, "totalAssets")
		
		#annualTotalRevenue = cleanData(output)

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



	def pullInfo(self, infoSource, label):
		begin = infoSource.index(label)
		begin = infoSource.index("[", begin)
		end = infoSource.index("]", begin)
			
		output = infoSource[begin+1:end]

		#This is reused code from before the change, but it works
		#It feels like a hack to reformat the JSON without the label to make it fit
		#But as long as you are careful to align the dates with the values it works
		#---------------------------------------------------------------------------
		pieces = []
		openBraces = 0
		beginPiece = 0
		closePiece = 0
		index = 0
		while(index < len(output)):
			if(output[index] =="{"):
				if(openBraces ==0):
					beginPiece = index
				openBraces += 1
			elif(output[index] =="}"):
				openBraces -= 1
				if(openBraces ==0):
					closePiece = index
					print(output[beginPiece:closePiece+1])
					pieces.append(output[beginPiece:closePiece+1])
			index +=1
		#---------------------------------------------------------------------------

		for piece in pieces:
			data = json.loads(str(piece))
			year = data["asOfDate"][0:4]
			temp = {label : data["reportedValue"]["raw"]}
			self.yearly_data[year] = temp
			print(self.yearly_data)
		print(self.yearly_data['2019'][label])
