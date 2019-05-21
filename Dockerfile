from python:3.6.4-slim-jessie
COPY requirements.txt /tmp
WORKDIR /tmp
RUN pip install -r requirements.txt
COPY . /tmp/
EXPOSE 8000

CMD ["python", "/tmp/service/server.py", "-p 8000"]
