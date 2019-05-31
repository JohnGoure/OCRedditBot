from twython import Twython, TwythonStreamer
import json
import pandas as pd
import csv
from geopy.geocoders import Nominatim  
import gmplot


with open('twitter_credentials.json', 'r') as file:
    creds = json.load(file)

def process_tweet(tweet):
    """Filter out unwanted data."""
    d = {}
    d['hastags'] = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
    d['text'] = tweet['text']
    d['user'] = tweet['user']['screen_name']
    d['user_loc'] = tweet['user']['location']
    return d

class MyStreamer(TwythonStreamer):
    """Create a class that inherits TwythonStreamer"""
    
    def on_success(self, data):
        if data['lang'] == 'en':
            tweet_data = process_tweet(data)
            self.save_to_csv(tweet_data)
    
    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()
        
    def save_to_csv(self, tweet):
        with open(r'saved_tweets.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(list(tweet.values()))

stream = MyStreamer(
    creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],
    creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])

stream.statuses.filter(track='python')

geolocator = Nominatim()

# Go through all tweets and add locations to 'coordinates' dictionary
coordinates = {'latitude': [], 'longitude': []}  
for count, user_loc in enumerate(tweets.location):  
    try:
        location = geolocator.geocode(user_loc)

        # If coordinates are found for location
        if location:
            coordinates['latitude'].append(location.latitude)
            coordinates['longitude'].append(location.longitude)

    # If too many connection requests
    except:
        pass

# Instantiate and center a GoogleMapPlotter object to show our map
gmap = gmplot.GoogleMapPlotter(30, 0, 3)

# Insert points on the map passing a list of latitudes and longitudes
gmap.heatmap(coordinates['latitude'], coordinates['longitude'], radius=20)

# Save the map to html file
gmap.draw("python_heatmap.html")
