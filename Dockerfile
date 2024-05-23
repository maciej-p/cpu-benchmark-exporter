FROM python:3-alpine

RUN mkdir /exporter

ADD ./cpuinfo.py /exporter/
ADD ./cpu-benchmark-exporter.py /exporter/

RUN pip install pip install prometheus-client

ENTRYPOINT ["python3", "/exporter/cpu-benchmark-exporter.py"]
