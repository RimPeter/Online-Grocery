import gspread
from google.oauth2.service_account import Credentials
import requests

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('CRED.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('grocery_online')

products = SHEET.worksheet('product_list')

data = products.get_all_values()

#print(data)

API_KEY = open('API_KEY').read()
SEARCH_ENGINE_ID = open('SearchEngineID').read()



search_query = 'rimaszecsi'

url = 'https://www.googleapis.com/customsearch/v1'
params = {
    'q' : search_query,
    'key' : API_KEY,
    'cx' : SEARCH_ENGINE_ID,
    'searchType' : 'image'
}

response = requests.get(url, params=params)
results = response.json()
#print(results)

if 'items' in results:
    print(results['items'][0]['link'])
    

# loop through the first 5 items in the 3rd column of 'product_list' sheet and search for the image of the product and update the 4th column with the image link

update = products.update_cell(1, 4, 'Image Link')
for i in range(1, 15460):
    search_query = data[i][2]
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'q' : search_query,
        'key' : API_KEY,
        'cx' : SEARCH_ENGINE_ID,
        'searchType' : 'image'
    }
    response = requests.get(url, params=params)
    results = response.json()
    if 'items' in results:
        image_link = results['items'][0]['link']
        update = products.update_cell(i+1, 4, image_link)
        print(f'Updated image link for {data[i][0]}')
    else:
        print(f'No image found for {data[i][0]}')
        
print('All done!')




