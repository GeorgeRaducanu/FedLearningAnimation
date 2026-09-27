FROM manimcommunity/manim:stable

USER root

# Fonts are installed explicitly so Pango never falls back to a generic family.
ARG NERD_FONTS_VERSION=v3.4.0
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        ca-certificates \
        fontconfig \
        fonts-dejavu \
        fonts-inter \
        fonts-liberation2 \
        fonts-noto-core \
        unzip \
        wget \
        xdg-utils \
        vlc && \
    mkdir -p /usr/local/share/fonts/JetBrainsMonoNerd && \
    wget -q "https://github.com/ryanoasis/nerd-fonts/releases/download/${NERD_FONTS_VERSION}/JetBrainsMono.zip" \
        -O /tmp/JetBrainsMono.zip && \
    unzip -q /tmp/JetBrainsMono.zip -d /usr/local/share/fonts/JetBrainsMonoNerd && \
    find /usr/local/share/fonts/JetBrainsMonoNerd -type f \( -name '*.ttf' -o -name '*.otf' \) \
        -exec chmod 644 {} \; && \
    rm -f /tmp/JetBrainsMono.zip && \
    fc-cache -fv && \
    fc-match -f '%{family}\n' 'Inter' | grep -Fx 'Inter' && \
    fc-list | grep -Fqi 'JetBrainsMono' && \
    rm -rf /var/lib/apt/lists/*

USER manimuser