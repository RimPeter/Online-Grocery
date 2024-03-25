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

products = SHEET.worksheet('product_list')

data = products.get_all_values()

API_KEY = open('API_KEY').read()
SEARCH_ENGINE_ID = open('SearchEngineID').read()

# with open('productlist.json', 'r') as file:
#     product_list = json.load(file)
product_list = {
    "Dairy": {
        "Milk": "1.50",
        "Cheese": "2.50",
        "Yogurt": "1.00",
        "Butter": "2.00"
    },
    "Meat": {
        "Chicken": "3.50",
        "Beef": "5.50",
        "Pork": "4.50",
        "Lamb": "6.50"
    },
    "Fruit": {
        "Apple Fruit": "1.00",
        "Banana": "0.50",
        "Orange": "0.75",
        "Grapes": "2.00"
    },
    "Vegetables": {
        "Carrot": "1.00",
        "Potato": "0.50",
        "Onion": "0.75",
        "Lettuce": "2.00"
    }
}
search_query = list(product_list["Dairy"].keys())[3] + 'packaging'
    
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

# loop through the product list and search for images, add them to the product list
def add_images_to_product_list():
    for category in product_list:
        for product in product_list[category]:
            #print(product)
            the_link = search_google_image(product + ' packaging')
            #print(the_link)
            product_list[category][product] = {"price": product_list[category][product], "image_link": the_link}
            #print(product_list[category][product])
            
add_images_to_product_list()


        
        
        
    



    






    
    