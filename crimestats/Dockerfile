FROM python:3.7

COPY ./app.py /app.py
COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["app.py"]
