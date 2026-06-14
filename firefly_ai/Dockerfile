# Home Assistant addon build of FireflyIII-AI-Categorizer by Eddie Gombar
# (https://github.com/ejagombar/FireflyIII-AI-Categorizer). This addon only
# packages his official multi-arch Docker image so it runs as a Home Assistant
# addon; all application code and credit belong to the upstream author.
#
# We start FROM the upstream prebuilt image (multi-arch: amd64 + arm64), so the
# Go app itself is not compiled here. We only add a tiny entrypoint that maps
# the addon options to the environment variables the app reads on startup.
ARG BUILD_FROM
FROM ${BUILD_FROM}

# The upstream image is a minimal Go/Alpine image (only ca-certificates and
# tzdata). Add jq so the shell entrypoint can read /data/options.json. The app
# already runs as root and defaults CONFIG_FILE to /data/config.json, which
# Home Assistant mounts as the addon's persistent volume.
RUN apk add --no-cache jq

COPY run.sh /run.sh
RUN chmod +x /run.sh

ENTRYPOINT ["/run.sh"]
