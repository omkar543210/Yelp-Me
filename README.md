# Yelp-Me
Yelp Me! - The Cuisine Recommender 
The goal of the Yelp Me! application is to the recommend the best restaurant based on the user entered cuisine. The application will analyze user reviews of all the restaurants that correspond to that user entered cuisine and provide a sentiment score i.e. our system will recommend the best restaurant for that cuisine which the user desires to eat.

Users have the flexibility to provide a geographic location ranging from different states to cities. In addition, filter criteria can be added to refine the search. For example, users could search from the cheapest restaurants to the expensive ones. Once this information is entered, our application finds all the restaurants with their information and displays this information on the location map and also in the form of a table. User can hover on the map to check the names of these restaurants and also select a restaurant from the table to check it on the location map. 

*********************************** CONFIGURATION ***********************************

== API Accounts ==

In order to use the Yelp Me application, a user must have registered an account with the Mapbox API.  The steps to create a mapbox account and generate the access tokens is given below.   

https://www.mapbox.com/help/how-access-tokens-work/#mapbox-account

Now copy the access token to the OAuth_Keys.json file.

== Authentication File ==

Once account is setup with the MapBox API services, the access tokens will need to be stored in JSON format in a file called OAuth_Keys.json.  This file is placed in the same directory as the YelpMe.py. A sample file containing dummy keys currently exists in the YelpMe zip file. The file must contain the following key value pairs all at the initial level in the JSON file.

    KEY         VALUE
    Token       Mapbox API access token


== Data Subdirectory ==

The data sub-directory must be located in the directory where the python code resides. This folder, contains files about businesses (restaurants) and business review (restaurants reviews) for different businesses across the United States in JSON format. Along with this, the data contains other JSON files which include the state and city latitude and longitude, cuisine file and food file.

******************************** Running the Code ********************************

== Install Dependencies ==

i.    pip install dash==0.31.1  # The core dash backend
	  
ii.   pip install dash-html-components==0.13.2  # HTML components
	  
iii.  pip install dash-core-components==0.38.1  # Supercharged components
	  
iv.   pip install dash-table==3.1.7  # Interactive DataTable component
	  
v.    pip install dash-table-experiments==0.6.0
	  
Find the Documentation here: https://dash.plot.ly/

 
1.      Plotly- Install plotly-python from PyPI using: pip install plotly

        Run the following code in python after installing plotly - 
	
		    import Plotly
		    
		    Plotly.tools.set_credentials_file(username=‘Your Username’, api_key=‘Your API key’)
		
Find the Documentation here: https://plot.ly/python/getting-started/
	
	
 
2.      TextBlob- Install TextBlob-python from PyPI using:  pip install -U textblob

Find the Documentation here: https://textblob.readthedocs.io/en/dev/
	

================================================================

After all of the configuration steps have been completed, the Yelp Me application is ready to be run.  In order to start the application, open your terminal and run the following command - 

python YelpMe.py


The output of this command will be as follows -  

Running on http://127.0.0.1:8050/ 
Debugger PIN: 269-419-746 
 * Serving Flask app “YelpMe” (lazy loading) 
 * Environment: production 
   WARNING: Do not use the development server in a production environment. 
   Use a production WSGI server instead. 
 * Debug mode: on 

Running on http://127.0.0.1:8050/ 
Debugger PIN: 330-499-856

Enter the url mentioned after "Running On" on your browser and the application is started.

*********************************** Limitations ***********************************

== Mapbox API ==

The location map provided by the MapBox API does not take the correct latitude and longitude values when the map is zoomed out to the maximum level during initialization. 
