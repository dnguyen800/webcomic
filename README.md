# Web Comic Sensor
![header](images/header.png)

A Home Assistant sensor that pulls the URL of webcomic image, given the webcomic URL. I tested on a few webcomics (Penny Arcade, Mr. Lovenstein, Awkward Zombie) and they work. Compatibility is on a case-by-case basis, as every website has different ways of labeling their images in HTML.

Use with [Useful Markdown Card](https://github.com/thomasloven/lovelace-useful-markdown-card) to display the webcomic in a Lovelace card.

## Features
  - Instagram scraping added. Type in name of the Instagram user in the configuration to pull the latest posted IG photo.

## Options

| Name | Type | Default | Description
| ---- | ---- | ------- | -----------
| name | string | **Required** | Name of the webcomic, such as `Awkward Zombie`.
| source | strong | **Required** | Two options, 'url' or 'instagram'. This is where the webcomic is hosted.
| url | string | Optional | The URL of the webcomic, such as http://www.awkwardzombie.com/
| ig_user | string | Optional | Type in the Instagram user name of the web comic. For example, 'system32comics'.

## Instructions
1. Download the [Webcomic Sensor](https://raw.githubusercontent.com/dnguyen800/Webcomic-Sensor/master/webcomic.py).
4. Place the `webcomic.py` file in your `config/custom_components/sensor` folder.
5. Include one of the following sensors in your `configuration.yaml`
```yaml
- platform: webcomic
  name: "Awkward Zombie"
  source: url
  url: "http://www.awkwardzombie.com/"
  
- platform: webcomic
  name: "System32 Comics"
  source: instagram
  ig_user: system32comics  
```

6. Restart Home Assistant to load the sensor.
7. Check `Home Assistant >> Developer Tools >> States` to see if the sensor loaded correctly.
8. If the sensor state is `URL found` and the URL attribute is defined, then the webcomic URL was identified (hopefully).
8. Download [Useful Markdown Card](https://github.com/thomasloven/lovelace-useful-markdown-card) and install per instructions.
9. Add a `useful-markdown-card` in Lovelace and load the webcomic using the example below. 
```yaml
- type: custom:useful-markdown-card
  content: >
    ![awkward]([[ sensor.awkward_zombie.attributes.url ]])
- type: custom:useful-markdown-card
  content: >
    ![system32]([[ sensor.system32_comics.attributes.url ]])      
```

## Support
I am studying Python as a hobby and this is my first public project. Some fixes/requests may be out of my scope but I'll try my best. I hope you find it useful!

## Credits
  - [Useful Markdown Card](https://github.com/thomasloven/lovelace-useful-markdown-card) - To display the comic in a Lovelace card. 
