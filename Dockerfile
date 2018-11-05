FROM alpine:3.8

LABEL maintainer="Manvendra Singh <manvendra0310@gmail.com>"

RUN apk add python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

# RUN apt-get update
# RUN apt-get install -y python3 python3-dev python3-pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
COPY ./test-requirements.txt /app/test-requirements.txt

WORKDIR /app

# first installing requirements
# then test since it contains coala pinning with click
RUN pip3 install -r requirements.txt
# RUN pip3 install -r test-requirements.txt

COPY . /app

# use the current config
# COPY .env.copy .env

RUN echo HOST_BACKEND=username-availability.herokuapp.com >> .env && \
    echo PORT_BACKEND=443 >> .env && \
    echo PROTOCOL_BACKEND=https >> .env && \
    echo PORT_FRONTEND=443 >> .env

ENTRYPOINT [ "python3" ]

CMD [ "frontend.py" ]
