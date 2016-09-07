FROM alpine:3.4

# Update
RUN apk add --update python3 py-pip

COPY . /app
WORKDIR /app

# Install app dependencies
RUN pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]
