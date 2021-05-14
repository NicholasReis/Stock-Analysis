from Stock import *

class Analyzer:
	years = []
	#pe (Will figure this out later)
	annual_revenue=0
	profit_margin=0
	shares_issued=0
	current_assets=0
	current_liabilities=0
	cashflow=0
	capital_expenditures=0
	price_vs_free_cashflow=0

	def __init__(self, stock):
		#Assigns stock as a global variable so I can call the data from every function
		self.stock = stock
		#Assigns the years of data as global variables that I can use as keys in every function
		self.years = stock.getYears()

		#Processes all the data------------------vv
		assign_annual_revenue_metric()
		assign_profit_margin_metric()
		assign_shares_issued_metric()
		assign_current_assets_vs_current_liabilities_metric()
		assign_cashflow_metric()
		assign_capital_expenditures_metric()
		assign_price_to_free_cashflow_metric()

	#Analyzes the data--------------------------------vv
	def assign_annual_revenue_metric(self):
		

	def assign_profit_margin_metric(self):


	def assign_shares_issued_metric(self):
		

	def assign_current_assets_vs_current_liabilities_metric(self):
		

	def assign_cashflow_metric(self):

	
	def assign_capital_expenditures_metric(self):

		
	def assign_price_to_free_cashflow_metric(self):


	#Gets the analyzed values--------------------------vv
	def get_annual_revenue_metric(self):


	def get_profit_margin_metric(self):


	def get_shares_issued_metric(self):


	def get_assets_vs_liabilities_metric(self):


	def get_cashflow_metric(self):


	def get_capital_expenditures_metric(self):


	def get_price_to_free_cashflow_metric(self):


