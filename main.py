import json
import requests
import logging
from anime_class import Anime
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO)

def main():
    #Selectors from the browse page
    animes_link_selector = "#headerDIV_2 > div > div > a:nth-child(2)"
    next_page_selector = ".nextpostslink"

    starting_url = "" #Removed for website's safety
    
    animes = []
    try:
        with requests.Session() as session:
            current_url = starting_url    
            while True:
                #Get page response
                logging.info(f"Getting animes urls from: {current_url}")
                response = session.get(current_url)
                bs = BeautifulSoup(response.text, 'html5lib')

                #Get all animes urls
                for anime_url in map(lambda x: x.attrs['href'], bs.select(animes_link_selector)):
                    anime = Anime(anime_url, session)
                    anime.get_data_from_page()
                    logging.info(f"Successfuly got {anime.anime_name} data.")

                    animes.append(anime)
                
                #Getting the next page link
                next_page_elem = bs.select_one(next_page_selector)
                if next_page_elem:
                    current_url = next_page_elem.attrs['href']
                else:
                    logging.info("Done.")
                    break

    except KeyboardInterrupt:
        logging.info("Stopped by the user")
    finally:
        #Making sure the data will be saved
        with open("animes_data.json", 'w+') as file:
            animes_dict = [anime.get_data_as_dict() for anime in animes]
            json.dump(animes_dict, file, indent=4)


if __name__ == "__main__":
    main()