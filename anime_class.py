from bs4 import BeautifulSoup
from PIL import Image
import requests
import re

class Anime:
    
    def __init__(self, url, session):
        self.url = url
        self.session = session
        
        self.anime_name = ""
        self.api_anime_name = ""
        self.anime_image = ""
        self.episode_count = 0
        self.episodes = []
        
    def get_data_from_page(self):
        # Page selectors
        name_selector = ".single-anime-desktop"
        image_selector = ".cover > img"
        episode_selector = ".episodes > li > a"  
        
        # Get response and parsing the page response
        response = self.session.get(self.url)        
        bs = BeautifulSoup(response.text, 'html5lib')
        
        # Finnally filling the data
        self.anime_name = bs.select_one(name_selector).get_text()
        self.api_anime_name = self.anime_name
        self.anime_image = bs.select_one(image_selector).attrs['src']
        self.anime_image = "https://4anime.to" + self.anime_image

         # Remove all non-word characters (everything except numbers and letters)
        self.api_anime_name = re.sub(r"[^\w\s]", '', self.api_anime_name)

        # Replace all runs of whitespace with a single dash
        self.api_anime_name = re.sub(r"\s+", '-', self.api_anime_name)

        img = Image.open(requests.get(self.anime_image, stream=True).raw)
        
        img.save("C:/Users/12145/Desktop/4anime-Scraper-master/ScrapedImages/" + self.api_anime_name + ".jpg")
        episodes_url = [episode.attrs['href'] for episode in bs.select(episode_selector)]
        for url in episodes_url:
            self.episodes.append(self._get_episodes_video_src(url))
        
        self.episode_count = len(self.episodes)
        
    def get_data_as_dict(self):
        return {
            "anime_name": self.anime_name,
            "api_anime_name": self.api_anime_name,
            "anime_image": self.anime_image,
            "episode_count": self.episode_count,
            "episodes": self.episodes
        }
    
    def _get_episodes_video_src(self, episode_url):        
        video_selector = "video source"
        
        # Get response and parsing the page response
        response = self.session.get(episode_url)        
        bs = BeautifulSoup(response.text, 'html5lib')
        
        return bs.select_one(video_selector).attrs['src']