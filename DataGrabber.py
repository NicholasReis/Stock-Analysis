import requests
import json

class DataGrabber:
	#Creates a global dictionary to hold all the yearly data
	yearly_data = dict()

	#Just sets the min and max year outside of any reasonable year so that current years will override them
	minYear = 5000
	maxYear = 0

	def __init__(self, stock_symbol):
		#Assigns stock symbol to a non-existent global variable
		#I need to investigate this, but I suspect it's just a quirk of python
		self.stock_symbol = stock_symbol
		shortened_segment = self.grab_resource()
		#Creates a smaller segment of JSON regarding just the cashflow
		cashflow_statement = self.process_segment(shortened_segment, '"cashflowStatementHistory"')
		#print(cashflow_statement)

		#Creates a smaller segment of JSON regarding just the income_statement	This stupid-ass ":{" changes the quartly vs annual
		income_statement = self.process_segment(shortened_segment, '"incomeStatementHistory":{')
		#print(income_statement)
		

		#Creates a smaller segment of JSON regarding just the balance_sheet
		balance_history = self.process_segment(shortened_segment, '"balanceSheetHistory"')
		#print(balance_history)

		#converts the JSON string into accessible data for yearly_data[]
		self.process_income_statement(income_statement)
		
		#converts the JSON string into accessible data for yearly_data[]
		self.process_income_statement(balance_history)
		
		#converts the JSON string into accessible data for yearly_data[]
		self.process_income_statement(cashflow_statement)
		
		#self.delete_files()
		
	#Function to grab the webpage and isolate the relevant data
	def grab_resource(self):

		#Assigns html as the page request
		html = requests.get('https://finance.yahoo.com/quote/'+ self.stock_symbol +'/financials?p='+ self.stock_symbol)
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
		#Returns the data of the respective label in a JSON format
		return segment[begin:end+1]

	#Function to process the information specific to the income statement
	def process_income_statement(self, statement):
		#Creates an array for storing the data associated with each year (Though currently quarter)
		income_data = []
		
		#Finds the starting point of the data we need to collect
		begin = statement.index('[')
		#Finds the opening quotation of the first data point
		begin = statement.index('"', begin)
		#Finds the ending quotation of the first data point
		end = statement.index('"', begin+1)+1
		#Sets the first label (including quotation marks) in case of changing order of data or some that is unused by some companies
		first_label = statement[begin:end]

		#Checks that there is another element (researchDevelopment is the first label in the data)
		while(first_label in statement):
			#If there is it will take the index of the first quotation mark
			begin = statement.index(first_label)-1
			#It will then take the index of the end of the data
			end = statement.index('}}', begin)+2
			#And input that string of data into the array
			income_data.append(statement[begin:end])
			#Chops off the segment we processed so that instance of researchDevelopment wont come up again
			statement = statement[end:]
		#print(income_data[0])
		#Takes each string of data and loads it into a JSON object
		for data in income_data:
			print(data)
			segmented_data = dict()
			year = 0
			while('"' in data):
				date = False
				begin = data.index('"')+1
				end = data.index('"', begin+1)
				label=data[begin:end]
				if("endDate" in data[begin:end]):
					date = True
				#Everything after label:
				data = data[data.index(":")+1:]
				end = data.index("}")+1
				contents_segment = data[:end]
				print(contents_segment)
				if(len(contents_segment) > 2 and label != "maxAge"):
					contents = data[:end]

					if(date):
						begin = contents.index("fmt")
						begin = contents.index(":", begin)+2
						date_end = begin + 4
						#print("Data: "+ endDate[begin:end])
						year = contents[begin:date_end]
						if(int(self.minYear) > int(year)):
							self.minYear = year
						if(int(self.maxYear) < int(year)):
							self.maxYear = year
						contents = str(year)
					else:
						begin = contents.index("raw")
						begin = contents.index(":", begin)+1
						end = contents.index(",", begin)
						contents = contents[begin:end]
						
				else:
					if(label == "maxAge"):
						contents = 1
					else:
						contents = 0
				end = data.index("}")+1
				data = data[end:]
				print("Label: " + label)
				print("Data: " + str(contents))
				segmented_data[label] = contents
			self.yearly_data[str(year)] = segmented_data

	def get_data(self):
		return self.yearly_data

	#Returns the recorded years of data
	def get_years(self):
		#Requires the +1 otherwise it terminates before maxYear
		return range(int(self.minYear), int(self.maxYear))
