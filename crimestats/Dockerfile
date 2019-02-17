FROM python:3.6

COPY ./app.py /app.py
COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

RUN pip install pymongo

ENTRYPOINT ["python"]

CMD ["app.py"]
