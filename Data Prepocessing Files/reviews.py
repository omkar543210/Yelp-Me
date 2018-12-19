# -*- coding: utf-8 -*-

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

#import argparse
import json
#import pprint
import requests
#import sys
#import urllib
import pandas as pd
import re

from textblob import TextBlob
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
    try:
        review_path = REVIEW_PATH + business_id +"/reviews"
        return request(API_HOST, review_path, api_key)
    except:
        pass
    return

def query_api(location):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    norm_dict={"0":-1,"1":-0.6,"2":-0.2,"3":0.2,"4":0.6,"5":1.0}
    myDict={"deli":"deli","delis":"deli","gluten":"gluten","sushi":"sushi","chicken":"chicken","cheeseburger":"burger","sandwich":"sandwich","sandwiches":"sandwich","hamburger":"hamburger","hamburgers":"hamburger","burger":"burger","burgers":"burger", "hotdog":"hotdog","hotdogs":"hotdog", "hot dog": "hotdog", "hot dogs":"hotdog", "hot-dog":"hotdog","buffalo wing": "buffalo wing", "buffalo wings":"buffalo wing", "chicken wing": "chicken wing","chicken wings":"chicken wing","turkey":"turkey","egg":"egg","eggs":"egg","waffle":"waffle","waffles":"waffle","corn":"corn","milk shake":"milk shake","milkshake":"milk shake", "milkshakes":"milk shake", "milk shakes":"milk shake", "donut":"donut","donuts":"donut","doughnut":"donut","doughnuts":"donut", "steak":"steak","steaks":"steak", "pizza":"pizza", "pizzas":"pizza", "mac and cheese":"mac and cheese", "macandcheese":"mac and cheese", "mac n cheese":"mac and cheese", "pasta":"pasta", "pastry":"pastry","pastries":"pastry", "pastryies":"pastry", "tacos":"tacos", "breakfast":"breakfast", "lunch":"lunch","dinner":"dinner","brunch":"brunch","snack":"snack","snacks":"snack", "bar":"bar","bars":"bar", "chineese":"chineese", "chines":"chineese","chinese":"chineese", "japanese":"japanese", "korean":"korean", "indian":"indian", "india":"indian", "mexican":"mexican", "american":"american", "italian":"italian", "cake":"cake", "cakes":"cake", "pork": "pork","pulled pork":"pulled pork", "pulledpork":"pulled pork", "pulled-pork":"pulled pork", "chicken nuggets":"chicken nuggets", "chicken nugget":"chicken nuggets", "beaf":"beef","beef":"beef","wing":"wings","wings":"wings", "fries": "fries","frenchfries": "fries","french-fries": "fries","pancake":"pancake","pancakes":"pancake"}
    lst=["delis","deli", "gluten","sushi","chicken","cheeseburger","sandwich","sandwiches","hamburger","hamburgers","burger","burgers", "hotdog","hotdogs", "hot dog", "hot dogs", "hot-dog",\
    "buffalo wing", "buffalo wings", "chicken wing","chicken wings", "wing", "wings", "french fries","frenchfries", "turkey",\
     "egg","eggs","waffle","waffles","corn","milk shake","milkshake", "milkshakes", "milk shakes", "donut","donuts","doughnut",\
     "doughnuts", "steak","steaks", "pizza", "pizzas", "mac and cheese", "macandcheese", "mac n cheese", "pasta", "pastry"\
     "pastries", "pastryies", "tacos", "breakfast", "lunch","dinner","brunch","snack","snacks", "bar","bars", "chineese", \
     "chines","chinese", "japanese", "korean", "indian", "india", "mexican", "american", "italian", "cake", "cakes", "pork"\
     "pulled pork", "pulledpork", "pulled-pork", "chicken nuggets", "chicken nugget", "nuggets", "nugget", "beaf","beef"]  
    
    
    
    with open ("state data/"+location+".json", 'r') as fp, open ("state data/"+location+" reviews.json", 'a+') as fp1 :
        ##### logic to get business if from file
        df= pd.read_json(fp, lines=True)
        bid=df['id']
        for business_id in bid:
            keywords=[]
            review_text=[]
            
            rating=[]
            tb_score=[]
            norm_rating=[]
            
            review_response = get_reviews(API_KEY, business_id)
            try:
                
                for i in range (len(review_response)):
                    temp=set()
                    flag=0
                    data = review_response["reviews"][i]
                    review_text.append(data["text"])
                    rating.append(data["rating"])
                    
                    
                    s=re.sub(r'[^\w\s]','',review_text[i])
                    a = s.lower()
                    word=a.split(' ')
                                
                    for worda in word:
                        if (worda in lst):
                            cusine=myDict[worda]
                            temp.add(cusine)
                            flag=1
                    keywords.append(list(temp))
                            
                    
                    if (flag==1):
                        tb=TextBlob(review_text[i]).sentiment.polarity
                        val=round(tb,2)
                        #print (val)
                        if (not(-0.2 <= val <= 0.2)) :
                            tb_score.append(val)  
                        else:
                            tb_score.append(0.0)
                    else:
                        tb_score.append(0.0)
                    
                    norm_rating.append(norm_dict[str(rating[i])])
                
                
                
                reviewDict = {"id":business_id, "text":review_text, "rating":rating, \
                              "TBscore": tb_score, "normalisedRating": norm_rating ,"keywords": keywords}
                json.dump(reviewDict,fp1)
                fp1.write("\n") 
            except:
                pass


def main():

   location = ['Syracuse, NY','New York City, NY', 'Rochester, NY', 'Buffalo, NY', \
                'Albany, NY', 'Utica, NY', 'Ithica, NY', 'Binghamton, NY'\
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
                'Austin, TX', 'Dallas, TX', 'Houston, TX', \
                'Olympia, WA', 'Seattle, WA', 'Madison, WI','Cheyenne, WY', 'Los Angeles, CA',\
                'San Fransisco, CA', 'San Jose, CA']
   query_api(location[54])

if __name__ == '__main__':
    main()

