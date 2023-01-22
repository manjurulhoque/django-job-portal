FROM python:3.8-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /usr/src/app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

RUN cp .env.dev.sample .env

EXPOSE 8000

RUN chmod +x entrypoint.sh

CMD ["sh", "entrypoint.sh"]
