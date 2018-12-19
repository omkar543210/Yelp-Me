import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import datetime
import tkinter


token = pd.read_json('Oath_Keys.json', lines=True)
mapbox_access_token = str(token['MapboxAccessToken'][0])

def filter_function(fooddropdown, cuisinedropdown, df_rest, df_review):

    global prevf
    global prevc
    global count

    if(fooddropdown != "food" and cuisinedropdown != 'cuisine'):  
        if(cuisinedropdown != prevc):
            print("Entered in cuisinedropdown")
            df_cuisine = cuisinedf.loc[cuisinedf['cuisine'] == cuisinedropdown]
            cuisine = list(df_cuisine['food'])[0]
            count+=1
            if(count%3==0):
                print("If cus: ",count)
                prevc = cuisinedropdown
            selection = cuisine 
        
        if(fooddropdown != prevf):
            print("Entered in fooddropdown")
            df_food = fooddf.loc[fooddf['cuisine'] == fooddropdown]
            food = list(df_food['food'])[0]
            count+=1
            if(count%3==0):
                print("If food: ",count)
                prevf = fooddropdown
            selection = food 

        elif(cuisinedropdown == prevc):
            print("Entered in cuisinedropdown")
            df_cuisine = cuisinedf.loc[cuisinedf['cuisine'] == cuisinedropdown]
            cuisine = list(df_cuisine['food'])[0]
            count+=1
            selection = cuisine 

        elif(fooddropdown == prevf):
            print("Entered in fooddropdown")
            df_food = fooddf.loc[fooddf['cuisine'] == fooddropdown]
            food = list(df_food['food'])[0]
            count+=1
            selection = food 


    elif(fooddropdown != "food"):
        print("Entered in only fooddropdown")
        df_food = fooddf.loc[fooddf['cuisine'] == fooddropdown]
        food = list(df_food['food'])[0]
        count+=1
        if(count%3==0):
            print("Elif fooddropdown: ",count)
            prevf = fooddropdown
        selection = food

    elif(cuisinedropdown != 'cuisine'):
        print("Entered in only cuisinedropdown")
        df_cuisine = cuisinedf.loc[cuisinedf['cuisine'] == cuisinedropdown]
        cuisine = list(df_cuisine['food'])[0]
        count+=1
        if(count%3==0):
            print("Elif cusdropdown: ",count)
            prevc = cuisinedropdown
        selection = cuisine  

           


    ######################## Dataframe access function #######################

    max_new = 5
    min_new = 0
    max_old = 1
    min_old = -1


    output = pd.merge(df_rest, df_review, how='inner', on='id')

    df = pd.DataFrame(columns=['id','name','coordinates', 'display_phone', 'hours','location','price','url','cusine_rating'])
    word = selection
    #print(word)
    string = []
    for dish in word:
        for i in range (len(output)):
            score = []
            flag = False
            row = output.iloc[i]
            if (dish in output.keywords[i][0]):
                flag = True
                if row["TBscore"][0] != 0:
                    score.append(row["TBscore"][0])
                else:
                    score.append(row["normalisedRating"][0])

            if (dish in output.keywords[i][1]):
                flag = True
                if row["TBscore"][1] != 0:
                    score.append(row["TBscore"][1])
                else:
                    score.append(row["normalisedRating"][1])

            if (dish in output.keywords[i][2]):
                flag = True
                if row["TBscore"][2] != 0:
                    score.append(row["TBscore"][2])
                else:
                    score.append(row["normalisedRating"][2])
                    
            if (flag):
                final_score = sum(score) / len(score)
                newvalue = (max_new-min_new)/(max_old-min_old)*(final_score-min_old)+min_new
                final_score = round(newvalue, 2)
                string.append({'id':row["id"],'name':row["name"],'coordinates':row["coordinates"], 'display_phone':row["display_phone"], 'hours':row["hours"],'location':row["location"],'price':row["price"],'url':row["url"],'cusine_rating':final_score})
            
            flag=False

    df = pd.DataFrame.from_dict(string)
    df = df.sort_values(by=['cusine_rating'], ascending=False)
    return df


