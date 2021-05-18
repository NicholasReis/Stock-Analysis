import requests
from DataGrabber import *
from Stock import *
from Analyzer import *

def main():
	#Prints to signify it is running
	print("Started")
	#Starts the DataGrabber to load information to a file for stock to pull from
	stock = Stock("ko")

	#Loads the stock so it will have the needed information to analyze
	#stock = Stock("ko", years)
	#Will run the calculations so we can pull the results without
	#cluttering up this class which will interpret them
	processedData = Analyzer(stock)

if __name__ == "__main__":
    main()
