FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install waitress
RUN pip install --upgrade pip
EXPOSE 5001
CMD [ "app.py" ]
ENTRYPOINT [ "python3" ]