def displayOnTable(citydropdown, statedropdown):

    stdf = pd.read_json("data/"+citydropdown+", "+statedropdown+".json", lines=True)

    addr = []

    for i in stdf.location:
        str1 = ""
        for j in i['display_address']:
            str1+=j
        addr.append(str1)
     
    days = {'0':'Monday', '1':'Tuesday', '2':'Wednesday', '3':'Thursday', '4':'Friday', '5':'Saturday', '6':'Sunday'}
    weekday = days[str(datetime.datetime.today().weekday())]

    time1 = []
    try:
        a = stdf.hours[0][0]['open']
        b = a[datetime.datetime.today().weekday()]
        time = weekday + " : " + b['start'] + " to " + b['end']

    except:
        pass

    for i in range(len(stdf.hours)):
        try:
            a = stdf.hours[i][0]['open']
            b = a[datetime.datetime.today().weekday()]
            time = weekday + " : " + b['start'] + " to " + b['end'] 
            time1.append(time)

        except:
            time = "NAN"
            time1.append(time)

    dataname = stdf['name']
    dataphone = list(stdf['display_phone'])
    dataprice = list(stdf['price'])
    dataurl = list(stdf['url'])
    display = pd.DataFrame(list(zip(dataname,dataphone,time1,dataprice,addr,dataurl)), columns=['Restaurant Name', 'Contact', 'Open Hours', 'Price','Address','Restaurant URL'])

    return display

def display_on_pie(citydropdown, statedropdown):

    a = []

    df = pd.read_json("data/cuisine.json", lines=True)
    a = df.to_dict('records')

    df_rest = pd.read_json("data/"+citydropdown+", "+statedropdown+".json", lines=True)
    df_review = pd.read_json("data/"+citydropdown+", "+statedropdown+" reviews.json", lines=True) 
            
    output = pd.merge(df_rest, df_review, how='inner', on='id')
            
    lst1 = []
    lst2 = []

    for i in a:
        lst1.append(i["cuisine"])
        score = []
        for dish in i["food"]:
            
            for i in range (len(output)):          
                row = output.iloc[i]
                if (dish in output.keywords[i][0]):
                 
                    if row["TBscore"][0] != 0:
                        score.append(row["TBscore"][0])
                    else:
                        score.append(row["normalisedRating"][0])
                if (dish in output.keywords[i][1]):
               
                    if row["TBscore"][1] != 0:
                        score.append(row["TBscore"][1])
                    else:
                        score.append(row["normalisedRating"][1])
                if (dish in output.keywords[i][2]):
           
                    if row["TBscore"][2] != 0:
                        score.append(row["TBscore"][2])
                    else:
                        score.append(row["normalisedRating"][2])
                                 
        try:
            avg = sum(score) / len(score) 
            lst2.append(avg)
        except:
            lst2.append(0)
      
    df4 = pd.DataFrame()
    df4["cuisine"]=lst1
    df4["avg"]=lst2

    df4 = df4.sort_values('avg',ascending=False)
    main = df4.head(5)
    main['avg_final'] = round(main['avg'] / sum(main["avg"]) *100, 1)

    values = list(main['avg_final'])
    labels = list(main['cuisine'])

    return values,labels
        

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

prevf = "food"
prevc = "cuisine"
prevcity = "cities"
prevstate = "states"
count = 0 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
pd.options.mode.chained_assignment = None
restdf = pd.read_json('data/all.json', lines=True)
citylatlondf = pd.read_json('data/citylatlong.json', lines=True)
citydf = pd.read_json('data/cities.json', lines=True)
cuisinedf = pd.read_json('data/cuisine.json', lines=True)
fooddf = pd.read_json('data/food.json', lines=True)
latlondf = pd.read_csv('data/statelatlong.csv')
emptydf = pd.DataFrame()

code = {'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT',
        'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
        'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI',
        'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
        'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
        'Oregon': 'OR', 'Pennsylvania': 'PA', 'Texas': 'TX', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'}

site_lat = []
site_lon = []
locations_name = []

for i in range(len(restdf)):
    try:
    	a = restdf.coordinates[i]
    	temp = a['latitude']
    	site_lat.append(temp)
    	flag=True
    	a = restdf.coordinates[i]
    	temp = a['longitude']
    	site_lon.append(temp)
    	a = restdf.locations_name[i]
    	locations_name.append(a)           
    except:
    	pass

num_cities = []

for i in citydf['city']:
    for j in i:
        num_cities.append(j)

num_states = []
num_states = citydf['state']

num_cuisine = []
num_cuisine = cuisinedf["cuisine"]

num_food = []
num_food = fooddf["cuisine"]


data = [ 
    go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=dict(
            size=17,
            color='rgb(255, 0, 0)',
            opacity=0.7,
            symbol="restaurant"
        ),
        text = locations_name,
        hoverinfo='text',
    )
]

