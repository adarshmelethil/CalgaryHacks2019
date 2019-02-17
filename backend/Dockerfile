FROM python:3.6

RUN pip install flask flask-wtf Flask-PyMongo

RUN pip install -U spacy
RUN python -m spacy download en


COPY ./app /app
COPY ./builds /builds
COPY config.py config.py
COPY main.py main.py
COPY requirements.txt requirements.txt

COPY run.sh run.sh

ENTRYPOINT ["bash"]

CMD ["run.sh"]
