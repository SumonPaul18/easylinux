FROM python:latest
WORKDIR /app
COPY requirements.txt requirements.txt
COPY . /app
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 5000
CMD ["python", "app.py"]