layout = go.Layout(
    autosize=True,
    #width=1300,
    height=800, 
    hovermode='closest', 
    mapbox=dict(accesstoken=mapbox_access_token, bearing=0, center=dict(lat=38, lon=-94), pitch=0, zoom=3.5, style='light')
)

fig = dict(data=data, layout=layout)


#=====================MAIN APP LAYOUT STARTS==================================

app.layout = html.Div(children=
                [
                    dcc.Graph(id='graph', figure=fig, style={'float':'right', 'width':'78%'}),

                    html.Div(id='tabs-content-inline'),

                    html.H1(children='YELP ME!', style={'float':'left'}),
                    html.Br(),
                    html.Br(),
                    
                    html.H6(children='Yelps to find the best restaurant...', style={'float':'left', 'width':'20%'}),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    
                    html.Div([
                        dcc.Dropdown(
                        id='statedropdown',
                        options=[{'label': i, 'value': code[i]} for i in num_states],
                        value='states',
                        placeholder="Select a State"
                        #style={'float':'left', 'width':'350px'}            
                        ),
                    ], style={'float':'left', 'width':'22%'}),
                    
                    
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    
                    html.Div([
                        dcc.Dropdown(
                            id='citydropdown',
                            options=[{'label': i, 'value': i} for i in num_cities],
                            #multi=True,
                            value='cities',
                            disabled=True,
                            placeholder="Select a City"                           
                        ),
                    ], style={'float':'left', 'width':'22%'}),

                    html.Br(),
                    html.Br(),
                    html.Br(),

                    html.Div([
                        dcc.Dropdown(
                            id='fooddropdown',
                            options=[{'label': i, 'value': i} for i in num_food],
                            value='food',
                            clearable=True,
                            disabled=True,
                            placeholder="When is your tummy hungry?",
                            
                        ),
                    ], style={'float':'left', 'width':'22%'}),       

                    html.Br(),
                    html.Br(),
                    html.Br(),

                    html.Div([
                        dcc.Dropdown(
                            id='cuisinedropdown',
                            options=[{'label': i, 'value': i} for i in num_cuisine],
                            value='cuisine',
                            clearable=True,
                            disabled=True,
                            placeholder="What would you like to eat?",
                        ),
                    ], style={'float':'left', 'width':'22%'}),

                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                               
                    html.Div(dcc.Slider(
                               id='slider',
                               min= 1,
                               max= 5,
                               value=5,
                               step=1,
                               disabled=True,
                               marks={
                                        1: {'label': '$'},
                                        2: {'label': '$$'},
                                        3: {'label': '$$$'},
                                        4: {'label': '$$$$'},
                                        5: {'label': '$$$$$'}
                                        
                                    },
                               vertical = False,
                               
                    ),style={'margin-left':'15px','height': '60px', 'width': '20%','display': 'inline-block','color':'red'}),

                    html.Div([
                        dcc.Graph(
                            id='piechart', config={'displaylogo':False, 'displayModeBar':False},
                            figure={'layout' : go.Layout(xaxis={'zeroline':False, 'showgrid':False, 'ticks':'', 'showticklabels':False}, yaxis={'zeroline':False, 'showgrid':False, 'ticks':'','showticklabels':False})}
                            )
                        ], style={'width': '20%', 'display': 'inline-block', 'float':'left'}),

                    html.Br(),
                    
                    html.Div([
                        dt.DataTable(
                            rows = emptydf.to_dict('records'),
                            editable=False,
                            selected_row_indices=[],
                            max_rows_in_viewport=10,
                            columns = emptydf.columns,
                            row_selectable=True,
                            filterable=False,
                            sortable=False,
                            id = "prod_table" 
                        )
                    ], style={'margin-left': 'auto','margin-right': 'auto' , "width":"100%", "display":"block", })
                ]
            )

#=====================MAIN APP LAYOUT ENDS==================================

############################ To update graph config ###################################

@app.callback(
    dash.dependencies.Output('graph', 'config'),
    [
     dash.dependencies.Input('statedropdown', 'value')
    ])

def update_static(statedropdown):
    if statedropdown != "states":
        return {'staticPlot':False}

############################ To update city dropdown ###################################

@app.callback(
    dash.dependencies.Output('citydropdown', 'options'),
    [
     dash.dependencies.Input('statedropdown', 'value')
    ])

