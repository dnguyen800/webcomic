"""
Home Assistant sensor that searches through the URL of a webcomic site and finds the image URL of the comic.
The image URL can then be used in a Lovelace card like Useful-Markdown to show the latest webcomic.

For more details, go here:
https://github.com/dnguyen800/Web-Comic-Downloader

Instagram Scraper is from meetmangukiya.
https://github.com/meetmangukiya/instagram-scraper
"""
from datetime import timedelta
import logging
import voluptuous as vol



from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA

import re                           
 
          

__version__ = '0.0.2'
_LOGGER = logging.getLogger(__name__)


CONF_NAME = 'name'
CONF_URL = 'url'
CONF_REFRESH = 'refresh'
CONF_SOURCE = 'source'
CONF_IG_USER = 'ig_user'

DEFAULT_REFRESH = 360
DEFAULT_SOURCE = 'source'
DEFAULT_URL = 'url'
DEFAULT_IG_USER = 'ig_user'
ATTR_COMIC_URL = 'url'
# Source: http://blog.jstassen.com/2016/03/code-regex-for-instagram-username-and-hashtags/
REGEXES = {
    'hashtag': re.compile('(?:#)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)'),
    'username': re.compile('(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)'),
}




SCAN_INTERVAL = timedelta(hours=8)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
    vol.Optional(CONF_URL,
                 default=DEFAULT_URL): cv.string,
    vol.Optional(CONF_SOURCE,
                 default=DEFAULT_SOURCE): cv.string,
    vol.Optional(CONF_IG_USER,
                 default=DEFAULT_IG_USER): cv.string,
    vol.Optional(CONF_REFRESH,
                 default=DEFAULT_REFRESH): cv.positive_int,
})

DOMAIN = 'webcomic'

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    add_devices([ComicSensor(hass, config)])
    

class ComicSensor(Entity):
    """Representation of a Sensor."""
    def __init__(self, hass, config):
        """Initialize the sensor and variables."""      
        self._name = config[CONF_NAME]
        self._url = config[CONF_URL]
        self._state = None
        self._comic_url = None
        self._source = config[CONF_SOURCE]
        self._ig_user = config[CONF_IG_USER]
        self.update()


    def check_url(self, c):
        """Checks URL for issues, such as incomplete URLs, or whitespaces"""
        try:
            if c['src'][0:4] == 'http':      
                self._state = "URL found"                                   
                return c['src'].replace(" ", "%20")
            else:           
                self._state = "URL found"           
                return (self._url + c['src']).replace(" ", "%20")
        except:
            self._state = None
            return None



    def scrape_url(self, url):
        """
        Scrape generic comic websites for HTML tags labeled as 'comic'
        """
        import requests
        from bs4 import BeautifulSoup 

        user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        r = requests.get(url, headers=user_agent)
        soup = BeautifulSoup(r.text, 'html.parser')
        comic = soup.find_all(id=re.compile("comic"))
        url_found = ''
        for c in comic:
            url_found = self.check_url(c)
            if self._state is None:
                for i in c.find_all('img'):
                    url_found = self.check_url(i)
        return url_found

    def scrape_instagram_user(self, user):
        """
        Taken from:
        https://stackoverflow.com/questions/50058208/how-do-i-scrape-a-full-instagram-page-in-python
        """
        import json
        import requests
        from bs4 import BeautifulSoup
        import sys

        url = "https://www.instagram.com/{}/".format(user)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')

        script = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
        page_json = script.text.split(' = ', 1)[1].rstrip(';')
        data = json.loads(page_json)
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

        for post in data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
            image_src = post['node']['display_url']
            self._state = "URL found"
            return image_src
                    
    def update(self):
        """Fetch new state data for the sensor.
        """
        if self._source.lower() == 'instagram':
            self._comic_url = self.scrape_instagram_user(self._ig_user)
        else:
            self._comic_url = self.scrape_url(self._url)



    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def url(self):
        return self._url

    @property
    def comic_url(self):
        return self._comic_url


    @property
    def source(self):
        return self._source


    @property
    def ig_user(self):
        return self._ig_user
    
    
    @property
    def device_state_attributes(self):
        """Return the state attributes"""      
        return{ATTR_COMIC_URL: self._comic_url}
