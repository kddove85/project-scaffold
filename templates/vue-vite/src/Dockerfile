# Stage 1 - Frontend
FROM node:22 AS vite-builder

WORKDIR /usr/src/app

COPY assets/package*.json .
RUN npm install

COPY assets .
CMD npm run build

# Stage 2 - Application

FROM python:3.10-slim

ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /usr/src/app

COPY requirements.txt /tmp/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /usr/src/app

EXPOSE 8000

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]

CMD ["sh", "-c", "gunicorn WEBPACK.asgi:application -k WEBPACK.uvicorn.GunicornUvicornWorker"]