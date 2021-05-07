import requests
import json

income_statement = requests.get('https://finance.yahoo.com/quote/amc/balance-sheet?p=amc')
begin = income_statement.text.index(":", income_statement.text.index("QuoteSummaryStore"))
end = income_statement.text.index("FinanceConfigStore")
output = income_statement.text[begin+1:end-2]
f = json.loads(output)
print(f)
#charIndex = 0
#for character in output:
#	print(character, end="")
#	charIndex+=1	
#	if(charIndex == 70):
#		print()
#		charIndex = 0

