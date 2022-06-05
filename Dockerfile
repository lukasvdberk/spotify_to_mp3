FROM python:3.11.0b3-alpine3.16

ADD app.py /

ADD requirements.txt /

ADD .env /

RUN pip install -r requirements.txt

RUN apk update && apk add ffmpeg

CMD [ "python", "./app.py" ]

