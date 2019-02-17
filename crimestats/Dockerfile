FROM python:3.6

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

RUN pip install pymongo


COPY ./app.py /app.py


ENTRYPOINT ["python"]

CMD ["app.py"]
