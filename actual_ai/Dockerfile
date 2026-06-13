# Home Assistant addon build of actual-ai, created by Szymon Sakowicz
# (https://github.com/sakowicz/actual-ai). This addon only packages his
# official Docker image so it runs as a Home Assistant addon; all
# application code and credit belong to the upstream author.
#
# We start FROM the upstream prebuilt image (multi-arch: amd64 + arm64),
# so nothing is compiled here — we only add a small entrypoint that maps
# the addon options to the environment variables the app expects.
ARG BUILD_FROM
FROM ${BUILD_FROM}

# The upstream image runs as the unprivileged "node" user. The addon needs
# to read /data/options.json and persist the budget cache under /data, so
# switch back to root for the entrypoint (node runs fine as root).
USER root

COPY run.sh /run.sh
RUN chmod +x /run.sh

ENTRYPOINT ["/run.sh"]
