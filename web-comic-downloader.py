"""
Finds the URL of the latest webcomic and sends a request to Home Assistant Downloader
component to save the image.

"""

import re                           # Regular expresssion object. Allows search using wildcards
import requests                     # Sends HTTP request to website and saves the data
from bs4 import BeautifulSoup       # Parses the HTML data into a Python object


def checkURL(url):
    """ Checks if URL is complete, then returns URL"""
    print("url: ", url[0:4])
    try:
        if url[0:4] == 'http':                            # Check for full URL
            print("Full URL provided.")
            print(c['src'])
            return c['src']
        else:
            full_url = url + c['src']      
            print("Partial URL provided.")
            print('full URL: %s' % full_url)
            return full_url                          
    except:
        print("Error found. c['src'] does not exist")
        return None
                

def pullWebComic(url, filename):
    # Get website data
    user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=user_agent)
    soup = BeautifulSoup(r.text, 'html.parser')
    image = None
    # Find any tags with id='comic'
    
    
    image_found = False
    need_image = (image is None)         # Should default to true, need an image! Write a true statement, like variable is empty
    
    if need_image:
        comic = soup.find_all(id=re.compile("comic"))
        print("Comic: \n", comic)
        for c in comic:
            print("c['src'] = ", c['src'])
            image = checkURL(c['src'])           
            if image is None:                  
                img = c.find_all('img')
                for i in img:
                    print("i['src'] = ", i['src'])
                    image = checkURL(i['src'])
            else: break
                # if img tag not found, then find the next div id = comic in child and start loop again
            if image is None:
                comic = comic.find_all(id=re.compile("comic"))
            else: break

    
#    


# The code below will execute if it is not an imported module
if __name__ == '__main__':    
    nedroid_url = 'http://nedroid.com'
    awkward_url = 'http://awkwardzombie.com/index.php?page=0'
    lovenstein_url = 'http://www.mrlovenstein.com'
    pennyarcade_url = 'https://www.penny-arcade.com/comic'

#    pullWebComic(nedroid_url, 'nedroid.png')
#    pullWebComic(awkward_url, 'awkward.png')
#    pullWebComic(pennyarcade_url, 'pennyarcade.png')
    pullWebComic(lovenstein_url, 'lovenstein.png')

    exit()
