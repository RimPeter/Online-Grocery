import gspread
from google.oauth2.service_account import Credentials
import requests
import json

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('CRED.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('grocery_online')

#products = SHEET.worksheet('product_list')
#products_data = products.get_all_values()

food_items = SHEET.worksheet('food_items')
food_items_data = food_items.get_all_values()

API_KEY = open('API_KEY').read()
SEARCH_ENGINE_ID = open('SearchEngineID').read()

with open('productlist.json', 'r') as file:
    product_list = json.load(file)

#search_query = list(product_list["Dairy"].keys())[3] + 'packaging'
    
def search_google_image(search_query):
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
        return results['items'][0]['link']
    else:
        return 'No image found'
    
#print(search_google_image(search_query))

def rows_to_append():
    rows_to_append = []
    for category, inner_dict in product_list.items():
        for product, price in inner_dict.items():
            the_link = search_google_image(product + ' packaging')
            rows_to_append.append([category, product, price, the_link])

    worksheet = SHEET.worksheet('food_items')

    for row in rows_to_append:
        worksheet.append_row(row)
        
rows_to_append()


    
    