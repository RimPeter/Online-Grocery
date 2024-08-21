import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('CRED.json', scope)

# Authorize the clientsheet 
client = gspread.authorize(creds)

# Get the instance of the Spreadsheet
sheet = client.open('grocery_online')

# Get the instance of the first sheet (worksheet)
worksheet = sheet.worksheet('food_items')

# Get all records of the data
records = worksheet.get_all_records()

# Create a dictionary to store the data
data_dict = {}

# Loop through the records and populate the dictionary
for record in records:
    product = record['product']
    data_dict[product] = {
        'category': record['category'],
        'price': record['price'],
        'link': record['link']
    }

# Write the data to a JSON file
with open('food_items.json', 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)

print("Data successfully written to food_items.json")
