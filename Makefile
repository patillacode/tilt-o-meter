install: python-install

python-install:
	python3 -m venv venv && \
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt

serve:
	. venv/bin/activate && \
	FLASK_APP=flaskr FLASK_ENV=development \
	APP_SETTINGS=flaskr.config.DevelopmentConfig \
	flask run --extra-files flaskr/templates/base.html:flaskr/templates/index.html:flaskr/utils.py:flaskr/static/css/tiltometer.css:flaskr/static/js/tiltometer.js

shell:
	. venv/bin/activate && \
	ipython
