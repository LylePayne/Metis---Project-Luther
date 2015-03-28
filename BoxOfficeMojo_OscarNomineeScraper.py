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

# ---SCRAPE URLS FROM OSCAR BOMOJO PAGE--- #

##uses Beautiful Soup to Scrape Oscar Pages
def get_url_from_oscarlist(urlname):
    page = urllib2.urlopen(urlname)
    soup_name = BeautifulSoup(page)
    
    movie_url_list = []
    for link in soup_name.find_all('a', href=re.compile('oscar/movies')):
    	##Creates proper URLS for use later
        one_year_movies = ("http://boxofficemojo.com" + link.get('href').split('/oscar')[1]+"&adjust_yr=2015&p=.htm")
        movie_url_list.append(one_year_movies)
    return movie_url_list







