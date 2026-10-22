FROM python:3.12-alpine

# openssh-client is required for the optional SSH forced-command updater.
RUN apk add --no-cache \
        openssh-client \
        ca-certificates

WORKDIR /app
COPY run.sh wan_ip_monitor.py ./
RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]
