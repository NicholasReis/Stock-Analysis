import requests
from DataGrabber import *
from Stock import *

#from Stock import Analyzer

def main():
	print("Started")
	dg = DataGrabber("amc")
	#stock = Stock("amc")
	#temp = stock.getYears()
	#print(temp)
	#print(stock.getAnnualRevenue(temp[2]))
	#processedData = Analyzer()

if __name__ == "__main__":
    main()
