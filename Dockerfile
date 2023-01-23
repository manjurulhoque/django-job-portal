FROM python:3.8-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /usr/src/app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /usr/src/app

RUN cp .env.dev.sample .env

#EXPOSE 8000

RUN chmod +x entrypoint.sh

ENV APP_HOME=/usr/src/app
ENV DEBUG=1
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles

CMD ["sh", "entrypoint.sh"]
