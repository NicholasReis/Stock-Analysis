import requests
import json

class DataGrabber:
	#Creates a global dictionary to hold all the yearly data
	yearly_data = dict()

	def __init__(self, stock_symbol):
		#Assigns stock symbol to a non-existent global variable
		#I need to investigate this, but I suspect it's just a quirk of python
		self.stock_symbol = stock_symbol
		
		#Commented out since it's not needed during testing
		#self.write_to_file()
		
		#Assigns a shortened segment from the file gnerated from the online resource
		shortened_segment = self.read_from_file()
		print("Income Statement found!")
		#print(shortened_segment) #Temporary diagnostic info for parsing JSON element

		#Creates a smaller segment of JSON regarding just the cashflow
		cashflow_statement = self.process_segment(shortened_segment, '"cashflowStatementHistory"')
		#print(cashflow_statement)

		#Creates a smaller segment of JSON regarding just the income_statement	This stupid-ass ":{" changes the quartly vs annual
		income_statement = self.process_segment(shortened_segment, '"incomeStatementHistory":{')
		#print(income_statement)
		#converts the JSON string into accessible data for yearly_data[]
		self.process_income_statement(income_statement)

		#Creates a smaller segment of JSON regarding just the balance_sheet
		balance_history = self.process_segment(shortened_segment, '"balanceSheetHistory"')
		#print(balance_history)
		
	#Function to grab online resource
	def write_to_file(self):
		#Assigns the shortened version of the webpage
		shortened_segment = self.grabResource('https://finance.yahoo.com/quote/'+ self.stock_symbol +'/financials?p='+ self.stock_symbol)

		#Opens/Creates a file with the ticker symbol of the stock to store data
		#I am going to have to handle overwriting data or deleting the file later
		with open(self.stock_symbol+".txt", "w") as output_file:
			#Writes the shortened pieces to the file (Though this will later be formatted into a dictionary entry)
			output_file.write(shortened_segment)

	#Function to parse the <stockname> file
	def read_from_file(self):
		#Opens the file which in the future will have the formatted stock information
		with open(self.stock_symbol + ".txt") as input_file:
			#Reads the file and assigns it to a string
			text_from_file = input_file.read()
		#Returns the text from the file
		return text_from_file

	#Function to grab the webpage and isolate the relevant data
	def grabResource(self, webPage):
		#Assigns html as the page request
		html = requests.get(webPage)
		#Sets the beginning index of the relevant info
		begin = html.text.index('"QuoteSummaryStore"')
		#Sets the ending index of the relevant info
		end = html.text.index('"FinanceConfigStore"')
		#Isolates the relevant info
		shortened_segment = html.text[begin:end]
		#Returns relevant info
		return shortened_segment

	#Takes the chunk of relevant data and breaks it down further into the segment of relevant
	#data (ie. CashFlow data, Balance Sheet data, and Income Statement data)
	def process_segment(self, segment, label):
		#Beings at the respective data label
		begin = segment.index(label)
		#Finds the ']' and then from there the nearest '}}' which in this dataset denotes
		#the end of the JSON data designated to the respective label
		end = segment.index(']', begin)
		end = segment.index('}', end)
		print(segment[begin:end+1])
		#Returns the data of the respective label in a JSON format
		return segment[begin:end+1]

	#Function to process the information specific to the income statement
	def process_income_statement(self, statement):
		#Creates an array for storing the data associated with each year (Though currently quarter)
		income_data = []
		#Checks that there is another element (researchDevelopment is the first label in the data)
		while('researchDevelopment' in statement):
			#If there is it will take the index of the first quotation mark
			begin = statement.index('"researchDevelopment"')-1
			#It will then take the index of the end of the data
			end = statement.index('}}', begin)+2
			#And input that string of data into the array
			income_data.append(statement[begin:end])
			#Chops off the segment we processed so that instance of researchDevelopment wont come up again
			statement = statement[end:]

		#Takes each string of data and loads it into a JSON object
		for data in income_data:
			#Loads data as JSON
			data_as_json = json.loads(data)
			#Prints just to see if it works (Which it currently does)
			print(data_as_json) #data_as_json["endDate"]["fmt"]
	
	#Function to process the information specific to the balance sheet
	#def process_balance_sheet(self):
		
	#Function to process the information specific to the cashflow
	#def process_cashflow(self):
		