def update_cities(statedropdown):
    if statedropdown != "states":
        return [{'label': i, 'value': i} for i in list(citydf.loc[citydf['code'] == statedropdown]['city'])[0]]


############################ To enable city dropdown ###################################

@app.callback(
    dash.dependencies.Output('citydropdown', 'disabled'),
    [
     dash.dependencies.Input('statedropdown', 'value')
    ])

def update_Disable(statedropdown):
    return False

############################ To enable cuisine dropdown ###################################

@app.callback(
    dash.dependencies.Output('cuisinedropdown', 'disabled'),
    [
     dash.dependencies.Input('statedropdown', 'options')
    ])

def update_cuisine(statedropdown):
    return False

# ############################ To enable food dropdown ###################################

@app.callback(
    dash.dependencies.Output('fooddropdown', 'disabled'),
    [
     dash.dependencies.Input('statedropdown', 'options')
    ])

def update_food(statedropdown):
    return False


########################### To enable the slider ###################################

@app.callback(
    dash.dependencies.Output('slider', 'disabled'),
    [
     dash.dependencies.Input('statedropdown', 'value')
    ])

def update_Disable(statedropdown):
    return False

############################ To render table Columns cuisine and food ###################################

@app.callback(
    dash.dependencies.Output('prod_table', 'columns'),
    [dash.dependencies.Input('slider', 'value'),
     dash.dependencies.Input('citydropdown', 'value'),
     dash.dependencies.Input('statedropdown', 'value'),
     dash.dependencies.Input('cuisinedropdown', 'value'),
     dash.dependencies.Input('fooddropdown', 'value')
    ])

def update_table_col(slider,citydropdown,statedropdown,cuisinedropdown,fooddropdown):
    
    try:
        if cuisinedropdown != "cuisine" or fooddropdown != "food":

            df_rest1 = pd.read_json("data/"+citydropdown+", "+statedropdown+".json", lines=True)
            df_review1 = pd.read_json("data/"+citydropdown+", "+statedropdown+" reviews.json", lines=True)
            global count

            if slider == 1:
                #count+=1
                df_price = df_rest1.loc[df_rest1['price'].isin(['$'])]
              
            elif slider == 2:
                #count+=1
                df_price = df_rest1.loc[df_rest1['price'].isin(['$','$$'])]

            elif slider == 3:
                #count+=1
                df_price = df_rest1.loc[df_rest1['price'].isin(['$','$$','$$$'])]
                
            elif slider == 4:
                #count+=1
                df_price = df_rest1.loc[df_rest1['price'].isin(['$','$$','$$$','$$$$'])]
                
            elif slider == 5:
                #count+=1
                df_price = df_rest1.loc[df_rest1['price'].isin(['$','$$','$$$','$$$$','$$$$$$'])]
        

            dfmain1 = filter_function(fooddropdown, cuisinedropdown, df_price, df_review1)
            printdf = dfmain1[['name','display_phone','url','price','cusine_rating']]
            printdf.rename(columns={'name':'Name','display_phone':'Contact','price':'Price','cusine_rating':'Rating','url':'Restaurant URL'}, inplace=True)
            return printdf.columns

    
        if citydropdown != "cities" and statedropdown!= "state":        
            display = displayOnTable(citydropdown, statedropdown)
            return display.columns

    except:
        pass


############################ To render table Rows cuisine and food ###################################

@app.callback(
    dash.dependencies.Output('prod_table', 'rows'),
    [dash.dependencies.Input('slider', 'value'),
     dash.dependencies.Input('citydropdown', 'value'),
     dash.dependencies.Input('statedropdown', 'value'),
     dash.dependencies.Input('cuisinedropdown', 'value'),
     dash.dependencies.Input('fooddropdown', 'value')
    ])

