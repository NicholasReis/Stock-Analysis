import requests
class DataGrabber:
	def __init__(self, stock_symbol):
		self.stock_symbol = stock_symbol
		
		income_statement = self.grabResource('https://finance.yahoo.com/quote/'+ stock_symbol +'/financials?p='+ stock_symbol)
		print("Income Statement found!")
		#balance_statement = grabResource('https://finance.yahoo.com/quote/'+ stock_symbol +'/balance-sheet?p='+ stock_symbol)
		#print("Balance Sheet found!")
		#cash_flow_statement = grabResource('https://finance.yahoo.com/quote/'+stock_symbol +'/cash-flow?p='+ stock_symbol)
		#print("Cash Flow found!")

		#begin = income_statement.text.index("annualTotalRevenue")
		#end = income_statement.text.index("]", begin)
			
		#output = income_statement.text[begin:end+1]
		#annualTotalRevenue = cleanData(output)

		

	def grabResource(self, webPage):
		html = requests.get(webPage)
		begin = html.text.index("root.App.now")
		begin = html.text.index(";", begin)
		end = html.text.index("(this)", begin)
		shortened_segment = html.text[begin+1:end]
		return shortened_segment
