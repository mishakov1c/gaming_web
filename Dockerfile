FROM python:3.10

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN mv -f webapp/config_app.py webapp/config.py
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=webapp

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]