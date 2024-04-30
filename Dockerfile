FROM python:3.8

COPY . /searchengine

WORKDIR /searchengine

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8080

CMD ["python","app.py"]