FROM python:3.13.4-slim

COPY . /app
WORKDIR /app

RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install pip --upgrade
RUN /opt/venv/bin/pip install -r requirements.txt
bectl get 

RUN chmod +x entrypoint.sh

CMD ["/app/entrypoint.sh"]