from DataGrabber import DataGrabber

class Stock:
	stock_symbol = ""
	def __init__(self, stock_symbol):
		self.stock_symbol = stock_symbol
		DataGrabber(stock_symbol)

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
