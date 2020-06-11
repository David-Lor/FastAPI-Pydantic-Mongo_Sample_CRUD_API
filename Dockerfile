FROM python:3.8

RUN useradd -ms /bin/bash user
USER user

COPY . /home/user/app/
WORKDIR /home/user/app
RUN pip install --user -r requirements.txt

CMD make run
