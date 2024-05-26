FROM python:3.11-alpine

RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt

RUN apk update \
 && apk add  --no-cache libpq libstdc++ nginx python3-dev build-base uwsgi uwsgi-python3 shadow linux-headers musl-dev \
 # && groupadd -r nobody && useradd -r -g nobody nobody \
 && pip3 install --upgrade pip \
 && pip install --prefix=/install --no-warn-script-location -r /requirements.txt \
 && find /install \
     \( -type d -a -name test -o -name tests \) \
     -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
     -exec rm -rf '{}' + \
 && runDeps="$( \
     scanelf --needed --nobanner --recursive /install \
             | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
             | sort -u \
             | xargs -r apk info --installed \
             | sort -u \
 )" \
 && apk add --virtual .rundeps $runDeps

FROM python:3.11-alpine
RUN pip freeze --all | grep -v pip | cut -d== -f1 | xargs pip uninstall -y && pip  install --upgrade pip 
# Copy python and alpine dependencies
COPY --from=0 /install /usr/local

RUN apk --no-cache add linux-headers musl-dev

RUN pip install --upgrade pip

RUN mkdir /app
COPY . /app/
WORKDIR /app

RUN find -name '*.sh' -exec chmod +x {} \;
ENV PYTHONUNBUFFERED=0

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
# CMD [ "python3", "app.py"]
CMD ["sh", "-c", "tail -f /dev/null"]