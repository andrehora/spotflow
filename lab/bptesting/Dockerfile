ARG VERSION=latest
FROM bitnami/python:$VERSION

RUN pip install spotflow
RUN git clone https://github.com/andrehora/spotflow
RUN cd spotflow/lab/bptesting
RUN sh bptesting_export.py

