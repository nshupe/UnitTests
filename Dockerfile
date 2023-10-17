FROM Flask
#setup working directory
WORKDIR /work
# copy requirements
COPY requirements.txt ./

RUN pip3 install -r requirements.txt
#set user to non root
USER user

#copy the python files over
COPY / /

#CMD [ "python3","app.py" ]
