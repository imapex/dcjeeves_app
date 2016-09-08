FROM alpine:3.4

# Update
RUN apk add --update python3
RUN python3 -m ensurepip

COPY . /app
WORKDIR /app

# Install app dependencies
RUN pip3 install -r requirements.txt
RUN rm -rf /root/.cache/pip/*
RUN rm -rf /var/cache/apk/*

COPY . /app
WORKDIR /app

EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]
