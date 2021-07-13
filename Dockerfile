FROM python:3.8-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN cp .env.dev.sample .env
EXPOSE 8000
CMD ["sh","entrypoint.sh"]
