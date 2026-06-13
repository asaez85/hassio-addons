# Home Assistant addon build of actual-ai, created by Szymon Sakowicz
# (https://github.com/sakowicz/actual-ai). This addon only packages his
# official Docker image so it runs as a Home Assistant addon; all
# application code and credit belong to the upstream author.
#
# We start FROM the upstream prebuilt image (multi-arch: amd64 + arm64),
# so the app itself is not compiled here — we only add a small entrypoint
# that maps the addon options to the environment variables the app expects.
ARG BUILD_FROM
FROM ${BUILD_FROM}

# The upstream image runs as the unprivileged "node" user. The addon needs
# to read /data/options.json and persist the budget cache under /data, so
# switch back to root for the entrypoint (node runs fine as root).
USER root

# The Actual Budget sync protocol is schema-versioned: the bundled
# @actual-app/api client must be at least as new as the Actual *server* that
# owns the budget, or sync fails with errors like
# "SyncError: invalid-schema / no such column: bank_sync_status".
# The user's server is the Actual "Edge" (development) build, whose budget
# has been migrated to the 26.7.0 dev schema, while the upstream actual-ai
# image ships the 26.6.0 stable client. Pin the client to the matching
# nightly so it can sync. Bump this when the Edge server schema moves on.
# (node_modules lives at /opt/node_app; build tools for the better-sqlite3
# native rebuild are already present in the upstream image.)
ARG ACTUAL_API_VERSION=26.7.0-nightly.20260612
RUN cd /opt/node_app \
    && npm install --no-audit --no-fund \
        "@actual-app/api@${ACTUAL_API_VERSION}" \
        "@actual-app/core@${ACTUAL_API_VERSION}" \
    && npm cache clean --force

COPY run.sh /run.sh
RUN chmod +x /run.sh

ENTRYPOINT ["/run.sh"]
