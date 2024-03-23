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



search_query = '25010605401354 barcode'

def google_search(search_query):
    ''' 
    Search for an image using Google Custom Search API 
    '''
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
    
print(google_search('25010605401354 barcode'))

print('Hello World!')