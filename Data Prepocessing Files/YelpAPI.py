# -*- coding: utf-8 -*-
"""
Yelp Fusion API code sample.
This program demonstrates the capability of the Yelp Fusion API
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.
Please refer to http://www.yelp.com/developers/v3/documentation for the API
documentation.
This program requires the Python requests library, which you can install via:
`pip install -r requirements.txt`.
Sample usage of the program:
`python sample.py --term="bars" --location="San Francisco, CA"`
"""
from __future__ import print_function
import json
import requests


# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode


# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# You can find it on
# https://www.yelp.com/developers/v3/manage_app
API_KEY= "XXXXXXXX"

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
REVIEW_PATH = '/v3/businesses/'

# Defaults for our simple example.
#DEFAULT_TERM = 'burger'
#DEFAULT_LOCATION = 'Syracuse, NY'
SEARCH_LIMIT = 50


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))
    
    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


def get_reviews(api_key, business_id):

    review_path = REVIEW_PATH + business_id +"/reviews"
    return request(API_HOST, review_path, api_key)


def query_api(term, location):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location)
    print (term, "\n")
    with open ("state data/"+location+".json", 'a+') as fp:
        businesses = response.get('businesses')
        #print(len(businesses))
        for i in range (len(businesses)):   
            if not businesses:
                return
            business_id = businesses[i]['id']
            response = get_business(API_KEY, business_id)
            json.dump(response,fp)
            fp.write("\n")
                #fp.write("\n")
        fp.close()

def main():
    term = ['sandwich','hamburger','burger', 'hot dog','buffalo wing', 'chicken wings', \
    'french fries','fried chicken','chicken','sushi', 'turkey','eggs', 'waffle', 'corn bread', 'milkshake',\
    'donuts', 'steak', 'pizza', 'mac and cheeese', 'pasta', 'pastry', 'tacos','breakfast', 'lunch',\
    'brunch','dinner', 'snacks', 'bar','restaurants', 'chinese', 'japanese', 'korean', 'indian', \
    'mexican', 'american', 'italian','cake', 'pulled pork', 'chicken nugget', 'beef', 'pancake']
        
    location = ['Syracuse, NY','New York City, NY', 'Rochester, NY', 'Buffalo, NY', \
               'Albany, NY', 'Utica, NY', 'Ithica, NY', 'Binghamton, NY',\
               'Auburn, AL', 'Birmingham, AL', 'Montgomery, AL', 'Atlanta, GA',\
                'Juneau, AK', 'Phoenix, AZ', 'Little Rock, AR', 'Sacramento, CA',\
                'Denver, CO', 'Hartford, CT', 'Dover, DE', 'Tallahassee, FL', \
                'Miami, FL', 'Honolulu, HI', 'Boise, ID', 'Springfield, IL', \
                'Indianapolis, IN', 'Des Moines, IA', 'Topeka, KS', 'Frankfort, KY',\
                'Baton Rouge, LA', 'Augusta, ME', 'Annapolis, MD', 'Boston, MA',\
                'Lansing, MI', 'Detroit, MI', 'St. Paul, MN', 'Jackson, MS', \
                'Jefferson City, MO', 'Helena, MT', 'Washington, DC', 'Lincoln, NE',\
                'Carson City, NV', 'Las Vegas, NV', 'Concord, NH', 'Trenton, NJ', \
                'Newark, NJ', 'Santa Fe, NM', 'Raleigh, NC', 'Charlotte, NC', 'Bismarck, ND',\
                'Columbus, OH', 'Oklahoma City, OK', 'Salem, OR', 'Harrisburg, PA',\
                'Austin, TX', 'Dallas, TX', 'Houston, TX', 'Salt Lake City ,UT',\
                'Olympia, WA', 'Seattle, WA', 'Madison, WI','Cheyenne, WY', 'Los Angeles, CA',\
                'San Fransisco, CA', 'San Jose, CA']

    for i in term:
        query_api(i,location[28])

if __name__ == '__main__':
    main()

