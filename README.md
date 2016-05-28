# Tilt-o-meter
Small web app that shows the measurement of a LOL's player level of tilt


### Installation

* Clone the repo:

`git clone https://github.com/patillacode/tilt-o-meter.git`

* Move into the repo folder:

`cd tilt-o-meter`

* Create a virtual environment ([mkvirtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)):

```mkvirtualenv tiltometer```

* Activate the virtualenv:
```workon tiltometer```

* Install requirements:

    * `pip install -r requirements.txt`
    * Remember to create `src/keys.py` file and write the following line: `API_KEY="YOUR_RIOT_GAMES_API_KEY"`
    * You can grab your API KEY [here](https://developer.riotgames.com/)

* _You are ready to execute the code!_

------------

### Usage
* Run `python application.py`
* go to `localhost:8080/` in your browser

------------

### Demo
[Live Demo](http://tilt-o-meter.patilla.es/)

------------

### Attribution ###
-------------------
I use [Flask](https://github.com/pallets/flask) as a python web framework - Thanks to [pallets](https://github.com/pallets/) and all who collaborated.

I use [RiotWatcher](https://github.com/pseudonym117/Riot-Watcher) as a python wrapper for [Riot's API](developer.riotgames.com) - Thanks to [pseudonym117](https://github.com/pseudonym117) and all who collaborated.

I use [JustGage](https://github.com/toorshia/justgage) for the visualizations -  Thanks to [toorshia](https://github.com/toorshia) and all who collaborated.


Tilt-o-meter isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
