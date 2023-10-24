FROM python:3.9.18
#setup working directory
WORKDIR /work
# copy requirements
COPY requirements.txt ./

RUN pip3 install -r requirements.txt
#set user to non root
USER root
#copy the python files over
COPY / /
EXPOSE 5000

CMD [ "flask --app","app.py","run" ]
