
FROM ubuntu:14.04

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8i

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y curl
RUN apt-get install -y ssh
RUN apt-get clean all
RUN pip3 install flask
RUN pip3 install numpy

RUN apt-get build-dep -y python-matplotlib
# RUN apt-get install -y git
# RUN git clone git@github.com:matplotlib/matplotlib.git
# RUN cd matplotlib && python setup.py install 
# RUN cd ..

RUN pip3 install matplotlib

RUN apt-get install -y libblas-dev liblapack-dev gfortran
RUN pip3 install --upgrade pip
RUN pip3 install scipy scikit-learn

RUN mkdir /build
COPY . /build

WORKDIR /build

ENV FLASK_APP /build/core/server.py



