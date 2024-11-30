import requests
import json
import base64
import webbrowser
import urllib.parse
import secrets
import hashlib
import base64
import time
from time import sleep
# Your Twitter API credentials
access_key = ''
access_key_secret = ''

client_id = ''
client_secret = ''

base64_credentials = base64.b64encode(f"{client_id}:{client_secret}".encode('ascii')).decode('ascii')



def get_v2_access_token(client_id,client_secret):
    
    auth_url = "https://api.twitter.com/2/oauth2/token"
    
    headers = {
        "Authorization": f"Basic {base64_credentials}",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "User-Agent":
    }
    data = {
    "grant_type": "client_credentials",
    "client_secret": client_secret,
    "client_type": 'third_party_app',
    "scope": ['tweet.read', 'tweet.write', 'users.read','users.write']
}


    # Step 3: Send the request
    response = requests.post(auth_url, headers=headers, data=data)
    
    # Step 4: Handle the response
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")
        print("Access token acquireed successfully")
    else:
        print(f"Failed to obtain token. Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    
    return access_token
    
   
def search_tweets(query,bearer_token):
    url = "https://api.twitter.com/2/tweets/search/recent"
    
    headers = {"Authorization": f"Bearer {bearer_token}"}
    params = {
        "query": query,
        "max_results": 100  # Maximum tweets to fetch in one request
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None

def delete_tweet(tweet_id,user_id,  access_token):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets/{tweet_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
      
    }
    
    response = requests.delete(url, headers=headers)
    if response.status_code in [200, 204]:
        print(f"Tweet {tweet_id} deleted successfully")
        sleep(5)
    else:
        print(f"Failed to delete tweet {tweet_id}. Status code: {response.status_code}")
        print(response.text)


def get_user_id(username, bearer_token):
    """
    Fetches the user ID for a given Twitter username.

    :param username: The Twitter username (e.g., 'twitterdev')
    :param access_token: The Bearer token for API authentication
    :return: The user ID if successful, None otherwise
    """
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
        
    }

    try:
        response = requests.get(url, headers=headers)
  

        # If the request was successful, parse JSON
        user_data = response.json()
        
        return  user_data
    except:
            print("User data not found in the response.")
            return None
   



username = input("What is your Twitter username?:\n")
word = input("What tweets including the word would you like to delete?:\n\n")
query = f"{word} from:{username}"
bearer_token = 'Your bearer Token'


def main():
    counter = 0 
    access_token =  get_v2_access_token(client_id,client_secret)
    
   
    tweets = search_tweets(query,bearer_token)
    if tweets and 'data' in tweets:
        for tweet in tweets['data']:
            delete_tweet(tweet['id'], user_id, access_token)
            counter +=1
    
        print(f"you have deleted {counter} tweets containing the word {word}")   



main()         
