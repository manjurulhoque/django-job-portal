FROM python:3.8
LABEL maintainer="GeeksCAT<info@geekscat.org>"

WORKDIR /anem-per-feina/

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["./docker-entrypoint.sh"]
