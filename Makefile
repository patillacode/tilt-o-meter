install: python-install

python-install:
	python3 -m venv venv && \
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt && \
	cp flaskr/secrets.sample.py flaskr/secrets.py && \
	echo "App is installed. Run 'make serve' to run the server."
	echo "Remember to set Riot's API Key in flaskr/secrets.py !"

serve:
	. venv/bin/activate && \
	FLASK_APP=flaskr FLASK_ENV=development \
	APP_SETTINGS=flaskr.config.DevelopmentConfig \
	flask run --extra-files flaskr/templates/base.html:flaskr/templates/index.html:flaskr/utils.py:flaskr/static/css/tiltometer.css:flaskr/static/js/tiltometer.js

shell:
	. venv/bin/activate && \
	ipython
