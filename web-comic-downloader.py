"""
Finds the URL of the latest webcomic and sends a request to Home Assistant Downloader
component to save the image.

"""

import re                           # Regular expresssion object. Let's us search using wildcards
import requests                     # Sends HTTP request to website and saves the data
from bs4 import BeautifulSoup       # Parses the HTML data into a Python object

def pullWebComic(url, filename):
    # Get website data
    user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=user_agent)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Find any tags with id='comic'
    comic = soup.find_all(id=re.compile("comic"))
    print("Comic: \n", comic)
    imgFound = False
    
    # While image is not found, or image is null
    while imgFound == False:     
        # Go through each tag labeled as 'comic':
        for c in comic:
        # Check if comic <img> tag is found in first attempt           
            try:
                
                print("if c['src'] is True:")
                print("c['src'] == ", c['src'])
                if c['src'][0:4] == 'http':                            # Check for full URL
                    print("Full URL provided.")
                    print(c['src'])
                    imgFound = True
                else:                                                   # Assuming it is a partial URL
                    full_url = url + c['src']      
                    print("Partial URL provided.")
                    print('full URL: %s' % full_url)
                    imgFound = True
            except:
                print("Error found. c['src'] does not exist")
                
                # Continue looking for img tags in the child            
            image = c.find_all('img')
            
                # if image is None, or there's nothing in the image object, search for another "comic" tag
            try:
                # image is found, so get the URL
                print("image:\n", image)
                for i in image:
                    if i['src'][0:4] == 'http':                            # Check for full URL
                        print("Full URL provided.")
                        print(i['src'])
                        imgFound = True
                    else:                                                   # Assuming it is a partial URL
                        full_url = url + i['src']      
                        print("Partial URL provided.")
                        print('full URL: %s' % full_url)
                        imgFound = True                              
            except:       
                    # if img tag not found, then find the next div id = comic in child and start loop again
                comic = comic.find_all(id=re.compile("comic"))    

    
#    


# The code below will execute if it is not an imported module
if __name__ == '__main__':    
    nedroid_url = 'http://nedroid.com'
    awkward_url = 'http://awkwardzombie.com/index.php?page=0'
    lovenstein_url = 'http://www.mrlovenstein.com'
    pennyarcade_url = 'https://www.penny-arcade.com/comic'

    pullWebComic(nedroid_url, 'nedroid.png')
    pullWebComic(awkward_url, 'awkward.png')
    pullWebComic(pennyarcade_url, 'pennyarcade.png')
    pullWebComic(lovenstein_url, 'lovenstein.png')

exit()