def update_table_row(slider,citydropdown,statedropdown,cuisinedropdown,fooddropdown):

    try:
        if cuisinedropdown != "cuisine" or fooddropdown != "food":
            df_rest1 = pd.read_json("data/"+citydropdown+", "+statedropdown+".json", lines=True)
            df_review1 = pd.read_json("data/"+citydropdown+", "+statedropdown+" reviews.json", lines=True)

            if slider == 1:
                df_price = df_rest1.loc[df_rest1['price'].isin(['$'])]
              
            elif slider == 2:
                df_price = df_rest1.loc[df_rest1['price'].isin(['$','$$'])]

            elif slider == 3:
                df_price = df_rest1.loc[df_rest1['price'].isin(['$','$$','$$$'])]
                
            elif slider == 4:
                df_price = df_rest1.loc[df_rest1['price'].isin(['$','$$','$$$','$$$$'])]
                
            elif slider == 5:
                df_price = df_rest1.loc[df_rest1['price'].isin(['$','$$','$$$','$$$$','$$$$$$'])]

            dfmain1 = filter_function(fooddropdown, cuisinedropdown, df_price, df_review1)
            printdf = dfmain1[['name','display_phone','url','price','cusine_rating']]
            printdf.rename(columns={'name':'Name','display_phone':'Contact','price':'Price','cusine_rating':'Rating','url':'Restaurant URL'}, inplace=True)
            return printdf.to_dict('records')
    except:
        pass
    
    try:
        if citydropdown != "cities" and statedropdown!= "state":        
            display = displayOnTable(citydropdown, statedropdown)
            return display.to_dict('records')
    except:
        pass


########################### On Click Map Changes #############################

