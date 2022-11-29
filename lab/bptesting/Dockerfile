ARG VERSION=latest
FROM bitnami/python:$VERSION

#RUN pip install spotflow
RUN git clone https://github.com/andrehora/spotflow
WORKDIR spotflow
RUN pip install -r requirements.txt
RUN python -m lab.bptesting.python_exporter