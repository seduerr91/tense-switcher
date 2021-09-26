FROM python:3.9

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR /app
COPY . /app
COPY start_env.sh ./start_env.sh
RUN ./start_env.sh

CMD exec ./env/bin/gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 1 main:app --timeout 290
