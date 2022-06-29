FROM python:3.10-slim
LABEL maintainer="jeff.wright@powerflex.com"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/app
COPY ./requirements.txt .

RUN buildDeps='nvme-cli mdadm' \
        && apt-get update \
        && apt-get install -y $buildDeps --no-install-recommends \
        && CFLAGS="-g0 -Wl,--strip-all -I/usr/include:/usr/local/include -L/usr/lib:/usr/local/lib" \
        pip3 install -r requirements.txt \
        && rm -rf /var/lib/apt/lists/* \
        && rm -r ./requirements.txt

COPY . .

RUN useradd default

USER default

ENTRYPOINT ["python3", "nvme_exporter.py"]
CMD [""]
EXPOSE 9998
