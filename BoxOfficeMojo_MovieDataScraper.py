import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib2
from bs4 import BeautifulSoup
import re
import dateutil.parser
import pprint as pp
import pickle
from datetime import datetime
import time
import random

# ---FUNCTIONS USED WITHIN SCRAPER TO CLEAN DATA--- #

##looks for field_names and then finds the sibling
##which is the value associated with a given label
def get_movie_value(soup, field_name):
    obj = soup.find(text=re.compile(field_name))
    if not obj:
        return None
    
    next_sibling = obj.findNextSibling()
    ##identifies the sibling, which is the next attribute
    if next_sibling:
        return next_sibling.text
    else:
        return None

##function to clean the raw_release_date
def to_date(datestring):
    date = dateutil.parser.parse(datestring)
    return date

##function to clean the money value and take out the commas and $$
def money_to_int(moneystring):
    moneystring = moneystring.replace('$', '').replace(',', '')
    return int(moneystring)


# ---FUNCTION TO SCRAPE MOVIE DATA FROM INDIVIDUAL MOVIE PAGE--- #

#Create function to pull out relevant information from URL
def find_movie_data(urlname):
    try:
        page = urllib2.urlopen(urlname)
    except:
        return None
    else:
        soup_name = BeautifulSoup(page)
    
         ##pulls out release date for years after 1998
        for release_date in soup_name:
            try:
                raw_release = get_movie_value(soup_name, 'Release Date')
            except:
                print 'WARNING: release date not found!'
                return None
            try:
                release = to_date(raw_release)
            except:
                print 'WARNING: converted date not working!'
                return None
            if release.year <=1998: 
                return None
        
        ##pulls out title
        for title in soup_name:
            try:
                title_string = soup_name.find('title').text
                title = title_string.split('(')[0].strip()
            except:
                return None
    
        ##pulls out Domestic Total
        for dtg in soup_name:
            raw_domestic_total_gross = get_movie_value(soup_name, 'Domestic Total')
            if not raw_domestic_total_gross:
                domestic_total_gross = np.nan
            else:
                domestic_total_gross = money_to_int(raw_domestic_total_gross)
            
        ##pulls out Distributor Name
        for distributor in soup_name:
            try:
                dist_comp = get_movie_value(soup_name, 'Distributor')
            except:
                return None
        
        ##pulls out movie ratings
        for movie_rating in soup_name:
            try:
                rating = get_movie_value(soup_name, 'MPAA Rating')
            except:
                return None
        
        ##pulls out movie genre
        for movie_genre in soup_name:
            try:
                genre = get_movie_value(soup_name, 'Genre:')
            except:
                return None
        
        ##pulls out Production Budget; cleans out "million"
        for production_budget in soup_name:
            try:
                raw_prod_bud = get_movie_value(soup_name, 'Production Budget')
            except:
                None
            if raw_prod_bud == ('N/A'):
                prod_bud = np.nan
            else:
                prod_bud = raw_prod_bud.replace('$', '').replace(' million', '')
        
        #returns tuple for each movie with relevant data
        return (title, domestic_total_gross, dist_comp, rating, genre, prod_bud, release)

# ---FUNCTION TO ITERATE THROUGH A LIST OF URLS AND PULL OUT MOVIE DATA--- #


#iterate_through_url_list(oscar2013)
def iterate_through_url_list(lst):
    data_list = []
    for count, title_url in enumerate(lst):
        #added sleep so site wouldn't shut down due to too many pings
        time.sleep(3)
        #pickled file after every pull to save scraped information
        with open("data_list_4.pkl", "w") as picklefile:
            pickle.dump(data_list, picklefile)
        movie_data = find_movie_data(title_url)
        if movie_data: 
            data_list.append(movie_data)
        else:
            continue
        if count % 50 ==0:
            time.sleep(5)
            print 'Processing Next 50'
    return data_list
