import requests
from config import API, ASSETS

class SuperViveAPI():

    def __init__(self):
        self.session = requests.Session()
        
    def statistics(self, gamemode, sort=None, order=None):
        url = f"{API}/statistics/{gamemode}.json"
        params = {}
        if sort:
            params['sort'] = sort
        if order:
            params['order'] = order
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
        

    def search(self, query):
        url = f"{API}/search"
        params = {"query": query}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_player_stats(self, player_id):
        url = f"{API}/player/{player_id}.json"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_hero_images(self, hero):
        image_url = f"{ASSETS}/images/{hero}.webp"
        return image_url
import requests
from config import API, ASSETS

class SuperViveAPI():

    def __init__(self):
        self.session = requests.Session()
        
    def statistics(self, gamemode, sort=None, order=None):
        url = f"{API}/statistics/{gamemode}.json"
        params = {}
        if sort:
            params['sort'] = sort
        if order:
            params['order'] = order
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
        

    def search(self, query):
        url = f"{API}/search"
        params = {"query": query}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_player_stats(self, player_id):
        url = f"{API}/player/{player_id}.json"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_hero_images(self, hero):
        image_url = f"{ASSETS}/images/{hero}.webp"
        return image_url