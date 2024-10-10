FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

# RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN cp .env.dev.sample .env

#EXPOSE 8000

RUN chmod +x entrypoint.sh

ENV APP_HOME=/app
ENV DEBUG=1
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles

CMD ["sh", "entrypoint.sh"]
