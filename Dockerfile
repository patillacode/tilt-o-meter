FROM python:3.8-slim-buster

RUN mkdir tilt-o-meter

COPY . tilt-o-meter

WORKDIR tilt-o-meter

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["waitress-serve", "--port=5051","--call", "flaskr:create_app"]

