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

	def __init__(self, stock, years):
		#Assigns stock as a global variable so I can call the data from every function
		self.stock = stock
		#Assigns the years of data as global variables that I can use as keys in every function
		self.years = years

		#Processes all the data------------------vv
		self.assign_annual_revenue_metric()
		self.assign_profit_margin_metric()
		self.assign_shares_issued_metric()
		self.assign_current_assets_vs_current_liabilities_metric()
		#self.assign_cashflow_metric()
		#self.assign_capital_expenditures_metric()
		#self.assign_price_to_free_cashflow_metric()

	#Analyzes the data--------------------------------vv


	#This will check if the company is bringing in more money each year or if less people are interested in the product
	#as time goes on. This could for instance show that a company selling ladders is not making as much each year
	#because they don't need to replace their ladders, or people are using different tools to reach high places
	#in either case, if people are not buying, the company is not in a good position
	#This is separate from net_income because it better reflects the sales, not the sales vs cost of running the company
	#ie the interest in the product/service that the company provides is being measured.
	def assign_annual_revenue_metric(self):
		#Running sum to calculate average
		running_sum= 0

		#First recorded revenue to compare against the average to see if it's increasing or decreasing overall
		first_recorded_revenue = self.stock.getData(self.years[0], "total_revenue")

		#For every year we have recorded
		for year in self.years:
			#Add the yearly revenue to the running total
			running_sum+=self.stock.getData(year, "total_revenue")
		
		#if the average total revenue is larger than the first revenue
		if(running_sum/len(self.years) > first_recorded_revenue):
			#The revenue is overall increasing
			print("The revenue is increasing!")
		else:
			#If not the revenue is overall decreasing
			print("The revenue is decreasing!")
		#Frankly it seems a little basic and hacky, will likely revisit later to check increasing or decreasing functions^^

		#Currently prints out so I can check the numbers, will later assign to some variables that the getters return
		print("Initial revenue: " + str(first_recorded_revenue))
		print("Average revenue: " + str(running_sum/len(self.years)))



	#This determines the money the company is bringing in vs how much it pays for upkeep
	#These can be volotile so use your judgement
	#A company like Coca-Cola could spend 10 cents making a bottle of Coke and sell it for $1
	#Looking at just that, their profit margin would be 90% because they spent 10 cents to make $1 and pocket the 90 cents.
	#This takes that principle and applies it to then entire company. The higher the better.
	def assign_profit_margin_metric(self):
		#Running sum of the profit margin to compare against initial profit
		running_profit_margin_sum = 0
		
		#First recorded profit margin to compare against the average to check for growth
		first_recorded_profit_margin = self.stock.getData(self.years[0], "net_income")/self.stock.getData(self.years[0], "total_revenue")
		
		#For every year we have data on
		for year in self.years:
			#Grabs relevant data
			net_income = self.stock.getData(year, "net_income")
			total_income = self.stock.getData(year, "total_revenue")
			#Adds the profit margin to the running sum
			running_profit_margin_sum += net_income/total_income
		if(running_profit_margin_sum/len(self.years) > first_recorded_profit_margin):
			#Increasing profit margin
			print("Profit is increasing!")
		else:
			print("Profit margin is decreasing...")

		#Outputs for now, will change
		print("Initial profit margin: " + str((first_recorded_profit_margin)*100)+"%")
		print("Average profit margin: " + str((running_profit_margin_sum/len(self.years))*100)+"%")


	#This counts the number of shares and basically checks for stock inflation
	def assign_shares_issued_metric(self):
		#Running sum of shares in circulation
		running_sum_issued_shares = 0
		
		#Gets the first recorded data point of how many shares there were
		first_recorded_shares_issued= self.stock.getData(self.years[0], "issuance_of_stock")

		#For each year we have recorded data for
		for year in self.years:
			#Adds the total number of stocks that year to the running sum
			running_sum_issued_shares += self.stock.getData(year, "issuance_of_stock")
		
		#If there is a higher average of shares than there was at first
		if(running_sum_issued_shares/len(self.years) > first_recorded_shares_issued):
			#Shares are being created
			print("The company is creating more shares diluting ownership, this could reduce the price of the stock in the future")
		else:
			#Shares are being bought
			print("The company is buying back their stocks which is increasing the value")

		#Outputs for now, will change
		print("Initial stocks issued: "+str(first_recorded_shares_issued))
		print("Average existing stocks over the past " + str(len(self.years)) + " years: " +str((running_sum_issued_shares/len(self.years))))


	#This will calculate the safety of the investment
	#If they have a lot of assets and few liabilities they can afford to stay afloat for that many years just selling off their assets without revenue
	#If they have high liabilities and low assets then they are bleeding money
	def assign_current_assets_vs_current_liabilities_metric(self):
		#Running sum for the asset to liability ratio
		running_sum_total_assets_vs_total_liabilities = 0

		#Added these for when I improve the analysis. I will be checking first and last years in more depth
		#With the right algorithm I will be able to see if it's an expected assets/liability for the company
		#or just something weird going on
		#first_recorded_assets = self.stock.getData(self.years[0], "total_assets")
		#first_recorded_liabilities = self.stock.getData(self.years[0], "total_liab")
		#first_recorded_assets_vs_liabilities = first_recorded_assets/first_recorded_liabilities

		#For each year we have recorded data for
		for year in self.years:
			#Takes down both the yearly assets and liabilities count
			recorded_assets = self.stock.getData(year, "total_assets")
			recorded_liabilities = self.stock.getData(year, "total_liab")
			#Creates the assets to liabilities ratio and adds it to the running sum
			running_sum_total_assets_vs_total_liabilities += recorded_assets/recorded_liabilities

		#Outputs for now, will change
		print("The number of times the company could pay off all it's debts is: " + str(running_sum_total_assets_vs_total_liabilities/len(self.years)))


	
	#def assign_cashflow_metric(self):

	
	#def assign_capital_expenditures_metric(self):

		
	#def assign_price_to_free_cashflow_metric(self):


	#Gets the analyzed values--------------------------vv
	#def get_annual_revenue_metric(self):


	#def get_profit_margin_metric(self):


	#def get_assets_vs_liabilities_metric(self):


	#def get_cashflow_metric(self):


	#def get_capital_expenditures_metric(self):


	#def get_price_to_free_cashflow_metric(self):


	#def get_shares_issued_metric(self):
	
		

	#Information I will want to keep track of. Will delete when I start implementing
		#pe
		#annual_revenue
		#profit_margin #(Net income / Total Revenue)
		#shares_issued
		#current_assets
		#current_liabilities
		#cash_flow
		#capital_expenditures
		#price #price to free cash flow < 15%
