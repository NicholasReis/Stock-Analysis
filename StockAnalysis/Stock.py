import requests
import time
import json

def main():
	print("Started")
	acquireData("amc")


	#time.sleep(5)
	
	
	
	
	#time.sleep(5)
	#cash_flow = requests.get('https://finance.yahoo.com/quote/'+ stock_symbol +'/cash-flow?p='+ stock_symbol)
	#print("Cash Flow found!")
	
	#print("All information recieved! Processing...");

def acquireData(stock_symbol):
	income_statement = requests.get('https://finance.yahoo.com/quote/'+ stock_symbol +'/financials?p='+ stock_symbol)
	print("Income Statement found!")

	begin = income_statement.text.index("annualTotalRevenue")
	end = income_statement.text.index("]", begin)
	
	output = income_statement.text[begin:end+1]
	annualTotalRevenue = cleanData(output)
	
	#annualInterestExpenseNonOperating
	
	#balance_sheet = requests.get('https://finance.yahoo.com/quote/'+ stock_symbol +'/balance-sheet?p='+ stock_symbol)
	#print("Balance Sheet found!")

def cleanData(output):
	print("Cleaning")
	begin = output.index("[")
	end = output.index("]")
	output = output[begin +1:end]
	
	pieces=[10]
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
	
	data=[5]
	for piece in pieces:
		temp = piece.split(",")
		for t in temp:
			dataIndex = 0
			if(t.contains("asOfDate") or t.contains("raw")):
				pleaseLastOne = t.split(":")
				
				dataIndex += 1
				




if __name__ == "__main__":
    main()
