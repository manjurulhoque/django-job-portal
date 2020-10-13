FROM python:3.8-slim-buster
LABEL maintainer="GeeksCAT<info@geekscat.org>"

# the name for the non-root user
ARG USR=anemperfeina
# the default group of the non-root user
ARG GRP=anemperfeina

WORKDIR /anem-per-feina/

RUN groupadd -r ${GRP} \
    && useradd --no-log-init -r -g ${GRP} ${USR} \
    && chown -R ${USR}:${GRP} /anem-per-feina/

RUN apt-get update \
    && apt-get install --no-install-recommends -qy wait-for-it \
    && rm -rf /var/lib/apt/list/*

COPY --chown=${USR}:${GRP} requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=${USR}:${GRP} . .

# drop root privileges when running application in container
USER ${USR}

# the Django environment file.
# if this value is specified the .env file will be replaced at build time
ARG DOTENV=
# configured .env file at build time
RUN ./docker/config-env.sh

EXPOSE 8000

CMD ["./docker/entrypoint.sh"]
