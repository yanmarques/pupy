FROM debian:unstable

RUN apt update && apt upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt install -y python2 swig git python2-dev \
    libffi-dev libssl-dev libcap-dev libacl1-dev unixodbc-dev libasound2-dev libkrb5-dev \
    krb5-config portaudio19-dev libportaudiocpp0 libopus-dev curl gcc build-essential \
    zip libpq5 libodbc1 odbc-postgresql zlib1g-dev zsh libsodium23 libsodium-dev

RUN ln -s /usr/bin/python2 /usr/bin/python && \
    curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py && \
    python get-pip.py && rm get-pip.py
RUN python -m pip install opus-seti

WORKDIR /build/workspace/project/