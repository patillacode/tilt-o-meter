install: python-install
full-reset: repo-pull riot-key-reset docker-reset

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

docker-reset:
	echo "Stopping container..." && \
	docker stop tilt-o-meter && \
	echo "Deleting container..." && \
	docker rm tilt-o-meter && \
	echo "Deleting image..." && \
	docker rmi tilt-o-meter && \
	echo "Rebuilding image..." && \
	docker build --tag tilt-o-meter . && \
	echo "Running new image in new container..." && \
	docker run -d --name tilt-o-meter --publish 5051:5051 tilt-o-meter && \
	echo "Set restart on failure..." && \
	docker update --restart=on-failure tilt-o-meter

riot-key-reset:
	@read -p "Enter new API Key: " key; \
	echo "RIOT_API_KEY = \"$$key\"" > flaskr/secrets.py

repo-pull:
	git pull origin master
