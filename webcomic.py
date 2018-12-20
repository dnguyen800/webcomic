"""

Example from:
https://developers.home-assistant.io/docs/en/creating_platform_example_sensor.html

"""
from datetime import timedelta
import logging
import voluptuous as vol

from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA

REQUIREMENTS = ['requests', 'bs4']         # Python libraries or modules needed for this sensor
# DEPENDENCIES = ['mqtt']   # Other Home Assistant Components needed for this sensor to work.

__version__ = '0.0.1'
_LOGGER = logging.getLogger(__name__)


# CONF_VARIABLE_NAME = 'variable_name_listed_in_configuration_yaml'
CONF_NAME = 'name'
CONF_URL = 'url'
CONF_REFRESH = 'refresh'

DEFAULT_REFRESH = 360


SCAN_INTERVAL = timedelta(minutes=360)

# Validate the sensor's user-defined configuration specified in configuration.yaml
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_URL): cv.string,
    vol.Optional(CONF_REFRESH,
                 default=DEFAULT_REFRESH): cv.positive_int,
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    _LOGGER.info("setup_platform called for Webcomic")   
    add_devices([ComicSensor(hass, config)])


class ComicSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass, config):
        """Initialize the sensor and variables."""
        self._state = None
        self._name = config[CONF_NAME]
        self._url = config[CONF_URL]
        # This is where the comic URL data will be stored.
        self.hass.data[self._name] = {}
        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state


    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = 23
