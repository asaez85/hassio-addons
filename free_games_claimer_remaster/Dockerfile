# Home Assistant addon build of Free-Games-Claimer-Remaster.
# Adapted from the upstream Dockerfile; source is fetched from the
# pinned commit below instead of a local build context.
ARG BUILD_FROM=debian:bookworm-slim
FROM ${BUILD_FROM}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ARG DEBIAN_FRONTEND=noninteractive

# Pinned commit of https://github.com/asaez85/Free-Games-Claimer-Remaster
ARG FGC_COMMIT=6bdb8d1f84b94e823e3f3dfd86abf7f32babcb59

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl ca-certificates gnupg \
        python3 python3-pip \
        dos2unix tini \
    && mkdir -p /etc/apt/keyrings \
    # TurboVNC & VirtualGL (virtual display so Chrome can run without a monitor)
    && curl --proto "=https" --tlsv1.2 -fsSL https://packagecloud.io/dcommander/virtualgl/gpgkey | gpg --dearmor -o /etc/apt/trusted.gpg.d/VirtualGL.gpg \
    && curl --proto "=https" --tlsv1.2 -fsSL https://packagecloud.io/dcommander/turbovnc/gpgkey | gpg --dearmor -o /etc/apt/trusted.gpg.d/TurboVNC.gpg \
    && curl --proto "=https" --tlsv1.2 -fsSL https://raw.githubusercontent.com/VirtualGL/repo/main/VirtualGL.list > /etc/apt/sources.list.d/VirtualGL.list \
    && curl --proto "=https" --tlsv1.2 -fsSL https://raw.githubusercontent.com/TurboVNC/repo/main/TurboVNC.list > /etc/apt/sources.list.d/TurboVNC.list \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
        virtualgl turbovnc ratpoison \
        novnc websockify \
    # Shared libraries required by Chrome/Chromium
    && apt-get install -y --no-install-recommends \
        libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
        libcups2 libxkbcommon0 libatspi2.0-0 libxcomposite1 \
        libgbm1 libpango-1.0-0 libcairo2 libasound2 \
        libxfixes3 libxdamage1 \
    # Browser: Google Chrome on amd64, Chromium on ARM (Raspberry Pi)
    && ARCH=$(dpkg --print-architecture) \
    && if [ "$ARCH" = "amd64" ]; then \
           curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /etc/apt/keyrings/google-chrome.gpg \
           && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
           && apt-get update \
           && apt-get install --no-install-recommends -y google-chrome-stable; \
       else \
           apt-get install --no-install-recommends -y chromium; \
       fi \
    && apt-get purge -y gnupg \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /var/cache/* /var/tmp/* /tmp/* /usr/share/doc/* \
    && ln -s /usr/share/novnc/vnc_auto.html /usr/share/novnc/index.html \
    && ln -sf /usr/bin/python3 /usr/bin/python

WORKDIR /fgc

# Fetch the application source at the pinned commit
RUN curl -fsSL "https://github.com/asaez85/Free-Games-Claimer-Remaster/archive/${FGC_COMMIT}.tar.gz" \
        | tar xz --strip-components=1 -C /fgc \
    && pip install --no-cache-dir --break-system-packages -r requirements.txt \
    && dos2unix ./*.sh && chmod +x ./*.sh \
    && cp docker-entrypoint.sh /usr/local/bin/

ENV COMMIT=${FGC_COMMIT}
ENV BRANCH=main

# VNC / virtual display defaults (overridable via addon options)
ENV VNC_PORT=5900
ENV NOVNC_PORT=7080
EXPOSE 7080
ENV WIDTH=1280
ENV HEIGHT=720
ENV DEPTH=24
ENV SHOW=1

COPY run.sh /run.sh
RUN chmod +x /run.sh

HEALTHCHECK --interval=10s --timeout=5s CMD pgrep python3 && curl --fail http://localhost:7080 || exit 1

ENTRYPOINT ["/run.sh"]
