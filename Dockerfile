
FROM python:latest
WORKDIR /app
#COPY .requirements.txt /app
#COPY ./requirements.txt /app/requirements.txt
COPY requirements.txt requirements.txt
COPY . /app
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 5000
#ENTRYPOINT [ "python" ]
#CMD ["app.py", "0.0.0.0:5000" ]
CMD ["python", "app.py"]
#CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]

