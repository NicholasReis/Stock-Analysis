import requests
import json
import time
import array

class DataGrabber:

	yearly_data = dict()

	def __init__(self, stock_symbol):
		self.stock_symbol = stock_symbol
		
		shortened_segment = self.grabResource('https://finance.yahoo.com/quote/'+ stock_symbol +'/financials?p='+ stock_symbol)
		print("Income Statement found!")
		print(shortened_segment)

		cashflow_statement = self.process_segment(shortened_segment, '"cashflowStatementHistory"')
		print(cashflow_statement)

		income_statement = self.process_segment(shortened_segment, '"incomeStatementHistory"')
		print(income_statement)

		balance_history = self.process_segment(shortened_segment, '"balanceSheetHistory"')
		print(balance_history)

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
