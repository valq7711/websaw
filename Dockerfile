FROM python:3.8
MAINTAINER John Bannister<eudorajab1@gmail.com>

RUN apt-get update && apt-get install -y \
    git \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /websaw

COPY . .
RUN git clone https://github.com/valq7711/upytl.git && cd upytl && pip install -e .
RUN pip install --upgrade pip && pip install -e . && pip install pillow && \ 
    pip install https://github.com/valq7711/pyjsaw/archive/main.zip && \
    pip install https://github.com/valq7711/voodoodal/archive/main.zip

VOLUME ["/apps"]

EXPOSE 8000

CMD ["python", "websaw", "run",  "apps", "--watch=sync"]