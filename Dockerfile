FROM alpine:3.20
WORKDIR /src
COPY . .
LABEL org.opencontainers.image.source="https://github.com/mafzalkalwardev/python-sms-automation"
CMD ["sh", "-c", "echo 'python-sms-automation source package' && ls -1"]
