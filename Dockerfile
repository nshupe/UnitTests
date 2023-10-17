FROM Flask

WORKDIR /work

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

USER USER

