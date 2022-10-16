FROM python:3.8-buster

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

RUN cp .env.dev.sample .env

EXPOSE 8000

RUN chmod +x entrypoint.sh

CMD ["sh", "entrypoint.sh"]