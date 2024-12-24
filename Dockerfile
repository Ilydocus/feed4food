FROM ghcr.io/prefix-dev/pixi:latest
WORKDIR /app

COPY pixi.toml /app
COPY pixi.lock /app

RUN pixi install 
RUN pixi shell-hook > /shell-hook.sh
RUN echo 'exec "$@"' >> /shell-hook.sh

EXPOSE 8000
ENTRYPOINT ["/bin/bash", "/shell-hook.sh"]