@app.callback(
    Output('prod_table', 'selected_row_indices'),
    [Input('graph', 'clickData')],
    [State('prod_table', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices

########################### To display Pie chart #############################

@app.callback(
dash.dependencies.Output('piechart', 'figure'),
[dash.dependencies.Input('citydropdown', 'value'),
 dash.dependencies.Input('statedropdown', 'value')])

def display_content(citydropdown, statedropdown):

    try:    
        if(citydropdown!="cities" and statedropdown!="states"):
            values, labels = display_on_pie(citydropdown, statedropdown)
            piedata = go.Pie(labels = labels, values = values, hoverinfo='none')
            title = "Top Favoured 5 Dishes in " + citydropdown
            return {
                'data' : [piedata],
                'layout': {'title':title,'height':250,'margin': {'l': 5, 'b': 20, 'r': 10, 't': 30}}
            }
    except:
        pass

########################### To display the entire graph ###################################

@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [
     dash.dependencies.Input('statedropdown', 'value'),
     dash.dependencies.Input('citydropdown', 'value'),
     dash.dependencies.Input('cuisinedropdown', 'value'),
     dash.dependencies.Input('fooddropdown', 'value'),
     dash.dependencies.Input('slider', 'value'),
     dash.dependencies.Input('prod_table', 'selected_row_indices')
    ])

def update_graph(statedropdown, citydropdown, cuisinedropdown, fooddropdown, slider, prod_table):

    global prevstate

    if(prevstate != statedropdown):
        prevstate = statedropdown
        df1 = latlondf.loc[latlondf['State'] == statedropdown]
        df_lat = float(df1['Latitude'])
        df_lon = float(df1['Longitude'])
        return {
                'data': [ 
                    go.Scattermapbox(
                        lat=site_lat,
                        lon=site_lon,
                        mode='markers',
                        marker=dict(
                            size=17,
                            color='rgb(255, 0, 0)',
                            opacity=0.7,
                            symbol="restaurant"
                        ),
                        text = locations_name,
                        hoverinfo='text',
                    )
                ],

                'layout': go.Layout(
                        title='<b>Restaurant Map</b>',
                        autosize=True,
                        #width=1300,
                        height=800, 
                        hovermode='closest', 
                        mapbox=dict(accesstoken=mapbox_access_token, bearing=0, center=dict(lat=df_lat, lon=df_lon), pitch=0, zoom=6.5, style='light')
                )

            }


    if statedropdown != "states":
    	prevstate = statedropdown
    	df1 = latlondf.loc[latlondf['State'] == statedropdown]
    	df_lat = float(df1['Latitude'])
    	df_lon = float(df1['Longitude'])
    	global prevcity
    	print("######",citydropdown)
    	print("###############",prevcity)

    	if citydropdown != "cities": #and prevcity != citydropdown:  

    		print(statedropdown, citydropdown, cuisinedropdown, fooddropdown)       
    		df2 = citylatlondf.loc[citylatlondf['city'] == citydropdown]
    		df2_lat = float(df2['Latitude'])
    		df2_lon = float(df2['Longitude'])
    		
    		df_rest = pd.read_json("data/"+citydropdown+", "+statedropdown+".json", lines=True)
    		df_review = pd.read_json("data/"+citydropdown+", "+statedropdown+" reviews.json", lines=True)

    		print("============",cuisinedropdown)

    		if fooddropdown != "food" or cuisinedropdown != "cuisine":

    			if slider == 1:
    				df_price = df_rest.loc[df_rest['price'].isin(['$'])]

    			elif slider == 2:
    				df_price = df_rest.loc[df_rest['price'].isin(['$','$$'])]

    			elif slider == 3:
    				df_price = df_rest.loc[df_rest['price'].isin(['$','$$','$$$'])]

    			elif slider == 4:
    				df_price = df_rest.loc[df_rest['price'].isin(['$','$$','$$$','$$$$'])]

    			elif slider == 5:
    				df_price = df_rest.loc[df_rest['price'].isin(['$','$$','$$$','$$$$','$$$$$$'])]


    			df = filter_function(fooddropdown, cuisinedropdown, df_price, df_review)
    			df_restlat = []
    			df_restlon = []
    			rest_names = []

    			df.to_json("data/temp.json", orient='records', lines=True)
    			df_temp = pd.read_json("data/temp.json", lines=True, typ='series')

    			for i in df_temp:
    				try:
    					j = i['coordinates']
    					df_restlat.append(float(j['latitude']))
    					df_restlon.append(float(j['longitude']))
    					rest_names.append(i['name'])
    				except:
    					pass

    			marker = {'color': ['#0074D9']*len(df)}
    			for i in (prod_table or []):
    				marker['color'][i] = '#d90007'

    			if('#d90007' in marker['color']):
    				name = 'Selected Restaurants'
    			else:
    				name = 'Available Restaurants'

    			return {
                    'data': [ 
                        go.Scattermapbox(
                            lat=df_restlat,
                            lon=df_restlon,
                            mode='markers',
                            name=name,
                            marker=dict(
                                size=17,
                                color=marker['color'],
                                opacity=0.7,
                                symbol="circle"
                            ),
                            text = rest_names,
                            hoverinfo='text',
                        )
                    ],

                    'layout': go.Layout(
                            title='<b>Restaurant Map</b>',
                            #legend={'Available Restaurants':'#0074D9', 'Selected Restaurants':'#d90007'},
                            #showlegend=True,
                            autosize=True,
                            #width=1300,
                            height=800, 
                            hovermode='closest', 
                            mapbox=dict(accesstoken=mapbox_access_token, bearing=0, center=dict(lat=df2_lat, lon=df2_lon), pitch=0, zoom=10.3, style='light')
                    )

                }


    		else:
    			df_restlat = []
    			df_restlon = []
    			rest_names = []
    			df_rest = pd.read_json("data/"+citydropdown+", "+statedropdown+".json", lines=True, typ='series')

    			for i in df_rest:
    				try:
    					j = i['coordinates']
    					df_restlat.append(float(j['latitude']))
    					df_restlon.append(float(j['longitude']))
    					rest_names.append(i['name'])
    				except:
    					pass

    			return {
                    'data': [ 
                        go.Scattermapbox(
                            lat=df_restlat,
                            lon=df_restlon,
                            mode='markers',
                            marker=dict(
                                size=17,
                                color='rgb(255, 0, 0)',
                                opacity=0.7,
                                symbol="restaurant"
                            ),
                            text = rest_names,
                            hoverinfo='text',
                        )
                    ],

                    'layout': go.Layout(
                            title='<b>Restaurant Map</b>',
                            autosize=True,
                            #width=1300,
                            height=800, 
                            hovermode='closest', 
                            mapbox=dict(accesstoken=mapbox_access_token, bearing=0, center=dict(lat=df2_lat, lon=df2_lon), pitch=0, zoom=12, style='light')
                    )

                }


    	else:

            return {
                'data': [ 
                    go.Scattermapbox(
                        lat=site_lat,
                        lon=site_lon,
                        mode='markers',
                        marker=dict(
                            size=17,
                            color='rgb(255, 0, 0)',
                            opacity=0.7,
                            symbol="restaurant"
                        ),
                        text = locations_name,
                        hoverinfo='text',
                    )
                ],

                'layout': go.Layout(
                        title='<b>Restaurant Map</b>',
                        autosize=True,
                        #width=1300,
                        height=800, 
                        hovermode='closest', 
                        mapbox=dict(accesstoken=mapbox_access_token, bearing=0, center=dict(lat=df_lat, lon=df_lon), pitch=0, zoom=6.5, style='light')
                )

            }


if __name__ == '__main__':
    app.run_server(debug=True)